# Stage 15 — Red team of the v2 rebuild and the 24-title portfolio

Two jobs: verify the rebuild landed, then attack what was built on it. Everything below was
re-executed against `parquet/` and the shipped artifacts.

---

# Part A — Did the rebuild land?

## A-0. The controller-gate discrepancy: **the analyst is right and I was wrong.**

This is the first thing that needs saying, plainly, because it is a finding against my own
Stage 11 artifact.

`artifacts/11_redteam_scoring.md` §"Precise rebuild spec" listed
`has_controller_support = true` as a hard gate in the screen table (RT-11 resolution). The
yield I then reported — **pool = 926, 44.2% metacritic, topped by SnowRunner / Dead Space /
Guardians / Verdun / ICARUS / Persona 3 Reload / Edith Finch / Journey / Lies of P /
Temtem** — was computed **without applying that gate**. Verified directly:

| pool definition | n |
|---|---|
| v2 screen without `has_controller_support` | **926** |
| v2 screen with `has_controller_support = true` | **638** |

And on the two specific names:

| title | `has_controller_support` |
|---|---|
| **Temtem** | **false** |
| **ICARUS** | **false** |

Both appeared in my reported top-10 and **neither can appear in a correctly gated pool**.
Five of the thirteen names I listed fail the gate (ICARUS, Temtem, Hurtworld, Deadside,
Zero Hour). I prescribed a gate and then reported a yield that did not apply it — the same
class of error (published figure not reproducible from the stated method) that RT-01
raised against v1. The analyst caught it, verified it independently rather than accepting
my number on trust, implemented the gate literally, and documented the divergence in
`12_scoring_v2.md` §Zero and `sql/12v2_candidate_screen.sql`. **That is the correct
handling. 638/215 is the right pair of numbers; 926 was mine and it was wrong.**

## A-1. Determinism (RT-01): **fixed. Verified beyond the claim.**

The analyst claimed two identical re-runs. I ran the full v2 pipeline (`11v2_build_fit_model.py`
then `12v2_score_candidates.py`) **five** consecutive times:

- `12_candidates_v2.csv` md5 `104ad4df78bbdf3a263397eaded9713f` on all five runs
- `_ridge_coef_v2.npy` md5 `73b30d2b23d3cf5fd23bef2ceec673e7` on all five runs
- Both identical to the **shipped** artifact taken before any re-run

`ORDER BY f.app_id` in `sql/11v2_fit_model_population.sql` plus the pandas re-sort is
belt-and-braces and it works. Model artifacts are committed, so the scoring script runs
from a clean checkout — v1's blocking defect is gone. **RT-01 resolved.**

## A-2. The 5,000-review floor: **the justification holds; the elbow is at ~4,000, not 5,000.**

I re-derived the table at finer granularity than the analyst published, precisely to test
whether an elbow had been reverse-engineered onto a number I supplied. It had not — the
published table reproduces exactly, and the curve genuinely flattens:

| floor | 500 | 1,000 | 2,000 | 3,000 | **4,000** | 4,500 | **5,000** | 5,500 | 6,000 | 7,000 | 7,500 | 10,000 | 15,000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| n | 3,241 | 2,239 | 1,442 | 1,047 | **802** | 713 | **638** | 576 | 519 | 439 | 399 | 271 | 132 |
| metacritic % | 33.4 | 38.2 | 42.2 | 44.6 | **47.3** | 47.8 | **48.0** | 48.1 | 48.0 | 48.1 | 47.4 | 47.6 | 44.7 |

- **Severity: MINOR.** The plateau begins at **4,000** (47.3%), not 5,000. From 4,000 the
  curve is flat within 0.8pp all the way to 7,000. Choosing 5,000 over 4,000 costs **164
  titles (−20% of the pool)** to buy **+0.7pp** metacritic density.
- **Objection:** "5,000 sits at the elbow" overstates it. 5,000 sits *on the plateau*, one
  step past the elbow. It is defensible; it is not uniquely determined by the data, and the
  artifact presents it as though it were.
- **Resolution:** restate as "any floor in the 4,000–7,000 plateau is equally defensible on
  recognition density; 5,000 was chosen inside that band," and note the 802-title
  alternative at 4,000. This matters because a larger pool is the cheapest available
  remedy for the concentration problem in Part B.

