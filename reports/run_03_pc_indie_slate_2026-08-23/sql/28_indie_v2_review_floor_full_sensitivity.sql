-- Stage 23 rebuild (A-4): full, untruncated review-floor sensitivity on the
-- REBUILT indie population (is_indie=true AND developer_title_count<=10),
-- reporting every row from 500 to 10,000 rather than stopping at 5,000.
-- Criterion (unchanged from Stage 20): Metacritic-presence density as a proxy
-- for recognised-quality concentration at each floor.

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
    AND f.owners_mid <= 750000   -- ceiling held fixed while floor is swept, per Stage 20 method
)
SELECT
  floors.floor AS review_floor,
  COUNT(*) FILTER (WHERE indie_pool.review_total >= floors.floor) AS n,
  ROUND(100.0 * COUNT(*) FILTER (WHERE indie_pool.review_total >= floors.floor AND indie_pool.metacritic_score IS NOT NULL)
        / NULLIF(COUNT(*) FILTER (WHERE indie_pool.review_total >= floors.floor), 0), 1) AS pct_with_metacritic
FROM indie_pool, (SELECT UNNEST([500,1000,2000,3000,4000,5000,6000,7500,10000]) AS floor) AS floors
GROUP BY floors.floor
ORDER BY floors.floor;
