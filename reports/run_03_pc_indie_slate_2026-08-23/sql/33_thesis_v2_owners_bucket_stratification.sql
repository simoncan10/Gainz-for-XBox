-- Stage 23 thesis revision (B-1) — propensity comparison stratified by owners_mid
-- bucket, the denominator of the propensity metric itself. The critic's finding: the
-- unconditional propensity gap is driven almost entirely by the smallest bucket, and
-- converges to (and repeatedly crosses) parity at higher ownership. Recomputed here on
-- the rebuilt indie population (sql/31).

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
  WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
    AND f.price_usd > 0 AND f.review_total >= 10
),
per_bucket AS (
  SELECT owners_mid,
    is_indie_strict,
    COUNT(*) AS n,
    AVG(review_total * 1.0 / owners_mid) AS mean_propensity
  FROM base
  GROUP BY owners_mid, is_indie_strict
)
SELECT
  owners_mid,
  MAX(CASE WHEN is_indie_strict THEN n END) AS n_indie,
  MAX(CASE WHEN NOT is_indie_strict THEN n END) AS n_nonindie,
  ROUND(MAX(CASE WHEN is_indie_strict THEN mean_propensity END), 6) AS indie_propensity,
  ROUND(MAX(CASE WHEN NOT is_indie_strict THEN mean_propensity END), 6) AS nonindie_propensity,
  ROUND(100.0 * MAX(CASE WHEN is_indie_strict THEN mean_propensity END)
        / NULLIF(MAX(CASE WHEN NOT is_indie_strict THEN mean_propensity END), 0), 1) AS indie_pct_of_nonindie
FROM per_bucket
GROUP BY owners_mid
ORDER BY owners_mid;
