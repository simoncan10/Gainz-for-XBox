-- Stage 21 (indie thesis) — confounder-controlled comparison: stratify by release-year
-- cohort and by price band, indie vs non-indie within each stratum. Population per
-- sql/21_thesis_population.sql. Tests whether the age gap (indie titles are on average
-- ~1 year newer at the median, per sql/22) or the price gap (indie titles are cheaper by
-- construction of the comparison) explains away the reach/propensity differences.

-- (1) release-year cohort control
WITH pop AS (
    SELECT *,
        (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS is_indie_strict,
        CASE WHEN release_year <= 2018 THEN '<=2018'
             WHEN release_year BETWEEN 2019 AND 2021 THEN '2019-2021'
             WHEN release_year >= 2022 THEN '2022-2024'
             ELSE 'unknown' END AS cohort
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
    WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10
      AND release_year IS NOT NULL
)
SELECT 'cohort' AS control, cohort AS stratum, is_indie_strict, count(*) AS n,
    round(avg(owners_mid), 0) AS mean_owners,
    round(100.0 * count(*) FILTER (WHERE owners_mid >= 100000) / count(*), 2) AS pct_ge_100k,
    round(avg(review_positive_ratio), 4) AS mean_sentiment,
    round(avg(review_total * 1.0 / owners_mid), 5) AS mean_propensity,
    round(avg(price_usd), 2) AS mean_price
FROM pop GROUP BY cohort, is_indie_strict
UNION ALL
-- (2) price-band control
SELECT 'price_band' AS control, price_band AS stratum, is_indie_strict, n,
    mean_owners, pct_ge_100k, mean_sentiment, mean_propensity, NULL AS mean_price
FROM (
    SELECT
        CASE WHEN price_usd <= 5 THEN '<=$5' WHEN price_usd <= 10 THEN '$5-10'
             WHEN price_usd <= 20 THEN '$10-20' ELSE '>$20' END AS price_band,
        (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS is_indie_strict,
        count(*) AS n,
        round(avg(owners_mid), 0) AS mean_owners,
        round(100.0 * count(*) FILTER (WHERE owners_mid >= 100000) / count(*), 2) AS pct_ge_100k,
        round(avg(review_positive_ratio), 4) AS mean_sentiment,
        round(avg(review_total * 1.0 / owners_mid), 5) AS mean_propensity
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
    WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10
    GROUP BY price_band, is_indie_strict
)
ORDER BY control, stratum, is_indie_strict;
