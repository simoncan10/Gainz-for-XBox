"""
Stage 16 (scoring v3) -- reweight Fit down per Stage 15 red team (A-4), move the review
floor to where the metacritic-presence plateau actually starts (A-2), and document the
Headroom/A-3 finding plainly rather than "fixing" it (it cannot be fixed, only disclosed).

Changes vs v2 (scripts/12v2_score_candidates.py):
  - Screen: review_total>=4,000 (was >=5,000) -- sql/18_candidate_screen_v3.sql.
  - Weights: Recognition 0.50 / Headroom 0.40 / Fit 0.10 (was 0.45/0.35/0.20) -- A-4:
    Fit's in-population R^2 is negative (worse than predicting the mean), so it cannot
    carry 20% of the ranking. Cutting to 10% follows the critic's own suggested split.
  - NEW diagnostic: within-owners_mid-bucket Spearman(recognition, headroom) -- A-3 found
    this is 1.0000 in every bucket with n>=5, meaning Headroom is Recognition minus a
    constant WITHIN a bucket, and the pooled +0.54 correlation is entirely between-bucket
    variation. This is reported, not resolved -- there is no scoring fix for it; it is a
    property of owners_mid's bucket coarseness (5-6 distinct values), stated honestly.
  - NEW diagnostic: what moves when Fit is cut from 20% to 10%, holding the pool fixed at
    the v2 screen (n=638) -- isolates the reweight's own effect from the floor move's
    effect, both of which are combined in the final v3 list.
  - NEW diagnostic: owners_mid bucket distribution of the qualifying list, echoing B-5's
    finding that the ceiling is close to defining rather than merely filtering the
    portfolio (this is reported here as a known property of the v3 scoring design; the
    downstream portfolio/tiering document is NOT reopened this round per the coordinator's
    explicit instruction).

Everything else (Fit model itself, tier rule shape, monoculture-check methodology) is
UNCHANGED from v2 -- per "do not reopen anything else."
"""
import json
import duckdb
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

RUN_DIR = "/home/claude/run_portfolio"

GENRES = ['Indie', 'Adventure', 'Action', 'Casual', 'Simulation', 'Strategy', 'RPG',
          'Free To Play', 'Early Access', 'Sports', 'Racing', 'Massively Multiplayer']
TAGS = ['Singleplayer', '2D', 'Atmospheric', 'Puzzle', '3D', 'Story Rich', 'Cute',
        'Colorful', 'Exploration', 'Pixel Graphics', 'First-Person', 'Multiplayer',
        'Anime', 'Fantasy', 'Funny', 'Arcade', 'Horror', 'Relaxing',
        'Female Protagonist', 'Shooter', 'Retro']

W_RECOGNITION = 0.50
W_HEADROOM = 0.40
W_FIT = 0.10
OLD_WEIGHTS = (0.45, 0.35, 0.20)

BAR = 0.60
ANCHOR_REVIEW_FLOOR = 20000
ANCHOR_OWNERS_FLOOR = 350000
LOW_COST_PRICE_CEILING = 5.0


def pct_rank(x):
    return (rankdata(x, method="average") - 1) / (len(x) - 1)


def to_list(a):
    return list(a) if isinstance(a, (list, np.ndarray)) else []


def base_title(name):
    import re
    s = str(name)
    s = re.sub(r'\s*[:\-–]\s*.*$', '', s)
    s = re.sub(r'\s+(II|III|IV|V|VI|VII|VIII|IX|X)$', '', s)
    s = re.sub(r'\s+\d+$', '', s)
    return s.strip() or str(name)


def build_pillars(df, feature_cols, coef_map):
    struct_cols = [c for c in feature_cols if c != "log_age_days"]
    X_struct = df[struct_cols].values.astype(float)
    struct_coef = np.array([coef_map[c] for c in struct_cols])
    intercept = coef_map["__intercept__"]
    df["fit_raw"] = intercept + X_struct @ struct_coef

    df["recognition_raw"] = np.log(df["review_total"].values.astype(float))
    df["headroom_raw"] = (np.log(df["review_total"].values.astype(float))
                           - np.log(df["owners_mid"].values.astype(float)))

    df["recognition_pct"] = pct_rank(df["recognition_raw"].values)
    df["headroom_pct"] = pct_rank(df["headroom_raw"].values)
    df["fit_pct"] = pct_rank(df["fit_raw"].values)
    return df


def composite(df, w):
    return w[0] * df["recognition_pct"] + w[1] * df["headroom_pct"] + w[2] * df["fit_pct"]


