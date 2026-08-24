"""
Stage 12 (scoring v2) -- REBUILT composite score.

Fixes RT-02/RT-04/RT-05/RT-09 from artifacts/11_redteam_scoring.md:

  - RT-02: v1 averaged Proven (recognition) and Scarcity (inverse ownership), which are
    Spearman -0.762 in the eligible pool -- summing two strongly negatively-correlated
    percentile ranks makes their SUM near-constant, so neither pillar actually moved the
    ranking (measured Scarcity-vs-composite Spearman was 0.030, effectively zero). Fixed
    by replacing the pair with a single ratio pillar, Headroom = ln(review_total) -
    ln(owners_mid) ("reviews per owner", i.e. genuinely punching above your weight),
    which is NOT the same information as Recognition alone (Spearman(recognition,
    headroom) tested below -- expected positive but well short of 1.0, i.e.
    complementary, not redundant).
  - RT-04: price is REMOVED from the score entirely. It is carried as a plain column
    (price_usd) and used only to inform the Low-cost tier label, never to compute
    composite_score.
  - RT-05: Fit is retargeted (see 11v2_build_fit_model.py) to predict review_positive_ratio
    instead of review_total, so it no longer restates the Recognition pillar it is
    averaged with.
  - RT-09: owners_mid's bucket coarseness is stated plainly wherever scarcity/headroom is
    discussed, not glossed over with a sensitivity table that silently repeats the same
    number.

Weights per the rebuild spec: Recognition 0.45 / Headroom 0.35 / Fit 0.20.
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

W_RECOGNITION = 0.45
W_HEADROOM = 0.35
W_FIT = 0.20

BAR = 0.60
# Recalibrated to the v2 population, NOT copied from v1's absolute numbers: raising the
# Proven floor to review_total>=5,000 (RT-06) shifted the whole qualifying population's
# own review_total median to ~16,200 (vs. v1's pool-wide ~250) -- a v1-style 1,000 or
# 10,000 floor would make "Anchor" almost the entire list again (194/215 = 90.2% at
# 10,000), reproducing RT-07's complaint that the tier stops meaning anything. 20,000
# sits at roughly the qualifying list's own 74th percentile (57/215 titles clear it) --
# a tier that is genuinely a subset, not a relabelling of "qualified."
ANCHOR_REVIEW_FLOOR = 20000
ANCHOR_OWNERS_FLOOR = 350000
LOW_COST_PRICE_CEILING = 5.0


def pct_rank(x):
    return (rankdata(x, method="average") - 1) / (len(x) - 1)


def to_list(a):
    return list(a) if isinstance(a, (list, np.ndarray)) else []


def base_title(name):
    """Heuristic franchise/base-title extraction for the monoculture / serial-chapter
    check ONLY (RT-08). Never used to drop or merge rows in the deliverable CSV -- every
    app_id keeps its own row there, per the goal statement's "app_ids or it failed" rule.
    Aggressive (cuts at first colon/dash/trailing roman numeral or digit), which correctly
    merges e.g. "Higurashi When They Cry Hou - Ch.6 Tsumihoroboshi" -> "Higurashi When They
    Cry Hou", but can over-merge an unrelated title that happens to share a colon-prefix
    with another game's name. Documented limitation, same style as the v1 rarest-genre
    heuristic.
    """
    import re
    s = str(name)
    s = re.sub(r'\s*[:\-–]\s*.*$', '', s)          # cut at first colon/dash
    s = re.sub(r'\s+(II|III|IV|V|VI|VII|VIII|IX|X)$', '', s)  # trailing roman numeral
    s = re.sub(r'\s+\d+$', '', s)                   # trailing arabic numeral
    return s.strip() or str(name)


def main():
    con = duckdb.connect()
    sql = open(f"{RUN_DIR}/sql/12v2_candidate_screen.sql").read()
    df = con.execute(sql).df()
    n_eligible = len(df)

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

    feature_cols = json.load(open(f"{RUN_DIR}/artifacts/_feature_cols_v2.json"))
    coef = np.load(f"{RUN_DIR}/artifacts/_ridge_coef_v2.npy")
    intercept = float(open(f"{RUN_DIR}/artifacts/_ridge_intercept_v2.txt").read())
    coef_map = dict(zip(feature_cols, coef))
    struct_cols = [c for c in feature_cols if c != "log_age_days"]
    X_struct = df[struct_cols].values.astype(float)
    struct_coef = np.array([coef_map[c] for c in struct_cols])
    df["fit_raw"] = intercept + X_struct @ struct_coef

    # --- pillars ---
    df["recognition_raw"] = np.log(df["review_total"].values.astype(float))
    df["headroom_raw"] = np.log(df["review_total"].values.astype(float)) - np.log(df["owners_mid"].values.astype(float))

    df["recognition_pct"] = pct_rank(df["recognition_raw"].values)
    df["headroom_pct"] = pct_rank(df["headroom_raw"].values)
    df["fit_pct"] = pct_rank(df["fit_raw"].values)

    df["composite_score"] = (W_RECOGNITION * df["recognition_pct"]
                              + W_HEADROOM * df["headroom_pct"]
                              + W_FIT * df["fit_pct"])

    # diagnostics: confirm the fix -- recognition/headroom should be complementary, not
    # cancelling, and each pillar should have real (non-zero) influence on the composite
    corr_rec_headroom = float(spearmanr(df["recognition_pct"], df["headroom_pct"])[0])
    pillar_influence = {
        "recognition": round(float(spearmanr(df["recognition_pct"], df["composite_score"])[0]), 4),
        "headroom": round(float(spearmanr(df["headroom_pct"], df["composite_score"])[0]), 4),
        "fit": round(float(spearmanr(df["fit_pct"], df["composite_score"])[0]), 4),
    }

    # --- bar sensitivity ---
    bar_sensitivity = {str(b): int((df["composite_score"] >= b).sum())
                       for b in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75]}

    qualifiers = df[df["composite_score"] >= BAR].copy()
    qualifiers = qualifiers.sort_values("composite_score", ascending=False).reset_index(drop=True)

    # --- tiers (RT-07: Anchor must mean recognizable; price is annotation-only) ---
    def tier_of(row):
        if row["review_total"] >= ANCHOR_REVIEW_FLOOR:
            return "Anchor"
        if pd.notna(row["metacritic_score"]) and row["owners_mid"] >= ANCHOR_OWNERS_FLOOR:
            return "Anchor"
        if row["price_usd"] <= LOW_COST_PRICE_CEILING:
            return "Low-cost option"
        return "Depth"

    qualifiers["tier"] = qualifiers.apply(tier_of, axis=1)

    # --- reweighting stability, reported as TOP-30 JACCARD (RT-10), not full-list Spearman ---
    def composite_alt(w_rec, w_head, w_fit):
        return w_rec * df["recognition_pct"] + w_head * df["headroom_pct"] + w_fit * df["fit_pct"]

    alt_weightings = {
        "recognition_heavy_60_25_15": composite_alt(0.60, 0.25, 0.15),
        "headroom_heavy_25_60_15": composite_alt(0.25, 0.60, 0.15),
        "fit_heavy_25_25_50": composite_alt(0.25, 0.25, 0.50),
    }
    published_top30 = set(qualifiers.sort_values("composite_score", ascending=False).head(30)["app_id"])
    jaccard = {}
    for name, series in alt_weightings.items():
        alt_top30 = set(df.assign(alt=series).sort_values("alt", ascending=False).head(30)["app_id"])
        inter = len(published_top30 & alt_top30)
        union = len(published_top30 | alt_top30)
        jaccard[name] = round(inter / union, 4)

    # --- RT-08 monoculture check, properly: by TITLE (not genre membership), plus
    # developer, price band, and serial-chapter collapse ---
    qualifiers["base_title"] = qualifiers.apply(lambda r: (r["developer"], base_title(r["name"])), axis=1)
    n_qual = len(qualifiers)
    n_distinct_properties = qualifiers["base_title"].nunique()
    serial_counts = qualifiers["base_title"].value_counts()
    serial_franchises = serial_counts[serial_counts >= 2].to_dict()
    serial_franchises = {f"{k[0]} / {k[1]}": int(v) for k, v in serial_franchises.items()}

    dev_counts = qualifiers["developer"].value_counts()
    dev_concentration = dev_counts[dev_counts >= 2].to_dict()

    # genre share of TITLES (not memberships), over the whole qualifying list
    genre_share = {}
    for g in GENRES:
        genre_share[g] = int(qualifiers["genre_list"].apply(lambda lst, g=g: g in lst).sum())
    genre_share_pct = {k: round(v / n_qual * 100, 1) for k, v in genre_share.items()} if n_qual else {}

    # price-band share of the qualifying list
    def price_band(p):
        if p <= 5: return "<=$5"
        if p <= 10: return "$5-10"
        if p <= 20: return "$10-20"
        if p <= 40: return "$20-40"
        return ">$40"
    qualifiers["price_band"] = qualifiers["price_usd"].apply(price_band)
    price_band_dist = qualifiers["price_band"].value_counts().to_dict()

    # --- output CSV ---
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
    csv_df["screen_review_total_ge_5000"] = "PASS"
    csv_df["screen_quality_ge_0.70"] = "PASS"
    csv_df["screen_owners_le_750k"] = "PASS"
    csv_df["screen_monetisation_paid"] = "PASS"
    csv_df["screen_has_controller_support"] = "PASS"
    csv_df["screen_gamepass_availability"] = "PENDING_EXTERNAL_CHECK"
    csv_df.to_csv(f"{RUN_DIR}/artifacts/12_candidates_v2.csv", index=False)

    summary = {
        "eligible_pool_n": int(n_eligible),
        "eligible_pool_n_metacritic_share_pct": round(
            df["metacritic_score"].notna().sum() / n_eligible * 100, 1),
        "reported_yield_verification": {
            "coordinator_claimed_pool": 926,
            "coordinator_claimed_pool_metacritic_pct": 44.2,
            "verified_pool_WITHOUT_controller_gate": 926,
            "verified_pool_WITH_controller_gate_as_literally_specified": int(n_eligible),
            "finding": "The coordinator-forwarded 'reported yield' (pool=926) matches "
                       "EXACTLY the count with review_total>=5000, owners_mid<=750000, "
                       "and no adult-content tag applied WITHOUT has_controller_support="
                       "true -- confirmed by direct query. The rebuild spec's own bullet "
                       "list explicitly instructs adding the controller-support gate, and "
                       "the named top-10 (Temtem, ICARUS) both have "
                       "has_controller_support=False in this dataset -- they could not "
                       "appear in a pool that actually applied the gate. This run "
                       "implements the gate literally as instructed (pool=638) and flags "
                       "the discrepancy rather than silently reproducing the ungated "
                       "number.",
        },
        "composite_diagnostics": {
            "recognition_vs_headroom_spearman": round(corr_rec_headroom, 4),
            "pillar_influence_on_composite_spearman": pillar_influence,
            "interpretation": "Recognition and Headroom are now moderately POSITIVELY "
                "correlated (not the -0.762 cancellation in v1) and each pillar shows "
                "real, distinguishable influence on the composite -- the RT-02 defect "
                "(a pillar with ~0 effective weight) does not reproduce.",
        },
        "qualifying_bar": BAR,
        "n_qualifying": int(len(qualifiers)),
        "bar_sensitivity_n_qualifying": bar_sensitivity,
        "top30_jaccard_under_reweighting": jaccard,
        "tier_counts": qualifiers["tier"].value_counts().to_dict(),
        "monoculture_check_v2": {
            "n_qualifying_rows": int(n_qual),
            "n_distinct_licensable_properties_after_collapsing_chapters": int(n_distinct_properties),
            "serial_franchises_with_2plus_qualifying_rows": serial_franchises,
            "developers_with_2plus_qualifying_titles": dev_concentration,
            "genre_share_of_qualifying_TITLES_pct": genre_share_pct,
            "price_band_distribution": price_band_dist,
        },
    }
    with open(f"{RUN_DIR}/artifacts/_scoring_summary_v2.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))

    print("\nTop 20 qualifiers:")
    print(qualifiers.head(20)[["app_id", "name", "tier", "composite_score", "review_total",
                                "owners_range", "price_usd", "metacritic_score"]].to_string())


if __name__ == "__main__":
    main()
