-- Stage 12 (scoring v2) — threshold sensitivity for the two thresholds that now carry
-- the qualifying list: review_total floor and owners_mid ceiling. Both other screens
-- (quality>=0.70, paid+price>0, no adult tag, has_controller_support=true) held fixed at
-- their chosen values. Run twice: once varying review_total with owners_mid fixed at
-- 750,000, once varying owners_mid with review_total fixed at 5,000. n and metacritic
-- presence reported for each combination — see artifacts/12_model_v2.json
-- "eligibility_screen.thresholds" for the two sensitivity tables and the elbow
-- justification for 5,000 drawn from them.

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
      AND f.has_controller_support = true AND a.app_id IS NULL
)
-- (1) vary review_total floor, owners_mid ceiling fixed at 750,000
SELECT 'review_total_sensitivity' AS check_name, rt AS threshold,
       count(*) FILTER (WHERE b.review_total >= rt AND b.owners_mid <= 750000) AS n,
       round(100.0 * count(*) FILTER (WHERE b.review_total >= rt AND b.owners_mid <= 750000
                                       AND b.metacritic_score IS NOT NULL)
             / NULLIF(count(*) FILTER (WHERE b.review_total >= rt AND b.owners_mid <= 750000), 0), 1)
             AS metacritic_pct
FROM base b, (VALUES (500),(1000),(2000),(3000),(5000),(7500),(10000),(15000)) AS t(rt)
GROUP BY rt
UNION ALL
-- (2) vary owners_mid ceiling, review_total floor fixed at 5,000
SELECT 'owners_ceiling_sensitivity' AS check_name, oc AS threshold,
       count(*) FILTER (WHERE b.review_total >= 5000 AND b.owners_mid <= oc) AS n,
       round(100.0 * count(*) FILTER (WHERE b.review_total >= 5000 AND b.owners_mid <= oc
                                       AND b.metacritic_score IS NOT NULL)
             / NULLIF(count(*) FILTER (WHERE b.review_total >= 5000 AND b.owners_mid <= oc), 0), 1)
             AS metacritic_pct
FROM base b, (VALUES (200000),(350000),(500000),(750000),(1000000),(1500000),(2000000),(3500000)) AS t(oc)
GROUP BY oc
ORDER BY check_name, threshold;
