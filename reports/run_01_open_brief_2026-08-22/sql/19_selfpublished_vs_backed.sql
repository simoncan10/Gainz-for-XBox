-- Q19: Self-published (developer == publisher, the closest proxy this dataset has for
-- "unbacked / no distinct publisher" -- NOT a real first/third-party field, see DECISIONS.md)
-- vs distinctly-published titles: out-of-sample residual against the same segment expectation
-- model as Q15/Q16 (genre x price-band mean owners_mid, fit on one half, evaluated on the
-- other). Answers: controlling for genre and price band, do titles with a distinct publisher
-- behind them outperform self-published ones, on the audience-reach proxy available here?
WITH base AS (
    SELECT app_id, owners_mid, price_usd, monetisation_model, is_self_published,
           hash(app_id) % 2 AS split
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game' AND owners_mid IS NOT NULL
      AND is_self_published IS NOT NULL
),
banded AS (
    SELECT *, CASE
        WHEN monetisation_model = 'free' THEN 'free'
        WHEN price_usd IS NULL THEN 'unknown'
        WHEN price_usd < 5 THEN 'u5' WHEN price_usd < 10 THEN '5_10'
        WHEN price_usd < 15 THEN '10_15' WHEN price_usd < 20 THEN '15_20'
        WHEN price_usd < 30 THEN '20_30' WHEN price_usd < 60 THEN '30_60'
        ELSE '60p' END AS price_band
    FROM base
),
genre_counts AS (
    SELECT genre, count(*) AS n FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') GROUP BY 1
),
app_primary_genre AS (
    SELECT gl.app_id, gl.genre AS primary_genre
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN genre_counts gc USING (genre)
    QUALIFY row_number() OVER (PARTITION BY gl.app_id ORDER BY gc.n ASC) = 1
),
scored AS (
    SELECT b.*, apg.primary_genre
    FROM banded b JOIN app_primary_genre apg USING (app_id)
),
fit_model AS (
    SELECT primary_genre, price_band, avg(owners_mid) AS expected_owners, count(*) AS n_fit
    FROM scored WHERE split = 0
    GROUP BY 1, 2
    HAVING count(*) >= 30
),
holdout_scored AS (
    SELECT s.*, fm.expected_owners
    FROM scored s
    JOIN fit_model fm USING (primary_genre, price_band)
    WHERE s.split = 1
)
SELECT is_self_published,
       count(*) AS n_holdout_titles,
       round(median(owners_mid / NULLIF(expected_owners,0)), 3) AS median_residual_ratio,
       round(avg(owners_mid / NULLIF(expected_owners,0)), 3) AS mean_residual_ratio
FROM holdout_scored
GROUP BY is_self_published
ORDER BY is_self_published;
