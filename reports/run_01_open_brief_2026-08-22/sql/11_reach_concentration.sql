-- Q11: Long-tail shape of estimated reach (owners_mid) per genre.
-- NOTE: owners_mid is a reach/ownership proxy, not engagement or playtime -- this dataset has
-- zero playtime signal (see hard scope limit). This measures how concentrated ownership is,
-- not how retained or engaged owners are.
-- pct_bottom_bucket = share of titles stuck in SteamSpy's lowest resolution bucket (0..20k owners).
-- top decile share = share of the genre's total estimated audience captured by its top 10% of
-- titles by owners_mid, i.e. how hit-driven the genre is.
WITH base AS (
    SELECT g.app_id, g.owners_mid, g.owners_low
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet') g
    WHERE g.is_demo = false AND g.app_type = 'game'
),
genre_titles AS (
    SELECT gl.genre, b.app_id, b.owners_mid, b.owners_low
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN base b USING (app_id)
),
ranked AS (
    SELECT genre, app_id, owners_mid, owners_low,
           percent_rank() OVER (PARTITION BY genre ORDER BY owners_mid) AS pr
    FROM genre_titles
),
agg AS (
    SELECT genre,
           count(*) AS n_titles,
           sum(owners_mid) AS total_audience,
           sum(owners_mid) FILTER (WHERE pr >= 0.90) AS top_decile_audience,
           avg(CASE WHEN owners_low = 0 THEN 1.0 ELSE 0.0 END) AS pct_bottom_bucket
    FROM ranked
    GROUP BY genre
    HAVING count(*) >= 100
)
SELECT genre, n_titles,
       round(100.0 * pct_bottom_bucket, 1) AS pct_titles_in_bottom_bucket,
       round(100.0 * top_decile_audience / NULLIF(total_audience,0), 1) AS pct_audience_in_top_decile
FROM agg
ORDER BY pct_audience_in_top_decile DESC;
