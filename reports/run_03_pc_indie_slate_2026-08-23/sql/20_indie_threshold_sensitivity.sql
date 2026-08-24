-- Stage 20 (indie scoring) — re-derive the review_total floor and owners_mid ceiling
-- within the indie+self-published population, rather than carrying v3's thresholds over
-- unexamined. Population: paid, price>0, quality>=0.70, no adult tag, is_indie=true,
-- is_self_published=true.

WITH adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
),
indie AS (
    SELECT f.*
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
    LEFT JOIN adult_tagged a USING (app_id)
    WHERE f.is_demo = false AND f.app_type = 'game' AND f.monetisation_model = 'paid'
      AND f.review_positive_ratio >= 0.70 AND f.price_usd > 0 AND a.app_id IS NULL
      AND f.is_indie = true AND f.is_self_published = true
)
-- (1) review_total floor sensitivity, owners_mid ceiling fixed at 750,000
SELECT 'review_total_floor' AS check_name, rt AS threshold,
       count(*) FILTER (WHERE review_total >= rt AND owners_mid <= 750000) AS n,
       round(100.0 * count(*) FILTER (WHERE review_total >= rt AND owners_mid <= 750000 AND metacritic_score IS NOT NULL)
             / NULLIF(count(*) FILTER (WHERE review_total >= rt AND owners_mid <= 750000), 0), 1) AS metacritic_pct
FROM indie, (VALUES (500),(1000),(2000),(3000),(4000),(5000),(6000),(7500),(10000)) AS t(rt)
GROUP BY rt
UNION ALL
-- (2) owners_mid ceiling sensitivity, review_total floor fixed at 4,000
SELECT 'owners_ceiling' AS check_name, oc AS threshold,
       count(*) FILTER (WHERE review_total >= 4000 AND owners_mid <= oc) AS n,
       round(100.0 * count(*) FILTER (WHERE review_total >= 4000 AND owners_mid <= oc AND metacritic_score IS NOT NULL)
             / NULLIF(count(*) FILTER (WHERE review_total >= 4000 AND owners_mid <= oc), 0), 1) AS metacritic_pct
FROM indie, (VALUES (200000),(350000),(500000),(750000),(1000000),(1500000),(3500000)) AS t(oc)
GROUP BY oc
ORDER BY check_name, threshold;
