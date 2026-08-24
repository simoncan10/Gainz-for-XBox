-- Stage 12 (scoring v2) — feature table for the RETARGETED "what wins" fit model.
--
-- Fixes RT-01 (non-determinism): DuckDB has no defined row order without ORDER BY, and
-- `train_test_split(random_state=42)` in the calling script partitions BY POSITION, so an
-- unordered result set made the whole pipeline non-reproducible (the red-team measured
-- three different out-of-sample r values — 0.5495/0.5599/0.5506 — from three re-runs of
-- the unmodified v1 script, none matching the published 0.564). Fix: `ORDER BY f.app_id`
-- below, AND the calling script (scripts/11v2_build_fit_model.py) additionally re-sorts
-- by app_id in pandas before splitting, belt-and-suspenders, so the split is reproducible
-- even if a future edit removes this ORDER BY or DuckDB's query plan changes.
--
-- Retargeted per RT-05: v1's Fit model predicted ln(1+review_total), which IS pillar 1
-- (Proven/Recognition) for every one of the 15,921 candidate rows -- substituting a noisy
-- r~0.53 prediction for an available measurement of the same quantity adds noise, not
-- information, and the noise (Spearman 0.540 vs composite) outranked the measurement it
-- approximated (0.329). Fit now predicts review_positive_ratio (RECEPTION QUALITY) --
-- a quantity Recognition and Headroom (see 12v2_candidate_screen.sql /
-- scripts/12v2_score_candidates.py) do not encode at all, so it contributes real,
-- non-redundant information instead of a duplicate of pillar 1 wearing a model.
--
-- price_usd_filled is DELIBERATELY EXCLUDED as a Fit feature (unlike v1) so the removal
-- of price from the composite (per rebuild spec) cannot be undone by the back door of
-- price driving the Fit prediction instead. is_indie_i is DELIBERATELY DROPPED (RT-05:
-- it was perfectly collinear with genre_Indie, double-counting "indie" at 2x weight).
--
-- Population unchanged from v1: all non-demo games with >=10 reviews (Valve's own minimum
-- for a review score to exist at all) and a known release_date (age-since-release control
-- for the dataset's right-truncation). Broader than the eligibility screen deliberately,
-- so genre/tag coefficients reflect the catalogue's general pattern, not just the small
-- eligible pool being ranked.

WITH top_genres AS (
    SELECT genre FROM (
        SELECT genre, count(*) n
        FROM read_parquet('parquet/genres_long.parquet') g
        JOIN read_parquet('parquet/fact_games.parquet') f USING(app_id)
        WHERE f.is_demo = false AND f.review_total >= 10
        GROUP BY 1 ORDER BY n DESC LIMIT 12
    )
),
top_tags AS (
    SELECT tag FROM (
        SELECT tag, count(*) n
        FROM read_parquet('parquet/tags_long.parquet') t
        JOIN read_parquet('parquet/fact_games.parquet') f USING(app_id)
        WHERE f.is_demo = false AND f.review_total >= 10
        GROUP BY 1 ORDER BY n DESC LIMIT 30
    )
),
genre_flags AS (
    SELECT app_id, list(DISTINCT genre) AS genre_list
    FROM read_parquet('parquet/genres_long.parquet')
    WHERE genre IN (SELECT genre FROM top_genres)
    GROUP BY app_id
),
tag_flags AS (
    SELECT app_id, list(DISTINCT tag) AS tag_list
    FROM read_parquet('parquet/tags_long.parquet')
    WHERE tag IN (SELECT tag FROM top_tags)
    GROUP BY app_id
)
SELECT
    f.app_id,
    f.name,
    f.developer,
    f.publisher,
    f.review_total,
    f.review_positive_ratio,
    f.owners_mid,
    f.price_usd,
    f.is_free,
    f.monetisation_model,
    f.is_indie,
    f.is_self_published,
    f.has_singleplayer,
    f.has_multiplayer,
    f.has_coop,
    f.has_controller_support,
    f.has_vr,
    f.n_tags,
    f.release_date,
    date_diff('day', f.release_date, DATE '2024-10-28') AS age_days,
    f.release_year,
    coalesce(gf.genre_list, []) AS genre_list,
    coalesce(tf.tag_list, []) AS tag_list,
    f.review_positive_ratio AS target_quality
FROM read_parquet('parquet/fact_games.parquet') f
LEFT JOIN genre_flags gf USING (app_id)
LEFT JOIN tag_flags tf USING (app_id)
WHERE f.is_demo = false
  AND f.review_total >= 10
  AND f.release_date IS NOT NULL
ORDER BY f.app_id;