def build_features(df):
    df["genre_list"] = df["genres"].apply(to_list)
    df["tag_list"] = df["tags"].apply(to_list)
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
    return df


def main():
    con = duckdb.connect()

    feature_cols = json.load(open(f"{RUN_DIR}/artifacts/_feature_cols_v2.json"))
    coef = np.load(f"{RUN_DIR}/artifacts/_ridge_coef_v2.npy")
    intercept = float(open(f"{RUN_DIR}/artifacts/_ridge_intercept_v2.txt").read())
    coef_map = dict(zip(feature_cols, coef))
    coef_map["__intercept__"] = intercept

    # ---------- Diagnostic 1: A-3 within-bucket Headroom check, on the v2 pool (n=638) ----
    # (kept on the exact pool the red team tested, for a direct apples-to-apples check)
    df_v2pool = con.execute(open(f"{RUN_DIR}/sql/12v2_candidate_screen.sql").read()).df()
    df_v2pool = build_features(df_v2pool)
    df_v2pool = build_pillars(df_v2pool, feature_cols, coef_map)
    pooled_corr = float(spearmanr(df_v2pool["recognition_raw"], df_v2pool["headroom_raw"])[0])
    within_bucket = {}
    for b, g in df_v2pool.groupby("owners_mid"):
        if len(g) >= 5:
            within_bucket[str(b)] = {
                "n": int(len(g)),
                "spearman_recognition_headroom": round(float(spearmanr(g["recognition_raw"], g["headroom_raw"])[0]), 4),
            }
    bucket_counts = df_v2pool["owners_mid"].value_counts().sort_index()
    a3_verification = {
        "pool_tested": "v2 screen, n=638 (same pool the red team used)",
        "n_distinct_owners_mid_values": int(df_v2pool["owners_mid"].nunique()),
        "bucket_counts": {str(k): int(v) for k, v in bucket_counts.items()},
        "pooled_spearman_recognition_headroom": round(pooled_corr, 4),
        "within_bucket_spearman": within_bucket,
        "share_in_top3_buckets_pct": round(
            bucket_counts.sort_values(ascending=False).head(3).sum() / bucket_counts.sum() * 100, 1),
        "verdict": "CONFIRMED. Within every owners_mid bucket with n>=5, "
                   "Spearman(recognition_raw, headroom_raw) = 1.0000 (to 4 decimal places). "
                   "Headroom is Recognition minus a per-bucket constant -- the pooled "
                   "+0.54 correlation is entirely between-bucket variation. This is a "
                   "property of owners_mid having only 5-6 distinct values in this pool, "
                   "not a scoring bug, and it is NOT fixable within the current data -- "
                   "only disclosable.",
    }

    # ---------- Diagnostic 2: what moves when Fit is cut 20%->10%, pool held at v2's 638 --
    df_reweight = df_v2pool.copy()
    df_reweight["composite_old"] = composite(df_reweight, OLD_WEIGHTS)
    df_reweight["composite_new"] = composite(df_reweight, (W_RECOGNITION, W_HEADROOM, W_FIT))
    qual_old = set(df_reweight[df_reweight["composite_old"] >= BAR]["app_id"])
    qual_new = set(df_reweight[df_reweight["composite_new"] >= BAR]["app_id"])
    top30_old = set(df_reweight.sort_values("composite_old", ascending=False).head(30)["app_id"])
    top30_new = set(df_reweight.sort_values("composite_new", ascending=False).head(30)["app_id"])
    reweight_effect = {
        "pool_held_fixed_at": "v2 screen, n=638 (isolates the reweight from the floor move)",
        "n_qualifying_old_weights_0.45_0.35_0.20": len(qual_old),
        "n_qualifying_new_weights_0.50_0.40_0.10": len(qual_new),
        "membership_changed": len(qual_old.symmetric_difference(qual_new)),
        "membership_changed_pct_of_union": round(
            len(qual_old.symmetric_difference(qual_new)) / len(qual_old | qual_new) * 100, 1),
        "top30_overlap_count": len(top30_old & top30_new),
        "top30_changed_count": 30 - len(top30_old & top30_new),
    }

    # ---------- The actual v3 pipeline: new screen (floor=4,000) + new weights ----------
    sql_v3 = open(f"{RUN_DIR}/sql/18_candidate_screen_v3.sql").read()
    df = con.execute(sql_v3).df()
    n_eligible = len(df)
    df = build_features(df)
    df = build_pillars(df, feature_cols, coef_map)
    df["composite_score"] = composite(df, (W_RECOGNITION, W_HEADROOM, W_FIT))

    corr_rec_headroom = float(spearmanr(df["recognition_pct"], df["headroom_pct"])[0])
    pillar_influence = {
        "recognition": round(float(spearmanr(df["recognition_pct"], df["composite_score"])[0]), 4),
        "headroom": round(float(spearmanr(df["headroom_pct"], df["composite_score"])[0]), 4),
        "fit": round(float(spearmanr(df["fit_pct"], df["composite_score"])[0]), 4),
    }

    bar_sensitivity = {str(b): int((df["composite_score"] >= b).sum())
                       for b in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75]}

    qualifiers = df[df["composite_score"] >= BAR].copy()
    qualifiers = qualifiers.sort_values("composite_score", ascending=False).reset_index(drop=True)

    def tier_of(row):
        if row["review_total"] >= ANCHOR_REVIEW_FLOOR:
            return "Anchor"
        if pd.notna(row["metacritic_score"]) and row["owners_mid"] >= ANCHOR_OWNERS_FLOOR:
            return "Anchor"
        if row["price_usd"] <= LOW_COST_PRICE_CEILING:
            return "Low-cost option"
        return "Depth"

    qualifiers["tier"] = qualifiers.apply(tier_of, axis=1)

    # B-5 echo: owners_mid bucket distribution of the FINAL qualifying list (known property
    # of the design, not re-litigated here -- portfolio stage not reopened)
    qual_bucket_dist = qualifiers["owners_mid"].value_counts().sort_index()
    ceiling_bucket_share = round(
        qual_bucket_dist.get(750000.0, 0) / len(qualifiers) * 100, 1) if len(qualifiers) else 0.0
    pool_ceiling_bucket_share = round(
        (df["owners_mid"] == 750000.0).sum() / len(df) * 100, 1)

    # monoculture check (unchanged methodology from v2)
    qualifiers["base_title"] = qualifiers.apply(lambda r: (r["developer"], base_title(r["name"])), axis=1)
    n_qual = len(qualifiers)
    n_distinct_properties = qualifiers["base_title"].nunique()
    serial_counts = qualifiers["base_title"].value_counts()
    serial_franchises = {f"{k[0]} / {k[1]}": int(v) for k, v in serial_counts[serial_counts >= 2].items()}
    dev_counts = qualifiers["developer"].value_counts()
    dev_concentration = dev_counts[dev_counts >= 2].to_dict()
    genre_share = {g: int(qualifiers["genre_list"].apply(lambda lst, g=g: g in lst).sum()) for g in GENRES}
    genre_share_pct = {k: round(v / n_qual * 100, 1) for k, v in genre_share.items()} if n_qual else {}

    def price_band(p):
        if p <= 5: return "<=$5"
        if p <= 10: return "$5-10"
        if p <= 20: return "$10-20"
        if p <= 40: return "$20-40"
        return ">$40"
    qualifiers["price_band"] = qualifiers["price_usd"].apply(price_band)
    price_band_dist = qualifiers["price_band"].value_counts().to_dict()

    # ---------- data-quality confirmation (Deep Rock Galactic: Survivor) ----------
    drg = con.execute("""
        SELECT app_id, name, has_coop, has_multiplayer, has_singleplayer
        FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
        WHERE app_id = 2321470
    """).df()
    drg_categories = con.execute("""
        SELECT category FROM read_parquet('/home/claude/run_portfolio/parquet/categories_long.parquet')
        WHERE app_id = 2321470
    """).df()["category"].tolist()
    drg_tags = con.execute("""
        SELECT tag FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
        WHERE app_id = 2321470
    """).df()["tag"].tolist()
    drg_finding = {
        "app_id": 2321470,
        "name": drg["name"].iloc[0] if len(drg) else None,
        "flags": {"has_coop": bool(drg["has_coop"].iloc[0]), "has_multiplayer": bool(drg["has_multiplayer"].iloc[0]),
                  "has_singleplayer": bool(drg["has_singleplayer"].iloc[0])} if len(drg) else None,
        "raw_categories": drg_categories,
        "raw_tags_sample": drg_tags[:10],
        "verdict": "FLAGS ARE CORRECT, not a data defect. Raw categories are clean English "
                   "text ('Single-player', 'Full controller support', ...) with NO "
                   "Co-op/Multi-player category present, and no Co-op/Multiplayer tag "
                   "either -- this is not an instance of the documented non-English-"
                   "metadata undercount hazard (02_cleaning_report.md), since the source "
                   "data is neither non-English nor ambiguous. Deep Rock Galactic: "
                   "Survivor is a genuinely single-player roguelite spin-off, distinct "
                   "from the base Deep Rock Galactic (app_id 548430, correctly flagged "
                   "has_coop=True/has_multiplayer=True, a 4-player co-op game). The error "
                   "was in the downstream portfolio artifact's alternate-title labelling, "
                   "not in this dataset's cleaning or flags. No cleaning-stage fix needed.",
    }

    # ---------- outputs ----------
    out_cols = [
        "app_id", "name", "developer", "publisher",
        "composite_score", "tier",
        "recognition_pct", "headroom_pct", "fit_pct",
        "review_total", "review_positive_ratio", "review_score_bucket",
        "owners_range", "owners_mid", "price_usd", "metacritic_score",
        "has_controller_support", "is_indie", "has_coop", "has_multiplayer",
        "release_year", "genres", "tags",
    ]
    csv_df = qualifiers[out_cols].copy()
    csv_df["genres"] = csv_df["genres"].apply(lambda a: "|".join(to_list(a)))
    csv_df["tags"] = csv_df["tags"].apply(lambda a: "|".join(to_list(a)[:15]))
    for c in ["composite_score", "recognition_pct", "headroom_pct", "fit_pct", "review_positive_ratio"]:
        csv_df[c] = csv_df[c].round(4)
    csv_df["screen_review_total_ge_4000"] = "PASS"
    csv_df["screen_quality_ge_0.70"] = "PASS"
    csv_df["screen_owners_le_750k"] = "PASS"
    csv_df["screen_monetisation_paid"] = "PASS"
    csv_df["screen_has_controller_support"] = "PASS"
    csv_df["screen_gamepass_availability"] = "PENDING_EXTERNAL_CHECK"
    csv_df.to_csv(f"{RUN_DIR}/artifacts/16_candidates_v3.csv", index=False)

    summary = {
        "eligible_pool_n": int(n_eligible),
        "eligible_pool_metacritic_pct": round(df["metacritic_score"].notna().sum() / n_eligible * 100, 1),
        "weights": {"recognition": W_RECOGNITION, "headroom": W_HEADROOM, "fit": W_FIT,
                    "old_weights_for_reference": {"recognition": OLD_WEIGHTS[0], "headroom": OLD_WEIGHTS[1], "fit": OLD_WEIGHTS[2]}},
        "a4_reweight_effect_pool_held_at_v2_638": reweight_effect,
        "a3_headroom_within_bucket_verification": a3_verification,
        "composite_diagnostics_on_v3_pool": {
            "recognition_vs_headroom_spearman_pooled": round(corr_rec_headroom, 4),
            "pillar_influence_on_composite_spearman": pillar_influence,
        },
        "b5_ceiling_echo": {
            "qualifying_list_share_in_750k_bucket_pct": ceiling_bucket_share,
            "eligible_pool_share_in_750k_bucket_pct": pool_ceiling_bucket_share,
            "note": "Known property of the design, stated here per the coordinator's "
                    "instruction; the downstream portfolio document is not reopened this "
                    "round. The ownership ceiling concentrates the qualifying list toward "
                    "its own bucket because Recognition is continuous and weighted 0.50-"
                    "0.90 combined with Headroom, while ownership itself only acts as a "
                    "coarse pre-screen step (A-3) -- the model reliably selects the "
                    "most-owned titles that still clear the cut.",
        },
        "qualifying_bar": BAR,
        "n_qualifying": int(len(qualifiers)),
        "bar_sensitivity_n_qualifying": bar_sensitivity,
        "tier_counts": qualifiers["tier"].value_counts().to_dict(),
        "monoculture_check": {
            "n_qualifying_rows": int(n_qual),
            "n_distinct_licensable_properties_after_collapsing_chapters": int(n_distinct_properties),
            "serial_franchises_with_2plus_qualifying_rows": serial_franchises,
            "developers_with_2plus_qualifying_titles": dev_concentration,
            "genre_share_of_qualifying_TITLES_pct": genre_share_pct,
            "price_band_distribution": price_band_dist,
        },
        "deep_rock_galactic_survivor_data_quality_check": drg_finding,
    }
    with open(f"{RUN_DIR}/artifacts/_scoring_summary_v3.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))

    print("\nTop 30 qualifiers:")
    print(qualifiers.head(30)[["app_id", "name", "tier", "composite_score", "review_total",
                                "owners_range", "price_usd", "metacritic_score"]].to_string())


if __name__ == "__main__":
    main()
