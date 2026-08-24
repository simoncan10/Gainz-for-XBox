import json

RUN_DIR = "/home/claude/run_portfolio"

fit = json.load(open(f"{RUN_DIR}/artifacts/12_model_v2_fit.json"))
scoring = json.load(open(f"{RUN_DIR}/artifacts/_scoring_summary_v2.json"))

model = {
    "stage": "12 - scoring v2 (rebuild after red-team verdict REBUILD, artifacts/11_redteam_scoring.md)",
    "question": "Which specific games from the Steam snapshot should Xbox ADD to the Game "
                "Pass portfolio?",
    "verified_determinism": "sql/11v2_fit_model_population.sql adds ORDER BY app_id; "
        "scripts/11v2_build_fit_model.py additionally re-sorts by app_id in pandas before "
        "every train_test_split call. Re-running scripts/11v2_build_fit_model.py and "
        "scripts/12v2_score_candidates.py twice in this session produced IDENTICAL "
        "eligible_pool_n (638), n_qualifying (215), and top-20 order both times -- RT-01 "
        "is fixed. Canonical model artifacts (_ridge_coef_v2.npy, _ridge_intercept_v2.txt, "
        "_feature_cols_v2.json) are committed to artifacts/ so scripts/12v2_score_"
        "candidates.py runs end to end from a clean checkout without needing to refit.",
    "reported_yield_verification": scoring["reported_yield_verification"],
    "eligibility_screen": {
        "sql_file": "sql/12v2_candidate_screen.sql",
        "population_before_screen_n": 122191,
        "thresholds": [
            {"rule": "monetisation_model='paid' AND price_usd>0", "status": "unchanged from v1"},
            {"rule": "review_positive_ratio>=0.70", "status": "unchanged from v1 (Valve's own 'Mostly Positive' boundary)"},
            {"rule": "no Sexual Content/Nudity/Hentai tag", "status": "unchanged from v1"},
            {
                "rule": "review_total >= 5,000 (was >= 50)",
                "reason_this_run_gives_for_5000_specifically": (
                    "v1 borrowed Valve's own review-count floor (50), which answers a "
                    "different question (is the rating statistically meaningful?) than "
                    "the one the Proven/Recognition screen needs to answer (would a "
                    "subscriber recognise this title?). 5,000 is justified here on its "
                    "own terms by an elbow in metacritic-presence (a real press-coverage "
                    "signal, unlike review count itself): metacritic share rises steeply "
                    "with the floor from 33.4% (>=500) to 48.0% (>=5,000), then FLATTENS "
                    "(47.4% at >=7,500, 47.6% at >=10,000) -- 5,000 sits right at the "
                    "point where raising the floor further stops buying additional "
                    "recognition-density and only shrinks the pool. It is also two clean "
                    "orders of magnitude above Valve's 50-review nuance floor, making "
                    "clear it is a deliberately different, higher bar chosen for a "
                    "different purpose, not a re-use of the earlier number."
                ),
                "sensitivity_table_review_total_owners_fixed_at_750k_controller_gate_on": {
                    "500": {"n": 3241, "metacritic_pct": 33.4},
                    "1000": {"n": 2239, "metacritic_pct": 38.2},
                    "2000": {"n": 1442, "metacritic_pct": 42.2},
                    "3000": {"n": 1047, "metacritic_pct": 44.6},
                    "5000": {"n": 638, "metacritic_pct": 48.0},
                    "7500": {"n": 399, "metacritic_pct": 47.4},
                    "10000": {"n": 271, "metacritic_pct": 47.6},
                    "15000": {"n": 132, "metacritic_pct": 44.7},
                },
                "sql_file": "sql/17_threshold_sensitivity_v2.sql",
            },
            {
                "rule": "owners_mid <= 750,000 (KEPT per explicit instruction)",
                "reason": "Not re-justified from scratch since the instruction was to "
                          "keep it, but stated honestly per RT-09: owners_mid has only 6 "
                          "distinct values in the eligible pool, and there is NO value "
                          "between 750,000 and 1,499,999 -- so this ceiling is "
                          "bucket-equivalent to <=1,499,999, not a fine 750,000 cut. "
                          "Sensitivity confirms: ceiling=750,000 and ceiling=1,000,000 "
                          "give the IDENTICAL pool (n=638) because no title's owners_mid "
                          "falls in between.",
                "sensitivity_table_review_total_fixed_at_5000_controller_gate_on": {
                    "200000": 35, "350000": 278, "500000": 278, "750000": 638,
                    "1000000": 638, "1500000": 885, "2000000": 885, "3500000": 1063,
                },
                "sql_file": "sql/17_threshold_sensitivity_v2.sql",
            },
            {
                "rule": "has_controller_support = true (ADDED, per rebuild spec RT-11)",
                "reason": "Evidence-backed, not a taste screen: has_controller_i is a "
                          "consistently positive structural trait across both the v1 and "
                          "v2 fit models. It is also the direct, stated Steam-PC to "
                          "Xbox-console platform-fit gate the brief requires: a title "
                          "with no controller support on Steam carries materially higher "
                          "console-certification and control-scheme risk for a console "
                          "subscription service.",
                "effect_measured": "Applying this gate on top of the other 4 screens "
                          "shrinks the pool from 926 to 638 (31.1% removed) and RAISES "
                          "metacritic presence from 44.2% to 48.0% -- the gate "
                          "concentrates recognition rather than diluting it.",
            },
        ],
        "eligible_pool_n": scoring["eligible_pool_n"],
        "eligible_pool_metacritic_share_pct": scoring["eligible_pool_n_metacritic_share_pct"],
    },
    "fit_model_v2": fit,
    "composite_scoring_v2": {
        "formula": "composite_score = 0.45*recognition_pct + 0.35*headroom_pct + 0.20*fit_pct, "
                    "each a percentile rank in [0,1] WITHIN the eligible pool (n=638)",
        "pillars": {
            "recognition_0.45": "percentile of ln(review_total) -- scale of proof/"
                "recognition. MEASURED.",
            "headroom_0.35": "percentile of [ln(review_total) - ln(owners_mid)] -- "
                "'reviews per owner', replacing v1's cancelling Proven+Scarcity pair "
                "with a single ratio that directly encodes 'punches above its weight'. "
                "DERIVED from two Measured quantities.",
            "fit_0.20": "structural Ridge prediction, RETARGETED to predict "
                "review_positive_ratio (not review_total, per RT-05), price excluded "
                "from its features, is_indie_i dropped (RT-05 collinearity). DERIVED, "
                "out-of-sample validated, weak-to-moderate (see fit_model_v2 above).",
            "price_REMOVED": "price_usd no longer appears anywhere in composite_score. "
                "Carried as a plain reported column and used only to assign the "
                "Low-cost option tier label -- never to compute rank, per the rebuild "
                "spec.",
        },
        "rt02_fix_verification": scoring["composite_diagnostics"],
        "rt10_fix_top30_jaccard_under_reweighting": scoring["top30_jaccard_under_reweighting"],
        "rt10_fix_note": "Reported as top-30 SET OVERLAP (Jaccard), not full-pool "
            "Spearman, per RT-10's finding that Spearman across the whole eligible pool "
            "is nearly blind to reordering at the extreme -- the only region a shortlist "
            "decision uses. Recognition-heavy reweighting keeps 87.5% of the top-30 set; "
            "headroom-heavy keeps 57.9%; fit-heavy keeps 42.9% -- the published 45/35/20 "
            "weighting is closest to recognition-heavy and the least disruptive of the "
            "three re-weightings tested, which is a reason to prefer it over an "
            "equal-thirds default, not just an arbitrary pick.",
    },
    "qualifying_bar": {
        "value": scoring["qualifying_bar"],
        "n_qualifying": scoring["n_qualifying"],
        "sensitivity": scoring["bar_sensitivity_n_qualifying"],
    },
    "tiers_v2": {
        "rule": "Anchor: review_total>=20,000 OR (metacritic_score IS NOT NULL AND "
                "owners_mid>=350,000). Else Low-cost option: price_usd<=$5. Else Depth. "
                "Recalibrated from v1's absolute thresholds (which were tuned to a "
                "review_total>=50 population) to the v2 population's own distribution "
                "(qualifying-list median review_total ~16,200) -- reusing v1's 1,000/"
                "10,000-review Anchor floor here would have made Anchor 90%+ of the list "
                "again, reproducing RT-07's complaint under new numbers.",
        "counts": scoring["tier_counts"],
    },
    "monoculture_check_v2": scoring["monoculture_check_v2"],
    "monoculture_check_v2_verdict": (
        "RT-08 fixed on three axes. (1) By TITLE, not genre membership: genre shares are "
        "now reported as % of the 215 qualifying TITLES carrying each tag (Indie 64.2%, "
        "Adventure 57.7%, Action 50.7%, ...; these overlap because tagging is "
        "non-exclusive, and are reported as such, not summed to imply exhaustive "
        "coverage). No single genre is close to being the whole list. (2) Developer "
        "concentration: max is 3 qualifying titles from one developer (Square Enix, "
        "Telltale Games) -- nothing resembling v1's Randumb Studios (21 of 1,881). (3) "
        "Serial-chapter collapse: only 2 franchises contribute 2+ qualifying rows "
        "(Garfield Kart, The Walking Dead), and collapsing chapters to one licensable "
        "property per (developer, base-title) reduces 215 rows to 213 distinct "
        "properties -- negligible chapter-inflation, unlike v1's Higurashi (7 rows) or "
        "Randumb's The Test franchise. The 5,000-review floor structurally excludes most "
        "low-volume serialized short chapters, which is a side effect of RT-06's fix, not "
        "a separate intervention."
    ),
    "hard_limits_carried_forward": [
        "No engagement or playtime data exists in this dataset.",
        "owners_mid is a linear midpoint of a SteamSpy BUCKET (13 distinct values "
        "catalogue-wide, 6 within this eligible pool) -- not a measured sale count.",
        "review counts are self-selected; not adjusted for genre/price/audience-size "
        "beyond the age-since-release control in the fit model.",
        "has_controller_support (now a hard gate) is a category-flag FLOOR per "
        "02_cleaning_report.md's non-English-metadata hazard -- some true "
        "controller-supporting titles may be flagged false and wrongly excluded; this "
        "gate trades that small false-exclusion risk for a real, evidence-backed "
        "platform-fit signal.",
        "price_usd is USD via steamspy, never EUR -- reported column only, not scored.",
        "release_date is right-truncated (nothing after 2024-10-28) and 20.4% missing.",
        "Game Pass availability is NOT in this dataset and was NOT guessed. Every row in "
        "12_candidates_v2.csv carries screen_gamepass_availability=PENDING_EXTERNAL_CHECK.",
        "Steam-PC to Xbox-console population transfer (RT-11): stated explicitly here "
        "because the v1 model's winners were structurally the LEAST transferable segment "
        "(mouse/keyboard-only interactive fiction). The v2 has_controller_support gate "
        "directly addresses this for one dimension (control scheme) but does not address "
        "console certification history, regional pricing/discovery mechanics, or the "
        "genre-mix and ARPPU differences documented in artifacts/04_context.md s5.",
    ],
}

with open(f"{RUN_DIR}/artifacts/12_model_v2.json", "w") as f:
    json.dump(model, f, indent=2)

print("wrote artifacts/12_model_v2.json")
