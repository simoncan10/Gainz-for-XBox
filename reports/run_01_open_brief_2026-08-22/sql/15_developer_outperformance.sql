-- Q15: Do specific developers/publishers repeatedly outperform the expectation for their
-- segment and price band, out of sample?
--
-- Method (fit / holdout split to avoid circularity):
--   1. Split apps 50/50 by hash(app_id) into FIT and HOLDOUT.
--   2. Assign each app a single "primary genre" = its rarest (most specific) genre tag
--      globally, to avoid one title inflating a developer's count across multiple genre rows
--      (Indie/Action/Adventure are near-universal tags and would otherwise dominate).
--   3. On FIT only, compute mean owners_mid per (primary_genre, price_band) segment (n>=30
--      cells only) -- this is the "expectation for segment and budget class".
--   4. Apply FIT segment means to HOLDOUT rows the model never saw. Compute the row-level
--      out-of-sample correlation between predicted and actual as the validation number.
--   5. Aggregate holdout residual (actual / predicted) by developer, requiring >=3 holdout
--      titles, to find repeat outperformers. A developer with 1-2 holdout hits is excluded
--      by construction -- consistency, not a single hit, is the point.
-- Caveat: owners_mid is a coarse SteamSpy-bucket proxy (83% of catalogue in one bucket), so
-- this residual is a coarse "did-better-than-segment-peers" signal, not a precise multiplier.
WITH base AS (
    SELECT app_id, owners_mid, price_usd, monetisation_model, developer, publisher,
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
    SELECT s.*, fm.expected_owners, fm.n_fit
    FROM scored s
    JOIN fit_model fm USING (primary_genre, price_band)
    WHERE s.split = 1
),
ranked_holdout AS (
    SELECT *,
        rank() OVER (ORDER BY expected_owners) AS rank_expected,
        rank() OVER (ORDER BY owners_mid) AS rank_actual
    FROM holdout_scored
),
validation AS (
    SELECT
        count(*) AS n_holdout_rows,
        corr(expected_owners, owners_mid) AS pearson_r_expected_vs_actual,
        corr(rank_expected, rank_actual) AS spearman_approx
    FROM ranked_holdout
),
dev_residual AS (
    SELECT developer,
           count(*) AS n_holdout_titles,
           round(median(owners_mid / NULLIF(expected_owners,0)), 2) AS median_residual_ratio,
           round(avg(owners_mid / NULLIF(expected_owners,0)), 2) AS mean_residual_ratio
    FROM holdout_scored
    WHERE developer IS NOT NULL AND developer != ''
    GROUP BY developer
    HAVING count(*) >= 3
)
SELECT 'VALIDATION' AS row_type, NULL AS developer, n_holdout_rows AS n_holdout_titles,
       pearson_r_expected_vs_actual AS median_residual_ratio, spearman_approx AS mean_residual_ratio
FROM validation
UNION ALL
SELECT 'DEVELOPER' AS row_type, developer, n_holdout_titles, median_residual_ratio, mean_residual_ratio
FROM dev_residual
ORDER BY row_type DESC, median_residual_ratio DESC;
