-- Stage 23 rebuild (A-1): sensitivity of the new indie definition.
--
-- First attempt (publisher catalogue size) was tried and is documented in
-- 20_indie_scoring.md's revision notes: it passes the hand-check for N in
-- roughly [32,105) but only narrows the raw is_indie=true pool from 67.6% of
-- the catalogue to ~48% at the smallest N that still passes the hand-check --
-- because the majority of publishers are one-off/self-publishing entities,
-- so almost the whole is_indie population survives any publisher-size cutoff
-- generous enough to keep Annapurna Interactive (32 titles, publishes Edith
-- Finch and Journey) in. Publisher size alone does not separate the segment
-- tightly enough. Reported for the record, not used.
--
-- Second attempt, adopted: DEVELOPER catalogue size. The red team's own
-- "admits" list (EroticGamesClub, Choice of Games, Boogygames, Hosted Games,
-- Sokpop) are self-published mills where the SAME entity is both developer
-- and publisher of record, so filtering on developer-title-count catches them
-- exactly as well as publisher-title-count -- but on the "excludes" side it
-- is decisive where publisher-size was not: Giant Sparrow (Edith Finch),
-- thatgamecompany (Journey), Lucas Pope (Obra Dinn / Papers Please), Witch
-- Beam (Unpacking), Crema (Temtem) each have a DEVELOPER title count of 1-2,
-- regardless of which publisher's name sits next to them. This lets the
-- definition track "is this a small independent studio" without depending on
-- whether a publishing deal happens to share a name string with the
-- developer.

WITH dev_counts AS (
  SELECT developer, COUNT(*) AS n_titles_by_developer
  FROM read_parquet('parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND developer IS NOT NULL AND developer <> ''
  GROUP BY developer
),
base AS (
  SELECT f.app_id, f.name, f.developer, f.is_indie, dc.n_titles_by_developer
  FROM read_parquet('parquet/fact_games.parquet') f
  LEFT JOIN dev_counts dc ON dc.developer = f.developer
  WHERE f.is_demo = false AND f.app_type = 'game'
),
total_catalogue AS (
  SELECT COUNT(*) AS n FROM read_parquet('parquet/fact_games.parquet')
  WHERE is_demo = false AND app_type = 'game' AND is_indie IS NOT NULL
)
SELECT
  cutoffs.n AS cutoff_n,
  COUNT(*) FILTER (WHERE base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n) AS pool_n,
  ROUND(100.0 * COUNT(*) FILTER (WHERE base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)
        / (SELECT n FROM total_catalogue), 1) AS pct_of_catalogue,
  BOOL_AND(base.name <> 'Return of the Obra Dinn' OR (base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS in_obra_dinn,
  BOOL_AND(base.name <> 'Papers, Please' OR (base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS in_papers_please,
  BOOL_AND(base.name <> 'What Remains of Edith Finch' OR (base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS in_edith_finch,
  BOOL_AND(base.name <> 'Journey' OR base.developer IS NULL OR (base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS in_journey,
  BOOL_AND(base.name <> 'Choice of Games' OR NOT(base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS out_choice_of_games,
  BOOL_AND(base.name <> 'EroticGamesClub' OR NOT(base.is_indie = true AND base.n_titles_by_developer <= cutoffs.n)) AS out_erotic_games_club
FROM base, (SELECT UNNEST([1,2,3,5,10,15,20,25,30,50,75,96]) AS n) AS cutoffs
GROUP BY cutoffs.n
ORDER BY cutoffs.n;
