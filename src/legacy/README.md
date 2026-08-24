# Legacy scripts

Superseded. **Not part of the pipeline** — see the pipeline table in the repo README.

Each of these ran at some point and its *output* survives in `data/processed/`, but its
*inputs* do not: `tags_one_row_per_app.csv`, `genres_onehot.csv`, `indie_games.csv`,
`reviews_cleaned.csv` and `games_clean.csv` were removed in an earlier cleanup, and the
script that produced the one-hot genres (`clean_genres.py`) no longer exists either.

They are kept because they document how the earlier phase of the project worked, and
because `find_indie.py` came from a classmate and is not ours to delete.

| Script | Superseded by | Missing inputs |
|---|---|---|
| `combine_datasets.py` | `src/pipeline.py` | `indie_games.csv` |
| `find_indie.py` | `src/pipeline.py` (Indie appears naturally as a genre/tag value) | `tags_one_row_per_app.csv`, `onehot/genres_onehot.csv` |
| `sample_indie_games.py` | — (the sample it drew is no longer used) | `indie_games.csv` |
| `enrich_indie_sample.py` | — | `reviews_cleaned.csv`, `games_clean.csv` |

Needs `pandas` and `openpyxl`, which the current pipeline does not.
