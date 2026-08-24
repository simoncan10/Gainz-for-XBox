-- Stage 23 thesis revision — headline comparison, recomputed on the population defined
-- in sql/31_thesis_v2_population.sql (rebuilt indie definition).

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
)
SELECT
  is_indie_strict,
  COUNT(*) AS n,
  ROUND(AVG(owners_mid), 0) AS mean_owners,
  ROUND(MEDIAN(owners_mid), 0) AS med_owners,
  ROUND(QUANTILE_CONT(owners_mid, 0.90), 0) AS p90_owners,
  ROUND(AVG(review_positive_ratio), 4) AS mean_sentiment,
  ROUND(MEDIAN(review_positive_ratio), 6) AS med_sentiment,
  ROUND(AVG(review_total * 1.0 / owners_mid), 5) AS mean_propensity_ratio_of_ratios,
  ROUND(SUM(review_total) * 1.0 / SUM(owners_mid), 5) AS propensity_ratio_of_totals,
  ROUND(MEDIAN(review_total * 1.0 / owners_mid), 6) AS med_propensity,
  ROUND(AVG(price_usd), 2) AS mean_price,
  ROUND(MEDIAN(price_usd), 6) AS med_price,
  ROUND(AVG(release_year), 1) AS mean_release_year,
  MEDIAN(release_year) AS med_release_year
FROM base
GROUP BY is_indie_strict
ORDER BY is_indie_strict;
