"""
Stage 10 (scoring) -- score the eligible pool (sql/12_candidate_screen.sql, n=18,955) on
four dimensions, combine into a composite, and apply the qualifying-bar threshold.

Dimensions map 1:1 onto the four pillars in the brief. Each is converted to a percentile
rank in [0,1] WITHIN the eligible pool, so all four are on the same scale and none
dominates by raw units. review_positive_ratio (quality) is NOT one of the four scored
dimensions -- it is already a hard gate (>=0.70, "Mostly Positive" or better) in
sql/12_candidate_screen.sql, so scoring on it again would double-count the same signal
that already decided eligibility.

  1. proven    = ln(review_total)                         (MEASURED) -- recognition/scale:
              how much real signal backs this title's reception, beyond the pass/fail
              floor of 50 reviews already applied.
  2. scarcity  = -owners_mid                                (MEASURED, coarse SteamSpy
              bucket proxy -- see caveats) -- not-already-owned.
  3. fit       = structural-only prediction from the Ridge model fit in
              11_build_fit_model.py, EXCLUDING the log_age_days control term (that term
              exists only to keep the "what wins" coefficients from being confounded by
              vintage -- including it here would just re-reward old age, which is not a
              "fit" property of the game). This is a DERIVED figure: a dot product of the
              fitted coefficients (from 10_model_fit.json) against each candidate's own
              structural features. It was fit on 60,502 titles OUTSIDE the eligible pool's
              own screen definition (a broader population, see 11_*.sql) and validated out
              of sample at Pearson r=0.56 / R^2=0.31 -- see artifacts/10_model_fit.json.
  4. cheap     = -price_usd                                 (MEASURED, proxy for licensing
              cost -- see caveats in 10_scoring.md)

Pillars 1 and 2 pull in opposite directions by construction (more reviews usually comes
with more owners), which is exactly the tension the brief calls out as the interesting
part of the problem -- a title that ranks well on BOTH at once (lots of proof, still a
small owner bucket) is precisely the "punches above its weight" profile a subscription
platform should want.

composite = mean of the four percentile ranks, equal weights (0.25 each) as the stated
default. A sensitivity check re-weighting toward fit and toward cheap is run separately
and reported in 10_model.json / 10_scoring.md.
"""
import json
import duckdb
import numpy as np
import pandas as pd
from scipy.stats import rankdata

RUN_DIR = "/home/claude/run_portfolio"

GENRES = ['Indie', 'Adventure', 'Action', 'Casual', 'Simulation', 'Strategy', 'RPG',
          'Free To Play', 'Early Access', 'Sports', 'Racing', 'Massively Multiplayer']
TAGS = ['Singleplayer', '2D', 'Atmospheric', 'Puzzle', '3D', 'Story Rich', 'Cute',
        'Colorful', 'Exploration', 'Pixel Graphics', 'First-Person', 'Multiplayer',
        'Anime', 'Fantasy', 'Funny', 'Arcade', 'Horror', 'Relaxing',
        'Female Protagonist', 'Shooter', 'Retro']


def pct_rank(x):
    return (rankdata(x, method="average") - 1) / (len(x) - 1)


