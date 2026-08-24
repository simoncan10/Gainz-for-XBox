-- 04_stage_long_tables.sql
-- categories.csv / genres.csv / tags.csv are already normalized long tables
-- in the raw source (one row per app_id + value pair) -- no comma-splitting
-- needed here. They are converted to Parquet as-is (deduplicated defensively
-- on the natural key) and kept SEPARATE from the wide fact table. Anyone
-- doing genre/tag/category-level analysis must query these directly or use
-- the pre-aggregated flags in fact_games -- never the fact table's arrays
-- as a comma-joined string, and never a naive app_id-only join (fans out
-- 3.9x / 2.9x / 14.8x respectively per the profile).

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE TABLE categories_long AS
SELECT DISTINCT app_id, trim(category) AS category
FROM read_csv('/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/categories.csv', header = true, sample_size = -1);

CREATE OR REPLACE TABLE genres_long AS
SELECT DISTINCT app_id, trim(genre) AS genre
FROM read_csv('/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/genres.csv', header = true, sample_size = -1);

CREATE OR REPLACE TABLE tags_long AS
SELECT DISTINCT app_id, trim(tag) AS tag
FROM read_csv('/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/tags.csv', header = true, sample_size = -1);

SELECT 'categories_long' AS tbl, count(*) AS n_rows, count(DISTINCT app_id) AS n_apps FROM categories_long
UNION ALL
SELECT 'genres_long', count(*), count(DISTINCT app_id) FROM genres_long
UNION ALL
SELECT 'tags_long', count(*), count(DISTINCT app_id) FROM tags_long;

COPY (SELECT * FROM categories_long ORDER BY app_id, category) TO '/home/claude/run_2026-08-22/parquet/categories_long.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
COPY (SELECT * FROM genres_long ORDER BY app_id, genre) TO '/home/claude/run_2026-08-22/parquet/genres_long.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
COPY (SELECT * FROM tags_long ORDER BY app_id, tag) TO '/home/claude/run_2026-08-22/parquet/tags_long.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
