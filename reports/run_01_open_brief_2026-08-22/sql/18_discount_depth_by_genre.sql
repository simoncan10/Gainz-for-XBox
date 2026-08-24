-- Q18: Discount depth by genre, single-point-in-time snapshot (~Dec 2024) from SteamSpy.
-- This is NOT discount frequency or a discount calendar -- the dataset has exactly one
-- observation per app (the snapshot date), so we can only report "what fraction of titles
-- happened to be on sale, and how deep, on the day of the snapshot" -- not how often a
-- genre discounts across a year. Restricted to paid, non-demo, non-free games with a
-- resolvable price and a valid discount_pct reading.
WITH base AS (
    SELECT f.app_id, f.price_usd, s.discount_pct_steamspy
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet') f
    JOIN read_parquet('/home/claude/run_2026-08-22/parquet/steamspy_stage.parquet') s USING (app_id)
    WHERE f.is_demo = false AND f.app_type = 'game'
      AND f.monetisation_model = 'paid' AND s.discount_pct_steamspy IS NOT NULL
),
genre_titles AS (
    SELECT gl.genre, b.discount_pct_steamspy
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN base b USING (app_id)
)
SELECT genre,
       count(*) AS n_titles,
       round(100.0 * avg(CASE WHEN discount_pct_steamspy > 0 THEN 1.0 ELSE 0.0 END), 1) AS pct_on_sale_at_snapshot,
       round(avg(discount_pct_steamspy) FILTER (WHERE discount_pct_steamspy > 0), 1) AS mean_discount_pct_when_on_sale
FROM genre_titles
GROUP BY genre
HAVING count(*) >= 100
ORDER BY pct_on_sale_at_snapshot DESC;
