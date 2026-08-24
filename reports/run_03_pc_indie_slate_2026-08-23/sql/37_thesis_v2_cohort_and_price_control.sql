-- Stage 23 thesis revision — cohort (release-year) and price-band stratified
-- comparison, recomputed on the rebuilt indie population. UNION ALL of two views.

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS developer_title_count
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
base AS (
  SELECT f.*, dc.developer_title_count,
    COALESCE(f.is_indie, false) AND COALESCE(dc.developer_title_count, 999999) <= 10 AS is_indie_strict,
    CASE WHEN f.release_year < 2018 THEN '<2018'
         WHEN f.release_year BETWEEN 2018 AND 2021 THEN '2018-2021'
         ELSE '2022+' END AS cohort,
    CASE WHEN f.price_usd <= 5 THEN '<=$5'
         WHEN f.price_usd <= 10 THEN '$5-10'
         WHEN f.price_usd <= 20 THEN '$10-20'
         ELSE '>$20' END AS price_band
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
  LEFT JOIN dev_counts dc ON dc.developer = f.developer
  WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
    AND f.price_usd > 0 AND f.review_total >= 10
)
SELECT 'cohort' AS dim, cohort AS bucket, is_indie_strict, COUNT(*) AS n,
  ROUND(AVG(owners_mid), 0) AS mean_owners,
  ROUND(AVG(review_positive_ratio), 4) AS mean_sentiment,
  ROUND(SUM(review_total) * 1.0 / SUM(owners_mid), 5) AS propensity_ratio_of_totals
FROM base GROUP BY cohort, is_indie_strict
UNION ALL
SELECT 'price_band' AS dim, price_band AS bucket, is_indie_strict, COUNT(*) AS n,
  ROUND(AVG(owners_mid), 0) AS mean_owners,
  ROUND(AVG(review_positive_ratio), 4) AS mean_sentiment,
  ROUND(SUM(review_total) * 1.0 / SUM(owners_mid), 5) AS propensity_ratio_of_totals
FROM base GROUP BY price_band, is_indie_strict
ORDER BY dim, bucket, is_indie_strict;
