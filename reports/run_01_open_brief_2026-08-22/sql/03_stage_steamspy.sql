-- 03_stage_steamspy.sql
-- Type steamspy_insights.csv. Two judgement calls made here (DECISIONS.md):
--
--  * The four playtime columns (playtime_average_forever/_2weeks,
--    playtime_median_forever/_2weeks) are DROPPED, not carried forward.
--    Verified: constant 0 across all 140,077 rows -- zero variance, not a
--    high null rate. Keeping them risks a downstream analyst plotting
--    "engagement" off a column that is silently all zeros. There is no
--    playtime/engagement signal anywhere in this dataset; this is recorded
--    as a hard scope limit, not patched with an imputed value.
--  * steamspy's own `languages` and `genres` (comma-joined) columns are
--    dropped as redundant/inferior duplicates of games_stage.languages and
--    the properly-normalized genres.csv long table respectively -- never
--    analyse a comma-separated string column when a long table exists.
--
-- owners_range ("10,000,000 .. 20,000,000") is parsed into numeric bounds
-- and a midpoint. This is a coarse proxy, not a real count: SteamSpy buckets
-- 83.2% of the entire catalogue into the single lowest bin (0..20,000), so
-- owners_mid resolves to 10,000 for the vast majority of apps and cannot
-- distinguish a niche title from a modest mid-size hit within that bin.
--
-- price / initial_price here are already USD cents (steamspy is a USD-
-- native aggregator; verified against known prices, e.g. app_id 10 = $9.99).
-- This is a materially better price source than games.csv's price_overview
-- (which is 99.1% EUR, not USD) and is used as the PRIMARY price source in
-- 05_build_fact_games.sql.

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE TABLE steamspy_stage AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/steamspy_insights.csv',
        header = true,
        sample_size = -1
    )
),
parsed AS (
    SELECT
        app_id,
        NULLIF(developer, '\N') AS developer,
        NULLIF(publisher, '\N') AS publisher,
        NULLIF(owners_range, '\N') AS owners_range,
        TRY_CAST(
            regexp_replace(split_part(NULLIF(owners_range, '\N'), ' .. ', 1), ',', '', 'g')
            AS BIGINT
        ) AS owners_low,
        TRY_CAST(
            regexp_replace(split_part(NULLIF(owners_range, '\N'), ' .. ', 2), ',', '', 'g')
            AS BIGINT
        ) AS owners_high,
        concurrent_users_yesterday,
        TRY_CAST(NULLIF(price, '\N') AS BIGINT)          AS price_cents_steamspy,
        TRY_CAST(NULLIF(initial_price, '\N') AS BIGINT)  AS initial_price_cents_steamspy,
        TRY_CAST(NULLIF(discount, '\N') AS INTEGER)      AS discount_pct_steamspy
    FROM raw
)
SELECT
    app_id,
    developer,
    publisher,
    -- self-published: developer and publisher are the same studio (case/
    -- whitespace-insensitive). Used downstream as a proxy for "indie /
    -- unbacked" vs "has a distinct publisher" -- this dataset has no actual
    -- Xbox first-/third-party field, so this is the closest analogous
    -- signal available (see DECISIONS.md).
    CASE
        WHEN developer IS NULL OR publisher IS NULL THEN NULL
        ELSE lower(trim(developer)) = lower(trim(publisher))
    END AS is_self_published,
    owners_range,
    owners_low,
    owners_high,
    (owners_low + owners_high) / 2.0 AS owners_mid,
    concurrent_users_yesterday,
    price_cents_steamspy,
    initial_price_cents_steamspy,
    discount_pct_steamspy
FROM parsed;

SELECT
    CASE WHEN count(*) = count(DISTINCT app_id) THEN 'OK: app_id unique in steamspy_stage'
         ELSE 'FAIL: app_id not unique in steamspy_stage' END AS pk_check,
    count(*) AS n_rows
FROM steamspy_stage;

COPY (SELECT * FROM steamspy_stage ORDER BY app_id)
    TO '/home/claude/run_2026-08-22/parquet/steamspy_stage.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD);
