"""
Stage 12 (scoring v2) -- fit the RETARGETED "what wins" model, deterministically.

Fixes vs v1 (see sql/11v2_fit_model_population.sql header and RUN_LOG.md Stage 12 for the
full rationale):
  - RT-01 (non-determinism): input sorted by app_id (both in SQL via ORDER BY and again
    here defensively) before train_test_split, so the split is actually reproducible.
    Model artifacts (_ridge_coef_v2.npy, _ridge_intercept_v2.txt, _feature_cols_v2.json)
    are committed to artifacts/ so the pipeline runs end to end from a clean checkout --
    v1 shipped without them, which is why 12_score_candidates.py could not run as shipped.
  - RT-05 (Fit restates Proven): target changed from ln(1+review_total) [used elsewhere
    as the Recognition pillar] to review_positive_ratio [reception QUALITY -- not encoded
    anywhere else in the v2 composite]. price_usd is excluded from the feature set (so
    price cannot re-enter the ranking through the Fit door after being removed from the
    composite). is_indie_i is dropped (was perfectly collinear with genre_Indie in v1,
    double-counting "indie").
  - Reports out-of-sample performance as a RANGE across 5 seeds, not a single point
    estimate, since the point estimate is exactly what turned out not to reproduce in v1.

All row-level data stays inside this script's memory; only aggregates are printed/saved.
"""
import json
import duckdb
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr, spearmanr

RUN_DIR = "/home/claude/run_portfolio"
SQL_FILE = f"{RUN_DIR}/sql/11v2_fit_model_population.sql"

GENRES = ['Indie', 'Adventure', 'Action', 'Casual', 'Simulation', 'Strategy', 'RPG',
          'Free To Play', 'Early Access', 'Sports', 'Racing', 'Massively Multiplayer']
TAGS = ['Singleplayer', '2D', 'Atmospheric', 'Puzzle', '3D', 'Story Rich', 'Cute',
        'Colorful', 'Exploration', 'Pixel Graphics', 'First-Person', 'Multiplayer',
        'Anime', 'Fantasy', 'Funny', 'Arcade', 'Horror', 'Relaxing',
        'Female Protagonist', 'Shooter', 'Retro']

SEEDS = [42, 7, 123, 2024, 99]
CANONICAL_SEED = 42  # the model actually persisted and used to score candidates


def build_features(df):
    for g in GENRES:
        df[f"genre_{g}"] = df["genre_list"].apply(lambda lst, g=g: g in lst).astype(int)
    for t in TAGS:
        df[f"tag_{t}"] = df["tag_list"].apply(lambda lst, t=t: t in lst).astype(int)

    df["is_self_pub_i"] = df["is_self_published"].fillna(False).astype(int)
    df["has_singleplayer_i"] = df["has_singleplayer"].fillna(False).astype(int)
    df["has_multiplayer_i"] = df["has_multiplayer"].fillna(False).astype(int)
    df["has_coop_i"] = df["has_coop"].fillna(False).astype(int)
    df["has_controller_i"] = df["has_controller_support"].fillna(False).astype(int)
    df["has_vr_i"] = df["has_vr"].fillna(False).astype(int)
    df["n_tags_filled"] = df["n_tags"].fillna(0)
    # NOTE: is_indie_i intentionally NOT built (RT-05: collinear with genre_Indie).
    # NOTE: price_usd_filled / is_free_i intentionally NOT built (price excluded from Fit
    # entirely, so it cannot re-enter the composite through the Fit door).
    df["log_age_days"] = np.log(df["age_days"])
    return df


def feature_cols():
    return (
        [f"genre_{g}" for g in GENRES]
        + [f"tag_{t}" for t in TAGS]
        + ["is_self_pub_i", "has_singleplayer_i", "has_multiplayer_i", "has_coop_i",
           "has_controller_i", "has_vr_i", "n_tags_filled", "log_age_days"]
    )


