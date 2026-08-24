-- Q12: Price distribution by genre, paid titles only, priced from steamspy/games.csv
-- (price_usd is NULL for monetisation_model = 'paid_price_unknown' -- excluded here, not
-- imputed). n reported per genre; genres with n < 30 priced titles are excluded.
WITH base AS (
    SELECT g.app_id, g.price_usd
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet') g
    WHERE g.is_demo = false AND g.app_type = 'game'
      AND g.monetisation_model = 'paid' AND g.price_usd IS NOT NULL AND g.price_usd > 0
),
genre_titles AS (
    SELECT gl.genre, b.price_usd
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN base b USING (app_id)
)
SELECT genre,
       count(*) AS n_priced,
       round(median(price_usd), 2) AS median_price_usd,
       round(quantile_cont(price_usd, 0.25), 2) AS p25_price_usd,
       round(quantile_cont(price_usd, 0.75), 2) AS p75_price_usd,
       round(avg(price_usd), 2) AS mean_price_usd
FROM genre_titles
GROUP BY genre
HAVING count(*) >= 30
ORDER BY median_price_usd DESC;
