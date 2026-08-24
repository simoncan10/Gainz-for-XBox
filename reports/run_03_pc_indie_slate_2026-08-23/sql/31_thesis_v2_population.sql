-- Stage 23 thesis revision — population redefined to match the rebuilt Stage 23 indie
-- definition (is_indie=true AND developer_title_count<=10, sql/30) rather than the
-- superseded is_self_published test, for consistency between the scoring document and
-- this thesis document (per A-5's cross-artifact resolution in 23_indie_v2.md).
-- Same population scope otherwise: paid, non-demo, priced>0, review_total>=10 (a light
-- floor to exclude titles with too few reviews to compute a stable sentiment ratio).
-- NULL developer (no developer_title_count computable) folds to the non-indie group via
-- COALESCE, same pattern used in the original 21_thesis_population.sql fix.

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS developer_title_count
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
base AS (
  SELECT f.*, dc.developer_title_count,
    COALESCE(f.is_indie, false) AND COALESCE(dc.developer_title_count, 999999) <= 10 AS is_indie_strict
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
  LEFT JOIN dev_counts dc ON dc.developer = f.developer
  WHERE f.is_demo = false
    AND f.app_type = 'game'
    AND f.monetisation_model = 'paid'
    AND f.price_usd > 0
    AND f.review_total >= 10
)
SELECT
  is_indie_strict,
  COUNT(*) AS n
FROM base
GROUP BY is_indie_strict;
