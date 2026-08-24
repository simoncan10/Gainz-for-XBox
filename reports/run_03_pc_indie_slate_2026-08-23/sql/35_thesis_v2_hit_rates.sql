-- Stage 23 thesis revision (B-3 continued, B-4 note) — hit rates at owner thresholds,
-- WITH and WITHOUT the review_total>=10 survivorship floor, recomputed on the rebuilt
-- indie population. Thresholds are named by the nearest owners_mid bucket boundary they
-- actually resolve to (B-4): >=100k resolves to >=150,000; >=500k resolves to >=750,000.

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
  COUNT(*) FILTER (WHERE review_total >= 10) AS n_with_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE review_total>=10 AND owners_mid>=150000) / COUNT(*) FILTER (WHERE review_total>=10), 2) AS pct_ge_150k_with_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE owners_mid>=150000) / COUNT(*), 2) AS pct_ge_150k_no_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE review_total>=10 AND owners_mid>=750000) / COUNT(*) FILTER (WHERE review_total>=10), 2) AS pct_ge_750k_with_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE owners_mid>=750000) / COUNT(*), 2) AS pct_ge_750k_no_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE review_total>=10 AND owners_mid>=1500000) / COUNT(*) FILTER (WHERE review_total>=10), 2) AS pct_ge_1_5m_with_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE owners_mid>=1500000) / COUNT(*), 2) AS pct_ge_1_5m_no_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE review_total>=10 AND owners_mid>=7500000) / COUNT(*) FILTER (WHERE review_total>=10), 2) AS pct_ge_7_5m_with_floor,
  ROUND(100.0 * COUNT(*) FILTER (WHERE owners_mid>=7500000) / COUNT(*), 2) AS pct_ge_7_5m_no_floor
FROM all_paid
GROUP BY is_indie_strict
ORDER BY is_indie_strict;