## A-3. Recognition and Headroom: **RT-02 cancellation is fixed, but replaced by a redundancy the reported statistic hides. MATERIAL.**

The pooled figures reproduce exactly: Spearman(Recognition, Headroom) = **+0.542**;
influence on composite Recognition **0.870**, Headroom **0.812**, Fit **0.179**. Nothing
cancels. That part of the rebuild worked.

But +0.542 is a **pooled** correlation, and it is an aggregation artifact. Headroom =
`ln(review_total) − ln(owners_mid)`, and `owners_mid` takes only **5 distinct values in the
638-title pool**, with three buckets holding **634 of 638 titles (99.4%)**. Conditional on
bucket, `owners_mid` is a constant, so Headroom is Recognition minus a constant:

| owners bucket | n | Spearman(recognition_raw, headroom_raw) |
|---|---|---|
| 100k–200k | 31 | **1.0000** |
| 200k–500k | 243 | **1.0000** |
| 500k–1M | 360 | **1.0000** |

- **Objection:** within every bucket that matters, Headroom is a **perfect monotone
  transform of Recognition**. The composite's combined 0.80 weight on the two is really
  0.80 on `ln(review_total)`, adjusted by a **three-level ownership step**. The +0.542
  figure is the between-bucket variation only, and reporting it as evidence of
  complementarity is a textbook Simpson-style artifact — exactly the check RT-08 demanded
  be run on the diversity claim, not run here.
- **Severity: MATERIAL** (not fatal — the model still ranks recognisable titles at the top,
  which was the point).
- **Evidence:** above; `owners_mid` distinct values in pool = {10,000; 35,000; 150,000;
  350,000; 750,000}.
- **Resolution:** report the **within-bucket** correlation alongside the pooled one, and
  restate the composite honestly as "recognition, with a coarse three-step ownership
  discount," which is what it is. Do not claim two independent measured pillars.

## A-4. Fit: reorders a third of the top 30 on a signal with negative in-population R². MATERIAL.

`12_model_v2_fit.json` reproduces: out-of-sample Pearson r **0.3771–0.3883** across seeds
{42, 7, 123, 2024, 99}, mean 0.3843. Reporting a range rather than a point estimate is the
right fix and it is honestly done. But `12_scoring_v2.md` also concedes **R² = −1.34** when
scoped to the actual eligible population — negative R² means the model predicts *worse than
the population mean* inside the slice it is applied to.

- **Objection:** a pillar that is worse than a constant within its own scoring population
  should not be permitted to reorder the shortlist. It does: dropping Fit and renormalising
  changes **21 of 215 memberships (90.2% overlap)** and **10 of the top 30 (20/30 overlap)**.
  A third of the leaderboard the portfolio is drawn from turns on an r≈0.38 signal with
  negative in-scope R².
- **Severity: MATERIAL.**
- **Resolution:** cut Fit to 10% (Recognition 0.50 / Headroom 0.40 / Fit 0.10) or drop it
  and state that the composite is two measured pillars, which it nearly is already. Either
  way, disclose the top-30 membership swing, not just the correlation.

## A-5. Monoculture check: **can now fail, and it correctly reports no monoculture. Verified.**

RT-08's complaint was that the v1 check counted 99 genre *memberships* across 30 titles, so
"spans 6+ genres" was arithmetically guaranteed. The v2 check is computed **by title** over
all 215, on four independent axes, and each can fail:

- Developer concentration max = **3** (v1: 21). Verified from `12_candidates_v2.csv`.
- Serial-chapter collapse: 215 rows → 213 distinct properties. The 5,000-review floor
  structurally removed v1's Higurashi-at-7-rows problem.
- Price-band spread; v2 top-20 median price $17.49 against v1's ~$2.
- Genre shares by title, non-exclusive and labelled as such.

**This check is genuine and it passes.** Credit where due — and it is the check that makes
Part B's concentration finding visible at all.

---

# Part B — The portfolio

## B-1. Traceability: the enforcement is real; the claim about it is overstated. MINOR.

