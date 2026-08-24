-- Q16: Publisher-level version of Q15's out-of-sample segment-expectation residual.
-- Same FIT/HOLDOUT split, same primary-genre x price-band segment model (see 15_ for the
-- full method note and the out-of-sample validation numbers: n=57,522 holdout rows,
-- Pearson r=0.114, Spearman-rank approx=0.297 between predicted segment expectation and
-- actual owners_mid -- a real but weak positive signal, not a strong predictive model).
-- Requires >=5 holdout titles per publisher (stricter than Q15's >=3 for developers, since
-- publisher rollups are the more decision-relevant cut for a licensing/backing decision).
WITH base AS (
    SELECT app_id, owners_mid, price_usd, monetisation_model, publisher,
           hash(app_id) % 2 AS split
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game' AND owners_mid IS NOT NULL
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
SELECT publisher,
       count(*) AS n_holdout_titles,
       round(median(owners_mid / NULLIF(expected_owners,0)), 2) AS median_residual_ratio,
       round(avg(owners_mid / NULLIF(expected_owners,0)), 2) AS mean_residual_ratio
FROM holdout_scored
WHERE publisher IS NOT NULL AND publisher != ''
GROUP BY publisher
HAVING count(*) >= 5
ORDER BY median_residual_ratio DESC
LIMIT 30;
