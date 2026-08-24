-- Stage 23 rebuild (per red-team A-1): the indie definition must split on SCALE
-- (how big is the publisher's catalogue) rather than on whether a publishing deal
-- exists at all (is_self_published, a literal developer==publisher string match).
--
-- Step 1: distribution of publisher catalogue size across the whole game catalogue,
-- so the cutoff is read off a real distribution rather than picked as a round number.
-- Publisher catalogue size = count of distinct app_ids (game, non-demo) carrying that
-- publisher string, computed over the FULL catalogue (not just is_indie=true titles),
-- because the whole point is to catch large "self-published" operations regardless of
-- whether their individual titles happen to carry the Indie genre tag.

WITH pub_counts AS (
  SELECT publisher, COUNT(*) AS n_titles_by_publisher
  FROM read_parquet('parquet/fact_games.parquet')
  WHERE is_demo = false
    AND app_type = 'game'
    AND publisher IS NOT NULL
    AND publisher <> ''
  GROUP BY publisher
)
SELECT
  n_titles_by_publisher,
  COUNT(*) AS n_publishers_at_this_size
FROM pub_counts
GROUP BY n_titles_by_publisher
ORDER BY n_titles_by_publisher
LIMIT 40;
