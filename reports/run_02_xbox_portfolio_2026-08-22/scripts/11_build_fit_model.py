"""
Stage 10 (scoring) -- fit the "what wins in this catalogue" model.

Reads the population built by sql/11_fit_model_population.sql (via DuckDB, straight from
the Parquet store -- no CSV touched), builds structural features (genre / tag one-hots,
price, mode flags, age-since-release control), fits a Ridge regression predicting
log1p(review_total) on a TRAIN split, and evaluates it on a HOLDOUT split it never saw.
Both in-sample and out-of-sample performance are reported and written to
artifacts/10_model.json -- per the task's explicit anti-circularity requirement.

All row-level data stays inside this script's memory. Only aggregates (coefficients,
R^2, correlations, counts) are printed or written to disk.
"""
import json
import duckdb
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr, spearmanr

RUN_DIR = "/home/claude/run_portfolio"
SQL_FILE = f"{RUN_DIR}/sql/11_fit_model_population.sql"

GENRES = ['Indie', 'Adventure', 'Action', 'Casual', 'Simulation', 'Strategy', 'RPG',
          'Free To Play', 'Early Access', 'Sports', 'Racing', 'Massively Multiplayer']
# Tags with genre-duplicate names dropped (Indie/Casual/Adventure/Action/Simulation/
# Strategy/RPG/Early Access/Free to Play already captured as genre dummies above) --
# kept distinct so a coefficient is never split across two identical-meaning columns.
TAGS = ['Singleplayer', '2D', 'Atmospheric', 'Puzzle', '3D', 'Story Rich', 'Cute',
        'Colorful', 'Exploration', 'Pixel Graphics', 'First-Person', 'Multiplayer',
        'Anime', 'Fantasy', 'Funny', 'Arcade', 'Horror', 'Relaxing',
        'Female Protagonist', 'Shooter', 'Retro']

RANDOM_STATE = 42


