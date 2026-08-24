-- 06_validate.sql
-- Validation pass: row counts at each stage, referential integrity on every
-- join key, join coverage recomputed against the built table (must match
-- the stage-1 profile), monetisation-model breakdown, and a five-record
-- end-to-end spot check on well-known app_ids.

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE VIEW fact_games AS SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet');
CREATE OR REPLACE VIEW categories_long AS SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/categories_long.parquet');
CREATE OR REPLACE VIEW genres_long AS SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet');
CREATE OR REPLACE VIEW tags_long AS SELECT * FROM read_parquet('/home/claude/run_2026-08-22/parquet/tags_long.parquet');

-- 1. Row counts at each stage
SELECT '1_row_counts' AS section, 'games_stage' AS tbl, count(*) AS n FROM read_parquet('/home/claude/run_2026-08-22/parquet/games_stage.parquet')
UNION ALL SELECT '1_row_counts', 'reviews_stage', count(*) FROM read_parquet('/home/claude/run_2026-08-22/parquet/reviews_stage.parquet')
UNION ALL SELECT '1_row_counts', 'steamspy_stage', count(*) FROM read_parquet('/home/claude/run_2026-08-22/parquet/steamspy_stage.parquet')
UNION ALL SELECT '1_row_counts', 'categories_long', count(*) FROM categories_long
UNION ALL SELECT '1_row_counts', 'genres_long', count(*) FROM genres_long
UNION ALL SELECT '1_row_counts', 'tags_long', count(*) FROM tags_long
UNION ALL SELECT '1_row_counts', 'fact_games', count(*) FROM fact_games;

-- 2. Referential integrity: every long-table app_id must exist in fact_games
SELECT '2_ref_integrity' AS section, 'categories_orphans' AS check_name,
       count(*) AS n_bad
FROM categories_long c LEFT JOIN fact_games f ON f.app_id = c.app_id WHERE f.app_id IS NULL
UNION ALL
SELECT '2_ref_integrity', 'genres_orphans', count(*)
FROM genres_long g LEFT JOIN fact_games f ON f.app_id = g.app_id WHERE f.app_id IS NULL
UNION ALL
SELECT '2_ref_integrity', 'tags_orphans', count(*)
FROM tags_long t LEFT JOIN fact_games f ON f.app_id = t.app_id WHERE f.app_id IS NULL
UNION ALL
SELECT '2_ref_integrity', 'fact_games_pk_dupe_check', count(*) - count(DISTINCT app_id)
FROM fact_games;

-- 3. Join coverage recomputed from the built table -- must match profile
SELECT '3_join_coverage' AS section, 'categories_pct' AS metric,
       round(100.0 * count(*) FILTER (WHERE n_categories > 0) / count(*), 2) AS pct
FROM fact_games
UNION ALL
SELECT '3_join_coverage', 'genres_pct', round(100.0 * count(*) FILTER (WHERE n_genres > 0) / count(*), 2) FROM fact_games
UNION ALL
SELECT '3_join_coverage', 'tags_pct', round(100.0 * count(*) FILTER (WHERE n_tags > 0) / count(*), 2) FROM fact_games
UNION ALL
SELECT '3_join_coverage', 'reviews_pct', round(100.0 * count(*) FILTER (WHERE review_total IS NOT NULL) / count(*), 2) FROM fact_games
UNION ALL
SELECT '3_join_coverage', 'steamspy_pct',
       round(100.0 * count(*) FILTER (WHERE s.app_id IS NOT NULL) / count(*), 2)
FROM fact_games f
LEFT JOIN read_parquet('/home/claude/run_2026-08-22/parquet/steamspy_stage.parquet') s ON s.app_id = f.app_id;

-- 4. Monetisation model breakdown
SELECT '4_monetisation' AS section, monetisation_model, count(*) AS n,
       round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS pct
FROM fact_games GROUP BY monetisation_model ORDER BY n DESC;

-- 5. Price source breakdown (among paid, priced titles)
SELECT '5_price_source' AS section, COALESCE(price_usd_source, 'NULL') AS src, count(*) AS n
FROM fact_games WHERE monetisation_model = 'paid' GROUP BY src ORDER BY n DESC;

-- 6. Demo vs game split
SELECT '6_app_type' AS section, app_type, count(*) AS n FROM fact_games GROUP BY app_type;

-- 7. game_mode distribution
SELECT '7_game_mode' AS section, game_mode, count(*) AS n FROM fact_games GROUP BY game_mode ORDER BY n DESC;

-- 8. Five known records traced end to end
SELECT '8_spot_check' AS section, app_id, name, app_type, release_date, is_free,
       monetisation_model, price_usd, price_usd_source, developer, publisher,
       owners_range, owners_mid, review_score_bucket, review_total,
       n_categories, has_multiplayer, has_coop, is_indie, n_genres, n_tags
FROM fact_games
WHERE app_id IN (10, 570, 730, 440, 400)
ORDER BY app_id;
