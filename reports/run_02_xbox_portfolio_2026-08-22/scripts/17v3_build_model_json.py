import json

RUN_DIR = "/home/claude/run_portfolio"
s = json.load(open(f"{RUN_DIR}/artifacts/_scoring_summary_v3.json"))

model = {
    "stage": "16 - scoring v3 (after Stage 15 red team of v2 rebuild + portfolio, "
              "artifacts/15_redteam_portfolio.md, Part A)",
    "scope_note": "Per the coordinator's explicit instruction, ONLY the two Part-A "
                  "scoring findings (A-4 reweight, A-3 disclosure) plus two cheap fixes "
                  "(A-2 floor, Deep Rock Galactic: Survivor data-quality check) are "
                  "addressed here. Part B (the downstream portfolio/tiering document, "
                  "T1-T4) is NOT reopened this round.",
    "credit_where_due": "The Stage 15 critic verified the analyst's Stage-12 controller-"
                  "gate catch was correct and its own Stage-11 reported yield (926) was "
                  "wrong (A-0); confirmed the v2 determinism fix across 5 consecutive "
                  "full-pipeline re-runs, byte-identical output, md5 104ad4df... (A-1); "
                  "and confirmed the 5,000-review elbow finding reproduces exactly, while "
                  "sharpening it to show the true plateau starts at 4,000 (A-2).",

    "a2_floor_moved_to_4000": {
        "finding": "Critic re-derived the metacritic-presence curve at 500-unit "
                   "granularity and found the plateau begins at review_total>=4,000 "
                   "(47.3%), not 5,000 (48.0%) -- flat within 0.8pp from 4,000 out to "
                   "7,000. Choosing 5,000 over 4,000 cost 164 titles (-20% of the pool) "
                   "for +0.7pp of metacritic density.",
        "verified_independently": "sql/19_threshold_sensitivity_v3_fine.sql reproduces "
                   "the critic's finer table exactly: floor=4000 -> n=802, 47.3%; "
                   "floor=5000 -> n=638, 48.0%.",
        "decision": "Moved the floor to 4,000. This is a strict improvement (larger pool, "
                   "negligible recognition-density cost) with no offsetting reason found "
                   "to prefer 5,000 -- per the coordinator's explicit instruction, "
                   "'it is where the critic put it' is not a justification, and none "
                   "better was found for keeping 5,000.",
        "new_eligible_pool_n": s["eligible_pool_n"],
        "new_eligible_pool_metacritic_pct": s["eligible_pool_metacritic_pct"],
    },

    "a4_fit_reweighted": {
        "finding": "Fit's in-population R^2 (scoped to the eligible pool, per "
                   "12_model_v2_fit.json) is -1.34 -- the model predicts WORSE than "
                   "simply using the population mean. A pillar performing below a "
                   "constant-prediction baseline cannot be permitted to carry 20% of "
                   "the ranking.",
        "new_weights": s["weights"],
        "what_moved": s["a4_reweight_effect_pool_held_at_v2_638"],
        "interpretation": "Isolating the reweight's own effect (pool held fixed at v2's "
                   "638 titles, only the weights changed from 0.45/0.35/0.20 to "
                   "0.50/0.40/0.10): 33 of 638 titles' qualifying status changed "
                   "(13.9% of the affected union), and 3 of the top 30 changed. This is "
                   "a smaller swing than the critic's own 'drop Fit entirely' test (21/"
                   "215 memberships, 10/30 top-30) because cutting a weight from 20% to "
                   "10% is a materially smaller intervention than removing it outright -- "
                   "both are reported so the two are not conflated.",
        "pillar_influence_on_final_v3_composite": s["composite_diagnostics_on_v3_pool"]["pillar_influence_on_composite_spearman"],
    },

    "a3_headroom_is_not_independent_HONEST_STATEMENT": {
        "verified": True,
        "evidence": s["a3_headroom_within_bucket_verification"],
        "plain_statement": (
            "Headroom is not a second independent pillar. owners_mid has only 5-6 "
            "distinct values in the eligible pool, and 3 buckets hold 99%+ of all "
            "titles. WITHIN every bucket that matters, Spearman(recognition_raw, "
            "headroom_raw) = 1.0000 exactly -- Headroom is Recognition minus a constant "
            "for every title sharing an ownership bucket. The pooled +0.54 (v2 pool) / "
            "+0.49 (v3 pool) correlation the earlier write-up cited as evidence of "
            "'complementary, not redundant' pillars is entirely BETWEEN-bucket "
            "variation, a Simpson's-paradox-shaped artifact of aggregating across a "
            "coarse step function. The honest framing: this composite is Recognition "
            "(a continuous, 0.50-weighted term), banded by a THREE-LEVEL ownership "
            "step (not a fourth, continuous, independently-informative pillar). Within "
            "any given ownership tier, the ranking is Recognition, full stop. This "
            "cannot be fixed by re-deriving Headroom differently from the same "
            "owners_mid column -- the coarseness is in the underlying SteamSpy bucket "
            "data (documented since 01_profile.md), not in the formula. It can only be "
            "disclosed, which this document and 12_scoring_v2.md now do."
        ),
        "consequence_for_the_qualifying_list": "The model still correctly surfaces "
            "recognisable titles at the top (that part of the v2 rebuild is not "
            "undermined) -- but the ranking WITHIN each ownership tier should be read "
            "as 'most-reviewed first,' not as a genuine two-factor blend.",
    },

    "b5_ceiling_echo_known_property_not_relitigated": s["b5_ceiling_echo"],

    "eligibility_screen_v3": {
        "sql_file": "sql/18_candidate_screen_v3.sql",
        "unchanged_from_v2": ["monetisation_model='paid' AND price_usd>0",
                               "review_positive_ratio>=0.70", "no adult-content tag",
                               "owners_mid<=750000 (still bucket-equivalent to <=1,499,999)",
                               "has_controller_support=true (A-0: verified sound, "
                               "corrects the critic's own erroneous ungated 926/13 yield)"],
        "changed": "review_total floor 5,000 -> 4,000 (A-2)",
        "eligible_pool_n": s["eligible_pool_n"],
        "eligible_pool_metacritic_pct": s["eligible_pool_metacritic_pct"],
    },

    "qualifying_bar": {"value": s["qualifying_bar"], "n_qualifying": s["n_qualifying"],
                        "sensitivity": s["bar_sensitivity_n_qualifying"]},
    "tiers": s["tier_counts"],
    "monoculture_check": s["monoculture_check"],
    "deep_rock_galactic_survivor_data_quality_check": s["deep_rock_galactic_survivor_data_quality_check"],

    "not_reopened_this_round_per_explicit_instruction": [
        "B-1 (traceability claim overstatement)", "B-2 (Tier 1 lead ordering)",
        "B-3 (Tier 3 under-sold, Tier 4 relabelling to watchlist)",
        "B-4 (concentration remedy correctness, Deep Rock Galactic: Survivor removal "
        "from the portfolio's alternate list, availability-screen extension to rank 120)",
        "B-6 (sizing/cost-anchor framing)",
        "These live in artifacts/15_redteam_portfolio.md Part B and belong to the "
        "downstream portfolio-construction stage, not this scoring stage.",
    ],
    "hard_limits_carried_forward": [
        "No engagement or playtime data exists in this dataset.",
        "owners_mid is a SteamSpy BUCKET midpoint with only 5-6 distinct values in this "
        "pool -- this is now understood to be the direct cause of A-3 (Headroom is not "
        "independent of Recognition within a bucket), not just a resolution-limit caveat.",
        "review counts are self-selected.",
        "has_controller_support is a category-flag FLOOR (non-English-metadata hazard) -- "
        "used as a hard gate anyway per A-0/RT-11, evidence-backed.",
        "price_usd is USD via steamspy, reported only, never scored.",
        "release_date is right-truncated (nothing after 2024-10-28) and 20.4% missing.",
        "Game Pass availability is NOT in this dataset. Every row in "
        "16_candidates_v3.csv carries screen_gamepass_availability=PENDING_EXTERNAL_CHECK.",
    ],
}

with open(f"{RUN_DIR}/artifacts/16_model_v3.json", "w") as f:
    json.dump(model, f, indent=2)
print("wrote artifacts/16_model_v3.json")
