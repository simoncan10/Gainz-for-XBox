-- Stage 23 rebuild: re-check the owners_mid ceiling on the rebuilt indie
-- population (is_indie=true AND developer_title_count<=10) with the
-- re-derived review floor (>=5,000) held fixed.

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS n FROM read_parquet('parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
indie_pool AS (
  SELECT f.*
  FROM read_parquet('parquet/fact_games.parquet') f
  LEFT JOIN dev_counts dc ON dc.developer = f.developer
  WHERE f.is_demo = false
    AND f.app_type = 'game'
    AND f.monetisation_model = 'paid'
    AND f.price_usd > 0
    AND f.is_indie = true
    AND dc.n <= 10
    AND f.review_total >= 5000
    AND f.review_positive_ratio >= 0.70
)
SELECT
  ceilings.c AS owners_ceiling,
  COUNT(*) FILTER (WHERE indie_pool.owners_mid <= ceilings.c) AS n,
  ROUND(100.0 * COUNT(*) FILTER (WHERE indie_pool.owners_mid <= ceilings.c AND indie_pool.metacritic_score IS NOT NULL)
        / NULLIF(COUNT(*) FILTER (WHERE indie_pool.owners_mid <= ceilings.c), 0), 1) AS pct_with_metacritic
FROM indie_pool, (SELECT UNNEST([150000,350000,500000,750000,1000000,1500000,3500000]) AS c) AS ceilings
GROUP BY ceilings.c
ORDER BY ceilings.c;
