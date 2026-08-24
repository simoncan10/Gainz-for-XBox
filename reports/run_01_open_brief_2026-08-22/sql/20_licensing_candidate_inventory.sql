-- Q20: Size of the "proven hit" back-catalogue pool available to license, by genre and
-- vintage. Proven hit = owners_low >= 1,000,000 (SteamSpy bucket floor, i.e. titles in the
-- top 4 of 14 ownership buckets) AND review_positive_ratio >= 0.7 (n reviews >= 50 to avoid
-- a tiny-sample ratio). This is a measured-catalogue inventory count, not a licensability or
-- cost estimate -- Xbox does not control which of these are actually licensable and at what
-- price; it only bounds how many exist per segment.
WITH base AS (
    SELECT app_id, owners_low, review_positive_ratio, review_total, release_year
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game'
      AND owners_low >= 1000000 AND review_total >= 50 AND review_positive_ratio >= 0.7
),
vintage AS (
    SELECT *, CASE
        WHEN release_year IS NULL THEN 'unknown'
        WHEN release_year <= 2014 THEN 'pre_2015'
        WHEN release_year BETWEEN 2015 AND 2019 THEN '2015_2019'
        WHEN release_year BETWEEN 2020 AND 2022 THEN '2020_2022'
        ELSE '2023_plus' END AS vintage_bucket
    FROM base
),
genre_titles AS (
    SELECT gl.genre, v.vintage_bucket, v.app_id
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN vintage v USING (app_id)
)
SELECT genre, vintage_bucket, count(DISTINCT app_id) AS n_proven_hits
FROM genre_titles
GROUP BY genre, vintage_bucket
HAVING count(DISTINCT app_id) >= 30
ORDER BY genre, vintage_bucket;
