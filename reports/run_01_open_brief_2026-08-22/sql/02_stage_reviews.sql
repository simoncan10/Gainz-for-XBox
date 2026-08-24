-- 02_stage_reviews.sql
-- Type reviews.csv properly. Every numeric-looking column is VARCHAR in the
-- raw file because '\N' sentinels defeat DuckDB's type inference; each is
-- cleaned with NULLIF + TRY_CAST here.
--
-- Judgement calls (see DECISIONS.md):
--  * steamspy_score_rank dropped entirely -- 99.96% null (51/140082 rows),
--    profiled as "effectively a dead column".
--  * review_score_description folds the low-volume buckets ('1 user
--    reviews' .. '9 user reviews') into a single 'Not enough user reviews'
--    label so they don't fragment any aggregation; the raw text is kept
--    alongside for anyone who needs the exact count.

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE TABLE reviews_stage AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/reviews.csv',
        header = true,
        sample_size = -1
    )
)
SELECT
    app_id,
    TRY_CAST(NULLIF(review_score, '\N') AS TINYINT)               AS review_score,
    NULLIF(review_score_description, '\N')                        AS review_score_description_raw,
    CASE
        WHEN NULLIF(review_score_description, '\N') IS NULL THEN NULL
        WHEN regexp_matches(review_score_description, '^[0-9]+ user reviews?$')
            THEN 'Not enough user reviews'
        ELSE review_score_description
    END                                                             AS review_score_bucket,
    TRY_CAST(NULLIF(positive, '\N') AS BIGINT)                    AS review_positive,
    TRY_CAST(NULLIF(negative, '\N') AS BIGINT)                    AS review_negative,
    TRY_CAST(NULLIF(total, '\N') AS BIGINT)                       AS review_total,
    TRY_CAST(NULLIF(metacritic_score, '\N') AS TINYINT)           AS metacritic_score,
    NULLIF(reviews, '\N')                                          AS review_blurb,
    TRY_CAST(NULLIF(recommendations, '\N') AS BIGINT)             AS steam_recommendations,
    TRY_CAST(NULLIF(steamspy_user_score, '\N') AS DOUBLE)         AS steamspy_user_score,
    TRY_CAST(NULLIF(steamspy_positive, '\N') AS BIGINT)           AS steamspy_positive,
    TRY_CAST(NULLIF(steamspy_negative, '\N') AS BIGINT)           AS steamspy_negative
FROM raw;

SELECT
    CASE WHEN count(*) = count(DISTINCT app_id) THEN 'OK: app_id unique in reviews_stage'
         ELSE 'FAIL: app_id not unique in reviews_stage' END AS pk_check,
    count(*) AS n_rows
FROM reviews_stage;

COPY (SELECT * FROM reviews_stage ORDER BY app_id)
    TO '/home/claude/run_2026-08-22/parquet/reviews_stage.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD);
