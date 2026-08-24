-- Stage 20 (indie scoring) — how broad is "indie" on this dataset, at each candidate
-- definition? Run against the full non-demo catalogue (n=122,191) to justify the
-- operational definition chosen in sql/20_indie_candidate_screen.sql.

SELECT
    count(*) AS n_total,
    count(*) FILTER (WHERE is_indie = true) AS n_indie_flag,
    round(100.0 * count(*) FILTER (WHERE is_indie = true) / count(*), 1) AS pct_indie_flag,
    count(*) FILTER (WHERE is_indie IS NULL) AS n_indie_null_nonenglish_floor,
    count(*) FILTER (WHERE is_indie = true AND is_self_published = true) AS n_indie_and_selfpub,
    round(100.0 * count(*) FILTER (WHERE is_indie = true AND is_self_published = true) / count(*), 1) AS pct_indie_and_selfpub
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
WHERE is_demo = false;
