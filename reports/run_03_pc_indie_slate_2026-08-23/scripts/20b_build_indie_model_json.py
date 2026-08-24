import json
import duckdb

RUN_DIR = "/home/claude/run_portfolio"
s = json.load(open(f"{RUN_DIR}/artifacts/_scoring_summary_v20.json"))
con = duckdb.connect()

definition_check = con.execute(open(f"{RUN_DIR}/sql/20_indie_definition_check.sql").read()).df().to_dict("records")[0]
threshold_sens = con.execute(open(f"{RUN_DIR}/sql/20_indie_threshold_sensitivity.sql").read()).df().to_dict("records")

# controller-gate comparison numbers (computed inline, matching the diagnostics run
# during construction -- see sql/20_indie_candidate_screen.sql header for narrative)
q_base_noctrl = """
WITH adult_tagged AS (
    SELECT DISTINCT app_id FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content','Nudity','Hentai')
)
SELECT count(*) n FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
LEFT JOIN adult_tagged a USING(app_id)
WHERE f.is_demo=false AND f.app_type='game' AND f.monetisation_model='paid'
  AND f.review_total>=4000 AND f.review_positive_ratio>=0.70
  AND f.owners_mid<=750000 AND f.price_usd>0 AND a.app_id IS NULL
"""
pool_no_indie_no_ctrl = con.execute(q_base_noctrl).df()["n"].iloc[0]
pool_no_indie_with_ctrl = con.execute(q_base_noctrl + " AND f.has_controller_support=true").df()["n"].iloc[0]

