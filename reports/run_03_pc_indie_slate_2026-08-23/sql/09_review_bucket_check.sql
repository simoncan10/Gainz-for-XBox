-- Stage 10 (scoring) — confirms Valve's own review-score-bucket boundaries empirically in
-- this dataset, used to justify the "Proven" (review_total>=50) and "quality"
-- (review_positive_ratio>=0.70) screens in sql/12_candidate_screen.sql.
-- n = 122,191 non-demo apps (the full games universe).

SELECT
    review_score_bucket,
    count(*) AS n,
    round(min(review_positive_ratio), 3) AS min_ratio,
    round(avg(review_positive_ratio), 3) AS avg_ratio,
    round(max(review_positive_ratio), 3) AS max_ratio,
    min(review_total) AS min_review_total,
    max(review_total) AS max_review_total
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
WHERE is_demo = false
GROUP BY 1
ORDER BY avg_ratio;
