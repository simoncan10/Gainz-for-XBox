-- Stage 10 (scoring) — the candidate eligibility screen.
--
-- Every threshold here is justified in artifacts/10_scoring.md and sensitivity-tested in
-- artifacts/10_model.json ("threshold_sensitivity"). Summary of each:
--
--  is_demo = false            -- demos are not licensable catalogue additions.
--  app_type = 'game'
--  monetisation_model = 'paid'  -- price_usd is known AND the title is not already free.
--                                 A free-to-play title gives Game Pass no exclusivity value
--                                 (anyone can already play it for $0), so it cannot pass the
--                                 "not already available to everyone" test regardless of
--                                 owners; and price_usd (the cost proxy) does not exist for
--                                 free titles.
--  review_total >= 50         -- Valve's own review-score algorithm requires 50 reviews
--                                 before a title gets a nuanced label (Mostly/Very/
--                                 Overwhelmingly Positive vs. plain binary Positive/Negative
--                                 below that; <10 gets no label at all). Measured directly
--                                 from review_score_bucket boundaries in this dataset
--                                 (sql/09_review_bucket_check.sql). This is the "Proven"
--                                 screen: below 50, a positive rating could plausibly be a
--                                 handful of friends-and-family reviews.
--  review_positive_ratio >= 0.70 -- Valve's own published boundary for "Mostly Positive" or
--                                 better, confirmed empirically against review_score_bucket
--                                 in this dataset (Mixed tops out at 0.700, Mostly Positive
--                                 starts at 0.700). Below this the title is "Mixed" reception
--                                 at best — not a reception a subscription platform should
--                                 be paying to feature.
--  owners_mid <= 750,000      -- "Not already widely owned." Empirically, this dataset's
--                                 owners_mid >= 1,000,000 bucket is where already-ubiquitous
--                                 franchise names cluster (Starfield, Baldur's Gate 3, Elden
--                                 Ring, Persona 5 Royal, Assassin's Creed Origins — see
--                                 sql/12b_ownership_ceiling_spotcheck.sql) — titles Xbox
--                                 either already publishes or the market has already reached
--                                 at scale. 750,000 keeps the top of the 500k-1M bucket
--                                 (still recognizable, still far from saturated) while
--                                 excluding the 1M+ tier. Sensitivity at 200k/350k/1M/1.5M/
--                                 3.5M is reported in 10_model.json; the eligible-pool size
--                                 is not sensitive to this choice (18,172-19,732 across the
--                                 whole tested range) because the review-count and quality
--                                 screens already do most of the filtering.
--  price_usd > 0               -- 4,057 rows carry monetisation_model='paid' (is_free=false)
--                                 with price_usd=0 (e.g. app_id 925100, "The Elder Scrolls
--                                 Online - Elsweyr" — an expansion whose steamspy price field
--                                 is a stale/regional 0, not a real free listing; caught by
--                                 spot-checking the first uncorrected candidate run). Since
--                                 price_usd is the cost-proxy input to the "cheap" score and
--                                 to the base-game-vs-DLC sanity of the list, a 0 here is a
--                                 data defect, not a signal, and is excluded rather than
--                                 scored as "free to license."
--  no Sexual Content / Nudity / Hentai tag -- Microsoft Store / Xbox content policy
--                                 restricts explicit sexual content far more tightly than
--                                 Steam's storefront does; this excludes 2,836 of the
--                                 remaining pool. This is a platform-fit screen, not a
--                                 taste judgment: verified during construction that several
--                                 of these titles were otherwise topping the composite score
--                                 on review volume and price alone (a handful of joke/shock
--                                 titles with cheap prices and meme-driven positive review
--                                 counts) — a board recommendation containing them would
--                                 fail on its face regardless of the metrics behind it.
--
-- This produces the ELIGIBLE POOL, not the final qualifying list. The composite score
-- (12_score_candidates.py) and its own threshold decide final membership.

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
    f.is_indie, f.is_self_published,
    f.has_singleplayer, f.has_multiplayer, f.has_coop, f.has_controller_support, f.has_vr,
    f.n_tags, f.release_date, f.release_year,
    f.genres, f.tags
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
LEFT JOIN adult_tagged a USING (app_id)
WHERE f.is_demo = false
  AND f.app_type = 'game'
  AND f.monetisation_model = 'paid'
  AND f.review_total >= 50
  AND f.review_positive_ratio >= 0.70
  AND f.owners_mid <= 750000
  AND f.price_usd > 0
  AND a.app_id IS NULL;
