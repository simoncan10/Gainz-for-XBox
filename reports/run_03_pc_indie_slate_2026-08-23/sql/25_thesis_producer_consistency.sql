-- Stage 21 (indie thesis) — producer consistency: among developers with at least one
-- "hit" (owners_mid>=100,000), what share repeat (>=2 hits)? Population per
-- sql/21_thesis_population.sql, developer IS NOT NULL.

WITH pop AS (
    SELECT *, (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS is_indie_strict
    FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
    WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10
      AND developer IS NOT NULL
),
dev_hits AS (
    SELECT developer, is_indie_strict, count(*) AS n_titles,
        count(*) FILTER (WHERE owners_mid >= 100000) AS n_hits
    FROM pop GROUP BY developer, is_indie_strict
)
SELECT is_indie_strict,
    count(*) AS n_developers,
    count(*) FILTER (WHERE n_hits >= 1) AS n_devs_with_1plus_hit,
    round(100.0 * count(*) FILTER (WHERE n_hits >= 1) / count(*), 2) AS pct_devs_ever_hit,
    count(*) FILTER (WHERE n_hits >= 2) AS n_devs_with_2plus_hits,
    round(100.0 * count(*) FILTER (WHERE n_hits >= 2) / NULLIF(count(*) FILTER (WHERE n_hits >= 1), 0), 2) AS pct_of_hitters_who_repeat
FROM dev_hits GROUP BY is_indie_strict;
