# Stage 6 — Red-team review

Adversarial review of `05_theses.json`. Every number below was traced to `03_findings.json`,
`04_sources.json` or re-computed from `parquet/` directly. Queries re-run and reproduced
exactly: `sql/11_reach_concentration.sql` (F1), `sql/20_licensing_candidate_inventory.sql` (F6),
`sql/17_cohort_trend.sql` (F2/F3), `sql/16_publisher_outperformance.sql` (F4),
`sql/19_selfpublished_vs_backed.sql` (F5). No reported finding failed to reproduce.

## Verification summary — what checked out

- **F1** reproduces exactly (Action 86.6 / 79.6; RPG 84.6 / 76.8; Indie 78.4 / 81.0; Sports 78.1 / 81.7; Strategy 80.2 / 76.7).
- **F2/F3** reproduce exactly (2015: 2,487 titles, mean owners 199,630, median reviews 147 → 2023: 15,030 / 32,096 / 11).
- **F4** reproduces exactly (Xbox Game Studios 5.80x n=32; Bethesda 6.23x n=25).
- **F5** reproduces exactly (0.307 / 1.610 n=12,594 vs 0.250 / 0.904 n=29,148).
- **F6** reproduces exactly (Action 198 / 217 / 117 / 42 = 574).
- **Churn arithmetic is internally correct.** 30M × 1pp = 300,000; × $168/yr = $50.4M; $90M ÷ $50.4M = 1.79pp ≈ 1.8pp. At 60% margin, $168 × 0.6 = $100.80 ≈ "~$100"; 300,000 × $100.80 = $30.24M; $90M ÷ $30.24M = 2.98pp ≈ 3pp. At $45M: 0.89pp ≈ 0.9pp. All four figures check.
- **$90M build checks:** 60 × $1.5M = $90M.
- Every external claim_id cited in `05_theses.json` exists in `04_sources.json`. The
  fabricated "15M copies" Meccha Chameleon figure was correctly caught at Stage 4 and does
  not appear in Stage 5. Credit where due.

The self-critique in `05_responses.md` was checked concession by concession. O2 (falsifier
moved from gross ARPU to contribution margin) and O5 (breakout claim narrowed from base rate
to tempo/existence) are real concessions, present in the revised text. O1 and O4 are
**partial** concessions presented as complete — see R1 and R4 below, which are the two
objections the self-critique came closest to and did not reach.

---

## Objections

