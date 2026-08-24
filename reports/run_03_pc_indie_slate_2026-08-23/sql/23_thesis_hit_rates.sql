-- Stage 21 (indie thesis) — hit rate at successive owners_mid thresholds, indie vs
-- non-indie. Population per sql/21_thesis_population.sql.

WITH pop AS (
    SELECT *, (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS is_indie_strict
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
    WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10
)
SELECT
    is_indie_strict, count(*) AS n,
    round(100.0 * count(*) FILTER (WHERE owners_mid >= 100000) / count(*), 2) AS pct_ge_100k,
    round(100.0 * count(*) FILTER (WHERE owners_mid >= 500000) / count(*), 2) AS pct_ge_500k,
    round(100.0 * count(*) FILTER (WHERE owners_mid >= 1000000) / count(*), 2) AS pct_ge_1m,
    round(100.0 * count(*) FILTER (WHERE owners_mid >= 5000000) / count(*), 2) AS pct_ge_5m
FROM pop GROUP BY is_indie_strict;