def metrics(y_true, y_pred):
    pear_r, pear_p = pearsonr(y_true, y_pred)
    spear_r, spear_p = spearmanr(y_true, y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    return dict(n=len(y_true), r2=round(float(r2), 4),
                pearson_r=round(float(pear_r), 4), pearson_p=float(pear_p),
                spearman_r=round(float(spear_r), 4), spearman_p=float(spear_p))


def main():
    con = duckdb.connect()
    sql = open(SQL_FILE).read()
    df = con.execute(sql).df()
    # Defensive re-sort even though the SQL already carries ORDER BY app_id -- this is
    # the exact belt-and-suspenders fix RT-01 asked for.
    df = df.sort_values("app_id").reset_index(drop=True)
    n_total = len(df)

    df = build_features(df)
    df = df[df["age_days"].notna() & (df["age_days"] > 0)].copy()
    df = df.sort_values("app_id").reset_index(drop=True)
    n_model = len(df)

    fcols = feature_cols()
    X = df[fcols].values.astype(float)
    y = df["target_quality"].values.astype(float)

    seed_results = {}
    for seed in SEEDS:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.30, random_state=seed, shuffle=True
        )
        m = Ridge(alpha=5.0, random_state=seed)
        m.fit(X_train, y_train)
        seed_results[seed] = {
            "in_sample": metrics(y_train, m.predict(X_train)),
            "out_of_sample": metrics(y_test, m.predict(X_test)),
        }

    oos_pearson = [seed_results[s]["out_of_sample"]["pearson_r"] for s in SEEDS]
    oos_r2 = [seed_results[s]["out_of_sample"]["r2"] for s in SEEDS]

    # --- canonical model: the one actually persisted and used to score candidates ---
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, df.index, test_size=0.30, random_state=CANONICAL_SEED, shuffle=True
    )
    model = Ridge(alpha=5.0, random_state=CANONICAL_SEED)
    model.fit(X_train, y_train)
    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)
    in_sample = metrics(y_train, pred_train)
    out_of_sample = metrics(y_test, pred_test)

    # scoped check: restricted to the actual v2 eligibility population (see
    # sql/12v2_candidate_screen.sql) within this holdout fold
    test_df = df.loc[idx_test].copy()
    test_df["pred"] = pred_test
    mask_scope = (
        (test_df["owners_mid"] <= 750000)
        & (test_df["monetisation_model"] == "paid")
        & (test_df["review_total"] >= 5000)
        & (test_df["review_positive_ratio"] >= 0.70)
        & (test_df["has_controller_support"] == True)  # noqa: E712
    )
    scoped = test_df[mask_scope]
    out_of_sample_scoped = (metrics(scoped["target_quality"].values, scoped["pred"].values)
                             if len(scoped) >= 10 else
                             {"n": int(len(scoped)), "note": "n<10, too small to report a correlation"})

    coefs = {name: round(float(c), 4) for name, c in zip(fcols, model.coef_)}
    coefs_ranked = dict(sorted(coefs.items(), key=lambda kv: -kv[1]))

    result = {
        "target": "review_positive_ratio -- RECEPTION QUALITY, retargeted from v1's "
                  "ln(1+review_total) per RT-05 (that target IS the Recognition pillar "
                  "for every candidate row, so predicting it added noise, not "
                  "information, and the noise outranked the measurement).",
        "population": {
            "definition": "is_demo=false AND review_total>=10 AND release_date IS NOT NULL, "
                          "ORDER BY app_id (RT-01 fix)",
            "n_total_rows_before_age_filter": int(n_total),
            "n_used_for_modeling": int(n_model),
        },
        "features": fcols,
        "features_removed_vs_v1": {
            "price_usd_filled": "excluded so price cannot re-enter the composite through "
                                 "the Fit door after being removed from scoring per the "
                                 "rebuild spec",
            "is_free_i": "excluded for the same reason (collinear with price regime)",
            "is_indie_i": "dropped -- RT-05 found it perfectly collinear with genre_Indie "
                          "in v1 (identical -0.1155 coefficients), double-counting indie "
                          "status",
        },
        "model": "Ridge regression, alpha=5.0 (unchanged from v1)",
        "determinism_fix": "df sorted by app_id (SQL ORDER BY + pandas re-sort) before "
                           "every train_test_split call -- RT-01.",
        "canonical_split": {"random_state": CANONICAL_SEED, "test_size": 0.30,
                             "n_train": int(len(y_train)), "n_test": int(len(y_test))},
        "canonical_in_sample_performance": in_sample,
        "canonical_out_of_sample_performance": out_of_sample,
        "canonical_out_of_sample_scoped_to_v2_eligible_population": out_of_sample_scoped,
        "out_of_sample_range_across_5_seeds": {
            "seeds": SEEDS,
            "pearson_r_per_seed": dict(zip(SEEDS, oos_pearson)),
            "r2_per_seed": dict(zip(SEEDS, oos_r2)),
            "pearson_r_range": [round(min(oos_pearson), 4), round(max(oos_pearson), 4)],
            "pearson_r_mean": round(float(np.mean(oos_pearson)), 4),
            "r2_range": [round(min(oos_r2), 4), round(max(oos_r2), 4)],
            "note": "This range is what should be quoted, not the canonical single-seed "
                    "figure alone -- v1 published a single point estimate (0.564) that "
                    "did not reproduce in any of the red-team's 3 re-runs because the "
                    "input row order (and therefore the position-based split) was not "
                    "fixed. With app_id-sorted input, re-running this exact script "
                    "produces the SAME canonical figure every time (determinism restored); "
                    "the range above instead captures genuine seed-to-seed VARIANCE, which "
                    "is a different and honest source of uncertainty to report.",
        },
        "coefficients_sorted_desc": coefs_ranked,
    }

    with open(f"{RUN_DIR}/artifacts/12_model_v2_fit.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({
        "canonical_in_sample": in_sample,
        "canonical_out_of_sample": out_of_sample,
        "canonical_out_of_sample_scoped": out_of_sample_scoped,
        "oos_pearson_range_across_seeds": [round(min(oos_pearson), 4), round(max(oos_pearson), 4)],
        "n_model": n_model,
    }, indent=2))
    print("\nTop 10 positive coefficients:")
    for k, v in list(coefs_ranked.items())[:10]:
        print(f"  {k}: {v}")
    print("\nBottom 10 (most negative) coefficients:")
    for k, v in list(coefs_ranked.items())[-10:]:
        print(f"  {k}: {v}")

    # Persist canonical model artifacts -- v1's shipped-without-these defect (RT-01).
    np.save(f"{RUN_DIR}/artifacts/_ridge_coef_v2.npy", model.coef_)
    with open(f"{RUN_DIR}/artifacts/_ridge_intercept_v2.txt", "w") as f:
        f.write(str(float(model.intercept_)))
    with open(f"{RUN_DIR}/artifacts/_feature_cols_v2.json", "w") as f:
        json.dump(fcols, f)
    print("\nPersisted: artifacts/_ridge_coef_v2.npy, _ridge_intercept_v2.txt, "
          "_feature_cols_v2.json")


if __name__ == "__main__":
    main()
