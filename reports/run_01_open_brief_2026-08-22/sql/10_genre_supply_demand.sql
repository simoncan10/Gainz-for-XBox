-- Q10: Supply-side (titles released) vs demand-side (estimated audience reached) per genre.
-- Demand proxy = sum(owners_mid), a linear midpoint of SteamSpy's bucketed owner range
-- (see DECISIONS.md: 83.2% of the catalogue sits in the single bottom bucket 0..20,000, so
-- owners_mid has almost no resolution below ~20k owners and this ratio is only meaningful
-- for genres with a real population of hits above the bottom bucket).
-- Scope: real games only (is_demo = false, app_type = 'game'); genres with n >= 100 titles
-- to keep the segment stable. All-time window (release_date up to 2024-10-28, right-truncated).
WITH base AS (
    SELECT g.app_id, g.owners_mid, g.review_total, g.release_year
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet') g
    WHERE g.is_demo = false AND g.app_type = 'game'
),
genre_titles AS (
    SELECT gl.genre, b.app_id, b.owners_mid, b.review_total
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN base b USING (app_id)
)
SELECT
    genre,
    count(*) AS n_titles,
    sum(owners_mid) AS total_audience_est,
    round(avg(owners_mid), 0) AS mean_owners_mid,
    round(median(owners_mid), 0) AS median_owners_mid,
    round(median(review_total), 1) AS median_review_total,
    round(sum(owners_mid) / count(*), 0) AS audience_per_title
FROM genre_titles
GROUP BY genre
HAVING count(*) >= 100
ORDER BY total_audience_est DESC;
