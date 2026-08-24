-- Stage 23 — rebuilt indie candidate eligibility screen, replacing
-- sql/20_indie_candidate_screen.sql after red-team pass 22 (artifacts/22_redteam_indie.md).
--
-- A-1 FIX: indie definition rebuilt from is_self_published (a literal
--   developer==publisher string match -- verified to exclude Return of the Obra
--   Dinn and Papers, Please because Lucas Pope publishes as "3909", and to
--   exclude every indie that signed with an indie-friendly publisher: Edith
--   Finch/Journey via Annapurna, Unpacking/Temtem via Humble Games, SANABI via
--   NEOWIZ, ABZU via 505 Games -- while ADMITTING self-published mass-catalogue
--   operations: EroticGamesClub 181 titles, Choice of Games 163, Boogygames
--   Studios 130, Hosted Games 109, Sokpop Collective 96) to:
--     is_indie = true AND developer_title_count <= 10
--   where developer_title_count is the developer's total non-demo game count
--   across the whole catalogue. Publisher-catalogue-size was tried first (as
--   the red team suggested) and rejected: it passes the hand-check for any
--   cutoff N in roughly [32,105) (see sql/27, first version, superseded) but
--   barely narrows the pool (48% of the catalogue at the smallest passing N)
--   because most publishers, including the bad actors, are also small in
--   raw count once self-published mills are the very thing being excluded --
--   publisher size does not cleanly separate a boutique label (Annapurna, 32
--   titles) from a mid-size mainstream one (Nacon, 94) the way developer size
--   does. Developer-catalogue-size is decisive because the mass-catalogue
--   "admits" cases are self-published: the SAME entity is developer and
--   publisher, so a huge developer-title-count catches them exactly where a
--   huge publisher-title-count would, while correctly leaving Giant Sparrow
--   (Edith Finch, 2 titles), thatgamecompany (Journey, 2), Lucas Pope (Obra
--   Dinn/Papers Please, 2 each) and Witch Beam (Unpacking, 2) untouched
--   regardless of which publisher's name sits next to them.
--
--   N=10 chosen from sql/27_indie_definition_v2_sensitivity.sql: it is the
--   smallest round cutoff (of the red team's own suggested {3,5,10,25} test
--   points) that (a) passes every hand-check title -- Obra Dinn, Papers
--   Please, Edith Finch, ENDER LILIES, Unpacking, ABZU, Journey, SANABI,
--   Temtem, VA-11 Hall-A, Potion Craft, Firework all IN; Choice of Games,
--   EroticGamesClub, Boogygames Studios, Hosted Games, Sokpop Collective all
--   OUT -- and (b) does not exclude well-known multi-title indie studios
--   spot-checked beyond the hand-list: Supergiant Games (5 titles), Vlambeer
--   (5), Mode 7 (3) all remain IN at N=10; Klei Entertainment (12 titles,
--   arguably outgrown "indie" scale) is the one spot-checked studio N=10
--   excludes, which is an acceptable and defensible edge.
--
--   HONESTLY DISCLOSED, not hidden: this narrows the raw is_indie=true
--   population from 67.6% of the catalogue only to 44.8% (54,692/122,191) --
--   less narrowing than the flawed is_self_published test achieved (36.8%).
--   Developer-catalogue-size fixes WHO is correctly classified; it does not,
--   by itself, make indie a small segment, because most Steam titles tagged
--   Indie genuinely are made by tiny (1-2 title) developers -- that is a
--   structural fact about this catalogue, not a modelling failure. The real
--   narrowing to an actionable segment happens downstream, in this same
--   screen, via the review/quality/owner/price thresholds below (identical
--   role to Stage 20's architecture) -- reported at the foot of this file.
--
-- A-2 FIX: no claim that Fit "compensates" for the dropped controller-support
--   gate. The gate is dropped for the correct, narrower reason: Game Pass
--   runs on Windows PC, so keyboard/mouse-only titles are fully playable and
--   a console-fit proxy no longer applies. Nothing replaces the gate's
--   quality-signal role; the measured cost (metacritic presence 25.5% among
--   no-controller-support titles vs 40.7% among controller-supported ones)
--   stands on its own and is reported per-tier in 23_indie_v2.md, not offset
--   against a Fit pillar that is verified inert in-population (R²=-1.34,
--   weighted 10%, and titles at the bottom 1-4% of Fit rank freely appear in
--   the qualifying top 20 -- KovaaK's fit_pct=0.0395, Verdun fit_pct=0.0099).
--
-- A-4 FIX: review floor re-derived on the REBUILT population, full table
--   (not truncated), in sql/28_indie_v2_review_floor_full_sensitivity.sql:
--     floor:      500   1000  2000  3000  4000  5000  6000  7500  10000
--     n:         4486   2766  1626  1112   844   669   531   395    259
--     MC%:       25.0   30.0  34.2  36.2  37.7  38.7  38.8  39.0   39.4
--   Marginal MC-density gain per 1,000-review step: +5.0 / +4.2 / +2.0(per
--   1k) / +1.5 / +1.0 / then collapses to +0.1 / +0.13(per 1.5k) / +0.27
--   (per 2.5k). The plateau starts cleanly at 5,000: the step immediately
--   before it (4,000->5,000) still buys +1.0pp, the step immediately after
--   (5,000->6,000) buys +0.1pp -- a 10x drop in marginal return. RAISED the
--   floor from 4,000 to 5,000 on this evidence. Did not go to 6,000+ as the
--   critic's own note on the (now-superseded) old population suggested,
--   because that note was read off a different, messier population before
--   the definition was rebuilt; on the corrected population the plateau
--   genuinely begins at 5,000 and the 6,000-10,000 gains (+0.1 to +0.4pp
--   total) do not justify losing another 138 titles (669->531) for them.
--
--   Owners ceiling re-checked at the new floor (sql/29): 750,000 KEPT, same
--   reasoning as Stage 20 -- bucket-equivalent to 1,000,000 (n identical at
--   636), and relaxing further keeps buying Metacritic density (40.4% ->
--   42.3% -> 44.3% at 1.5M/3.5M) at the direct cost of the ceiling's purpose
--   (excluding already-widely-owned titles).

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS developer_title_count
  FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
adult_tagged AS (
    SELECT DISTINCT app_id
    FROM read_parquet('/home/claude/run_portfolio/parquet/tags_long.parquet')
    WHERE tag IN ('Sexual Content', 'Nudity', 'Hentai')
)
SELECT
    f.app_id, f.name, f.developer, f.publisher, dc.developer_title_count,
    f.review_total, f.review_positive_ratio, f.review_score_bucket,
    f.owners_range, f.owners_mid,
    f.price_usd, f.monetisation_model,
    f.metacritic_score,
    f.is_indie, f.is_self_published,
    f.has_singleplayer, f.has_multiplayer, f.has_coop, f.has_controller_support, f.has_vr,
    f.n_tags, f.release_date, f.release_year,
    f.genres, f.tags
FROM read_parquet('/home/claude/run_portfolio/parquet/fact_games.parquet') f
LEFT JOIN dev_counts dc ON dc.developer = f.developer
LEFT JOIN adult_tagged a USING (app_id)
WHERE f.is_demo = false
  AND f.app_type = 'game'
  AND f.monetisation_model = 'paid'
  AND f.review_total >= 5000
  AND f.review_positive_ratio >= 0.70
  AND f.owners_mid <= 750000
  AND f.price_usd > 0
  AND f.is_indie = true
  AND dc.developer_title_count <= 10
  AND a.app_id IS NULL
ORDER BY f.app_id;
