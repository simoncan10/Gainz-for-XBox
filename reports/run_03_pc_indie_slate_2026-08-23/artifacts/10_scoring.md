# Stage 10 — Scoring: which titles qualify, and where the bar sits

Every number below is either **Measured** (a `.sql` file + n) or **Derived** (arithmetic
traced to a Measured input). All queries are saved in `sql/`; all scoring code is in
`scripts/`. Full detail (thresholds, sensitivity, model coefficients) is in
`artifacts/10_model.json`. The full ranked list is `artifacts/10_candidates.csv` (1,881
rows, one per qualifying title).

## What this stage does NOT do

It does not check Game Pass availability (not in this dataset — every row in
`10_candidates.csv` carries `screen_gamepass_availability = PENDING_EXTERNAL_CHECK`), and
it does not claim anything about engagement or retention (no playtime column exists in
this dataset; every one is constant zero, per `01_profile.md`).

## Step 1 — the eligibility screen (sql/12_candidate_screen.sql)

Starting from 122,191 non-demo games, five hard conditions produce an **eligible pool of
15,921 titles (13.0% of the catalogue)**:

| Screen | Threshold | Why it sits there | n after |
|---|---|---|---|
| Not free | `monetisation_model='paid'` AND `price_usd>0` | Free titles give Game Pass no exclusivity value and have no usable cost proxy. Also drops 4,057 `paid`-labelled rows with a stale `price_usd=0` (data defect, e.g. an ESO expansion). | — |
| Proven | `review_total>=50` | Valve's own algorithm needs 50 reviews before a nuanced score exists (below 10: no score at all; 10-49: coarse binary). Confirmed against this dataset's own bucket boundaries (`sql/09_review_bucket_check.sql`, n=122,191). | — |
| Quality | `review_positive_ratio>=0.70` | Valve's own published "Mostly Positive" boundary — confirmed exactly in this data (Mixed tops out at 0.700, Mostly Positive starts at 0.700). | — |
| Not already owned | `owners_mid<=750,000` | Above 1,000,000 this dataset is dominated by already-ubiquitous names (Starfield, Baldur's Gate 3, Elden Ring, Persona 5 Royal — `sql/12b_ownership_ceiling_spotcheck.sql`). Pool size is barely sensitive to this exact cutoff (18,172–19,732 across 200k–3.5M tested). | — |
| Platform fit | no Sexual Content / Nudity / Hentai tag | Xbox/Microsoft Store content policy is stricter than Steam's. Verified necessary: several shock/meme titles topped an early, uncorrected composite on price and review volume alone. | **15,921** |

## Step 2 — what wins in this catalogue (sql/11_fit_model_population.sql, scripts/11_build_fit_model.py)

A Ridge regression predicts `ln(1+review_total)` from **structural** features only (genre,
tag, price, co-op/multiplayer/controller/VR flags, self-published flag) plus an
age-since-release control, fit on a **broader** population (60,502 titles with ≥10
reviews and a known release date — not just the eligible pool) and validated on a 30%
holdout it never saw:

| | n | Pearson r | Spearman r | R² |
|---|---|---|---|---|
| In-sample (train) | 42,351 | 0.555 | 0.479 | 0.309 |
| Out-of-sample (holdout) | 18,151 | **0.564** | 0.483 | 0.318 |
| Out-of-sample, scoped to the actual candidate population (owners≤750k, paid) | 14,421 | **0.527** | 0.475 | 0.272 |

**Honest read:** the model explains roughly 30% of the variance in log-review-count from
structural traits alone, and holds up nearly as well inside the low-owner population it is
actually used to rank (0.527 vs. 0.564) — a moderate, real, non-overfit signal, not a
strong one and not the earlier-run's near-zero signal either. It should be read as a
*tiebreaker among already-screened titles*, not as proof that any one genre is "the"
answer. Top positive structural traits: `Multiplayer` tag, controller support, `Co-op`,
`Simulation` genre, `Story Rich`/`Atmospheric`/`Singleplayer` tags. Top negative: `3D` tag,
VR, self-published, `Arcade`/`2D`/`Colorful` tags, `Sports`/`Casual`/`Racing` genres. One
flagged inconsistency: the categorical `has_multiplayer` flag (known to undercount per the
non-English-metadata hazard in `02_cleaning_report.md`) scores negative while the
community-applied `Multiplayer` *tag* scores strongly positive — the tag is the sturdier
signal.

## Step 3 — composite score and the qualifying bar (scripts/12_score_candidates.py)

Four pillars, each a percentile rank in [0,1] **within the eligible pool**, averaged with
equal weight (the transparent no-further-assumptions default):

1. **Proven** = percentile of `ln(review_total)` — recognition/scale beyond the pass-fail floor.
2. **Scarcity** = percentile of `−owners_mid` — not-already-owned.
3. **Fit** = the Step-2 model's structural prediction (age term excluded — age is a
   control, not a fit property).
