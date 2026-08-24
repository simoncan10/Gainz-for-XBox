-- Stage 23 thesis revision (B-5) — the yardstick calculation the original document
-- reported both inputs for and never divided. Two views of the same cheaper-but-
-- smaller-reach finding, recomputed on the rebuilt indie population:
--   (1) cost per owner reached (price / mean owners) -- reach-per-title framing.
--   (2) qualifying titles per $1,000 of retail price at a fixed quality bar
--       (review_total>=4000, review_positive_ratio>=0.80) -- catalogue-breadth
--       framing, matching how a subscription actually monetises (many titles
--       against a fixed monthly fee, not owners-per-title).

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
  COUNT(*) AS n_population,
  ROUND(AVG(price_usd), 2) AS mean_price_population,
  ROUND(AVG(owners_mid), 0) AS mean_owners_population,
  ROUND(AVG(price_usd) * 1.0e6 / AVG(owners_mid), 2) AS cost_usd_per_million_owners,
  COUNT(*) FILTER (WHERE review_total >= 4000 AND review_positive_ratio >= 0.80) AS n_qualifying_fixed_bar,
  ROUND(AVG(price_usd) FILTER (WHERE review_total >= 4000 AND review_positive_ratio >= 0.80), 2) AS mean_price_qualifying,
  ROUND(1000.0 * COUNT(*) FILTER (WHERE review_total >= 4000 AND review_positive_ratio >= 0.80)
        / NULLIF(SUM(price_usd) FILTER (WHERE review_total >= 4000 AND review_positive_ratio >= 0.80), 0), 2) AS titles_per_1000_usd_retail
FROM base
GROUP BY is_indie_strict
ORDER BY is_indie_strict;