### R1 — T1's candidate pool is double-counted, and the deduped pool cannot sustain the steady state
- **Target:** T1 `size.basis` ("F6's candidate pool (574 Action + ~195 RPG + ~391 Indie proven hits), of which 60/year is roughly 5%"); T1 `steady_state_if_continued` ($90M/yr); T1 evidence[0].
- **Severity:** **FATAL to the $90M/year steady state.** (The $23M first tranche survives.)
- **Objection:** The three genre counts are summed as if disjoint. They are not. F1's own
  caveat states it: "A game can carry multiple genre tags (fan-out is intentional here)."
  Steam titles routinely carry Action + Indie + RPG simultaneously. Re-running F6's bar
  (`owners_low>=1e6 AND review_total>=50 AND review_positive_ratio>=0.7`, real games only)
  against `fact_games.parquet`:

  | Cut | Count |
  |---|---|
  | Distinct titles meeting the bar, **entire catalogue, all genres** | **1,094** |
  | Action ∪ RPG ∪ Indie, deduplicated | **885** |
  | T1's stated sum (574 + 195 + 391) | 1,160 |

  T1's stated pool for three genres (1,160) **exceeds the total number of distinct titles
  meeting the bar in the whole dataset (1,094)**. That is a decisive arithmetic
  impossibility, not an approximation.

  It gets worse when T1's own screens are applied. T1 specifies non-exclusive, **3+ year old**
  titles, and licensing a free-to-play title into a subscription buys nothing:

  | Screen (cumulative) | Remaining |
  |---|---|
  | Meets F6 bar | 1,094 |
  | …excluding free-to-play (177 are F2P, 16.2%) | 917 |
  | …and released 2022 or earlier (T1's "3+ year old") | 727 |
  | …and excluding Microsoft's own + structurally unlicensable publishers¹ | **646** |

  ¹ Bethesda Softworks (34) and Xbox Game Studios (22) are already owned — zero incremental
  licensing value. Valve (29), PlayStation Publishing (9), Activision (9, also Microsoft),
  Rockstar (8) will not license back catalogue non-exclusively to a rival subscription.

  646 is **before** netting the ~500 titles already in Game Pass (`gp-tiers-2026-04`) — the
  overlap O1 conceded but never quantified — and before rights availability. A plausible
  netted, available pool is 200–350 titles.

  At 60 titles/year against ≤646, T1 consumes **≥9.3% of inventory per year**; against a
  netted 250, **24% per year**. The pool is exhausted inside 3–4 years — *within T1's own
  stated "3-5 years to full value" horizon*. The sizing rationale ("60/year is roughly 5% —
  deliberately small relative to inventory so that selection can be genuinely top-decile
  rather than volume-driven") is therefore false in its own terms. By year two the selection
  discipline that is T1's entire quality argument is arithmetically unavailable.
- **Evidence:** `parquet/fact_games.parquet` + `parquet/genres_long.parquet`, F6 bar re-applied;
  `03_findings.json` F1 caveat[2]; `04_sources.json` gp-tiers-2026-04.
- **Resolution:** Recompute the pool deduplicated, screened and netted against the live Game
  Pass catalogue **before** any figure is shown to the board. Then either restate the steady
  state as a declining-quality annuity with an explicit exhaustion date, or withdraw the
  $90M/year figure and present T1 as a bounded one-to-three-year programme.

### R2 — T1 proposes to buy for $23M a natural experiment Microsoft has already run 500 times
- **Target:** T1 `first_step.why_this_is_the_right_first_step` — "it produces the single piece of evidence neither this dataset nor any public source contains"; T1's rank-1 position.
- **Severity:** **material** (inverts the T1/T2 ranking).
- **Objection:** T1's own cited source, `gp-deal-cost-range`, states Microsoft has negotiated
  **500+ Game Pass licensing deals**. T1's proposal is 20 more. The framing that no evidence
  on catalogue→churn exists is true of *this dataset and public sources* — and false of
  Microsoft. Five hundred title additions, staggered across years, territories and genres, is
  a far larger and better-powered natural experiment than a 20-title block, and it already
  sits in Xbox's telemetry at zero acquisition cost. T1's "why this is the right first step"
  argument does not survive its own evidence base.

  This inverts the ranking. `ranking_rationale` places T2 second because "measurement with no
  decision downstream is worth nothing" — but the decision downstream already exists: the
  standing licence-renewal book across 500+ deals. T2's retrospective is cheaper, faster
  (retrospective, not 18–30 months forward) and better-powered than T1's tranche.
- **Evidence:** `04_sources.json` gp-deal-cost-range; `04_context.md` s3; T1 `first_step`.
- **Resolution:** Re-rank T2 first. Add to T2's zero-cost first-step audit a fourth question:
  *can per-title cohort retention be reconstructed retrospectively from the existing 500-deal
  add/remove history?* Approve T1's $23M tranche only if the retrospective cannot identify the
  effect — which is a genuinely possible answer (non-random title selection, no holdout), but
  it must be established rather than assumed.

### R3 — T1's selection rule is anti-correlated with the incremental value it claims to buy
- **Target:** T1 `mechanism` ("recognisable titles a subscriber already wanted → higher perceived value at the renewal decision"); F6's bar as a selection rule.
- **Severity:** **material** (claim must be narrowed).
- **Objection:** F6 selects on `owners_low >= 1,000,000` — titles with **maximum existing
  market penetration**. For a subscription, incremental value at the renewal decision is
  access to a title the subscriber wants and **does not already own**. T1's selection rule is
  therefore positively correlated with the probability that the target subscriber already owns
  the title, which is the opposite of what the mechanism requires. The more "proven" a title is
  by F6's metric, the lower its expected marginal subscription value.

  This is not the survivorship objection and it is not addressed anywhere in
  `05_theses.json`, `05_responses.md` or `DECISIONS.md`. It attacks the mechanism, not the data.
- **Evidence:** `sql/20_licensing_candidate_inventory.sql` bar definition; T1 `mechanism`; F1
  ("the top decile captures 78-93% of a genre's estimated audience").
- **Resolution:** The screen must be **penetration-adjusted**: high recognition × *low* console
  ownership rate. That is a different and much smaller pool, and identifying it needs the
  console-side ownership data only T2 delivers — reinforcing R2's re-ranking. Narrow T1's claim
  to "high-recognition, low-penetration back catalogue" and state that the pool cannot be sized
  from this dataset at all.

### R4 — T3's load-bearing base rate is drawn from the wrong reference class, and it is wrong by 12x
- **Target:** T3 `mechanism` leg one — "F1 sets the base rate very low… so selection ability is the entire value of the strategy"; T3 evidence[0].
- **Severity:** **FATAL as argued.**
- **Objection:** After O4 correctly demoted F4 to "supporting context only, not load-bearing",
  F1's base rate is the leg T3 leans on hardest. But F1 is computed across **all 122,191** real
  games on Steam — a population overwhelmingly composed of sub-$10 hobbyist and self-published
  titles. A $50M+ studio acquisition or internal greenlight does not draw from that population.
  Re-computing the probability of reaching `owners_low >= 1M` by reference class:

  | Reference class | n | % reaching 1M+ owners |
  |---|---:|---:|
  | All titles (the class T3 uses) | 122,191 | **1.01%** |
  | Publisher with ≥20 titles | 15,003 | 3.24% |
  | Priced $30–60 | 1,542 | 12.32% |
  | Priced ≥$30 **and** publisher with ≥20 titles | 842 | **12.59%** |

  The base rate for the reference class a studio-scale commitment actually occupies is
  **12.5x** the one T3 uses. This is precisely the same category error O4 conceded for F4 —
  measuring one thing and arguing about another — committed a second time, on the leg that
  survived the first concession. `05_responses.md` O4 did not reach it.

  Note what this does and does not do. It does not prove studio investment is a good idea:
  12.59% is still a minority outcome, it is Steam-PC and survivorship-filtered, and "reaching
  1M owners" is not "returning $50M." What it destroys is T3's *quantitative* argument that
  the base rate is so low that ex-ante selection ability is "the entire value of the strategy."
  At 12.6%, a portfolio of premium titles from established publishers is not a lottery.
- **Evidence:** re-computed from `parquet/fact_games.parquet`; `03_findings.json` F1, F7
  (`30_to_60`: n=1,542, mean owners 744,792); `05_responses.md` O4.
- **Resolution:** Recompute F1's concentration and the hit base rate restricted to the funded /
  premium reference class, and re-derive the threshold from it — or withdraw the base-rate leg
  entirely and rest T3 on the tempo argument plus the board's own July 2026 revealed
  preference, which is a much weaker and explicitly non-quantitative case that should be
  presented as such.

### R5 — T1's first tranche and steady state use two different central deal prices
- **Target:** T1 `size.first_tranche` vs `size.steady_state_if_continued`.
- **Severity:** **material.**
- **Objection:** `first_tranche` reads "20 titles at an assumed $0.5-1.5M each … (~$20M)" —
  that is a **$1.0M** average. `steady_state_if_continued` reads "$90M/year — ~60 titles/year
  at a $1.5M central assumption", and `size.basis` calls $1.5M "the conservative central case".
  Two different central assumptions in the same size block. At the stated conservative central
  case, 20 titles cost $30M and the first tranche is **$33M, not $23M**. Every downstream
  figure inherits the inconsistency, including the "$31M combined" in
  `materiality_objection_answered` and the entire framing of the ask.
- **Evidence:** T1 `size`; 20 × $1.5M = $30M; 20 × $1.0M = $20M.
- **Resolution:** Pick one central deal price and restate the tranche, the combined ask and the
  materiality calculation from it. If $1.5M is the conservative case, the ask is $33M.

### R6 — the sentence justifying T1's ask contains a 5x arithmetic error
- **Target:** T1 `first_step.why_this_is_the_right_first_step` — "It is ~0.5% of the segment's reported annual revenue scale".
- **Severity:** **material.**
- **Objection:** $23M ÷ $21.8B (`xbox-revenue-fall-2026`) = **0.106%**, not 0.5%. 0.5% of
  $21.8B would be $109M. The document's own `materiality_objection_answered` computes the
  larger $31M figure correctly at 0.14%, so the two sections disagree with each other. The
  error appears in the sentence arguing the ask is proportionate, and it runs in the direction
  that flatters the argument — while in fact making the materiality objection (O7) *worse*,
  since the ask is five times smaller relative to the segment than T1 claims.
- **Evidence:** T1 `first_step`; `materiality_objection_answered`; `04_sources.json` xbox-revenue-fall-2026.
- **Resolution:** Correct to ~0.1% and note explicitly that this strengthens rather than
  answers O7.

### R7 — the hurdle and the falsifier are denominated in different, unreconciled units
- **Target:** T1 `return.expected_outcome` (1.8pp / 3pp of **annual** churn) vs T1 `falsifier` ("90-day churn") vs `size.first_tranche` (12-month window) vs `return.horizon` (18–30 months).
- **Severity:** **material.**
- **Objection:** The entire $90M hurdle is denominated in percentage points of *annual* churn.
  The falsifier that decides continuation is denominated in *90-day* churn. No conversion
  between the two appears anywhere. These are not interchangeable: a 90-day churn delta that
  decays to zero by month twelve produces no annual improvement at all, and the mapping depends
  on the shape of the hazard function, which is unobserved. Separately, a **12-month** licence
  window cannot deliver a **12-month** annual-churn readout — the licences expire as the
  measurement window closes, and the stated readout horizon (18–30 months) runs past the
  window's expiry.
- **Evidence:** T1 `return.expected_outcome`, `falsifier`, `size.first_tranche`, `return.horizon`.
- **Resolution:** State the hazard-shape assumption converting 90-day to annual churn
  explicitly, or restate the hurdle in the falsifier's units. Write the licence windows at
  24 months minimum so the treatment outlives the readout.

### R8 — T2 promises a per-title causal attribution its own proposed design cannot identify
- **Target:** T2 `claim` ("per-title cohort retention attribution — the capability to answer 'which titles kept which subscribers subscribed'"); T1 `first_step.action` (single ~10% subscriber holdout against a 20-title block).
- **Severity:** **material** (claim must be narrowed, or the design must change).
- **Objection:** A single randomised holdout against a 20-title block identifies **one**
  tranche-level average treatment effect, not twenty per-title effects. Per-title effects
  within a shared catalogue are observational and self-selected: subscribers who choose to play
  title X are systematically the more engaged subscribers, who were more likely to renew
  regardless. The resulting attribution will credit retention to titles played by people who
  were never going to churn — which is exactly the reverse-causality problem F5's own caveat
  already names for publishers ("cannot separate 'publisher backing helped' from 'publishers
  select projects that were already going to do well'"). T2 is proposing to spend $8M building
  a measurement with a known identification failure that this run has already documented
  elsewhere in its own findings.

  The fix exists but is a **business-development** constraint, not an analytics one: per-title
  randomisation requires staggered territory or date windows written into the licence terms
  before signature. T1's `first_step` does not mention it, so the T1 tranche as specified would
  foreclose the design T2 needs.
- **Evidence:** T2 `claim`; T1 `first_step.action`; `03_findings.json` F5 uncertainty/caveats.
- **Resolution:** Either narrow T2's claim to "tranche-level causal readout plus explicitly
  correlational per-title descriptives", or add per-title randomisation (staggered territory/
  date add windows) to T1's licence terms as a **precondition (d)** of the first step. The
  second is preferable and nearly free if done before signature; it is impossible afterwards.

### R9 — T2's stated payback is computed against a base whose value T2 exists to establish
- **Target:** T2 `return.expected_outcome` — "if attribution improves title selection efficiency by 20% against a $45-90M/year tranche, that is $9-18M/year… payback inside a year".
- **Severity:** **material.**
- **Objection:** This treats 20% of the **spend** as the return. Improving the selection of a
  tranche is worth 20% of that tranche's *value*, not 20% of its cost. If T1's churn delta is
  zero — the possibility T2 exists to test, and the one T1's own `honest_statement` refuses to
  rule out — then 20% better selection of a worthless tranche is worth zero, not $9–18M. The
  ROI is circular: it is quoted against T1's budget, while T1's value is the thing T2 is being
  built to measure. `assumptions[1]` concedes the 20% is illustrative, but the dollar figure
  and the words "payback inside a year" remain in `expected_outcome` and are what a board will
  read and repeat.
- **Evidence:** T2 `return.expected_outcome` and `assumptions[1]`; T1 `return.honest_statement`.
- **Resolution:** Strike the $9–18M/year figure and the payback claim. State T2's return as
  option value on a decision of currently unknown magnitude — which is what T2's own
  `mechanism` paragraph correctly says, and which the ROI line contradicts.

### R10 — T3's claim and T3's risk mitigation state two different policies
- **Target:** T3 `claim` vs T3 `risks[0].mitigation`.
- **Severity:** **material.**
- **Objection:** The claim is a **prohibition**: "Decline any studio-side capital deployment
  above $50M in FY27 — no acquisitions, no equity funding of external studios, no new internal
  studio formation — and hold or return that capital instead." The mitigation is an
  **escalation gate**: "The threshold escalates rather than prohibits: proposals above $50M go
  to the board with the backtest attached, they are not banned." These are materially different
  decisions with different consequences, and the board would be voting on the headline while
  the fine print implements something else. Given R4, only the escalation version is defensible
  on the available evidence.
- **Evidence:** T3 `claim`; T3 `risks[0].mitigation`.
- **Resolution:** Rewrite the claim as the escalation gate. Say so in the headline sentence,
  not in a risk mitigation four levels down.

### R11 — T3's $50M threshold is anchored on an unrelated quantity
- **Target:** T3 `size.basis` — "The $50M threshold is set at roughly the top of the observed Game Pass per-deal range (gp-deal-cost-range: up to $50M+ per deal)".
- **Severity:** **material.**
- **Objection:** A content-licensing per-deal ceiling has no analytic relationship to a
  studio-equity threshold. T1 and T3 both argue at length that these are different instruments
  with different reversibility, duration, headcount and balance-sheet treatment — which is
  exactly why one's price ceiling cannot calibrate the other's. The number is a judgement call
  presented as a derivation, and the derivation is a non-sequitur. `size.basis` deserves credit
  for refusing to fabricate an FY27 envelope figure; it then anchors on the wrong number
  instead of admitting there is none.
- **Evidence:** T3 `size.basis`; `04_sources.json` gp-deal-cost-range; T1 `mechanism`
  (instrument-difference argument).
- **Resolution:** Derive the threshold from the FY27 studio envelope, or from a stated
  irreversibility criterion (e.g. commitments whose exit cost exceeds one year of segment
  operating margin), or present it plainly as an unanchored judgement.

### R12 — Microsoft's revealed churn lever is price, at roughly 10x T1's proposed spend
- **Target:** T1 as a whole; `objective_function_assumed`.
- **Severity:** **material** (incentive realism).
- **Objection:** The "why has nobody done this" test. `gp-price-history-2025-2026` records
  Ultimate rolled back $29.99 → $22.99 **after churn**, plus PC Game Pass $16.49 → $13.99.
  A $7/month reduction across even 10M Ultimate subscribers is on the order of **$840M/year**
  of forgone revenue deployed against churn — roughly **10x** T1's proposed $90M/year and
  **36x** the first tranche. Simultaneously, Microsoft already runs a 500+ deal catalogue
  licensing programme (R2). So the company has both (a) been buying catalogue for years and
  (b) chosen, most recently, to spend an order of magnitude more on price than T1 proposes on
  catalogue. The straightforward reading of that revealed preference is that Microsoft's
  internal evidence does not support catalogue as the cheaper churn lever.

  T1 cites the price rollback as evidence *for* itself ("establishes that perceived catalogue
  value per dollar is the live constraint"). That inference runs backwards: the rollback shows
  *price* is the live constraint, and that Microsoft reached for price rather than catalogue.
- **Evidence:** `04_sources.json` gp-price-history-2025-2026, gp-tiers-2026-04,
  gp-deal-cost-range; T1 evidence[5].
- **Resolution:** Compute cost-per-retained-subscriber for the April 2026 price action from
  internal data and compare it directly against T1's ~$100 contribution-margin hurdle. That
  comparison — not the Steam catalogue — is the actual decision in front of this board, and it
  is available internally at near-zero cost.

---

## Minor objections

- **M1 — F6 understates its own Action count.** The query returns a further 61 Action titles in
  the `unknown` vintage bucket (release_date is `\N` for 22.7% of games), so 635 meet the bar,
  not 574. Understatement, harmless to the argument, but the number should be right.
- **M2 — publisher rollups sit on a roster missing 29.7% of titles.** `fact_games.parquet` has
  no publisher for 36,286 of 122,191 real games (`01_profile.md` line 64 flagged ~35% in the
  raw source). Missingness correlates with low-profile titles, so every publisher residual in
  F4 — including Xbox Game Studios 5.80x (n=32) and Bethesda 6.23x (n=25) — is biased upward by
  an unquantified amount. Correctly not load-bearing in any surviving thesis (C3 was killed on
  related grounds); noted so it is not resurrected.
- **M3 — 16.2% of F6's pool is free-to-play.** 177 of 1,094 titles meeting the bar are F2P.
  Licensing a free title into a subscription buys nothing. F6's bar has no monetisation filter.
  Folded into R1's screen table.
- **M4 — Silksong is used as evidence in two contradictory directions.** T1 cites it as evidence
  that day-one Game Pass inclusion does not cannibalise (`silksong-2025-sales`). T3 cites the
  2025-26 breakouts as titles that "all broke out organically on Steam first… none was funded
  or acquired pre-launch by a platform holder" — but Silksong shipped **day-one on Game Pass**
  (`04_context.md` s3). Licensing is not acquisition, so this is not a strict contradiction,
  but the T3 wording is false as written for one of its three examples.
- **M5 — Silksong is the wrong title profile for T1's own proposal.** It is a brand-new
  premium release; T1 proposes 3+ year-old back catalogue whose sales curve has decayed. The
  cannibalisation evidence transfers only weakly, and T1's `risks[3].mitigation` says so — but
  then the same citation appears in `evidence` without that qualifier.
- **M6 — survivorship runs in T1's favour here, and the document should say so.** Delisted and
  failed titles are absent from a storefront snapshot. Adding them back would add near-zero-owner
  rows, enlarging the denominator and *raising* the top-decile audience share. F1's 78–93% is
  therefore conservative, not inflated. Recording this so the board is not sold false
  conservatism elsewhere — and because the same fact means F6's "proven hit" inventory is
  unaffected by survivorship (proven hits are the survivors by construction).
- **M7 — F1's precision is bucket-generated.** 83.2% of the catalogue carries an identical
  imputed `owners_mid` (`03_findings.json` scope_reminder). "78–93%" should be read as a shape,
  not a measured share, and should never be quoted to one decimal place in a board room.
- **M8 — the $50M/pp churn value is conservative in one direction and optimistic in another.**
  Conservative: retention compounds, so a sustained 1pp reduction raises the steady-state base
  by considerably more than 300,000 subscribers. Optimistic: the $90M excludes the platform,
  certification and marketing costs T1's own falsifier concedes exist. The two partially offset
  and neither is quantified. Net direction unknown; the hurdle should be presented as a range.
- **M9 — O8's F3 defence is accepted.** Citing F3 to close off a tempting bad argument
  ("newer games perform worse, so buy old catalogue") is a legitimate use and is labelled as
  such inline. No objection. It would read more clearly under a `disclaimed_arguments` key.

---

## Verdicts

**T1 — license back catalogue into Game Pass: STANDS NARROWED, and re-sequenced.**
The $23M instrumented tranche is a defensible bounded experiment and the honesty of
`return.honest_statement` ("This is a hurdle, not a forecast") is real and unusual. But three
things must change before it goes to a board. (1) **The $90M/year steady state must be
withdrawn** pending a deduplicated, screened and netted pool count — the stated pool for three
genres exceeds the entire catalogue's distinct qualifying population (R1). (2) **It must rank
second, behind T2**, because Microsoft's existing 500+ deal history is a larger and cheaper
natural experiment than the one T1 proposes to buy (R2). (3) **The selection rule must become
penetration-adjusted**, because as specified it maximises the chance the subscriber already
owns the title (R3). Plus the arithmetic corrections at R5, R6 and R7. What survives is: a
$23–33M bounded, reversible, instrumented tranche, sequenced after a retrospective, with no
steady-state number attached.

**T2 — build per-title retention attribution: STANDS NARROWED, and should rank first.**
The premise is directly verified rather than inferred — playtime columns confirmed constant-zero
at row level, external equivalent searched for and not found — and the zero-cost first-step
audit is the best-designed step in the document. Two required changes. (1) **Drop "per-title"
from the causal claim** unless per-title randomisation (staggered territory/date windows) is
written into T1's licence terms before signature; the single-holdout design identifies a
tranche-level effect only, and the observational per-title version reproduces the exact
reverse-causality failure F5 already documents (R8). (2) **Strike the "$9-18M/year, payback
inside a year" figure** — it is 20% of a spend, not 20% of a value, and it is circular (R9).
Add the retrospective-on-500-deals question to the audit. So amended, this is the strongest
thesis in the set and the ranking rationale that put it second does not survive R2.

**T3 — decline studio-side capital above $50M: WITHDRAW AS ARGUED.**
The load-bearing leg fails a reference-class check by a factor of 12.5 (1.01% catalogue-wide
vs 12.59% among premium titles from established publishers, R4). This is the same category
error `05_responses.md` O4 conceded for F4, repeated on the leg that survived that concession —
and it is the leg T3 explicitly leans on hardest after the demotion. With F4 demoted, F1
disqualified and the breakout evidence self-declared as n=3 and outcome-selected, what remains
is a tempo argument and the board's own revealed preference, neither of which is quantitative
and neither of which supports a specific dollar threshold. The threshold itself is anchored on
an unrelated quantity (R11), and the claim and its mitigation state two different policies (R10).

May be **re-proposed** in a narrower form that this reviewer would not object to: an
**escalation gate**, not a prohibition, justified on **irreversibility** — permanent headcount,
multi-year commitments, an exit cost the board has just paid three times over — with the
quantitative base-rate claim removed entirely and the threshold presented as a judgement call.
That version is smaller than what is currently written, and honest.

---

## The three questions a hostile board member is most likely to ask

**1. "We have done more than five hundred Game Pass deals. Why are you asking me for twenty-three
million dollars to learn something our own telemetry has already recorded five hundred times?"**

This is the question that ends the meeting if it is not pre-empted, and it comes straight out of
the pitch's own cited source. The only acceptable answer is to have already checked: either the
retrospective works — in which case the tranche is unnecessary and the pitch is T2 alone — or it
demonstrably cannot identify the effect because title selection was non-random and no holdout
ever existed, in which case say precisely that and the forward test is justified. Do not walk in
without having asked.

**2. "You tell me the hit rate is one percent. That is the hit rate for the entire Steam store,
including things two people made in a weekend. What is the hit rate for the kind of studio we
would actually consider buying?"**

The answer, from this run's own data, is roughly **12.6%** — twelve and a half times higher.
T3 cannot be presented until this number is in the deck and the argument has been rebuilt
around it. A board member who has ever seen a portfolio return distribution will ask this, and
being caught having used the whole-catalogue base rate to argue against studio investment will
cost the credibility of all three theses, not just T3.

**3. "We just cut Ultimate by seven dollars a month to stop churn. What did that cost us per
retained subscriber, and is your catalogue cheaper than that?"**

The April 2026 rollback is on the order of $840M/year against even ten million Ultimate
subscribers — roughly ten times T1's proposed annual spend, deployed against the identical
objective, and chosen by this company over catalogue only months ago. T1 cites the rollback as
evidence *for* itself; the board will read it as evidence the company already picked a different
lever. The pitch needs the internal cost-per-retained-subscriber for the price action, side by
side with T1's ~$100 contribution-margin hurdle. That single comparison is more decision-relevant
than every Steam finding in this run combined, and it costs nothing to produce internally.
