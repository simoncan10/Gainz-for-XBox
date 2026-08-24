-- Stage 16 (scoring v3) — the candidate eligibility screen, floor moved per Stage 15
-- red team (artifacts/15_redteam_portfolio.md, A-2).
--
-- Unchanged from v2 (sql/12v2_candidate_screen.sql):
--   monetisation_model='paid' AND price_usd>0
--   review_positive_ratio >= 0.70
--   no Sexual Content / Nudity / Hentai tag
--   owners_mid <= 750,000  -- KEPT. Still bucket-equivalent to <=1,499,999 (RT-09/A-3);
--                              see 16_scoring_v3.md for the honest restatement of what
--                              this ceiling actually does to the composite (A-3/B-5).
--   has_controller_support = true  -- verified sound at Stage 15 (A-0): the critic's own
--                              reported "926/13-title" yield failed to apply this gate,
--                              and 5 of its own 13 named titles (including Temtem, ICARUS)
--                              fail it. This run's 638/215 was confirmed correct.
--
-- CHANGED per Stage 15 red team (A-2, MINOR-but-actioned):
--   review_total >= 4,000  (was >=5,000). The critic re-derived the metacritic-presence
--   curve at finer granularity than v2 published and found the plateau genuinely begins
--   at 4,000 (47.3%), not 5,000 (48.0%) -- from 4,000 the curve is flat within 0.8pp out
--   to 7,000. Choosing 5,000 over 4,000 was costing 164 titles (-20% of the pool) to buy
--   +0.7pp of metacritic density, which the critic correctly called not a real
--   discrimination in the data. Moved to 4,000: it is where the plateau actually starts,
--   and the larger resulting pool (802 vs 638) is a strict improvement with no offsetting
--   cost -- "it is where the critic put it" is not the reason (the coordinator explicitly
--   ruled that out); "it is where the metacritic-presence curve's own elbow sits, and the
--   larger pool costs nothing in recognition density" is.
--
-- Verified: floor=4,000 gives n=802, 47.3% metacritic presence -- reproduces the critic's
-- number exactly (sql/17_threshold_sensitivity_v2.sql already contains the coarser table;
-- see artifacts/16_scoring_v3.md for the finer-grained 500-unit-step table run here).

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
  AND f.review_total >= 4000
  AND f.review_positive_ratio >= 0.70
  AND f.owners_mid <= 750000
  AND f.price_usd > 0
  AND f.has_controller_support = true
  AND a.app_id IS NULL
ORDER BY f.app_id;
