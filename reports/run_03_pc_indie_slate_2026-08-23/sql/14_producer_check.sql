-- Stage 10 (scoring) — producer-level check: which developers place MULTIPLE titles in
-- the qualifying list (composite_score >= 0.60 on the eligible pool)? Consistency across
-- titles is stronger evidence than a single hit. Read against
-- artifacts/10_candidates.csv (the actual qualifying list; this query reproduces the
-- eligibility+bar logic inline for a standalone, auditable check).
--
-- NOTE: this SQL reproduces the SCREEN (sql/12_candidate_screen.sql) but not the
-- percentile-rank composite score itself (that requires the fitted model coefficients
-- and is computed in scripts/12_score_candidates.py). This query is a sanity cross-check
-- on developer concentration among titles that at least clear the eligibility screen —
-- the exact composite-based qualifying counts by developer are read from
-- artifacts/10_candidates.csv directly (see scripts/13_build_model_json.py).

WITH adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
),
eligible AS (
    SELECT f.app_id, f.developer
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
    LEFT JOIN adult_tagged a USING (app_id)
    WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
      AND f.review_total >= 50 AND f.review_positive_ratio >= 0.70
      AND f.owners_mid <= 750000 AND f.price_usd > 0 AND a.app_id IS NULL
)
SELECT developer, count(*) AS n_eligible_titles
FROM eligible
WHERE developer IS NOT NULL
GROUP BY 1
HAVING count(*) >= 3
ORDER BY n_eligible_titles DESC;