def main():
    con = duckdb.connect()
    sql = open(f"{RUN_DIR}/sql/12_candidate_screen.sql").read()
    df = con.execute(sql).df()
    n_eligible = len(df)

    # attach genre/tag lists (fact_games already carries `genres`/`tags` arrays)
    def to_list(a):
        return list(a) if isinstance(a, (list, np.ndarray)) else []

    df["genre_list"] = df["genres"].apply(to_list)
    df["tag_list"] = df["tags"].apply(to_list)

    for g in GENRES:
        df[f"genre_{g}"] = df["genre_list"].apply(lambda lst, g=g: g in lst).astype(int)
    for t in TAGS:
        df[f"tag_{t}"] = df["tag_list"].apply(lambda lst, t=t: t in lst).astype(int)
    df["price_usd_filled"] = df["price_usd"].fillna(0.0)
    df["is_free_i"] = 0  # screen already restricts to monetisation_model='paid'
    df["is_indie_i"] = df["is_indie"].fillna(False).astype(int)
    df["is_self_pub_i"] = df["is_self_published"].fillna(False).astype(int)
    df["has_singleplayer_i"] = df["has_singleplayer"].fillna(False).astype(int)
    df["has_multiplayer_i"] = df["has_multiplayer"].fillna(False).astype(int)
    df["has_coop_i"] = df["has_coop"].fillna(False).astype(int)
    df["has_controller_i"] = df["has_controller_support"].fillna(False).astype(int)
    df["has_vr_i"] = df["has_vr"].fillna(False).astype(int)
    df["n_tags_filled"] = df["n_tags"].fillna(0)

    feature_cols = json.load(open(f"{RUN_DIR}/artifacts/_feature_cols.json"))
    coef = np.load(f"{RUN_DIR}/artifacts/_ridge_coef.npy")
    intercept = float(open(f"{RUN_DIR}/artifacts/_ridge_intercept.txt").read())
    coef_map = dict(zip(feature_cols, coef))

    structural_cols = [c for c in feature_cols if c != "log_age_days"]
    X_struct = df[structural_cols].values.astype(float)
    struct_coef = np.array([coef_map[c] for c in structural_cols])
    df["fit_raw"] = intercept + X_struct @ struct_coef

    # --- percentile ranks within the eligible pool ---
    df["proven_pct"] = pct_rank(np.log(df["review_total"].values.astype(float)))
    df["scarcity_pct"] = pct_rank(-df["owners_mid"].values)
    df["fit_pct"] = pct_rank(df["fit_raw"].values)
    df["cheap_pct"] = pct_rank(-df["price_usd"].values)

    df["composite_score"] = df[["proven_pct", "scarcity_pct", "fit_pct", "cheap_pct"]].mean(axis=1)

    # Sensitivity: alternate weightings
    df["composite_fit_heavy"] = (0.15 * df["proven_pct"] + 0.15 * df["scarcity_pct"]
                                  + 0.55 * df["fit_pct"] + 0.15 * df["cheap_pct"])
    df["composite_cheap_heavy"] = (0.20 * df["proven_pct"] + 0.20 * df["scarcity_pct"]
                                    + 0.10 * df["fit_pct"] + 0.50 * df["cheap_pct"])

    from scipy.stats import spearmanr
    rank_stability = {
        "equal_vs_fit_heavy_spearman": round(float(spearmanr(df["composite_score"], df["composite_fit_heavy"])[0]), 4),
        "equal_vs_cheap_heavy_spearman": round(float(spearmanr(df["composite_score"], df["composite_cheap_heavy"])[0]), 4),
    }

    # --- qualifying bar sensitivity ---
    bar_sensitivity = {}
    for bar in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75]:
        bar_sensitivity[str(bar)] = int((df["composite_score"] >= bar).sum())

    BAR = 0.60
    qualifiers = df[df["composite_score"] >= BAR].copy()
    qualifiers = qualifiers.sort_values("composite_score", ascending=False).reset_index(drop=True)

    # --- tiering ---
    # Tiers read the qualifying list as a portfolio, by ROLE -- not just re-slicing the
    # same composite score into thirds. A high composite score alone does not make a title
    # "Anchor" material if only 60 people ever reviewed it; the tier rule adds an explicit
    # recognition floor so "Anchor" means what a board would expect it to mean.
    #   Anchor          = review_total >= 1,000 (a genuinely well-attested reception, not
    #                      just past the 50-review proof floor -- these are the names
    #                      credible enough to lead the pitch with).
    #   Low-cost option = price_usd <= $5.00 and not already Anchor -- the deliberately
    #                      cheap, small-audience end; licensing risk is low because the ask
    #                      price is low, regardless of composite rank.
    #   Depth           = everything else that cleared the bar -- solid mid-tier qualifiers
    #                      that round out genre breadth without being flagship names or the
    #                      cheapest option.
    ANCHOR_REVIEW_FLOOR = 1000
    LOW_COST_PRICE_CEILING = 5.0

    def tier_of(row):
        if row["review_total"] >= ANCHOR_REVIEW_FLOOR:
            return "Anchor"
        if row["price_usd"] <= LOW_COST_PRICE_CEILING:
            return "Low-cost option"
        return "Depth"

    qualifiers["tier"] = qualifiers.apply(tier_of, axis=1)
    anchor_cut = ANCHOR_REVIEW_FLOOR  # kept in summary for reference

    # genre-within-rank check (monoculture test): top 30 by composite, tag distribution
    top30_tags = qualifiers.head(30)["tag_list"].explode().value_counts().head(10).to_dict()
    top30_genres = qualifiers.head(30)["genre_list"].explode().value_counts().head(10).to_dict()

    # rank-within-genre: primary genre assigned by RAREST matching genre first (not simple
    # list order), so a multi-tagged title isn't defaulted into whichever generic genre
    # happens to be checked first -- same heuristic used in the prior full-pipeline run
    # (01_profile.md-era genres are near-universal for Indie/Action/Adventure/Casual and
    # would otherwise swallow the diversity check).
    RAREST_FIRST = ['Massively Multiplayer', 'Racing', 'Sports', 'RPG', 'Strategy',
                    'Simulation', 'Casual', 'Adventure', 'Action']
    primary_genre = qualifiers["genre_list"].apply(
        lambda lst: next((g for g in RAREST_FIRST if g in lst), (lst[0] if lst else "Unknown"))
    )
    qualifiers["primary_genre_for_diversity_check"] = primary_genre
    genre_counts = qualifiers["primary_genre_for_diversity_check"].value_counts().to_dict()

    # --- write outputs ---
    out_cols = [
        "app_id", "name", "developer", "publisher",
        "composite_score", "tier",
        "proven_pct", "scarcity_pct", "fit_pct", "cheap_pct",
        "review_total", "review_positive_ratio", "review_score_bucket",
        "owners_range", "owners_mid", "price_usd",
        "is_indie", "has_coop", "has_multiplayer", "has_singleplayer",
        "release_year", "genres", "tags",
    ]
    csv_df = qualifiers[out_cols].copy()
    csv_df["genres"] = csv_df["genres"].apply(lambda a: "|".join(to_list(a)))
    csv_df["tags"] = csv_df["tags"].apply(lambda a: "|".join(to_list(a)[:15]))
    for c in ["composite_score", "proven_pct", "scarcity_pct", "fit_pct", "cheap_pct", "review_positive_ratio"]:
        csv_df[c] = csv_df[c].round(4)
    csv_df["screen_review_total_ge_50"] = "PASS"
    csv_df["screen_quality_ge_0.70"] = "PASS"
    csv_df["screen_owners_le_750k"] = "PASS"
    csv_df["screen_monetisation_paid"] = "PASS"
    csv_df["screen_gamepass_availability"] = "PENDING_EXTERNAL_CHECK"
    csv_df.to_csv(f"{RUN_DIR}/artifacts/10_candidates.csv", index=False)

    summary = {
        "eligible_pool_n": int(n_eligible),
        "qualifying_bar": BAR,
        "n_qualifying": int(len(qualifiers)),
        "bar_sensitivity_n_qualifying": bar_sensitivity,
        "rank_stability_under_reweighting": rank_stability,
        "tier_counts": qualifiers["tier"].value_counts().to_dict(),
        "top30_by_composite_tag_distribution": top30_tags,
        "top30_by_composite_genre_distribution": top30_genres,
        "qualifiers_primary_genre_distribution": genre_counts,
        "anchor_review_total_floor": ANCHOR_REVIEW_FLOOR,
        "low_cost_price_ceiling": LOW_COST_PRICE_CEILING,
    }
    with open(f"{RUN_DIR}/artifacts/_scoring_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))

    print("\nTop 20 qualifiers overall:")
    print(qualifiers.head(20)[["app_id", "name", "tier", "composite_score", "review_total",
                                "owners_range", "price_usd", "genres"]].to_string())

    for tier in ["Anchor", "Depth", "Low-cost option"]:
        sub = qualifiers[qualifiers["tier"] == tier].sort_values("composite_score", ascending=False)
        print(f"\nTop 15 in tier={tier} (n={len(sub)}):")
        print(sub.head(15)[["app_id", "name", "composite_score", "review_total",
                             "owners_range", "price_usd", "genres"]].to_string())


if __name__ == "__main__":
    main()
