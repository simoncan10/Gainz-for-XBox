"""
Stage 20 (indie scoring) -- rescope to indie + PC-eligible, reusing the v2/v3 Fit model
and the v3 pillar weights UNCHANGED (Change 3: carry forward, re-test don't re-derive
blindly).

Screen: sql/20_indie_candidate_screen.sql (indie=true & self_published=true, no
controller-support gate, review_total>=4000, owners_mid<=750000 -- all re-tested against
the indie population in sql/20_indie_threshold_sensitivity.sql, both kept).

Composite: UNCHANGED formula and weights from v3 -- Recognition 0.50 / Headroom 0.40 /
Fit 0.10, using the SAME fitted Ridge coefficients as v2/v3 (artifacts/_ridge_coef_v2.npy
etc.) -- no retraining, since Change 3 explicitly carries the fit model forward. The A-3
Headroom disclosure (Recognition banded by a 3-level ownership step, not an independent
pillar) is re-verified on this new, smaller, indie-only pool rather than assumed to still
hold.
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

W_RECOGNITION, W_HEADROOM, W_FIT = 0.50, 0.40, 0.10
BAR = 0.60

# Recalibrated to THIS population's own distribution (median review_total ~7,250, vs
# v3's ~16,200 -- a straight carry-over of v3's 20,000-review Anchor floor would leave
# only 23/406 titles (5.7%) eligible for Anchor, reproducing the exact RT-07 defect this
# run must not repeat under new numbers).
ANCHOR_REVIEW_FLOOR = 10000
ANCHOR_OWNERS_FLOOR = 350000
LOW_COST_PRICE_CEILING = 10.0  # indie price distribution is itself lower; see script output


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
    struct_cols = [c for c in feature_cols if c != "log_age_days"]
    struct_coef = np.array([coef_map[c] for c in struct_cols])

    df = con.execute(open(f"{RUN_DIR}/sql/20_indie_candidate_screen.sql").read()).df()
    n_eligible = len(df)
    df = build_features(df)
    X_struct = df[struct_cols].values.astype(float)
    df["fit_raw"] = intercept + X_struct @ struct_coef

    df["recognition_raw"] = np.log(df["review_total"].values.astype(float))
    df["headroom_raw"] = np.log(df["review_total"].values.astype(float)) - np.log(df["owners_mid"].values.astype(float))
    df["recognition_pct"] = pct_rank(df["recognition_raw"].values)
    df["headroom_pct"] = pct_rank(df["headroom_raw"].values)
    df["fit_pct"] = pct_rank(df["fit_raw"].values)
    df["composite_score"] = W_RECOGNITION * df["recognition_pct"] + W_HEADROOM * df["headroom_pct"] + W_FIT * df["fit_pct"]

    corr_rec_headroom_pooled = float(spearmanr(df["recognition_raw"], df["headroom_raw"])[0])
    bucket_counts = df["owners_mid"].value_counts().sort_index()
    within_bucket = {}
    for b, g in df.groupby("owners_mid"):
        if len(g) >= 5:
            within_bucket[str(b)] = {"n": int(len(g)),
                "spearman": round(float(spearmanr(g["recognition_raw"], g["headroom_raw"])[0]), 4)}
    a3_check = {
        "n_distinct_owners_mid": int(df["owners_mid"].nunique()),
        "bucket_counts": {str(k): int(v) for k, v in bucket_counts.items()},
        "pooled_spearman_recognition_headroom": round(corr_rec_headroom_pooled, 4),
        "within_bucket_spearman": within_bucket,
    }

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

    # newly-admitted-vs-v3 check: which qualifiers here have has_controller_support=false
    # (could NOT have appeared in v3's list, regardless of indie status)
    n_no_controller = int((qualifiers["has_controller_support"] == False).sum())  # noqa: E712

    out_cols = [
        "app_id", "name", "developer", "publisher",
        "composite_score", "tier",
        "recognition_pct", "headroom_pct", "fit_pct",
        "review_total", "review_positive_ratio", "review_score_bucket",
        "owners_range", "owners_mid", "price_usd", "metacritic_score",
        "has_controller_support", "is_indie", "is_self_published",
        "has_coop", "has_multiplayer",
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
    csv_df["screen_is_indie_and_selfpublished"] = "PASS"
    csv_df["screen_controller_support"] = "NOT GATED (scored feature only, see 20_indie_scoring.md)"
    csv_df["screen_gamepass_availability"] = "PENDING_EXTERNAL_CHECK"
    csv_df.to_csv(f"{RUN_DIR}/artifacts/20_indie_candidates.csv", index=False)

    summary = {
        "eligible_pool_n": int(n_eligible),
        "eligible_pool_metacritic_pct": round(df["metacritic_score"].notna().sum() / n_eligible * 100, 1),
        "a3_headroom_check": a3_check,
        "pillar_influence_on_composite": pillar_influence,
        "qualifying_bar": BAR,
        "n_qualifying": int(len(qualifiers)),
        "n_qualifying_without_controller_support": n_no_controller,
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
    }
    with open(f"{RUN_DIR}/artifacts/_scoring_summary_v20.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))

    print("\nTop 20 qualifiers:")
    print(qualifiers.head(20)[["app_id", "name", "tier", "composite_score", "review_total",
                                "owners_range", "price_usd", "metacritic_score",
                                "has_controller_support"]].to_string())


if __name__ == "__main__":
    main()
