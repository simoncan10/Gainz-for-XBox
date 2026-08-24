-- Stage 23 thesis revision — producer (developer) hit-consistency comparison,
-- recomputed on the rebuilt indie population. "Hit" = a title in the population with
-- owners_mid >= 500,000 (unchanged threshold from the original thesis document).

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
    AND f.price_usd > 0 AND f.review_total >= 10 AND f.developer IS NOT NULL AND f.developer <> ''
),
dev_hits AS (
  SELECT developer, is_indie_strict,
    COUNT(*) AS n_titles,
    COUNT(*) FILTER (WHERE owners_mid >= 500000) AS n_hits
  FROM base
  GROUP BY developer, is_indie_strict
)
SELECT
  is_indie_strict,
  COUNT(*) AS n_developers,
  COUNT(*) FILTER (WHERE n_hits >= 1) AS n_devs_with_1plus_hit,
  ROUND(100.0 * COUNT(*) FILTER (WHERE n_hits >= 1) / COUNT(*), 2) AS pct_devs_with_1plus_hit,
  COUNT(*) FILTER (WHERE n_hits >= 2) AS n_devs_with_2plus_hits,
  ROUND(100.0 * COUNT(*) FILTER (WHERE n_hits >= 2) / NULLIF(COUNT(*) FILTER (WHERE n_hits >= 1), 0), 2) AS pct_of_hitters_who_repeat,
  ROUND(AVG(n_titles) FILTER (WHERE n_hits >= 1), 2) AS mean_titles_among_hitters
FROM dev_hits
GROUP BY is_indie_strict
ORDER BY is_indie_strict;
