-- Stage 12 (scoring v2) — the REBUILT candidate eligibility screen.
--
-- Carried unchanged from v1 (sql/12_candidate_screen.sql), still sourced the same way:
--   monetisation_model='paid' AND price_usd>0   -- not free; price data present (though
--                                                   price no longer drives the score, see
--                                                   scripts/12v2_score_candidates.py)
--   review_positive_ratio >= 0.70                -- Valve's own "Mostly Positive" boundary,
--                                                   confirmed exactly in this dataset
--                                                   (sql/09_review_bucket_check.sql)
--   no Sexual Content / Nudity / Hentai tag       -- platform-fit screen
--   owners_mid <= 750,000                         -- KEPT PER EXPLICIT INSTRUCTION. Note
--                                                   the red-team's own finding (RT-09):
--                                                   owners_mid has only 6 distinct values
--                                                   in the eligible pool, and there is NO
--                                                   value between 750,000 and 1,499,999 --
--                                                   so this ceiling is bucket-equivalent to
--                                                   a 1,499,999 ceiling, not a fine-grained
--                                                   750,000 cut. Stated honestly rather
--                                                   than implying false precision.
--
-- CHANGED per the rebuild spec (RT-06):
--   review_total >= 5,000  (was >=50). The v1 floor answered "is this rating
--   statistically meaningful?" (Valve's own bucket-nuance threshold) -- a different
--   question from "would a Game Pass subscriber recognise this title?", which is what
--   the brief actually asks the Proven/Recognition screen to establish. 5,000 is
--   justified and sensitivity-tested on its own terms in artifacts/12_scoring_v2.md /
--   12_model_v2.json (sql/17_threshold_sensitivity_v2.sql), not by borrowing Valve's
--   number for a different purpose.
--
-- ADDED per the rebuild spec (RT-11):
--   has_controller_support = true. The v2 fit model's own strongest surviving positive
--   coefficient after retargeting is has_controller_i (see 12_model_v2_fit.json) --
--   evidence-backed, not a taste screen. This is also the Steam-PC -> Xbox-console
--   platform-fit gate the brief requires be stated: a title with no controller support on
--   Steam carries meaningfully higher console-certification and control-scheme risk.
--   NOTE: applying this gate removes Temtem and ICARUS from eligibility (both
--   has_controller_support=false) -- see DECISIONS.md for why this run does NOT match
--   the coordinator-forwarded "reported yield" (pool=926), which was verified to have
--   been computed WITHOUT this gate despite the rebuild spec listing it as a hard gate.

WITH adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
)
SELECT
    f.app_id, f.name, f.developer, f.publisher,
    f.review_total, f.review_positive_ratio, f.review_score_bucket,
    f.owners_range, f.owners_mid,
    f.price_usd, f.monetisation_model,
    f.metacritic_score,
    f.is_indie, f.is_self_published,
    f.has_singleplayer, f.has_multiplayer, f.has_coop, f.has_controller_support, f.has_vr,
    f.n_tags, f.release_date, f.release_year,
    f.genres, f.tags
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
LEFT JOIN adult_tagged a USING (app_id)
WHERE f.is_demo = false
  AND f.app_type = 'game'
  AND f.monetisation_model = 'paid'
  AND f.review_total >= 5000
  AND f.review_positive_ratio >= 0.70
  AND f.owners_mid <= 750000
  AND f.price_usd > 0
  AND f.has_controller_support = true
  AND a.app_id IS NULL
ORDER BY f.app_id;