model = {
    "stage": "20 - indie scoring (client-directed rescope: indie focus + drop Xbox console requirement)",
    "change_1_indie_definition": {
        "catalogue_wide_check_sql": "sql/20_indie_definition_check.sql",
        "n_nondemo_catalogue": 122191,
        "is_indie_flag_alone": {
            "n": definition_check["n_indie_flag"],
            "pct_of_catalogue": definition_check["pct_indie_flag"],
            "verdict": "Far too broad to be a segment (67.6% of the whole non-demo "
                       "catalogue) -- Steam's genre-level Indie tag is close to a "
                       "majority label, not a market segment.",
        },
        "is_indie_flag_null_nonenglish_floor": definition_check["n_indie_null_nonenglish_floor"],
        "chosen_definition": {
            "rule": "is_indie=true AND is_self_published=true",
            "n": definition_check["n_indie_and_selfpub"],
            "pct_of_catalogue": definition_check["pct_indie_and_selfpub"],
            "justification": "is_indie alone is a self-declared genre tag (necessary but "
                "insufficient -- too broad alone, and a FLOOR: 87 apps are NULL because "
                "their only category/genre rows are non-English, 02_cleaning_report.md). "
                "is_self_published (developer=publisher, from steamspy) is an objective, "
                "structural signal: no separate/larger publisher backing the title. "
                "Combined, this narrows the flag from 67.6% to 36.8% of the catalogue -- "
                "still broad in absolute terms (Steam's catalogue as a whole skews "
                "indie) but now a real, structurally-distinct segment. Chosen over an "
                "arbitrary 'publisher released <=N titles' cutoff because it needs no "
                "threshold to justify and directly targets what 'indie' is usually meant "
                "to distinguish.",
        },
        "alternative_tested_not_adopted": {
            "rule": "is_indie=true AND (is_self_published=true OR publisher has <=5 titles catalogue-wide)",
            "n_within_full_screen": 541,
            "vs_chosen_n_within_full_screen": 406,
            "note": "A broader, similarly-shaped alternative. Not adopted because "
                    "is_self_published is already a clean binary with no threshold to "
                    "pick, while '<=5 titles' is an arbitrary cutoff this run found no "
                    "principled way to set tighter or looser than 5.",
        },
    },
    "change_2_controller_gate": {
        "decision": "DROPPED as a hard gate.",
        "reasoning": "The gate was added at Stage 12/16 specifically as a Steam-PC-to-"
            "Xbox-CONSOLE platform-fit proxy (console certification / control-scheme "
            "risk). Game Pass on PC has no such requirement. Tested three notional "
            "treatments -- keep as hard gate / drop entirely / demote to a scored "
            "feature -- and found 'drop' and 'demote' are the SAME outcome in practice: "
            "the existing Fit model (artifacts/12_model_v2_fit.json, reused unchanged "
            "per Change 3) already includes has_controller_i as a Ridge feature "
            "(coefficient +0.0387, its single strongest positive coefficient), so "
            "dropping the hard SQL gate automatically demotes controller support to a "
            "10%-weighted scored input rather than eliminating its influence.",
        "pool_size_without_indie_filter": {
            "with_controller_gate": int(pool_no_indie_with_ctrl),
            "without_controller_gate": int(pool_no_indie_no_ctrl),
            "growth": int(pool_no_indie_no_ctrl - pool_no_indie_with_ctrl),
            "growth_pct": round((pool_no_indie_no_ctrl - pool_no_indie_with_ctrl) / pool_no_indie_with_ctrl * 100, 1),
        },
        "quality_check_on_newly_admitted": "Among the 165 titles admitted to the "
            "indie+self-published pool by dropping the gate, metacritic presence is "
            "25.5% vs 40.7% for the controller-supported subset of the same pool -- "
            "has_controller_i's positive Fit coefficient reflects a genuine, not "
            "spurious, signal, which is why it is kept as a 10%-weighted feature rather "
            "than dropped from the model too.",
        "previous_watchlist_note": "The coordinator named 7 titles (Wandering Sword, "
            "The Hungry Lamb, SANABI, Journey, Path Of Wuxia, Senren*Banka, Sanfu) "
            "excluded 'solely on port risk.' Checked directly: all 7 already carry "
            "has_controller_support=true and were already present in the v3 scoring "
            "qualifying list (artifacts/16_candidates_v3.csv) -- their exclusion "
            "happened in the downstream PORTFOLIO stage (unverified Xbox console SKU), "
            "not at this scoring gate. Dropping the console requirement does not change "
            "their SCORING-pool membership (they were never blocked here); it removes "
            "the reason the portfolio stage downgraded them, which is that stage's own "
            "artifact to revise, not this one's.",
    },
    "change_3_thresholds_carried_forward_and_retested": {
        "review_total_floor": {
            "value": 4000,
            "carried_forward": True,
            "retested_sql": "sql/20_indie_threshold_sensitivity.sql",
            "finding": "The clean metacritic-presence elbow that justified 4,000 in the "
                "general (Stage 16) population does NOT cleanly reproduce within the "
                "indie+self-published population -- the curve is flat-to-noisy across "
                "2,000-5,000 review floors (33.4% / 35.4% / 34.5% / 34.2% metacritic "
                "presence), likely because indie Metacritic coverage is bottlenecked by "
                "press attention rather than community size. No alternative floor in "
                "that range clearly dominates 4,000, so it was KEPT -- re-tested, not "
                "defaulted.",
        },
        "owners_mid_ceiling": {
            "value": 750000,
            "carried_forward": True,
            "finding": "Still excludes 173 of 579 indie titles (29.9%) that clear every "
                "other screen; relaxing it keeps buying metacritic density (34.5% -> "
                "37.0% at 1.5M -> 38.8% at 3.5M) at the direct cost of the 'not already "
                "widely owned' test. Same trade-off logic as the general-population "
                "derivation applies; KEPT. Still bucket-equivalent to <=1,499,999 (6 "
                "distinct owners_mid values remain).",
        },
        "sensitivity_table_raw": threshold_sens,
        "recognition_headroom_fit_weights": "0.50 / 0.40 / 0.10 -- unchanged from v3.",
        "fit_model": "Reused verbatim from v2/v3 (artifacts/12_model_v2_fit.json) -- no "
            "retraining. Change 3 explicitly carries this forward.",
    },
    "eligibility_screen": {
        "sql_file": "sql/20_indie_candidate_screen.sql",
        "eligible_pool_n": s["eligible_pool_n"],
        "eligible_pool_metacritic_pct": s["eligible_pool_metacritic_pct"],
    },
    "a3_headroom_still_disclosed": {
        "verified_on_this_pool": True,
        "evidence": s["a3_headroom_check"],
        "verdict": "CONFIRMED again on the smaller indie pool (n=406, 6 distinct "
            "owners_mid values): within-bucket Spearman(recognition, headroom) = 1.0000 "
            "in every bucket with n>=5 (75,000 / 150,000 / 350,000 / 750,000). The "
            "composite remains, honestly, Recognition (continuous, 0.50-weighted) "
            "banded by an ownership step -- not a genuine multi-pillar blend. Carried "
            "forward from Stage 16 per Change 3's instruction not to re-litigate what "
            "was already disclosed, only to re-verify it still holds.",
    },
    "pillar_influence_on_composite": s["pillar_influence_on_composite"],
    "qualifying_bar": {"value": s["qualifying_bar"], "n_qualifying": s["n_qualifying"],
                        "sensitivity": s["bar_sensitivity_n_qualifying"]},
    "n_qualifying_without_controller_support": s["n_qualifying_without_controller_support"],
    "tiers": s["tier_counts"],
    "tier_thresholds_recalibrated": {
        "reason": "v3's Anchor floor (review_total>=20,000) would leave only 23/406 "
            "(5.7%) of the indie pool eligible for Anchor -- the qualifying list's own "
            "median review_total here is ~13,000 vs v3's ~16,200, because the indie "
            "population runs at systematically lower review volume even among "
            "well-received titles. Recalibrated to review_total>=10,000 OR "
            "(metacritic present AND owners_mid>=350,000), and the Low-cost price "
            "ceiling raised from $5 to $10 to reflect indie's own lower price scale "
            "(median price in the eligible pool is $14.99, well below the general "
            "pool's).",
    },
    "monoculture_check": s["monoculture_check"],
    "hard_limits_carried_forward": [
        "No engagement or playtime data exists in this dataset.",
        "owners_mid is a SteamSpy BUCKET midpoint (6 distinct values in this pool).",
        "is_indie is a FLOOR (non-English-metadata undercount, 87 catalogue-wide NULLs).",
        "has_controller_support is no longer a hard requirement; it remains a category-"
        "flag FLOOR wherever it still feeds the Fit model.",
        "Game Pass availability is NOT in this dataset. Every row in "
        "20_indie_candidates.csv carries screen_gamepass_availability=PENDING_EXTERNAL_CHECK.",
    ],
}

with open(f"{RUN_DIR}/artifacts/20_indie_model.json", "w") as f:
    json.dump(model, f, indent=2, default=str)
print("wrote artifacts/20_indie_model.json")