4. **Cheap** = percentile of `−price_usd` — licensing-cost proxy.

Pillars 1 and 2 pull in opposite directions by construction (more reviews usually means
more owners) — a title strong on **both at once** is the "punches above its weight"
profile a subscription platform should want. Quality (`review_positive_ratio`) is **not**
a fifth scored pillar — it is already a hard gate, and scoring it again would double-count
the same signal.

**The bar: composite ≥ 0.60.** Because each pillar is a uniform percentile, an
unremarkable title scores ~0.50 by construction; 0.60 requires beating the
already-screened pool by a real margin on all four pillars at once, not just clearing one.
This yields **1,881 qualifying titles — 11.8% of the eligible pool, 1.54% of the entire
non-demo catalogue.**

| Bar | 0.50 | 0.55 | **0.60** | 0.65 | 0.70 | 0.75 |
|---|---|---|---|---|---|---|
| n qualifying | 7,989 | 4,186 | **1,881** | 755 | 217 | 41 |

**Weight sensitivity:** re-weighting toward fit (55%) leaves ranking largely intact
(Spearman 0.75 vs. equal-weight); re-weighting toward cheap (50%) shifts it more (Spearman
0.56) — read exact rank order near the bar as indicative, not precise.

## Tiers — read as a portfolio, not a leaderboard

Tiers are assigned by **role**, not by re-slicing the same score into thirds:

| Tier | Rule | n | Price range (median) | Review-total median / p90 |
|---|---|---|---|---|
| **Anchor** | `review_total≥1,000` | 538 | $0.49–$49.99 ($4.99) | 2,597 / 8,352 |
| **Depth** | else, and `price>$5` | 487 | $5.19–$69.99 ($9.99) | 366 / 751 |
| **Low-cost option** | else, `price≤$5` | 856 | $0.27–$4.99 ($2.99) | 233 / 684 |

## Monoculture check

Top-30-by-composite genre mix: Indie 19, Adventure 18, Simulation 16, Casual 14, Action
11, RPG 9 — no single micro-genre dominates the top of the ranking. Across the full
qualifying list, primary genre (assigned by rarest-tag-first, so generic tags don't
swallow the count) tops out at RPG 378/1,881 (20.1%) — genuinely diverse, not a monoculture
restating the fit model's own top coefficients.

## Producer-level finding

Several small developers place **multiple** titles in the qualifying list — evidence of a
repeatable formula, not a single lucky hit: **Randumb Studios (21 titles** — a ~$2
interactive-fiction/choice-quiz format; flagship title "The Test" has 19,646 reviews at
500k–1M owners), **Chilla's Art (10** — a known Japanese indie horror studio), **07th
Expansion (8** — the Higurashi/Umineko visual-novel studio).

**Interesting but not yet defensible:** the broader eligible pool (before the composite
bar) also shows large numbers of niche back-catalogue titles from *established* studios —
Kairosoft (38), KOEI TECMO (38), Square Enix (32), Nihon Falcom (27) — none of which
placed in the actual top-composite list (their pricing and structural fit score lower).
This hints at a "deep-catalogue licensing" angle this model was not built to evaluate and
has not been ranked or reweighted to test.

## Confidence statement

The eligibility screen is built entirely on Measured, externally-verifiable thresholds
(Valve's own review-bucket boundaries, an empirically-grounded ownership ceiling). The
composite ranking's *ordering* rests on a Derived fit score with real but moderate
out-of-sample power (r≈0.53 in-population) and an unweighted-by-evidence 25/25/25/25 split
across pillars — treat the exact rank order as a reasonable sort, not a precise ranking,
and treat the 0.60 bar and its immediate neighborhood (755–4,186 titles across 0.55–0.65)
as the real zone of ambiguity. The list's *membership at the top* (Anchor tier, high
composite) is far more robust than its precise order near the cutoff.