`scripts/14_build_portfolio.py` does `sys.exit` on any app_id missing from
`12_candidates_v2.csv` or `13_availability.json` (lines 338, 340, 395), and every numeric
`trace` field is read from the joined row. I verified all 24 rows: **0 rank mismatches**
against a rank recomputed independently from the CSV, and the CSV is confirmed sorted by
composite descending.

- **Objection:** `14_portfolio.md` says "**no row in the portfolio was typed by hand**."
  The app_ids, tier assignments, within-tier ordering, `why_in_portfolio` and
  `removal_trigger` strings are all hand-authored literals in the `TIERS` structure. Only
  the *numbers* are joined. Also, picks derive `candidates_v2_rank` from
  `13_availability.json`'s `rank` field while alternates derive it from CSV row position —
  two different methods in one file (they agree today; nothing enforces that).
- **Resolution:** restate as "every *figure* is joined, never typed; tier membership and
  rationale are authored judgments." Derive both ranks from the CSV.

## B-2. Tier 1 leads on executability, not desirability. MATERIAL — reorder.

The strategist states the dilemma honestly and completely: either the publisher declined
renewal (price is above what Microsoft would pay) or **Microsoft declined renewal (its own
engagement data already returned a verdict of no)**, and no source establishes which for any
of the eight. It then leads with the tier anyway.

- **Objection:** the stated defence is that Microsoft can settle the unknown "at zero
  external cost and within one day." That argues Tier 1 is the cheapest tier to *validate*.
  It does not argue it is the best tier to *buy*, and leading the pitch with it presents
  executability as desirability. Under the second branch, six of the portfolio's twenty-four
  picks — and the first six the board hears — are a recommendation to re-buy titles
  Microsoft already rejected on evidence it holds and this analysis does not. Meanwhile
  **Tier 2's three titles carry no such unknown at all.**
- **Severity: MATERIAL** (not fatal — the titles are individually sound: all 6 are
  `rotated_out` with `xbox_version = yes`, verified in `13_availability.json`).
- **Resolution:** **lead with Tier 2, then Tier 1.** This costs nothing — Tier 1 keeps its
  cost advantage and its removal rule — and it removes the strongest opening attack
  available to a hostile board. Rename Tier 1 from a ranked lead to "cheapest to execute,
  pending one internal check."

## B-3. The verified core is 3 of 24 — but the tiers are not equally exposed, and the artifact under-sells Tier 3. MATERIAL, in the analysis's favour.

Verified per-title from `13_availability.json`:

| tier | n | Game Pass status | **Xbox SKU** |
|---|---|---|---|
| T1 | 6 | 6 `rotated_out` | **6 `yes`** |
| T2 | 3 | 3 `no` (never on GP) | **3 `yes`** |
| T3 | 8 | 6 `unknown`, 2 `not_verified` | **8 `yes`** |
| T4 | 7 | 6 `not_verified`, 1 `rotated_out` | **6 `not_verified`, 1 `other_console_only`** |

- **On the framing "15 of 24 rest on unverified availability":** that pools two very
  different risks. **All 8 Tier 3 titles have a confirmed Xbox console SKU.** Their only open
  question is whether the title is *currently* in the subscription — a question with exactly
  two answers, both of which the portfolio's own removal rule already handles (if included,
  nothing to buy; if departed, it moves to T1). Tier 3 is genuinely low-risk and the
  artifact is too modest about it.
- **Tier 4 is the real exposure**, and it is worse than stated. **Six of seven have an
  unverified Xbox SKU**, and the underlying evidence is thin: SANABI, The Hungry Lamb, Path
  Of Wuxia, Sanfu and Senren＊Banka each rest on a **single source**, two of them
  (`The Hungry Lamb`, `Senren＊Banka`) at **`confidence: "low"`**. "No evidence found" from
  one low-confidence search is not a finding. The portfolio's own removal rule — "no native
  Xbox console SKU exists and none is dated" — **cannot be evaluated for six of these seven
  titles**, so the rule that is supposed to discipline the list is inoperative on the tier
  that most needs it.
