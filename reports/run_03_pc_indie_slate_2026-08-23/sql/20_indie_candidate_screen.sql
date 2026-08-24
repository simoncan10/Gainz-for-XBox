-- Stage 20 (indie scoring) — the candidate eligibility screen, rescoped to indie titles
-- and to PC (Game Pass runs on Windows PC; Xbox console availability is no longer a
-- requirement) per the coordinator's three change instructions.
--
-- CHANGE 1 (indie focus) — operational definition, justified:
--   is_indie = true          -- Steam's own genre-level self-declaration. MEASURED, but
--                                a FLOOR: 87 apps have NULL is_indie because their only
--                                category/genre rows are entirely non-English
--                                (02_cleaning_report.md hazard) -- these can never enter
--                                an is_indie=true filter even if truly indie, so this
--                                screen slightly undercounts. On its own this flag is
--                                FAR too broad to be a segment: 82,552 of 122,191
--                                non-demo games (67.6%) carry it (sql/20_indie_
--                                definition_check.sql) -- "a definition that admits
--                                two-thirds of the catalogue is not a segment."
--   AND is_self_published = true  -- (developer = publisher, from steamspy). A
--                                structural, harder-to-game signal: no separate/larger
--                                publisher backing the title. Chosen over an arbitrary
--                                "publisher released <=N titles" cutoff because it is
--                                already a clean binary in the data with no threshold
--                                to justify, and it directly targets what "indie" is
--                                usually meant to distinguish -- self-funded, not
--                                published through a larger house -- rather than merely
--                                a genre-tag aesthetic. Narrows is_indie=true from 67.6%
--                                of the catalogue to 36.8% (44,920/122,191) -- still
--                                broad in absolute terms (Steam's whole catalogue skews
--                                indie) but now a real, structurally-distinct segment,
--                                not a majority-admitting label. A small-publisher-
--                                title-count alternative (publisher has <=5 titles OR
--                                self-published) was tested and gives a similar-sized,
--                                slightly broader pool (541 vs 406 within the full
--                                screen, see 20_indie_scoring.md) -- reported as a
--                                sensitivity check, not adopted, to avoid an arbitrary
--                                numeric cutoff where a clean binary already exists.
--
-- CHANGE 2 (drop Xbox console requirement) — has_controller_support gate REMOVED.
--   It was added at Stage 12/16 (RT-11) specifically as a Steam-PC-to-Xbox-CONSOLE
--   platform-fit proxy (console certification / control-scheme risk). Game Pass on PC
--   has no such requirement -- keyboard/mouse-only titles are fully playable. Tested
--   three treatments (20_indie_scoring.md): (1) keep as hard gate, (2) drop entirely,
--   (3) demote to a scored feature. (2) and (3) turn out to be the SAME outcome here,
--   because the existing Fit model (artifacts/12_model_v2_fit.json, unchanged, reused
--   verbatim per Change 3) already includes has_controller_i as one of its Ridge
--   features (coefficient +0.0387, its single strongest positive coefficient) -- so
--   dropping the hard gate automatically demotes controller support to a 10%-weighted
--   scored input rather than eliminating its influence altogether. Chose (2)/(3):
--   dropped the hard gate. Admits 165 titles that could not pass v3's screen (Five
--   Nights at Freddy's 2/4, Fran Bow, Pony Island, There Is No Game: Wrong Dimension,
--   Finding Paradise, ...) at a real but non-fatal cost (metacritic presence among the
--   newly-admitted no-controller-support titles is 25.5% vs 40.7% among the
--   controller-supported subset of the same indie pool -- has_controller_i's positive
--   Fit coefficient is picking up a genuine, not spurious, signal, which is exactly why
--   it stays IN the model as a 10%-weighted feature rather than being dropped too).
--
-- CHANGE 3 (carried forward, unchanged, then re-tested against the new population,
--   per explicit instruction not to carry a threshold over just because it was there):
--   review_total >= 4,000  -- re-derived within the indie+self-published population
--                              (sql/20_indie_threshold_sensitivity.sql): the clean
--                              metacritic-presence elbow that justified 4,000 in the
--                              general population does NOT cleanly reproduce here (the
--                              curve is flat-to-noisy across 2,000-5,000: 33.4% / 35.4%
--                              / 34.5% / 34.2%, likely because indie metacritic
--                              coverage is bottlenecked by press attention rather than
--                              community size). No alternative floor clearly dominates
--                              4,000 in this range, so it is KEPT -- re-tested, not
--                              defaulted.
--   owners_mid <= 750,000  -- re-derived (same sql file): still excludes 173 of 579
--                              indie titles that clear every other screen (29.9%), and
--                              relaxing it keeps buying metacritic density (34.5% ->
--                              37.0% -> 38.8% at 1.5M / 3.5M) at the direct cost of the
--                              "not already widely owned" test -- the same trade-off
--                              that justified 750,000 originally still applies. KEPT.
--                              Still bucket-equivalent to <=1,499,999 (only 6 distinct
--                              owners_mid values remain in this pool).
--   review_positive_ratio >= 0.70, monetisation_model='paid' AND price_usd>0, no adult
--   tag -- unchanged, no indie-specific reason found to revisit any of these.

WITH adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
)
SELECT
    f.app_id, f.name, f.developer, f.publisher,
    f.review_total, f.review_positive_ratio, f.review_score_bucket,
    f.owners_range, f.owners_mid,
    f.price_usd, f.monetisation_model,
    f.metacritic_score,
    f.is_indie, f.is_self_published,
    f.has_singleplayer, f.has_multiplayer, f.has_coop, f.has_controller_support, f.has_vr,
    f.n_tags, f.release_date, f.release_year,
    f.genres, f.tags
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
LEFT JOIN adult_tagged a USING (app_id)
WHERE f.is_demo = false
  AND f.app_type = 'game'
  AND f.monetisation_model = 'paid'
  AND f.review_total >= 4000
  AND f.review_positive_ratio >= 0.70
  AND f.owners_mid <= 750000
  AND f.price_usd > 0
  AND f.is_indie = true
  AND f.is_self_published = true
  AND a.app_id IS NULL
ORDER BY f.app_id;
