-- Stage 10 (scoring) — feature table for the "what wins in this catalogue" fit model.
--
-- Population: all non-demo games with >=10 reviews (Valve's own minimum for a review
-- score to exist at all — below this the bucket is literally "Not enough user reviews")
-- and a known release_date (release_date is 20.4% missing per 01_profile.md; age-since-
-- release is used below as a right-censoring control, so rows without a date cannot be
-- used to fit it and are excluded from TRAINING, though they can still be SCORED later
-- using the fitted coefficients on their non-age features).
--
-- This is a broader population than the final candidate-eligibility screen (see
-- 12_candidate_screen.sql) — the model is fit on the whole reviewed catalogue so genre/tag
-- coefficients reflect the catalogue's general pattern, not just the small-owner subset we
-- are trying to rank. That separation (fit population != scoring population) is what keeps
-- the "what wins" signal from being a restatement of the screens we already apply.
--
-- Target: log1p(review_total) — a reception-SCALE proxy. This is a MEASURED column
-- (reviews_stage.review_total), never described as "engagement" or "playtime" (no such
-- column exists in this dataset per hard limits).
--
-- One row per app_id. Output written to parquet by the calling Python script
-- (11_build_fit_model.py) via `COPY (this query) TO ... (FORMAT PARQUET)`.

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
    ln(1 + f.review_total) AS target_log_reviews
FROM read_parquet('parquet/fact_games.parquet') f
LEFT JOIN genre_flags gf USING (app_id)
LEFT JOIN tag_flags tf USING (app_id)
WHERE f.is_demo = false
  AND f.review_total >= 10
  AND f.release_date IS NOT NULL;
