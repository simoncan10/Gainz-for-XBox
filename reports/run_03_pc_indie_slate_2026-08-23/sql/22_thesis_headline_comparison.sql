-- Stage 21 (indie thesis) — headline indie-vs-non-indie comparison, unconditional
-- (no age/price control; see 24/25 for controlled versions). Population: same as
-- sql/21_thesis_population.sql (n=48,682). Group: chosen indie definition
-- (is_indie=true AND is_self_published=true) vs everyone else in the population.
--
-- review_propensity = review_total / owners_mid — reviews per estimated owner. A WEAK,
-- CONFOUNDED proxy for player involvement (see artifacts/21_indie_thesis.md for the full
-- caveat) — NOT a measurement of engagement, playtime, retention, or session frequency
-- (no such columns exist in this dataset; every playtime column is constant zero).

WITH pop AS (
    SELECT *,
        (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS is_indie_strict,
        review_total * 1.0 / owners_mid AS review_propensity
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
    WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10
)
SELECT
    is_indie_strict,
    count(*) AS n,
    round(avg(owners_mid), 0) AS mean_owners,
    approx_quantile(owners_mid, 0.5) AS med_owners,
    approx_quantile(owners_mid, 0.9) AS p90_owners,
    round(avg(review_positive_ratio), 4) AS mean_sentiment,
    approx_quantile(review_positive_ratio, 0.5) AS med_sentiment,
    round(avg(review_propensity), 5) AS mean_propensity,
    approx_quantile(review_propensity, 0.5) AS med_propensity,
    round(avg(price_usd), 2) AS mean_price,
    approx_quantile(price_usd, 0.5) AS med_price,
    round(avg(release_year), 1) AS mean_release_year,
    approx_quantile(release_year, 0.5) AS med_release_year
FROM pop
GROUP BY is_indie_strict;
