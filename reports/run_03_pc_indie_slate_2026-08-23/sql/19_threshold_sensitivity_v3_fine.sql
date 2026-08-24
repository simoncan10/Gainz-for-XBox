-- Stage 16 (scoring v3) — fine-grained (500-unit-step) review_total sensitivity, run to
-- verify the Stage 15 red team's A-2 finding that the metacritic-presence plateau begins
-- at 4,000, not 5,000. Owners_mid ceiling fixed at 750,000; all other v3 screens applied.

WITH adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
),
base AS (
    SELECT f.*
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
    LEFT JOIN adult_tagged a USING (app_id)
    WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
      AND f.review_positive_ratio >= 0.70 AND f.price_usd > 0
      AND f.has_controller_support = true AND f.owners_mid <= 750000 AND a.app_id IS NULL
)
SELECT rt AS floor,
       count(*) FILTER (WHERE b.review_total >= rt) AS n,
       round(100.0 * count(*) FILTER (WHERE b.review_total >= rt AND b.metacritic_score IS NOT NULL)
             / NULLIF(count(*) FILTER (WHERE b.review_total >= rt), 0), 1) AS metacritic_pct
FROM base b,
     (VALUES (500),(1000),(2000),(3000),(4000),(4500),(5000),(5500),(6000),(7000),(7500),(10000),(15000)) AS t(rt)
GROUP BY rt
ORDER BY rt;