def main():
    con = duckdb.connect()
    sql = open(SQL_FILE).read()
    df = con.execute(sql).df()
    n_total = len(df)

    # --- feature engineering (in-script only, never printed row-level) ---
    for g in GENRES:
        df[f"genre_{g}"] = df["genre_list"].apply(lambda lst, g=g: g in lst).astype(int)
    for t in TAGS:
        df[f"tag_{t}"] = df["tag_list"].apply(lambda lst, t=t: t in lst).astype(int)

    df["price_usd_filled"] = df["price_usd"].fillna(0.0)
    df["is_free_i"] = df["is_free"].fillna(False).astype(int)
    df["is_indie_i"] = df["is_indie"].fillna(False).astype(int)
    df["is_self_pub_i"] = df["is_self_published"].fillna(False).astype(int)
    df["has_singleplayer_i"] = df["has_singleplayer"].fillna(False).astype(int)
    df["has_multiplayer_i"] = df["has_multiplayer"].fillna(False).astype(int)
    df["has_coop_i"] = df["has_coop"].fillna(False).astype(int)
    df["has_controller_i"] = df["has_controller_support"].fillna(False).astype(int)
    df["has_vr_i"] = df["has_vr"].fillna(False).astype(int)
    df["n_tags_filled"] = df["n_tags"].fillna(0)
    # age control: log-days-since-release, right-censoring per 01_profile.md / hard limits.
    df = df[df["age_days"].notna() & (df["age_days"] > 0)].copy()
    df["log_age_days"] = np.log(df["age_days"])

    feature_cols = (
        [f"genre_{g}" for g in GENRES]
        + [f"tag_{t}" for t in TAGS]
        + ["price_usd_filled", "is_free_i", "is_indie_i", "is_self_pub_i",
           "has_singleplayer_i", "has_multiplayer_i", "has_coop_i",
           "has_controller_i", "has_vr_i", "n_tags_filled", "log_age_days"]
    )

    X = df[feature_cols].values.astype(float)
    y = df["target_log_reviews"].values.astype(float)
    n_model = len(df)

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, df.index, test_size=0.30, random_state=RANDOM_STATE
    )

    model = Ridge(alpha=5.0, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)

    def metrics(y_true, y_pred):
        pear_r, pear_p = pearsonr(y_true, y_pred)
        spear_r, spear_p = spearmanr(y_true, y_pred)
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - y_true.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot
        return dict(n=len(y_true), r2=round(float(r2), 4),
                    pearson_r=round(float(pear_r), 4), pearson_p=float(pear_p),
                    spearman_r=round(float(spear_r), 4), spearman_p=float(spear_p))

    in_sample = metrics(y_train, pred_train)
    out_of_sample = metrics(y_test, pred_test)

    # Extra out-of-sample check restricted to the population the model is actually USED to
    # rank (owners_mid <= 750,000, paid) -- the whole-catalogue r above could look fine while
    # the model discriminates poorly inside the specific low-owner slice we care about.
    test_df = df.loc[idx_test].copy()
    test_df["pred"] = pred_test
    mask_scope = (test_df["owners_mid"] <= 750000) & (test_df["monetisation_model"] == "paid")
    scoped = test_df[mask_scope]
    out_of_sample_scoped = metrics(scoped["target_log_reviews"].values, scoped["pred"].values)

    coefs = {name: round(float(c), 4) for name, c in zip(feature_cols, model.coef_)}
    coefs_ranked = dict(sorted(coefs.items(), key=lambda kv: -kv[1]))

    result = {
        "target": "ln(1 + review_total) -- a RECEPTION-SCALE proxy, not engagement/playtime "
                  "(no such column exists in this dataset; every playtime column is constant "
                  "zero per 01_profile.md and 02_cleaning_report.md).",
        "population": {
            "definition": "is_demo=false AND review_total>=10 AND release_date IS NOT NULL",
            "n_total_rows_before_age_filter": int(n_total),
            "n_used_for_modeling": int(n_model),
            "note": "review_total>=10 is Valve's own threshold below which no review score "
                    "exists at all (bucket = 'Not enough user reviews'); release_date required "
                    "to compute the age-since-release right-censoring control.",
        },
        "features": feature_cols,
        "model": "Ridge regression, alpha=5.0 (L2-regularized to stabilize genre/tag "
                 "coefficients that are correlated with each other, e.g. genre_Indie and "
                 "tag_Singleplayer)",
        "split": {"method": "random_state=42 train_test_split, test_size=0.30",
                   "n_train": int(len(y_train)), "n_test": int(len(y_test))},
        "in_sample_performance": in_sample,
        "out_of_sample_performance": out_of_sample,
        "out_of_sample_performance_scoped_to_candidate_population": {
            **out_of_sample_scoped,
            "note": "Same holdout fold, restricted to owners_mid<=750,000 AND "
                    "monetisation_model='paid' -- i.e. the actual population the fit score "
                    "is used to rank in 12_score_candidates.py. This is the more decision-"
                    "relevant of the two out-of-sample numbers; a gap between this and the "
                    "whole-catalogue figure above means the model's real discriminating "
                    "power inside the low-owner pool is different from its headline number.",
        },
        "coefficients_sorted_desc": coefs_ranked,
        "honest_read": (
            "Out-of-sample Pearson r and Spearman r are the numbers that matter for how "
            "much weight this model's ranking can carry -- see artifacts/10_scoring.md for "
            "the plain-language verdict."
        ),
    }

    with open(f"{RUN_DIR}/artifacts/10_model_fit.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({"in_sample": in_sample, "out_of_sample": out_of_sample,
                       "out_of_sample_scoped": out_of_sample_scoped,
                       "n_model": n_model}, indent=2))
    print("\nTop 10 positive coefficients:")
    for k, v in list(coefs_ranked.items())[:10]:
        print(f"  {k}: {v}")
    print("\nBottom 10 (most negative) coefficients:")
    for k, v in list(coefs_ranked.items())[-10:]:
        print(f"  {k}: {v}")

    # Save the fitted model's coefficients + means needed to score the FULL candidate
    # population later (12_score_candidates.py reads this file, never refits on candidates).
    np.save(f"{RUN_DIR}/artifacts/_ridge_coef.npy", model.coef_)
    with open(f"{RUN_DIR}/artifacts/_ridge_intercept.txt", "w") as f:
        f.write(str(float(model.intercept_)))
    with open(f"{RUN_DIR}/artifacts/_feature_cols.json", "w") as f:
        json.dump(feature_cols, f)


if __name__ == "__main__":
    main()
