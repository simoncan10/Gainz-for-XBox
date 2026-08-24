-- Stage 23 thesis revision (B-3) — the review_total>=10 floor is itself a survivorship
-- filter; check whether it bites indie and non-indie titles evenly. Recomputed on the
-- rebuilt indie population.

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS developer_title_count
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
all_paid AS (
  SELECT f.*, dc.developer_title_count,
    COALESCE(f.is_indie, false) AND COALESCE(dc.developer_title_count, 999999) <= 10 AS is_indie_strict
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
  LEFT JOIN dev_counts dc ON dc.developer = f.developer
  WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
    AND f.price_usd > 0
)
SELECT
  is_indie_strict,
  COUNT(*) AS n_all_paid_priced,
  COUNT(*) FILTER (WHERE review_total >= 10) AS n_in_population,
  COUNT(*) FILTER (WHERE review_total < 10 OR review_total IS NULL) AS n_excluded,
  ROUND(100.0 * COUNT(*) FILTER (WHERE review_total < 10 OR review_total IS NULL) / COUNT(*), 1) AS pct_excluded
FROM all_paid
GROUP BY is_indie_strict
ORDER BY is_indie_strict;
