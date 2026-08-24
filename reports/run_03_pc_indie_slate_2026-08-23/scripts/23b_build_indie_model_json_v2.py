import json
import duckdb

RUN_DIR = "/home/claude/run_portfolio"
s = json.load(open(f"{RUN_DIR}/artifacts/_scoring_summary_v23.json"))
con = duckdb.connect()

def_sens = con.execute(open(f"{RUN_DIR}/sql/27_indie_definition_v2_sensitivity.sql").read()).df().to_dict("records")
floor_sens = con.execute(open(f"{RUN_DIR}/sql/28_indie_v2_review_floor_full_sensitivity.sql").read()).df().to_dict("records")
ceiling_sens = con.execute(open(f"{RUN_DIR}/sql/29_indie_v2_owners_ceiling_sensitivity.sql").read()).df().to_dict("records")

model = {
    "stage": "23 - indie scoring REBUILD after red-team pass 22 (artifacts/22_redteam_indie.md)",
    "supersedes": "artifacts/20_indie_scoring.md, 20_indie_candidates.csv, 20_indie_model.json "
                  "(kept unmodified for the record -- this is a new version, not an edit)",
    "change_a1_indie_definition_rebuilt": {
        "problem_found_by_critic": "is_self_published (developer==publisher, a literal string "
            "match) misclassified indie titles at BOTH ends: excluded Return of the Obra Dinn "
            "and Papers, Please because Lucas Pope publishes as the label '3909' (a different "
            "string from his developer name), and excluded every indie that signed with an "
            "indie-friendly PUBLISHER -- What Remains of Edith Finch and Journey (Annapurna "
            "Interactive), Unpacking and Temtem (Humble Games), SANABI (NEOWIZ), ABZU (505 "
            "Games) -- while ADMITTING self-published mass-catalogue operations: "
            "EroticGamesClub (181 titles), Choice of Games (163), Boogygames Studios (130), "
            "Hosted Games (109), Sokpop Collective (96).",
        "first_attempt_tried_and_rejected": {
            "rule": "is_indie=true AND publisher_title_count<=N",
            "sql_file": "sql/27_indie_definition_v2_sensitivity.sql (publisher version, superseded)",
            "finding": "Passes the hand-check for any N roughly in [32,105) but barely narrows "
                "the raw is_indie population (48% of the catalogue at the smallest passing N) "
                "-- publisher catalogue size does not separate a boutique label (Annapurna, 32 "
                "titles) from a mainstream mid-size one (Nacon, 94 titles, only 4 indie-tagged) "
                "the way developer size does, because the SAME entity being developer and "
                "publisher is what makes the mass-catalogue 'admits' cases mass-catalogue -- "
                "the publisher axis catches that by coincidence, not by design.",
        },
        "adopted_definition": {
            "rule": "is_indie=true AND developer_title_count<=10",
            "sensitivity_table_sql": "sql/27_indie_definition_v2_sensitivity.sql "
                "(developer version, current file)",
            "sensitivity_table_raw": def_sens,
            "hand_check_result": "PASSES at N=10: Return of the Obra Dinn (developer Lucas "
                "Pope, 2 titles), Papers Please (Lucas Pope, 2), What Remains of Edith Finch "
                "(Giant Sparrow, 2), ENDER LILIES (Live Wire/Adglobe, 1), Unpacking (Witch "
                "Beam, 2), ABZU (Giant Squid, 2), Journey (thatgamecompany, 2), SANABI (WONDER "
                "POTION, 1), Temtem (Crema, 2), VA-11 Hall-A (Sukeban Games, 2), Potion Craft "
                "(niceplay games, 1), Firework (Shiying Studio, 2) all classify IN. Choice of "
                "Games (163), EroticGamesClub (181), Boogygames Studios (130), Hosted Games "
                "(109), Sokpop Collective (96) all classify OUT.",
            "extended_spot_check_beyond_the_required_hand_list": "Supergiant Games (5 titles: "
                "Bastion/Transistor/Pyre/Hades/Hades II), Vlambeer (5), Mode 7 (3) all remain "
                "IN at N=10 -- multi-title but genuinely small studios are not penalised. Klei "
                "Entertainment (12 titles) is excluded at N=10, an acceptable edge case (Klei "
                "has arguably outgrown indie scale by title count, and no hand-check item "
                "requires including it).",
            "why_n10_and_not_smaller": "N=2 (the smallest cutoff that still passes the "
                "required hand-check) would also exclude Supergiant Games and Vlambeer (5 "
                "titles each) and Mode 7 (3) -- well-known, genuinely small indie studios "
                "whose only 'fault' is having shipped more than two games. N=10 is the "
                "smallest of the critic's own suggested test points {3,5,10,25} clear of that "
                "problem.",
            "honestly_disclosed_limitation": "This narrows the raw is_indie=true population "
                "from 67.6% of the non-demo catalogue to only 44.8% (54,692/122,191) -- LESS "
                "narrowing than the flawed is_self_published rule achieved (36.8%). Developer-"
                "catalogue-size fixes WHO is correctly classified as indie; it does not, by "
                "itself, make 'indie' a small segment, because most Steam titles carrying the "
                "Indie genre tag genuinely are made by tiny (1-2 title) developers -- a "
                "structural fact about this catalogue, not a modelling failure. The real "
                "narrowing to an actionable candidate segment happens downstream in the same "
                "screen (review/quality/owner/price thresholds), exactly as it did before -- "
                "see eligibility_screen below (573 titles, 0.47% of the non-demo catalogue).",
        },
    },
    "change_a2_fit_compensation_claim_dropped": {
        "old_claim_conceded_wrong": "Stage 20 argued dropping the controller-support hard "
            "gate was equivalent to 'demoting' it because the Fit model already scores "
            "has_controller_i. Technically true (coefficient +0.0387, the model's strongest "
            "positive) but practically empty: Fit is weighted 10%, has in-population "
            "R2=-1.34, and titles at the bottom 1-4% of Fit rank appear freely in the "
            "qualifying top 20 (KovaaK's fit_pct=0.0395, Verdun fit_pct=0.0099 in the v20 "
            "run). A pillar that leaves bottom-percentile-on-Fit titles inside the top ranks "
            "is not compensating for anything.",
        "corrected_reasoning": "The controller-support gate is dropped for the narrower, "
            "correct reason only: Game Pass runs on Windows PC, so a console-fit proxy no "
            "longer applies to a keyboard/mouse-only title. NOTHING replaces the gate's "
            "quality-signal role. The measured cost stands on its own, reported per tier "
            "(not just pool-wide) as the critic asked: see "
            "n_qualifying_without_controller_support_by_tier below.",
    },
    "change_a4_review_floor_full_resensitivity": {
        "problem_found_by_critic": "Stage 20 ran a 9-row sensitivity table and quoted only "
            "the first 4 rows (500-5,000), stopping exactly before the curve's monotone rise "
            "at 6,000+ became visible, and kept the inherited 4,000 floor as a result.",
        "full_table_on_rebuilt_population_sql": "sql/28_indie_v2_review_floor_full_sensitivity.sql",
        "full_table_raw": floor_sens,
        "marginal_metacritic_density_gain_per_step_pct_points": {
            "500_to_1000": 5.0, "1000_to_2000": 4.2, "2000_to_3000": 2.0,
            "3000_to_4000": 1.5, "4000_to_5000": 1.0, "5000_to_6000": 0.1,
            "6000_to_7500": 0.2, "7500_to_10000": 0.4,
        },
        "decision": "RAISED the floor from 4,000 to 5,000. The plateau begins cleanly at "
            "5,000: the step immediately before it (4,000->5,000) still buys +1.0 "
            "percentage point of metacritic density; the step immediately after "
            "(5,000->6,000) buys +0.1pp, a 10x drop in marginal return. Did not move to "
            "6,000+ as the critic's note on the OLD (is_self_published) population implied, "
            "because that note was read off a different, messier, now-superseded curve -- on "
            "the corrected population the plateau genuinely starts at 5,000, and the "
            "remaining 6,000-10,000 gains (+0.1 to +0.4pp total, cumulative +0.7pp) do not "
            "justify losing another 138 titles (669->531) to reach them.",
        "owners_ceiling_recheck_sql": "sql/29_indie_v2_owners_ceiling_sensitivity.sql",
        "owners_ceiling_recheck_raw": ceiling_sens,
        "owners_ceiling_decision": "KEPT at 750,000 -- bucket-equivalent to 1,000,000 (n "
            "identical at 636 in the pre-adult-tag-exclusion check), and relaxing further "
            "keeps buying metacritic density (40.4% -> 42.3% -> 44.3% at 1.5M/3.5M) at the "
            "direct cost of the ceiling's purpose (excluding titles that are already widely "
            "owned).",
    },
    "change_a5_composite_degeneracy_disclosed": {
        "finding": s["a5_composite_degeneracy_check"],
        "cross_artifact_contradiction_the_critic_found": "artifacts/21_indie_thesis.md warns "
            "that reviews-per-owner (review_total/owners_mid) is a confounded, weak proxy "
            "not to be read as engagement. This scoring model's composite is, within a "
            "6-value owners_mid bucket structure, overwhelmingly a re-expression of "
            "log(review_total) (pooled R2 against composite = 0.775; within-bucket Spearman "
            "between Recognition and Headroom = 1.0000 in every bucket with n>=5). Both "
            "statements are individually defensible and they are in genuine tension: this "
            "scoring model leans on the volume side of exactly the metric the thesis document "
            "says is confounded. RESOLUTION: this document now states plainly that the "
            "composite is a review-VOLUME ranking banded by a near-constant ownership step, "
            "not a broad multi-signal quality blend, and the thesis document's propensity "
            "section is revised (23_indie_thesis.md v2) to stop treating reach and propensity "
            "as two independent lines of evidence -- they are the same measurement counted "
            "twice within an owners bucket. Neither document is 'wrong' in isolation; the "
            "same caveat now travels with both.",
    },
    "unchanged_per_standing_instruction": {
        "recognition_headroom_fit_weights": "0.50 / 0.40 / 0.10 -- not challenged by this "
            "red-team pass; carried forward.",
        "fit_model": "Reused verbatim from v2/v3 (artifacts/12_model_v2_fit.json) -- no "
            "retraining.",
        "qualifying_bar": 0.60,
        "tier_thresholds": "review_total>=10,000 OR (metacritic present AND "
            "owners_mid>=350,000) for Anchor; price<=$10 for Low-cost option -- checked "
            "against the larger rebuilt pool (573 vs 406 eligible) and still produces a "
            "sane split (178/12/11), so kept unchanged rather than re-tuned for its own sake.",
    },
    "eligibility_screen": {
        "sql_file": "sql/30_indie_v2_candidate_screen.sql",
        "eligible_pool_n": s["eligible_pool_n"],
        "eligible_pool_metacritic_pct": s["eligible_pool_metacritic_pct"],
        "vs_v20": {"eligible_pool_n": 406, "eligible_pool_metacritic_pct": 34.5},
    },
    "a3_headroom_still_disclosed": {
        "verified_on_rebuilt_pool": True,
        "evidence": s["a3_headroom_check"],
        "verdict": "CONFIRMED again (n=573, 6 distinct owners_mid values): within-bucket "
            "Spearman(recognition, headroom)=1.0000 in every bucket with n>=5 (150,000 / "
            "350,000 / 750,000). The composite remains, honestly, Recognition (continuous, "
            "0.50-weighted) banded by an ownership step -- not a genuine multi-pillar blend. "
            "See change_a5 above for the sharper version of this same finding.",
    },
    "pillar_influence_on_composite": s["pillar_influence_on_composite"],
    "qualifying_bar": {"value": s["qualifying_bar"], "n_qualifying": s["n_qualifying"],
                        "sensitivity": s["bar_sensitivity_n_qualifying"]},
    "n_qualifying_without_controller_support_total": s["n_qualifying_without_controller_support_total"],
    "n_qualifying_without_controller_support_by_tier": s["n_qualifying_without_controller_support_by_tier"],
    "tiers": s["tier_counts"],
    "monoculture_check": s["monoculture_check"],
    "hard_limits_carried_forward": [
        "No engagement or playtime data exists in this dataset.",
        "owners_mid is a SteamSpy BUCKET midpoint (6 distinct values in this pool).",
        "is_indie is a FLOOR (non-English-metadata undercount, 87 catalogue-wide NULLs).",
        "has_controller_support is no longer a hard requirement; it remains a category-flag "
        "FLOOR wherever it still feeds the Fit model, and Fit does not meaningfully "
        "compensate for dropping the gate (see change_a2).",
        "Game Pass availability is NOT in this dataset. Every row in "
        "23_indie_candidates_v2.csv carries screen_gamepass_availability=PENDING_EXTERNAL_CHECK.",
        "The composite is a review-volume ranking banded by a near-constant ownership step, "
        "not an independent multi-pillar blend -- see change_a5.",
    ],
}

with open(f"{RUN_DIR}/artifacts/23_indie_model_v2.json", "w") as f:
    json.dump(model, f, indent=2, default=str)
print("wrote artifacts/23_indie_model_v2.json")
