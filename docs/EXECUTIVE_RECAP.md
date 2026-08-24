# Executive recap — Gainz-for-XBox multi-agent run

**Date:** 22 August 2026 · **Question:** which games should Xbox add to the Game Pass portfolio?
**Answer:** 17 named titles plus a 7-title watchlist, selected from 122,191 by stated thresholds.

---

## 1. What was built

A seven-agent network (tier 3), installed as a Cowork plugin, `steam-board-intel`:

| Stage | Agent | Model | Role |
|---|---|---|---|
| 1 | data-profiler | Sonnet | Schemas, row counts, join coverage, hazards |
| 2 | data-engineer | Sonnet | Cleaning, normalisation, Parquet store |
| 3 | competitive-researcher | Sonnet | External context and availability verification |
| 4 | market-analyst | Sonnet | Scoring model, thresholds, ranked candidate list |
| 5 | investment-strategist | Opus | Portfolio assembly and tiering |
| 6 | red-team-critic | Opus | Adversarial verification |
| 7 | pitch-writer | Opus | Spoken pitch, deck, Q&A, one-pager |

It is a **network**, not a pipeline, because of two structural features: stages 2 and 3 run
**in parallel** (research has no data dependency) and reconverge at stage 5, and stages 5 and 6
form a **feedback loop** that iterates until the critic's verdicts clear.

Model tiering is deliberate: mechanical stages run on Sonnet, judgement stages on Opus.

## 2. What was run

**Run A — open brief.** Full seven stages, ~700K tokens. It produced a rigorous answer to the
wrong question, because the brief said "what should the board invest in" without specifying
that an answer must contain game names. Under adversarial pressure the strategist retreated to
"spend nothing, run an audit first." Discarded as a deliverable, retained as a finding.

**Run B — corrected brief.** A written `GOAL_STATEMENT.md` fixed the failure by specifying the
*shape* of a valid answer: named titles with app_ids, a justified threshold rather than an
arbitrary count, candidates sourced only from the dataset, and measurement-as-headline named
explicitly as a forbidden outcome. Run B reused Run A's validated Parquet store and re-ran
stages 3–7. This produced the delivered portfolio.

## 3. Data findings that changed the project

Established by stages 1 and 2 against 140,082 apps across six raw files:

- **All four playtime columns are constant zero.** There is no engagement or retention signal
  anywhere in the dataset — material, because Game Pass is an engagement business.
- **`games.csv` prices are 99.1% EUR, not USD.** Prior price findings in the project's own
  README were euro figures labelled as dollars. The steamspy USD column was used instead.
- **Backslash-escaped JSON misaligns 54.5% of rows** under a naive Python CSV reader — four
  times worse than the ~13% previously assumed. DuckDB's sniffer handles it correctly.
- **Category values are not uniformly English**, silently breaking co-op flags on titles
  including Counter-Strike 2 and Dota 2. Flags are treated as a floor, not an exact count.
- **`release_date` is right-truncated** (nothing after Oct 2024) and 20.4% missing.
- **A previously cited figure — "Meccha Chameleon, 15M copies in under a month" — is
  unsupported.** Highest credible sourcing is ~10M at 16 days.

## 4. What the adversarial loop caught

This is the substantive argument for the architecture, and the run log records all of it.

**Against the first scoring model — verdict: rebuild.** The model ranked *Chushpan Simulator*
and *BBQ Simulator: The Squad* at the top while Hi-Fi RUSH (Metacritic 90) sat at rank
8,439 of 15,921. The critic diagnosed why, by re-running the code rather than reading it:

- The model was **non-deterministic** — no `ORDER BY`, so a positional train/test split gave a
  different answer each run. Three re-runs returned r = 0.5495 / 0.5599 / 0.5506; the published
  0.564 appeared in none of them.
- **No recognition term existed.** Measured pillar influence was fit 0.540, proven 0.329,
  cheap 0.263, scarcity 0.030 — the brief's central tension contributed nothing.
- **"Cheap" was a production-budget filter**: 24.8% qualify rate below $2 versus 2.1% above $20.
- **Fit restated Proven**, since it predicted the very quantity Proven measured.

**Against the rebuild.** The analyst caught the critic forwarding a yield computed without a
gate its own spec required; the critic verified and conceded. The critic then found the
replacement Headroom pillar was redundant — Spearman(recognition, headroom) = 1.0000 *within
every ownership bucket* — and that the Fit component had in-population R² of −1.34, worse than
predicting the mean. Fit was cut to a 10% tiebreaker.

**Against the portfolio.** Reduced from 24 picks to **17 picks plus a 7-title watchlist**, on
the grounds that 7 rested on unverified Xbox availability and were being presented with the
same confidence as verified ones. A proposed diversity remedy was **tested and withdrawn**
because it did not work — one named "co-op alternate" turned out to have no co-op flag at all.

## 5. The delivered portfolio

Funnel: **122,191 games → 802 eligible → 275 qualifying → 30 externally verified → 17 picks.**

- **Clean spine (3, leads):** A Hat in Time, Return of the Obra Dinn, Baba Is You — never on
  Game Pass, Xbox version confirmed, no blockers.
- **Restarts (6):** Unpacking, Phoenix Wright Trilogy, What Remains of Edith Finch, Library Of
  Ruina, Danganronpa 2, Persona 3 Reload — previously on Game Pass and rotated out, so ports
  exist and rights holders have said yes once. Cheapest to execute, but deliberately *second*:
  nobody outside Microsoft knows whether they left because the publisher declined renewal or
  because Xbox's own data said no.
- **Confirm-then-sign (8):** Firework, ENDER LILIES, DJMAX RESPECT V, A Short Hike, Potion
  Craft, Chants of Sennaar, CARRION, Rhythm Doctor — Xbox SKUs confirmed, only current
  subscription status open.
- **Watchlist (7):** no verified Xbox version. Explicitly not picks, with a promotion trigger.

Structurally excluded and stated: UNCHARTED (Sony), The Outer Worlds (Microsoft already owns
it), and three already in the subscription including Hi-Fi RUSH.

## 6. Stated limitations

Disclosed in the deck rather than buried:

- The scoring model is honestly **"Recognition, banded by a three-level ownership step"** — not
  a multi-pillar blend. Within any ownership tier, ranking is most-reviewed-first. This is a
  SteamSpy granularity limit and cannot be fixed, only disclosed.
- **No engagement data exists**, so no retention claim is made anywhere.
- **No sourced per-title deal price exists** for this tier. The portfolio is ordered by deal
  *structure* — restarts are cheapest because the work is already done — rather than by price.
- **Steam PC data, Xbox console recommendation.** Console ARPPU is ~48% higher and the genre
  mix differs. Named by the speaker before the board can raise it.
- **Concentration is real and accepted**: picks are 17.6% Action against a qualifying list at
  53.8%. The remedy was tested and withdrawn rather than faked.
- **Two of eight raw files** (`descriptions.csv`, `promotional.csv`, ~1 GB combined) exceeded
  the transfer limit and were not analysed. Recorded as a scope limit.

## 7. Reproducibility

Every figure is Measured (names its `.sql` file and n), Sourced (URL and date), or Derived
(arithmetic shown, inputs traced). The final pipeline is deterministic — verified by five
consecutive re-runs producing byte-identical output. All three model versions are retained
so the progression under criticism is visible rather than tidied away.

`RUN_LOG.md` and `DECISIONS.md` record what was decided, what the alternatives were, and the
measured effect of each choice — including the two occasions where an agent was wrong and was
corrected by another.