- **Severity: MATERIAL.**
- **Resolution:** do not withdraw them — relabel. Present the portfolio as **"17 picks + 7
  named port-gap watchlist entries."** Tier 4's own stated job is already "to be visible …
  so the board can see what it is choosing not to chase"; the label should match the job.
  The headline becomes 17 named titles of which 17/17 have a confirmed Xbox SKU and 3 are
  fully clean — a stronger and more honest claim than 24 with a 3-title core.

## B-4. The concentration remedy does not work, and one of its five named titles is misdescribed. MATERIAL.

The concentration is verified exactly as reported: portfolio **Action 16.7%** vs qualifying
list **50.7%**; **multiplayer 16.7%** vs **30.7%**; co-op 12.5% vs 22.3%. Naming it
unprompted is good practice. The remedy fails on two counts.

**(a) The named fix is contradicted by the data it points at.** The artifact says
"extending that screen to rank 60 is the cheapest way to fix the concentration." Measured
across the qualifying list:

| slice | n | Action % | multiplayer % | co-op % |
|---|---|---|---|---|
| ranks 1–30 | 30 | 26.7 | **16.7** | **13.3** |
| **ranks 31–60** | 30 | 50.0 | **16.7** | **13.3** |
| ranks 61–120 | 60 | 55.0 | 31.7 | 21.7 |
| ranks 121–215 | 95 | 55.8 | 38.9 | 28.4 |

Ranks 31–60 are **identically** multiplayer/co-op to ranks 1–30 (16.7% / 13.3% in both).
Extending the availability screen to rank 60 raises Action share but does **nothing** for
the multiplayer and co-op gap the remedy is offered to close. Multiplayer density only
rises past rank 60.

**(b) One of the five named alternates does not have the property claimed.** The artifact
says the five "all carry co-op and multiplayer flags." Verified against
`12_candidates_v2.csv`:

| title | rank | `has_coop` | `has_multiplayer` |
|---|---|---|---|
| Deep Rock Galactic: Survivor | 40 | **False** | **False** |
| Streets of Rogue | 43 | True | True |
| Children of Morta | 47 | True | True |
| SnowRunner | 54 | True | True |
| TMNT: Shredder's Revenge | 58 | True | True |

- **Severity: MATERIAL** — a checkable factual error inside the remedy for the portfolio's
  own headline weakness.
- **Root cause, which the artifact does not diagnose:** the gradient is monotone across all
  four rank bands, so this is a **property of the composite**, not of the availability
  screen. The v2 Fit model penalises exactly these traits — `genre_Massively Multiplayer`
  **−0.0851**, `genre_Action` **−0.0247**, `has_multiplayer_i` **−0.0095** — because
  retargeting Fit onto `review_positive_ratio` made it a proxy for *review sentiment*, and
  multiplayer titles carry systematically lower positive ratios (server issues, review
  bombing). Fit's retarget fixed RT-05 and introduced a genre tilt.
- **Resolution:** drop Deep Rock Galactic: Survivor from the alternate list; extend the
  availability screen to **rank 120**, not 60, which is where multiplayer density actually
  doubles; and disclose the Fit-coefficient tilt as the mechanism.

## B-5. The ownership ceiling is shaping the portfolio, and the artifact's explanation is incomplete. MATERIAL.

20 of 24 (83.3%) sit in the 500k–1M bucket, against 63.7% of the qualifying list — verified.

- **Objection:** the artifact attributes this to "Recognition carrying 45% while recognition
  and ownership correlate." That is half the mechanism. The other half is A-3: because
  Headroom collapses to Recognition-minus-a-constant *within* each bucket, the ownership
  term is only a **three-level step**, far too coarse to offset a 0.45-weighted continuous
  recognition term. The result is that the model reliably selects **the most-owned titles
  that still clear the ceiling** — the ceiling is not filtering the portfolio so much as
  *defining* it. And per RT-09/A-3, `owners_mid ≤ 750,000` is bucket-identical to
  `≤ 1,499,999`, so the "not already widely owned" test is being enforced at a granularity
  the data cannot support.
- **Severity: MATERIAL** (the artifact does flag the symptom unprompted — this is a
  completeness objection, not a concealment one).
- **Resolution:** state the mechanism completely, and report what the portfolio looks like
  one bucket down (200k–500k) as a sensitivity, so the board can see whether "not already
  widely owned" is doing real work or just naming the top surviving bucket.

