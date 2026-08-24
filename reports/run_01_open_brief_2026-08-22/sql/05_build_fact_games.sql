-- 05_build_fact_games.sql
-- Build the canonical analytical table: fact_games.
--
-- Grain: one row per app_id (the games.csv universe, 140,082 rows -- games
-- AND demos; see is_demo). This is a LEFT-join build from games_stage, so
-- every coverage gap in reviews/steamspy/categories/genres/tags surfaces as
-- NULL rather than silently dropping rows. Long tables (categories/genres/
-- tags) are pre-aggregated into per-app boolean flags / counts BEFORE the
-- join so no fan-out reaches this table (naive app_id joins would multiply
-- rows 3.9x/2.9x/14.8x respectively -- see profile).
--
-- Everything reads from parquet/, never from the raw CSVs, per "Parquet is
-- the boundary".
--
-- PRICE NORMALIZATION (judgement call, see DECISIONS.md):
--   games.csv's price_overview is priced in the STOREFRONT's local currency
--   -- 99.1% of priced rows are EUR, not USD, with a long tail of ~30 other
--   currencies (RUB, BRL, KRW, JPY, ...). This was NOT flagged in the
--   stage-1 profile and would silently understate "average price" by ~4-8%
--   if EUR cent-values were read as USD dollars-of-cents outright.
--   steamspy_insights.price is already USD cents (verified against known
--   prices, e.g. app_id 10 Counter-Strike = 999 = $9.99) and is used as the
--   PRIMARY source. Where steamspy's price is missing, games.csv's
--   price_overview is converted using a STATIC, APPROXIMATE, SINGLE-
--   POINT-IN-TIME (~Dec 2024) FX table hardcoded below. This is adequate
--   for aggregate USD-denominated price distributions (EUR+USD alone cover
--   99.3% of priced rows) but NOT precise enough for currency-sensitive or
--   time-sensitive pricing analysis, and NOT a live/audited FX feed.
--
-- MONETISATION MODEL keeps three states distinct, per the task brief:
--   'free'               -- is_free = true in games.csv
--   'paid'                -- is_free = false AND a USD price was resolved
--   'paid_price_unknown'  -- is_free = false but NO price data anywhere
--                            (24.5% of paid titles after combining both
--                            price sources -- down from 28.3% using
--                            games.csv's price_overview alone, but still
--                            material: never treat this bucket as free or
--                            impute a price for it).

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE TABLE fx_to_usd (currency VARCHAR, rate DOUBLE);
INSERT INTO fx_to_usd VALUES
    ('USD', 1.0),
    ('EUR', 1.04),
    ('GBP', 1.26),
    ('RUB', 0.0096),
    ('CAD', 0.70),
    ('ILS', 0.27),
    ('BRL', 0.165),
    ('PLN', 0.24),
    ('CNY', 0.137),
    ('KRW', 0.00069),
    ('AUD', 0.62),
    ('MXN', 0.048),
    ('TWD', 0.030),
    ('UAH', 0.024),
    ('SGD', 0.73),
    ('PHP', 0.017),
    ('HKD', 0.129),
    ('INR', 0.0118),
    ('IDR', 0.000062),
    ('JPY', 0.0064),
    ('SAR', 0.267),
    ('KWD', 3.25),
    ('MYR', 0.22),
    ('KZT', 0.0019),
    ('VND', 0.0000393),
    ('PEN', 0.265),
    ('COP', 0.00022),
    ('NZD', 0.565),
    ('THB', 0.0288),
    ('AED', 0.272),
    ('NOK', 0.088);

