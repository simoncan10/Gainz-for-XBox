-- Q14: Competitive density weighted by recency. All-time titles-per-audience-unit vs the
-- same ratio restricted to the 2021-2023 cohort (last 3 *complete* release years -- 2024 is
-- excluded because it is right-truncated at 2024-10-28, and pre-2021 is excluded so a genre
-- saturated years ago doesn't look artificially open based on stale supply counts).
-- Caveat: recent-cohort owners_mid is itself right-censored (less time to accumulate owners
-- than older cohorts), so 'recent audience' here understates true eventual audience for
-- 2021-2023 titles -- treat the recent ratio as a lower bound on how open a genre now looks,
-- not an exact figure.
WITH base AS (
    SELECT app_id, owners_mid, release_year
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/fact_games.parquet')
    WHERE is_demo = false AND app_type = 'game' AND release_year IS NOT NULL
),
genre_titles AS (
    SELECT gl.genre, b.app_id, b.owners_mid, b.release_year
    FROM read_parquet('/home/claude/run_2026-08-22/parquet/genres_long.parquet') gl
    JOIN base b USING (app_id)
),
alltime AS (
    SELECT genre, count(*) AS n_alltime, sum(owners_mid) AS audience_alltime
    FROM genre_titles GROUP BY genre
),
recent AS (
    SELECT genre, count(*) AS n_recent, sum(owners_mid) AS audience_recent
    FROM genre_titles WHERE release_year BETWEEN 2021 AND 2023
    GROUP BY genre
)
SELECT a.genre, a.n_alltime, r.n_recent,
       round(a.audience_alltime / a.n_alltime, 0) AS alltime_audience_per_title,
       round(r.audience_recent / NULLIF(r.n_recent,0), 0) AS recent_audience_per_title,
       round(100.0 * r.n_recent / a.n_alltime, 1) AS pct_of_alltime_supply_is_recent
FROM alltime a
JOIN recent r USING (genre)
WHERE a.n_alltime >= 100 AND r.n_recent >= 30
ORDER BY recent_audience_per_title DESC;
