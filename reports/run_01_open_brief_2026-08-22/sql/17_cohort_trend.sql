-- Q17: Catalogue-wide trend by release cohort: supply (titles), demand-proxy (owners_mid),
-- and review volume normalized by time-since-release (to counter right-censoring: a 2023
-- title has had far less time to accumulate reviews/owners than a 2015 title).
-- 2024 excluded from headline trend (right-truncated at 2024-10-28, confirmed zero Nov/Dec
-- rows -- see profile); shown separately and flagged as partial-year.
-- Snapshot date used for "days since release" = 2024-12-15 (approximate profile snapshot date).
WITH base AS (
    SELECT app_id, release_year, release_date, owners_mid, review_total,
           datediff('day', release_date, DATE '2024-12-15') AS days_since_release
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game' AND release_date IS NOT NULL
)
SELECT release_year,
       count(*) AS n_titles,
       round(median(owners_mid), 0) AS median_owners_mid,
       round(avg(owners_mid), 0) AS mean_owners_mid,
       round(median(review_total), 1) AS median_review_total,
       round(median(review_total * 365.0 / NULLIF(days_since_release,0)), 3) AS median_reviews_per_year_since_release
FROM base
WHERE release_year BETWEEN 2015 AND 2024
GROUP BY release_year
ORDER BY release_year;
