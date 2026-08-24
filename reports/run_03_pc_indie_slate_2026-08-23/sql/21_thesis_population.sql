-- Stage 21 (indie thesis) — comparison population and group definition.
-- Population: is_demo=false, monetisation_model='paid', price_usd>0, review_total>=10
-- (Valve's own minimum for a review score to exist at all -- below this there is no
-- reception signal to compare). This is DELIBERATELY BROADER than the Stage 20 candidate
-- screen (no owners ceiling, no quality floor, no review_total>=4000 floor) because the
-- thesis question is about the whole catalogue's indie-vs-non-indie pattern, not about
-- the already-curated shortlist -- screening to the shortlist population first would
-- answer "do our finalists look different" rather than "do indies as a class differ,"
-- which is the question actually asked.
--
-- Group definition: the SAME operational indie definition chosen in
-- sql/20_indie_candidate_screen.sql (is_indie=true AND is_self_published=true), applied
-- with COALESCE so the 73 NULL-is_indie rows (non-English-metadata floor,
-- 02_cleaning_report.md) fall into the non-indie group rather than vanishing from both.

SELECT
    count(*) AS n_total,
    count(*) FILTER (WHERE coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true) AS n_indie,
    count(*) FILTER (WHERE NOT (coalesce(is_indie, false) = true AND coalesce(is_self_published, false) = true)) AS n_nonindie,
    count(*) FILTER (WHERE is_indie IS NULL) AS n_indie_flag_null_floor
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
WHERE is_demo = false AND monetisation_model = 'paid' AND price_usd > 0 AND review_total >= 10;
