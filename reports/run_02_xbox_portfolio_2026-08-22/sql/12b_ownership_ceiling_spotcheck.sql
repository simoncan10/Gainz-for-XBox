-- Stage 10 (scoring) — spot-check of what sits just above the owners_mid=750,000 ceiling,
-- used to justify that ceiling in sql/12_candidate_screen.sql. n=1,025 non-demo titles in
-- the 1,000,000-2,000,000 and 2,000,000-5,000,000 owners buckets combined.

SELECT name, owners_range, review_total, price_usd
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
WHERE is_demo = false AND owners_mid IN (1500000, 3500000)
ORDER BY owners_mid DESC, review_total DESC
LIMIT 40;
