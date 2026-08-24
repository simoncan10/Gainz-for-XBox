import json

RUN_DIR = "/home/claude/run_portfolio"

fit = json.load(open(f"{RUN_DIR}/artifacts/10_model_fit.json"))
scoring = json.load(open(f"{RUN_DIR}/artifacts/_scoring_summary.json"))

model = {
    "stage": "10 - scoring",
    "question": "Which specific games from the Steam snapshot should Xbox ADD to the Game "
                "Pass portfolio?",
    "pipeline": [
        "1. sql/12_candidate_screen.sql -- hard eligibility screen -> ELIGIBLE POOL",
        "2. sql/11_fit_model_population.sql + scripts/11_build_fit_model.py -- fit the "
        "'what wins' model on a broader population, validate out of sample",
        "3. scripts/12_score_candidates.py -- score the eligible pool on 4 pillars, apply "
        "composite threshold -> QUALIFYING LIST, assign tiers",
    ],
    "eligibility_screen": {
        "sql_file": "sql/12_candidate_screen.sql",
        "population_before_screen": {"is_demo_false_games": 122191, "sql_file": "sql/01_profile facts (02_cleaning_report.md)"},
        "thresholds": [
            {
                "rule": "is_demo = false AND app_type = 'game'",
                "reason": "Demos are not licensable catalogue additions.",
            },
            {
                "rule": "monetisation_model = 'paid' AND price_usd > 0",
                "reason": "A free-to-play title gives Game Pass no exclusivity value (it "
                          "is already free to everyone) and has no usable price for the "
                          "cost proxy. 4,057 rows labelled 'paid' with price_usd=0 were "
                          "additionally excluded as a data defect (e.g. app_id 925100, "
                          "an Elder Scrolls Online expansion with a stale/regional $0 "
                          "steamspy price, not a real free listing) -- caught by spot-"
                          "checking the first uncorrected run.",
            },
            {
                "rule": "review_total >= 50",
                "reason": "Proven. Valve's own review-score algorithm requires 50 reviews "
                          "before a title gets a nuanced label (Mostly/Very/Overwhelmingly "
                          "Positive); below that the label is a coarse binary Positive/"
                          "Negative (10-49) or 'Not enough user reviews' (<10). Empirically "
                          "confirmed against review_score_bucket boundaries in this dataset "
                          "-- sql/09_review_bucket_check.sql, n=122,191.",
                "sensitivity": "Eligible-pool size at review_total>=25/50/100/250/500 "
                                "(pre-adult/price screen): 24,870 / 18,955 / 14,346 / "
                                "9,467 / 6,562.",
            },
            {
                "rule": "review_positive_ratio >= 0.70",
                "reason": "Quality floor. 0.70 is Valve's own published boundary for "
                          "'Mostly Positive' or better -- confirmed empirically: the "
                          "'Mixed' bucket tops out at exactly 0.700 and 'Mostly Positive' "
                          "starts at exactly 0.700 in this dataset (sql/09_review_bucket_"
                          "check.sql). Below this a title is 'Mixed' reception at best.",
                "sensitivity": "Eligible-pool size at ratio>=0.40/0.60/0.70/0.80 (pre-"
                                "adult/price screen): 24,749 / 22,077 / 18,955 / 13,745.",
            },
            {
                "rule": "owners_mid <= 750,000",
                "reason": "Not already widely owned. Empirically, this dataset's "
                          "owners_mid>=1,000,000 tier is where already-ubiquitous "
                          "franchise names cluster: Starfield, Baldur's Gate 3, Elden "
                          "Ring, Persona 5 Royal, Assassin's Creed Origins (sql/12b_"
                          "ownership_ceiling_spotcheck.sql) -- titles Xbox already "
                          "publishes or the market has already reached at scale. 750,000 "
                          "keeps the top of the 500k-1M bucket (still recognizable, still "
                          "far from saturated) while excluding the 1M+ tier.",
                "sensitivity": "Eligible-pool size at ceiling=200k/350k/750k/1M/1.5M/3.5M "
                                "(pre-adult/price screen): 16,499 / 18,172 / 18,955 / "
                                "18,955 / 19,427 / 19,732 -- the pool size is NOT very "
                                "sensitive to this choice because the review-count and "
                                "quality screens already do most of the filtering.",
            },
            {
                "rule": "no 'Sexual Content' / 'Nudity' / 'Hentai' tag",
                "reason": "Platform-fit screen, not a taste judgment: Microsoft Store / "
                          "Xbox content policy restricts explicit sexual content far more "
                          "tightly than Steam's storefront does. Excludes 2,836 titles. "
                          "Verified necessary: several of these titles topped the "
                          "composite score on review volume and cheap price alone before "
                          "this screen was added (meme/shock titles farming ironic "
                          "positive reviews) -- a board recommendation containing them "
                          "would fail on its face regardless of the metrics behind it.",
            },
        ],
        "eligible_pool_n": scoring["eligible_pool_n"],
        "eligible_pool_share_of_catalogue": round(scoring["eligible_pool_n"] / 122191, 4),
    },
    "fit_model": fit,
    "composite_scoring": {
        "formula": "composite_score = mean(proven_pct, scarcity_pct, fit_pct, cheap_pct), "
                    "each a percentile rank in [0,1] computed WITHIN the eligible pool "
                    "(n=15,921)",
        "pillars": {
            "1_proven": "percentile rank of ln(review_total) -- recognition/scale beyond "
                        "the pass/fail 50-review floor. MEASURED.",
            "2_scarcity": "percentile rank of -owners_mid -- not-already-owned. MEASURED, "
                          "coarse SteamSpy bucket proxy (83.2% of the whole catalogue sits "
                          "in the bottom bucket per 01_profile.md -- owners_mid has weak "
                          "resolution below ~200k and should be read as an order-of-"
                          "magnitude proxy, not a precise count).",
            "3_fit": "DERIVED. Structural-only prediction from the Ridge model, "
                     "EXCLUDING the log_age_days control term (which exists only to stop "
                     "vintage from confounding the genre/tag coefficients -- including it "
                     "here would just reward age, not fit).",
            "4_cheap": "percentile rank of -price_usd -- MEASURED, proxy for licensing "
                       "cost. price_usd is a retail-price proxy, not an observed licensing "
                       "fee; no licensing-fee data exists in this dataset or was sourced "
                       "externally. Directional only: assumes lower retail price broadly "
                       "correlates with lower Game Pass acquisition cost, which is a "
                       "reasonable but unverified assumption.",
        },
        "why_equal_weights": "0.25 each is the transparent, no-further-assumptions "
                              "default across four pillars that are not all measured on "
                              "the same scale and have no external ground truth to fit "
                              "weights against. Reweighted alternatives were tested for "
                              "rank stability (below) rather than picked to alter the "
                              "outcome.",
        "quality_gate_not_scored": "review_positive_ratio is a hard gate (>=0.70) in the "
                                    "eligibility screen, not a 5th scored pillar -- "
                                    "scoring on it again would double-count the same "
                                    "signal that already decided eligibility.",
        "rank_stability_under_reweighting": scoring["rank_stability_under_reweighting"],
        "rank_stability_note": "Spearman correlation between the equal-weight ranking and "
                                "a fit-heavy (55%) reweighting is 0.75; against a cheap-"
                                "heavy (50%) reweighting it is 0.56. The list's membership "
                                "and rough ordering survive fit-heavy reweighting well; it "
                                "is moderately sensitive to how much weight 'cheap' "
                                "carries -- read the exact rank order as indicative, not "
                                "precise, especially near the qualifying bar.",
    },
    "qualifying_bar": {
        "value": scoring["qualifying_bar"],
        "n_qualifying": scoring["n_qualifying"],
        "share_of_eligible_pool": round(scoring["n_qualifying"] / scoring["eligible_pool_n"], 4),
        "share_of_whole_catalogue": round(scoring["n_qualifying"] / 122191, 4),
        "reason": "composite_score is the mean of four uniform-on-[0,1] percentile ranks, "
                  "so a random/unremarkable title scores ~0.50 by construction. A bar of "
                  "0.60 requires a title to outperform the ALREADY-SCREENED pool (itself "
                  "the top 13.0% of the non-demo catalogue) by a further meaningful margin "
                  "across all four pillars simultaneously -- not just be adequate on one. "
                  "The result is a list that is the top ~1.5% of the entire 122,191-title "
                  "non-demo catalogue, small enough to be a curated shortlist and large "
                  "enough that a portfolio, not a single bet, can be built from it.",
        "sensitivity": scoring["bar_sensitivity_n_qualifying"],
    },
    "tiers": {
        "rule": "Priority order: review_total>=1,000 -> Anchor; else price_usd<=$5.00 -> "
                "Low-cost option; else -> Depth. NOT a re-slice of the composite score "
                "into thirds -- a high composite score alone does not make a title "
                "'Anchor' material if only ~60 people ever reviewed it.",
        "counts": scoring["tier_counts"],
        "characterisation": {
            "Anchor": "n=538. price $0.49-$49.99 (median $4.99), review_total median "
                      "2,597 / p90 8,352. The most well-attested reception in the "
                      "qualifying list.",
            "Depth": "n=487. price $5.19-$69.99 (median $9.99), review_total median 366 "
                     "/ p90 751. Solid mid-tier titles that round out genre breadth "
                     "without being flagship names or the cheapest option.",
            "Low-cost option": "n=856. price $0.27-$4.99 (median $2.99), review_total "
                                "median 233 / p90 684. Deliberately cheap, smaller-"
                                "audience picks -- low licensing risk because the retail "
                                "price itself is low.",
        },
    },
    "diversity_check": {
        "note": "'Primary genre' assigned by RAREST matching genre tag first (Massively "
                "Multiplayer > Racing > Sports > RPG > Strategy > Simulation > Casual > "
                "Adventure > Action), not simple list order or first-listed genre -- "
                "otherwise near-universal tags (Indie, Adventure, Action, Casual) would "
                "swallow the check regardless of the real content mix.",
        "qualifiers_primary_genre_distribution": scoring["qualifiers_primary_genre_distribution"],
        "verdict": "No single genre exceeds 20.1% of the qualifying list (RPG 378/1,881). "
                   "The list is genuinely genre-diverse -- this is NOT a monoculture "
                   "finding; see 10_scoring.md for the top-of-list tag/genre check that "
                   "was run specifically to test whether the ranking metric was just "
                   "restating its own inputs.",
        "top30_by_composite_tag_distribution": scoring["top30_by_composite_tag_distribution"],
        "top30_by_composite_genre_distribution": scoring["top30_by_composite_genre_distribution"],
    },
    "producer_level_finding": {
        "sql_file": "sql/14_producer_check.sql",
        "finding": "Several small developers place MULTIPLE titles in the qualifying "
                   "list, evidence of a repeatable formula rather than a single lucky "
                   "hit: Randumb Studios (21 qualifying titles -- a cheap ~$2 interactive-"
                   "fiction/choice-quiz format, flagship title 'The Test' has 19,646 "
                   "reviews at 500k-1M owners), Chilla's Art (10 titles -- a known "
                   "Japanese indie horror studio), 07th Expansion (8 titles -- the "
                   "visual-novel studio behind the Higurashi/Umineko series).",
        "caveat": "This is a genuine repeat-qualifier pattern (n=21/10/8 titles per "
                  "studio, well above noise), not a single-title fluke, but it has NOT "
                  "been checked against Game Pass availability, and licensing a large "
                  "back-catalogue from one small studio concentrates counterparty risk "
                  "in a way a single-title pick does not -- flagged for the strategist, "
                  "not resolved here.",
        "adjacent_unvetted_finding_interesting_not_defensible": "sql/14_producer_check.sql "
            "run at the broader ELIGIBLE-POOL level (before the composite score/bar, "
            "n=15,921) shows established studios with unexpectedly large numbers of "
            "niche back-catalogue titles clearing the proof+quality+ownership screens: "
            "Kairosoft (38), KOEI TECMO (38), Square Enix (32), Nihon Falcom (27). None "
            "of these placed a title in the actual top-composite qualifying list shown "
            "above -- their titles tend to score lower on 'cheap' (higher price) and "
            "'fit' than the small-studio qualifiers do. This is flagged as INTERESTING "
            "BUT NOT YET DEFENSIBLE: it suggests a possible 'deep-catalogue licensing' "
            "angle (bundling many niche titles from one already-relationship-holding "
            "publisher) that this scoring model was not built to evaluate, and it has "
            "not been composite-ranked or reweighted to test.",
    },
    "hard_limits_carried_forward": [
        "No engagement or playtime data exists in this dataset -- every playtime column "
        "is constant zero (01_profile.md, 02_cleaning_report.md). Nothing here measures "
        "retention or session length; 'proven' means review volume/quality, not "
        "engagement.",
        "owners_mid is a linear midpoint of a SteamSpy BUCKET, not a measured sale count "
        "or a Game Pass audience estimate.",
        "review counts are self-selected and vary by genre, price, and audience size -- "
        "not adjusted for this in the current model beyond the age-since-release control.",
        "category flags (has_coop, has_multiplayer, is_indie) are a FLOOR: some source "
        "categories are non-English and undercounted (02_cleaning_report.md localization "
        "hazard) -- not used as hard screens for this reason, only as fit-model features.",
        "price_usd is USD via steamspy, never EUR.",
        "release_date is right-truncated (nothing after 2024-10-28) and 20.4% missing -- "
        "the fit model's age control partially addresses this but candidates released in "
        "the last few months of the visible window are still under-counted on reviews "
        "relative to their eventual total.",
        "Game Pass availability is NOT in this dataset and was NOT guessed. Every row in "
        "10_candidates.csv carries screen_gamepass_availability=PENDING_EXTERNAL_CHECK -- "
        "a later stage must check this per title, with a source and a date, before any "
        "title here is actually pitched.",
    ],
}

with open(f"{RUN_DIR}/artifacts/10_model.json", "w") as f:
    json.dump(model, f, indent=2)

print("wrote artifacts/10_model.json")