## B-6. Sizing: honest, and genuinely actionable as structured — but the range is not a range. MINOR→MATERIAL.

Refusing to invent a per-title price is correct, and the substitution — ordering by **deal
structure** (prior deal exists / port exists / status known / counterparty scale) rather than
by sticker price — is a real answer to "what can the board do tomorrow," not an evasion.
RT-04's finding is correctly applied: `price_usd_retail_not_licence_cost` does no ordering
work anywhere, verified in the JSON schema.

- **Objection:** `$50K to over $50M across 500+ deals` is a 1,000× span with no
  breakdown, cited from a LinkedIn post relayed by TweakTown. Quoted as the portfolio's only
  cost anchor it is decorative — it excludes no possibility and supports no decision. A
  board cannot approve a budget against it.
- **Severity: MATERIAL** for the pitch, MINOR for the analysis (which correctly declines to
  extrapolate).
- **Resolution:** stop presenting it as a sizing figure. Say instead: "we have no
  defensible per-title price; we have an execution ordering that lets you commit tier by
  tier and stop when quotes stop making sense" — which is what the portfolio actually
  delivers — and put the $50K–$50M line in the Q&A sheet as context, not in the sizing
  section as an anchor.

---

# Verdicts

| Tier | n | Verdict | Condition |
|---|---|---|---|
| **T1 — Restarts** | 6 | **stands narrowed** | Titles stand; **must not lead the pitch.** Reorder behind T2 and relabel as "cheapest to execute, pending one internal check." The re-buy risk is real and unresolved. |
| **T2 — Clean spine** | 3 | **stands** | No change. 3/3 confirmed never on Game Pass, 3/3 confirmed Xbox SKU, no blockers. This is the pitch's opening. |
| **T3 — Confirm-then-sign** | 8 | **stands** | Stronger than the artifact claims: 8/8 have a confirmed Xbox SKU; only current-subscription status is open, and the existing removal rule already resolves both branches. State that explicitly. |
| **T4 — Dated / PC-first** | 7 | **stands narrowed** | Not withdrawn — **relabelled from picks to a named port-gap watchlist.** 6/7 have an unverified Xbox SKU on a single source, 2 at `confidence: low`, and the portfolio's own removal rule is inoperative on them. Headline becomes **17 picks + 7 watchlist**. |

**On the scoring model (v2): stands narrowed.** Determinism fixed, controller gate correctly
applied, monoculture check genuine, recognisable titles now at the top — the rebuild
succeeded. Narrow two claims: Headroom is not an independent pillar (A-3), and Fit reorders
a third of the top 30 on a negative-in-scope-R² signal and should carry 10%, not 20% (A-4).

---

# The three questions a hostile board member will ask

1. **"Your first six picks are games we already had and gave up. Did we drop them, or did
   they drop us — and if it was us, why are you asking me to buy them back?"**
   The honest answer is "we cannot tell from outside, and you can tell from inside in one
   day." That answer survives *only* if these titles are not the opening. Lead with A Hat in
   Time, Obra Dinn and Baba Is You — three titles with no prior run to explain — and Tier 1
   becomes a cheap follow-on instead of the pitch's weakest point stated first.

2. **"You told us the catalogue's strongest signal is Action and multiplayer — half the
   qualifying list — and then brought us a portfolio that is 17% each, with a fix that your
   own numbers say doesn't fix it. Which is it?"**
   Ranks 31–60 are no more multiplayer than ranks 1–30 (16.7% in both), and one of the five
   named co-op alternates has neither flag. Pre-empt by correcting the alternate list,
   extending the screen to rank 120, and naming the mechanism: Fit's retarget onto review
   sentiment penalises multiplayer titles by construction.

3. **"Twenty of your twenty-four are jammed against your own ownership ceiling. Did you
   pick these games, or did the threshold pick them?"**
   Largely the threshold. Because the ownership term collapses to a three-level step while
   recognition is continuous and weighted 0.45, the model selects the most-owned titles that
   still clear the cut — and the cut itself is bucket-identical to a 1.5M ceiling. Bring the
   200k–500k sensitivity into the room rather than conceding this cold.