-- DISCOVERED HAZARD (not in stage-1 profile): category values are captured
-- in whatever locale Steam's API happened to return per app, not uniformly
-- in English -- 154 of 315 distinct category strings (795 of 522,582 rows,
-- 0.15%) are non-ASCII translations of the same ~40 canonical category
-- types (e.g. Russian "Кооператив" = "Co-op", Polish "Wieloosobowa" =
-- "Multiplayer"). English-string matching (has_multiplayer, has_coop, etc.)
-- would silently read these apps as false/single-player. Confirmed this
-- hits only 53 of 134,393 apps with categories (0.04%) where NOT ONE row
-- is ASCII/English -- but two of those 53 are Dota 2 and Counter-Strike 2,
-- caught by the 5-record spot check in 06_validate.sql. Fix: track
-- has_any_ascii_category per app and downgrade the boolean flags to NULL
-- (unknown), never false, for the handful of apps with zero English-
-- language category rows -- see DECISIONS.md.
CREATE OR REPLACE TABLE categories_agg AS
SELECT
    app_id,
    list(category ORDER BY category)                                                          AS categories,
    count(*)                                                                                    AS n_categories,
    bool_or(regexp_matches(category, '^[[:ascii:]]+$'))                                         AS has_any_ascii_category,
    bool_or(category = 'Single-player')                                                         AS has_singleplayer,
    bool_or(category IN (
        'Multi-player','PvP','Co-op','Online PvP','Online Co-op','Shared/Split Screen',
        'Shared/Split Screen PvP','Shared/Split Screen Co-op','Cross-Platform Multiplayer',
        'MMO','LAN Co-op','LAN PvP'
    ))                                                                                           AS has_multiplayer,
    bool_or(category ILIKE '%co-op%')                                                            AS has_coop,
    bool_or(category IN ('Full controller support','Partial Controller Support'))                AS has_controller_support,
    bool_or(category ILIKE '%VR%')                                                                AS has_vr
FROM read_parquet('/home/claude/run_2026-08-22/parquet/categories_long.parquet')
GROUP BY app_id;

-- Same localization hazard as categories, smaller scale: 303/353,339 genre
-- rows (0.09%) are non-ASCII translations. Same NULL-not-false treatment.
CREATE OR REPLACE TABLE genres_agg AS
SELECT
    app_id,
    list(genre ORDER BY genre)      AS genres,
    count(*)                         AS n_genres,
    bool_or(regexp_matches(genre, '^[[:ascii:]]+$')) AS has_any_ascii_genre,
    bool_or(genre = 'Indie')         AS is_indie_raw
FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet')
GROUP BY app_id;

CREATE OR REPLACE TABLE tags_agg AS
SELECT
    app_id,
    list(tag ORDER BY tag) AS tags,
    count(*)                AS n_tags
FROM read_parquet('/home/claude/run_2026-08-22/parquet/tags_long.parquet')
GROUP BY app_id;

