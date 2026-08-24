-- Q13: Price band vs estimated audience (owners_mid). Observational only -- price, quality,
-- and marketing spend are confounded in this data; this cannot support a causal elasticity
-- claim, only a descriptive association.
WITH base AS (
    SELECT app_id, price_usd, owners_mid, review_total
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game'
      AND monetisation_model = 'paid' AND price_usd IS NOT NULL AND price_usd > 0
),
banded AS (
    SELECT *,
        CASE
            WHEN price_usd < 5 THEN '01_under_5'
            WHEN price_usd < 10 THEN '02_5_to_10'
            WHEN price_usd < 15 THEN '03_10_to_15'
            WHEN price_usd < 20 THEN '04_15_to_20'
            WHEN price_usd < 30 THEN '05_20_to_30'
            WHEN price_usd < 60 THEN '06_30_to_60'
            ELSE '07_60_plus'
        END AS price_band
    FROM base
)
SELECT price_band,
       count(*) AS n_titles,
       round(median(owners_mid), 0) AS median_owners_mid,
       round(avg(owners_mid), 0) AS mean_owners_mid,
       round(median(review_total), 1) AS median_review_total
FROM banded
GROUP BY price_band
HAVING count(*) >= 30
ORDER BY price_band;
