# Gainz-for-XBox

**The question:** which specific games should Xbox add to the Game Pass portfolio?

**The method:** score every game in a ~140,000-app Steam snapshot against a statistical
profile of what actually wins in this catalogue, screen the survivors for titles that are
proven but *not already owned* by subscribers, then verify availability externally — one
title at a time, with a source and a date.

**The answer** is always a ranked list of named titles with app_ids. An output that
describes what should be *considered* has failed the brief. The full statement of that
brief is in [`docs/GOAL_STATEMENT.md`](docs/GOAL_STATEMENT.md).

---

## Where to start reading

| If you want… | Read this |
|---|---|
| The short version of what was built and what it found | [`docs/EXECUTIVE_RECAP.md`](docs/EXECUTIVE_RECAP.md) |
| The brief every agent was held to | [`docs/GOAL_STATEMENT.md`](docs/GOAL_STATEMENT.md) |
| The final recommendation (newest run) | [`reports/run_03_pc_indie_slate_2026-08-23/deliverables/onepager.md`](reports/run_03_pc_indie_slate_2026-08-23/deliverables/) |
| How the score was built, and what it cannot do | [`reports/methodology/`](reports/methodology/) |
| Proof that the analysis was attacked before it was believed | `reports/run_01_open_brief_2026-08-22/DECISIONS.md` and `RUN_LOG.md` |
| The reproducible code path | [Pipeline](#pipeline-run-in-this-order), below |

---

## Folder structure

```
Gainz-for-XBox/
│
├── README.md                  ← you are here: what everything is and how to run it
├── .gitignore
│
├── docs/                      Project-level documents. Read these first.
│   ├── GOAL_STATEMENT.md      The brief. Pasted unchanged at the top of every agent run:
│   │                          required output shape, what is out of scope, what counts
│   │                          as a failure, and the sourcing rules every number obeys.
│   └── EXECUTIVE_RECAP.md     One-page account of the multi-agent architecture, the two
│                              runs it produced, and the findings that changed the project.
│
├── src/                       All reproducible analysis code. Run from the repo root.
│   ├── extract_owners_price.py    step 1 — owners + price buckets
│   ├── extract_reviews.py         step 2 — review score + review-count buckets
│   ├── pipeline.py                step 3 — builds the master dataset (runs 1 & 2 itself)
│   ├── build_top50_datasheet.py   step 4 — the "winning profile" and the scored universe
│   ├── find_underdogs.py          step 5 — the underdog shortlist
│   ├── profile_bigfiles.py        optional — profiles the two ~500 MB raw files
│   │                              without loading them into memory
│   └── legacy/                    Superseded scripts, kept for the record. NOT part of
│       ├── README.md              the pipeline; their inputs no longer exist. See the
│       ├── combine_datasets.py    note in that folder before running anything here.
│       ├── find_indie.py
│       ├── sample_indie_games.py
│       └── enrich_indie_sample.py
│
├── data/                      GIT-IGNORED except data/reference/*.csv — see "Data" below.
│   ├── raw/
│   │   ├── super raw/         The untouched Steam snapshot (~Dec 2024). Source of truth.
│   │   └── _unverified/       Three loose CSVs no current script reads. Quarantined
│   │                          pending a decision — see "Loose ends", below.
│   ├── reference/             Hand-curated research. NOT regenerable. Committed to git.
│   └── processed/             Everything a script in src/ writes. Safe to delete and
│                              rebuild; nothing here is a source of truth.
│
├── reports/                   One folder per agent run, plus supporting material.
│   ├── run_01_open_brief_2026-08-22/       Run A — see "The three runs"
│   ├── run_02_xbox_portfolio_2026-08-22/   Run B — the Xbox console portfolio
│   ├── run_03_pc_indie_slate_2026-08-23/   The PC indie slate (newest)
│   ├── methodology/           The "how the score was built" slide and its speaker script
│   └── logs/                  Prompt-by-prompt session logs (2026-08-20, 2026-08-21)
│
└── .claude/                   Local Claude Code settings. Not part of the analysis.
```

### The one rule that keeps it clean

Every folder answers a single question, and nothing lives in two of them:

- **`docs/`** — what we were trying to do.
- **`src/`** — code that turns `data/raw/` into `data/processed/`. Deterministic, rerunnable.
- **`data/`** — inputs and derived tables. Never edited by hand except `data/reference/`.
- **`reports/`** — the record of a *run*: what an agent network decided, on a given day,
  from a given state of the data. Immutable once written.

If a new file does not obviously belong to one of those four, that is a sign the structure
needs a new folder rather than that the file needs a home in the nearest one.

### Naming conventions

- Run folders: `run_NN_<short-theme>_<YYYY-MM-DD>/`. The number gives reading order, the
  date gives provenance.
- Inside a run: `artifacts/` (numbered intermediate outputs, in stage order), `sql/`
  (every query that produced a number — numbered to match), `scripts/` (the code that built
  the artifacts, numbered to match — run 01 keeps its two equivalents inside `sql/` instead),
  `deliverables/` (what a human actually receives).
- Scripts in `src/` are named for what they *produce*, not for what they read.
- Nothing is zipped inside the repo. An archive hides its contents from `grep`, from
  `git diff`, and from anyone reading the project.

---

## Data

`data/` is git-ignored, with one deliberate exception. Cloning this repo therefore means
re-running the pipeline to regenerate `data/processed/`, and obtaining the raw snapshot
separately.

| Path | What it is | Regenerable? |
|---|---|---|
| `data/raw/super raw/` | Steam snapshot, ~Dec 2024, from SteamSpy + Steam reviews. Eight files: `games.csv`, `genres.csv`, `tags.csv`, `categories.csv`, `steamspy_insights.csv`, `reviews.csv`, `descriptions.csv`, `promotional.csv`. ~140,000 apps, ~1.1 GB. | No — external source |
| `data/reference/web_indie_2025_2026.csv` | 30 Steam indie breakouts from 2025–2026, newer than the snapshot. Hand-researched from gaming press, one source URL per row. | **No — and it is committed to git for exactly that reason.** Losing it loses the research behind it. |
| `data/processed/` | Every table a script in `src/` writes. | Yes — all of it |

### Known raw-data hazards

These are not trivia. Each one silently changed an answer at some point in this project.

1. **`games.csv` embeds JSON with backslash-escaped quotes** (`\"`) in `price_overview`,
   not standard doubled CSV quotes. A plain `csv.DictReader` misaligns the `name`/`type`
   columns and drops well-known indie hits from the "game" filter. Any Python reader must
   pass `escapechar="\\"`. DuckDB's sniffer handles it correctly on its own.
   *The scale of this was initially estimated at ~13% of rows; a later DuckDB-based check
   measured **54.5%**.*
2. **Prices in `games.csv` are 99.1% EUR, not USD.** Use the SteamSpy price column for
   dollar figures. Any price finding sourced from `games.csv` and stated in dollars is
   wrong by definition — see the correction note under step 4 below.
3. **All four playtime columns are constant zero.** There is no engagement, retention or
   session-length signal anywhere in this dataset. No claim about any of those is
   supportable, and none is made.
4. **Owners are bucketed SteamSpy estimates, not measured sales.** Inside one bucket,
   ownership carries no information at all.
5. **`release_date` is right-truncated** — nothing after Oct 2024 — and 20.4% missing.
6. **Category values are not uniformly English**, which silently breaks co-op flags on
   titles including Counter-Strike 2 and Dota 2. Treat flag counts as a floor.

---

## Pipeline (run in this order)

Run everything from the repo root; the scripts resolve their own paths.

```bash
python src/pipeline.py                # steps 1-3
python src/build_top50_datasheet.py   # step 4
python src/find_underdogs.py          # step 5
```

| # | Script | Reads | Writes (all into `data/processed/`) |
|---|---|---|---|
| 1 | `src/extract_owners_price.py` | `steamspy_insights.csv` | `owners_price_buckets.csv` |
| 2 | `src/extract_reviews.py` | `reviews.csv` | `review_amount_buckets.csv` |
| 3 | `src/pipeline.py` *(runs 1 and 2 itself)* | the above, plus `genres.csv` / `tags.csv` direct from raw | `pipeline_dataset.csv` — one row per app: `app_id, genres, price_cents, review_score, total, owners_range,` + one 0/1 column per tag |
| 4 | `src/build_top50_datasheet.py` | `games.csv`, `genres.csv`, `tags.csv`, steps 1–2, `data/reference/web_indie_2025_2026.csv` | `top50_indie_reference.csv`, `top50_match_profile.csv`, `indie_candidates_scored.csv` |
| 5 | `src/find_underdogs.py` | `indie_candidates_scored.csv` | `underdog_candidates.csv` |

Optional, and not part of the chain:

```bash
python src/profile_bigfiles.py   # streams descriptions.csv + promotional.csv (~1 GB),
                                 # writes a small profile into data/processed/
```

### Step 4 — what makes a winner

`build_top50_datasheet.py` blends two evidence sources into one top 50
(`top50_indie_reference.csv`): 30 web-researched 2025–26 breakouts too new for the
snapshot, and the top 20 apps *in the snapshot itself* by a composite score
(`0.35·z(log owners) + 0.35·z(log reviews) + 0.30·z(review_score)`, among indie games with
≥5,000 reviews). Non-game utilities such as Wallpaper Engine are excluded by hand, with the
reason written into the script.

From that it builds a **winning profile** (`top50_match_profile.csv`): a naive-Bayes lift
table comparing a 300-game winner cohort (indie, review_score ≥8, ≥20,000 reviews,
≥1,000,000 owners) against the other 85,332 indie games, per tag / genre / price band.
Minimum support 5 winners and 50 total, Laplace smoothing 0.02 — 216 attributes survive.

Every indie game is then scored against that profile
(`indie_candidates_scored.csv`, 85,632 rows) with a full naive-Bayes log-likelihood ratio.
Absent attributes count, so a game is not rewarded merely for carrying more Steam tags.

**Validation:** `profile_fit_score` separates the winner cohort from the rest at
**AUC 0.939 in-sample and 0.950 on a held-out 30%** of the cohort (seed 7) — the profile
generalises rather than memorises.

**What it found:**

- **Co-op is the strongest signal** — Co-op 5.5× lift, Online Co-Op 5.1×, Multiplayer 4.5×.
- **Systems depth** — Moddable 4.5×, Sandbox 4.1×, Open World 3.4×, Open World Survival
  Craft 3.4×, Building 2.9×, Crafting 2.5×.
- **Negative signals** — Stylized 0.31×, Combat 0.32×, 3D 0.47×, Minimalist 0.50×,
  Casual 0.52×, Early Access 0.68×.
- **Price:** the €20–29.99 band shows the strongest lift (5.8×); free and sub-€5 badly
  under-perform (0.40–0.41×).
  > ⚠️ **Correction.** These price figures are **euros**, not dollars — they come from
  > `games.csv`, which is 99.1% EUR. An earlier version of this README labelled them with
  > `$`. The dollar-denominated equivalent has not been recomputed; if a price claim is
  > needed in USD, rebuild it from the SteamSpy price column.

  > ⚠️ **Withdrawn.** An earlier version cited "Meccha Chameleon, 15M copies in under a
  > month." That figure is unsupported; the highest credible sourcing is ~10M at 16 days.
  > It is recorded here rather than deleted, because a withdrawn number that vanishes
  > quietly is a number that comes back.

### Step 5 — the underdog shortlist

The goal is not "games that match the profile" — the winner cohort matches it perfectly and
is already a hit. The goal is games that match the winning DNA **but have not broken out and
are not already on Game Pass**: things Xbox could add that subscribers do not already own.

Filters applied to `indie_candidates_scored.csv`:

- `in_winner_cohort == 0` — already broke out, so by definition not an underdog
- `in_top50_reference == 0` — excludes the reference set itself
- `evidence_tier == "high"` (≥5,000 reviews) — enough signal to trust the review score
- `review_score >= 6` — excludes games that fit on paper but were poorly received
- ranked by `profile_fit_score` descending

**Game Pass availability is not in any dataset here.** It is not derivable from
`data/raw/`, so leading candidates were checked individually by web search (dated
2026-08-21) and recorded in the script as `GAMEPASS_STATUS_OVERRIDES`, each with a source
note. Titles confirmed on Game Pass stay **visible** in the output rather than being
silently dropped, and are excluded only from the final pick.

Output: `data/processed/underdog_candidates.csv` — the full ranked pool (~1,034 games), not
just the top few, so the next-best option is visible if a pick turns out to be unavailable.

---

## The three runs

`reports/` holds one folder per agent-network run. They are not drafts of each other; each
answers a different framing of the question, and all three are kept because the *difference*
between them is a finding.

| Folder | Date | Brief | Outcome |
|---|---|---|---|
| `run_01_open_brief_2026-08-22/` | 22 Aug, midday | Open: "what should the board invest in" — with no requirement that the answer contain game names | Produced a rigorous answer to the wrong question. Under adversarial pressure the strategist retreated to *"spend nothing, run an audit first."* **Discarded as a deliverable, retained as a finding** — it is the reason `docs/GOAL_STATEMENT.md` exists. `KNOWN_FIXES.md` lists four wording fixes never applied. |
| `run_02_xbox_portfolio_2026-08-22/` | 22 Aug, late | Corrected by `GOAL_STATEMENT.md`: named titles with app_ids, a *justified threshold* instead of an arbitrary count, picks sourced only from the dataset | **17 picks + a 7-title watchlist**, Xbox console. Funnel: 122,191 → 802 eligible → 275 qualifying → 30 verified → 17. This is the run `docs/EXECUTIVE_RECAP.md` describes. |
| `run_03_pc_indie_slate_2026-08-23/` | 23 Aug | Same brief, narrowed to a **PC Game Pass indie slate** | **21 picks** in three tiers by deal structure. Retail sum $417.69, 50.28 titles per $1,000. Post-dates `EXECUTIVE_RECAP.md`, so it is **not** covered there. |

Each run folder holds the same things:

- **`artifacts/`** — numbered stage outputs (`01_profile`, `02_cleaning_report`,
  `03_findings`, … `07_final_check`). The audit trail.
- **`sql/`** — every query that produced a number, numbered to match. A figure computed in
  a throwaway command exists nowhere and is therefore unsourced, even when correct.
- **`deliverables/`** — the deck, the spoken pitch script, the Q&A sheet, the one-pager.
- **`scripts/`** — the code that built the artifacts, numbered to match. Run 01's equivalent
  lives inside `sql/` instead, as `_run_sql.py` / `_run_validate.py`, rather than a separate
  folder.
- **`RUN_LOG.md`** — the prompt-by-prompt session record.
- **`DECISIONS.md`** — what was decided, what the alternatives were, and the measured effect
  of each choice.

Run 01 additionally carries `KNOWN_FIXES.md` — four wording fixes drafted for that run's
deliverables but never applied, since the deliverables themselves were discarded (see the
table above).

### Why the runs are worth reading

The architecture's whole claim is that an adversarial critic catches things a single pass
does not. The logs record it doing so:

- The first scoring model ranked *Chushpan Simulator* and *BBQ Simulator: The Squad* at the
  top while Hi-Fi RUSH (Metacritic 90) sat at rank 8,439 of 15,921. The critic diagnosed it
  by **re-running the code rather than reading it**: no `ORDER BY`, so the train/test split
  was non-deterministic — three re-runs gave r = 0.5495 / 0.5599 / 0.5506, and the published
  0.564 appeared in none of them.
- The replacement model's Headroom pillar turned out to be redundant:
  Spearman(recognition, headroom) = **1.0000 within every ownership bucket**. Fit had
  in-population R² of −1.34 — worse than predicting the mean — and was cut to a 10%
  tiebreaker.
- The portfolio was cut from 24 picks to 17 + watchlist, because 7 rested on unverified
  Xbox availability while being presented with the same confidence as verified ones.
- A proposed diversity remedy was **tested and withdrawn** because it did not work — one
  named "co-op alternate" had no co-op flag at all.

Two agents were also wrong and corrected by another agent; both occasions are in the log.

---

## What this project does not claim

Stated here rather than buried, because a professor and a board will both ask.

- **No engagement or retention claim**, anywhere. The playtime columns are zero.
- **Owners are estimates in buckets**, not sales.
- **Review counts are self-selected** and vary by genre, price and audience size.
- **The data is Steam PC; the console recommendation is an extrapolation.** Console ARPPU
  is roughly 48% higher and the genre mix differs.
- **Game Pass availability is external to the dataset** and was checked per title, with a
  source and a date, in August 2026. It goes stale.
- **The run-02 scoring model is honestly "Recognition, banded by a three-level ownership
  step"** — not a multi-pillar blend. Within an ownership tier, the ranking is
  most-reviewed-first. That is a SteamSpy granularity limit; it cannot be fixed, only
  disclosed.
- **Two of eight raw files** (`descriptions.csv`, `promotional.csv`, ~1 GB combined)
  exceeded the transfer limit and were not analysed in run 01. Recorded as a scope limit.
- **Concentration is real and accepted** — run 02's picks are 17.6% Action against a
  qualifying list at 53.8%. The remedy was tested and withdrawn rather than faked.

---

## Loose ends

Honest list of what is unresolved, so nobody has to discover it by reading the folder.

1. **`data/raw/_unverified/`** holds `categories.csv`, `genres.csv` and `reviews.csv` —
   loose files that sit outside `super raw/` and are read by **no current script**. They
   are slightly larger than their `super raw/` namesakes, which suggests they are
   translated or cleaned intermediates from a step whose script (`clean_genres.py`) no
   longer exists. They are quarantined rather than deleted until that is confirmed.
2. **`src/legacy/`** — `find_indie.py`, `combine_datasets.py`, `sample_indie_games.py` and
   `enrich_indie_sample.py` depend on processed files (`tags_one_row_per_app.csv`,
   `genres_onehot.csv`, `indie_games.csv`, `reviews_cleaned.csv`, `games_clean.csv`) that
   no longer exist. Their *outputs* survive in `data/processed/`. Kept for provenance;
   not runnable as-is.
3. **`GOAL_STATEMENT.md` carries an open question** — whether
   `data/reference/web_indie_2025_2026.csv`, being web-sourced in origin, may be used to
   define what "winning" looks like. It never supplies picks either way. The decision
   should be written into that file before the next run.
4. **The folder `data/raw/super raw/` contains a space.** Renaming it to `super_raw`
   would be cleaner, but the path is hardcoded in five scripts *and* in the archived
   `.sql` files of run 01 — which are records of what was run, and should not be edited
   after the fact. Left as-is deliberately.