CREATE OR REPLACE TABLE fact_games AS
WITH g AS (
    SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/games_stage.parquet')
),
r AS (
    SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/reviews_stage.parquet')
),
s AS (
    SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/steamspy_stage.parquet')
),
priced AS (
    SELECT
        g.app_id,
        g.price_final_cents * fx.rate AS games_price_usd_cents
    FROM g
    LEFT JOIN fx_to_usd fx ON fx.currency = g.price_currency
    WHERE g.price_final_cents IS NOT NULL
)
SELECT
    g.app_id,
    g.name,
    g.app_type,
    g.is_demo,
    g.release_date,
    year(g.release_date)                                                    AS release_year,
    COALESCE(CAST(year(g.release_date) AS VARCHAR), 'unknown')              AS release_cohort,
    (year(g.release_date) = 2024)                                           AS release_year_is_partial_2024,
    g.languages,
    g.is_free,
    COALESCE(s.price_cents_steamspy, p.games_price_usd_cents)               AS price_usd_cents_resolved,
    CASE
        WHEN g.is_free THEN 0.0
        WHEN s.price_cents_steamspy IS NOT NULL THEN s.price_cents_steamspy / 100.0
        WHEN p.games_price_usd_cents IS NOT NULL THEN p.games_price_usd_cents / 100.0
        ELSE NULL
    END                                                                      AS price_usd,
    CASE
        WHEN s.price_cents_steamspy IS NOT NULL THEN 'steamspy'
        WHEN p.games_price_usd_cents IS NOT NULL THEN 'games_csv_fx_converted'
        ELSE NULL
    END                                                                      AS price_usd_source,
    CASE
        WHEN g.is_free THEN 'free'
        WHEN s.price_cents_steamspy IS NOT NULL OR p.games_price_usd_cents IS NOT NULL THEN 'paid'
        ELSE 'paid_price_unknown'
    END                                                                      AS monetisation_model,
    s.developer,
    s.publisher,
    s.is_self_published,
    s.owners_range,
    s.owners_low,
    s.owners_high,
    s.owners_mid,
    s.concurrent_users_yesterday,
    r.review_score,
    r.review_score_bucket,
    r.review_positive,
    r.review_negative,
    r.review_total,
    CASE WHEN r.review_total > 0 THEN r.review_positive::DOUBLE / r.review_total ELSE NULL END AS review_positive_ratio,
    r.metacritic_score,
    r.steam_recommendations,
    COALESCE(cg.n_categories, 0)      AS n_categories,
    -- NULL (unknown), not false, when the app has categories but every one
    -- of them is in a non-English locale (0.04% of apps with categories --
    -- see note on categories_agg above). Only genuinely false when at
    -- least one English-language category row exists and none matched.
    CASE WHEN cg.app_id IS NULL THEN false
         WHEN NOT cg.has_any_ascii_category THEN NULL
         ELSE cg.has_singleplayer END AS has_singleplayer,
    CASE WHEN cg.app_id IS NULL THEN false
         WHEN NOT cg.has_any_ascii_category THEN NULL
         ELSE cg.has_multiplayer END AS has_multiplayer,
    CASE WHEN cg.app_id IS NULL THEN false
         WHEN NOT cg.has_any_ascii_category THEN NULL
         ELSE cg.has_coop END AS has_coop,
    CASE WHEN cg.app_id IS NULL THEN false
         WHEN NOT cg.has_any_ascii_category THEN NULL
         ELSE cg.has_controller_support END AS has_controller_support,
    CASE WHEN cg.app_id IS NULL THEN false
         WHEN NOT cg.has_any_ascii_category THEN NULL
         ELSE cg.has_vr END AS has_vr,
    CASE
        WHEN cg.app_id IS NOT NULL AND NOT cg.has_any_ascii_category THEN 'unknown_non_english_metadata'
        WHEN COALESCE(cg.has_multiplayer,false) AND COALESCE(cg.has_singleplayer,false) THEN 'single_and_multiplayer'
        WHEN COALESCE(cg.has_multiplayer,false) THEN 'multiplayer_only'
        WHEN COALESCE(cg.has_singleplayer,false) THEN 'single_player_only'
        ELSE 'unspecified'
    END                                   AS game_mode,
    cg.categories,
    COALESCE(gn.n_genres, 0)             AS n_genres,
    CASE WHEN gn.app_id IS NULL THEN false
         WHEN NOT gn.has_any_ascii_genre THEN NULL
         ELSE gn.is_indie_raw END        AS is_indie,
    gn.genres,
    COALESCE(tg.n_tags, 0)               AS n_tags,
    tg.tags
FROM g
LEFT JOIN r ON r.app_id = g.app_id
LEFT JOIN s ON s.app_id = g.app_id
LEFT JOIN priced p ON p.app_id = g.app_id
LEFT JOIN categories_agg cg ON cg.app_id = g.app_id
LEFT JOIN genres_agg gn ON gn.app_id = g.app_id
LEFT JOIN tags_agg tg ON tg.app_id = g.app_id;

SELECT
    CASE WHEN count(*) = count(DISTINCT app_id) THEN 'OK: app_id unique in fact_games'
         ELSE 'FAIL: app_id not unique in fact_games' END AS pk_check,
    count(*) AS n_rows
FROM fact_games;

COPY (SELECT * FROM fact_games ORDER BY app_id)
    TO '/home/claude/run_2026-08-22/parquet/fact_games.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD);
