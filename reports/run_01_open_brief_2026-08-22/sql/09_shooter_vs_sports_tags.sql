-- Q09: Direct catalogue-level check of Stage 3's context claim that Steam's PC population
-- skews toward shooters while Xbox's console population skews toward sports. Tag counts are
-- not mutually exclusive per app (a title can carry both a Shooter and a Sports tag).
SELECT tag, count(*) AS n
FROM read_parquet('/home/claude/run_2026-08-22/parquet/tags_long.parquet')
WHERE tag ILIKE '%shoot%' OR tag ILIKE '%sport%' OR tag ILIKE '%fps%'
GROUP BY 1
ORDER BY n DESC;
