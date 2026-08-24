# Indie slate for PC Game Pass — Evidence Appendix

**Every number that supports the deck lives here, with its source artifact and its
arithmetic. Nothing in the deck is a figure this document cannot reproduce.**

Written to be read against the slides, not instead of them. The deck carries the reasoning;
this carries the evidence, the counterargument at full strength, and the limits.

**Date:** 22 August 2026 · **Run:** `run_portfolio` · **Data:** Steam / SteamSpy extract,
`parquet/`, 140,077 rows, 122,191 non-demo titles.

---

## 0. Standing caveats — read these before any number below

These are not boilerplate. Each one changes how a specific figure may be used.

1. **There is no playtime data.** Every playtime column in `steamspy_stage` is constant zero
   across all 140,077 rows (`01_profile.md`, `02_cleaning_report.md`). **No engagement,
   retention or session-length claim is made anywhere in this analysis, for any title, in
   either direction.** The original thesis's "high engagement" leg is withdrawn as
   unmeasurable, not softened. See §3.1.
2. **Owners are bucketed SteamSpy estimates, not sales.** `owners_mid` takes **12 distinct
   values catalogue-wide** and **6** within the eligible pool. It is a step function. A
   "threshold" of 100,000 owners does not exist; it resolves to the nearest bucket midpoint.
   Every threshold below is named by the bucket it actually resolves to.
3. **Retail price is not licensing cost.** Steam retail price is used as a *directional
   proxy*, measured identically on both groups. Stage 11 (RT-04) established it is at best a
   **production-budget** proxy. Every per-dollar figure in this document is a **comparison,
   not a cost figure**, and must not be spoken as one.
4. **This is Steam PC data, and the target is now PC Game Pass.** The rescope (Game Pass runs
   on Windows PC; console SKU is a reach bonus, not a gate) makes the transfer far better than
   in earlier stages. **What still does not transfer:** Steam's storefront population is not
   the Game Pass subscriber population; Steam review counts measure purchaser behaviour, not
   subscriber behaviour; console reach and console ARPPU (**+47.3%**, $81.68 ÷ $55.47 − 1;
   MIDiA 2024 estimates via Plarium, `04_sources.json`) are outside anything Steam data can
   speak to; and Game Pass discovery/merchandising, which materially drives in-service
   performance, has no analogue in this dataset at all.
5. **Review counts are self-selected.** Reviewers are not a random sample of owners.
6. **`release_date` is right-truncated** (nothing after October 2024) and **20.4% missing**
   (`02_cleaning_report.md`).
7. **No sourced indie-tier Game Pass licensing price exists in the public record.** None is
   invented here. See §9.

---

## 1. The funnel, with every count

| Step | n | Source |
|---|---|---|
| Non-demo catalogue | **122,191** | `sql/20_indie_definition_check.sql` |
| `is_indie = true` (raw Steam genre flag) | 82,552 (67.6%) | same |
| **Indie, corrected definition** (`is_indie AND developer_title_count ≤ 10`) | **54,692 (44.8%)** | `sql/27_indie_definition_v2_sensitivity.sql` |
| **Eligible pool** (full screen, §4.1) | **573** (0.47% of catalogue; 42.8% carry Metacritic) | `sql/30_indie_v2_candidate_screen.sql` |
| **Qualifying** (composite ≥ 0.60) | **201** — Anchor 178 / Depth 12 / Low-cost 11 | `23_indie_model_v2.json` |
| **Availability-verified** (top 25 by composite, external research) | **25** | `24_availability_indie.md` |
| **Picks** | **21** | `25_indie_portfolio.json` |

The 25 screened titles reconcile exactly: **21 picks + 2 named-and-not-picked (KovaaK's, Milk
inside a bag of milk) + 2 already in the service with nothing to license (BlazBlue Entropy
Effect, Halls of Torment) = 25.** Asserted in `scripts/25_build_indie_portfolio.py`, which
aborts on a mismatch.

**Qualifying-bar sensitivity** (`23_indie_model_v2.json`): 0.50 → 270 · 0.55 → 234 · **0.60 →
201** · 0.65 → 167 · 0.70 → 134 · 0.75 → 110. The bar is a round number carried forward from
earlier stages, not derived; it is disclosed as such. It affects the size of the pool the
picks are drawn from, not the identity of the top 25 (all 25 sit far above any of these bars).

---

## 2. THE INDIE INVESTMENT CASE, IN FULL

### 2.1 Population

`sql/31_thesis_v2_population.sql`: non-demo, paid, priced titles with **≥10 reviews** (Valve's
own minimum for a review score to exist at all).

| | n |
|---|---|
| **Total** | **48,682** |
| Indie (`is_indie=true AND developer_title_count≤10`) | **30,003** |
| Non-indie (everyone else; NULL `is_indie` or NULL developer folds here via COALESCE) | **18,679** |

### 2.2 Leg (a) — "Cheaper": TRUE, well-supported

`sql/32_thesis_v2_headline_comparison.sql`, n=48,682.

| | mean price | median price |
|---|---|---|
| Indie | **$8.74** | **$5.99** |
| Non-indie | **$12.51** | **$7.99** |
| Indie discount | **30.1%** | **25.0%** |

Arithmetic: 1 − (8.74 ÷ 12.51) = 0.3013 → **30.1%**. 1 − (5.99 ÷ 7.99) = 0.2503 → **25.0%**.

This is the strongest and cleanest single result in the analysis. It holds in every release
cohort and every price band tested (§3.4). **Caveat 3 applies in full: this is a retail-price
finding, not a licensing-cost finding, and this dataset cannot bridge that gap.** Note also
that developer/publisher scale is baked into the indie *definition* itself, so reusing scale
as a "better cost proxy" would be circular — there is no better proxy available here.

### 2.3 The full unconditional comparison

`sql/32_thesis_v2_headline_comparison.sql`.

| | n | mean owners | p90 owners | mean sentiment | propensity (Σreviews/Σowners) | mean price | mean release yr |
|---|---|---|---|---|---|---|---|
| **Indie** | 30,003 | 94,162 | 150,000 | **0.7788** | 0.01340 | **$8.74** | 2019.9 |
| **Non-indie** | 18,679 | **202,037** | **350,000** | 0.7496 | **0.01626** | $12.51 | 2019.4 |
| Indie as % of non-indie | — | 46.6% | 42.9% | +2.9pp | 82.4% | 69.9% | +0.5 yr |

Propensity is the **ratio of totals**, not the mean of per-title ratios — the mean-of-ratios
version over-weights the enormous population of very-low-owner titles. The 82.4% figure here
is a **composition effect and is not a finding**; see §3.2.

### 2.4 The two yardsticks — the calculation that decides the question

`sql/36_thesis_v2_cost_per_owner_vs_per_slot.sql`.

**Yardstick 1 — cost per owner reached** (price ÷ mean owners, expressed per million owners):

| | mean price | mean owners | cost per million owners reached |
|---|---|---|---|
| Indie | $8.74 | 94,162 | **$92.81** |
| Non-indie | $12.51 | 202,037 | **$61.93** |

Arithmetic: 8.74 ÷ (94,162 ÷ 1,000,000) = **$92.82** (published $92.81; sub-cent rounding on
the unrounded mean). 12.51 ÷ (202,037 ÷ 1,000,000) = **$61.92** (published $61.93, same
cause). Ratio 92.81 ÷ 61.93 = **1.4986 → indie is 1.50× more expensive per owner reached.**

**Yardstick 2 — titles per $1,000 at a fixed quality bar** (`review_total ≥ 4,000` AND
`review_positive_ratio ≥ 0.80`, applied identically to both groups):

| | n qualifying | mean price | titles per $1,000 of retail price |
|---|---|---|---|
| Indie | 994 | $15.75 | **63.47** |
| Non-indie | 931 | $24.16 | **41.39** |

Arithmetic: 1,000 ÷ 15.75 = 63.49 (published **63.47** off the unrounded mean $15.7557);
1,000 ÷ 24.16 = 41.39. Ratio 63.47 ÷ 41.39 = **1.5334 → indie delivers 1.53× more qualifying
catalogue slots per dollar.**

**Both are true. They answer different questions.** See §5 for the reconciliation.

Note the quality bar here (4,000 reviews) is *not* the portfolio screen's 5,000-review floor.
The two are deliberately different instruments: 4,000 is a **population-comparison** bar set
low enough to keep both groups' n in the high hundreds; 5,000 is the **candidate-selection**
floor derived in §6.1. Using the selection floor for the population comparison would shrink
the non-indie side and flatter indie.

---

## 3. THE COUNTERARGUMENT, AT FULL STRENGTH

*This section exists because the recommendation must be judged against it, not around it.
Nothing here is softened, and every item survived a red-team re-execution
(`22_redteam_indie.md`).*

### 3.1 "Higher engagement" is UNSUPPORTED and UNMEASURABLE

The original thesis was that indie is a better Game Pass buy because it is (a) cheaper and
(b) more engaging. **Leg (b) is withdrawn entirely.**

- Every playtime column in `steamspy_stage` is **constant zero across all 140,077 rows**.
  There is no session length, no retention curve, no time-spent signal anywhere in this data,
  for indie or non-indie titles.
- This is not "the proxies say no." It is "**there is no data that can answer this**."
- The two nearest measurable proxies were examined and neither is engagement:
  - **Review propensity** (`review_total / owners_mid`) — see §3.2. Confounded by community
    and genre norms, in-client review solicitation (larger studios can afford to prompt more
    systematically), review-bombing, and `owners_mid`'s coarse bucketing.
  - **Review sentiment** (`review_positive_ratio`) — a quality-perception signal among people
    who chose to review. Indie holds a **small, consistent +2.9pp edge** that holds in every
    cohort and price band tested. It is a perception signal, not an engagement signal.

**Anyone who repeats "indie games are more engaging" on the strength of this analysis is
saying something the analysis specifically found untestable.**

### 3.2 The propensity "advantage" is a small-bucket artifact — the claim is withdrawn

The prior version of the thesis claimed indie propensity ran at ~74% of non-indie's rate
"unconditionally and within every age cohort and price band." That claim never stratified by
`owners_mid` — **the denominator of its own metric**. Doing so
(`sql/33_thesis_v2_owners_bucket_stratification.sql`):

| owners_mid | n indie | n non-indie | indie propensity | non-indie propensity | indie as % of non-indie |
|---|---|---|---|---|---|
| 10,000 | 19,558 | 11,651 | 0.00805 | 0.00794 | **101.4%** |
| 35,000 | 4,646 | 2,588 | 0.00731 | 0.00759 | 96.3% |
| 75,000 | 2,274 | 1,400 | 0.00792 | 0.00830 | 95.5% |
| 150,000 | 1,526 | 1,039 | 0.00905 | 0.00947 | 95.6% |
| 350,000 | 1,200 | 919 | 0.01016 | 0.00945 | **107.5%** |
| 750,000 | 452 | 463 | 0.01362 | 0.01315 | **103.6%** |
| 1,500,000 | 195 | 318 | 0.01540 | 0.01494 | **103.0%** |
| 3,500,000 | 106 | 205 | 0.01731 | 0.01883 | 91.9% |
| 7,500,000 | 30 | 61 | 0.01968 | 0.02127 | 92.5% |
| 15,000,000+ | n<30 | n<30 | — | — | suppressed, n<30 |

**Within every bucket with n≥30 on both sides, indie sits at 92–108% of non-indie — parity,
crossing above and below repeatedly.** The unconditional 82.4% headline is a mix effect.

Further: **propensity and reach are not two independent lines of evidence.** Within a bucket,
`review_total / owners_mid` is review volume divided by a near-constant — the *same*
measurement as the reach comparison, rescaled. The prior version presented them as converging
evidence. They are one line, counted twice.

### 3.3 Reach per title is GENUINELY WORSE, and survivorship widens the gap

**Hit rates**, named by the bucket midpoint each threshold actually resolves to
(`sql/35_thesis_v2_hit_rates.sql`):

| threshold (nearest bucket) | indie (n=30,003) | non-indie (n=18,679) | indie as % of non-indie rate |
|---|---|---|---|
| ≥150,000 owners | 11.75% | 16.27% | **72.2%** |
| ≥750,000 owners | 2.66% | 5.79% | **45.9%** |
| ≥1,500,000 owners | 1.16% | 3.31% | **35.0%** |
| ≥7,500,000 owners | 0.15% | 0.51% | **29.4%** |

**Indie reaches a meaningfully smaller audience at every scale tested, and the gap widens at
the top end.** Unlike propensity, this survives stratification by cohort and price band
without exception (§3.4).

**Survivorship runs against indie, not for it** (`sql/34_thesis_v2_survivorship_check.sql`).
The ≥10-review floor is itself a filter and it does not bite evenly:

| group | all paid, priced | in population (≥10 reviews) | excluded | % excluded |
|---|---|---|---|---|
| non-indie | 28,795 | 18,679 | 10,116 | **35.1%** |
| indie | 47,541 | 30,003 | 17,538 | **36.9%** |

Indie is the **more heavily survivor-filtered** group. Removing the floor moves the
indie-as-%-of-non-indie ratio **down**: from 72.2% to **70.5%** at ≥150k, and from 45.9% to
**44.8%** at ≥750k. So the table above is, if anything, **generous to indie**. A hostile
reader will assume survivorship runs the other way (failed indies vanish while AAA persists);
on Steam, delisting is rare and the binding filter is the review floor, which removes indie
titles *more* often.

### 3.4 The reach deficit survives every control tested

`sql/37_thesis_v2_cohort_and_price_control.sql`.

| cohort | group | n | mean owners | mean sentiment | propensity |
|---|---|---|---|---|---|
| <2018 | non-indie | 4,989 | 329,647 | 0.7182 | 0.01273 |
| <2018 | indie | 7,234 | 153,240 | 0.7177 | 0.01060 |
| 2018–2021 | non-indie | 6,769 | 127,893 | 0.7293 | 0.01768 |
| 2018–2021 | indie | 11,823 | 78,894 | 0.7690 | 0.01565 |
| 2022+ | non-indie | 6,921 | 182,563 | 0.7920 | 0.01988 |
| 2022+ | indie | 10,946 | 71,610 | 0.8298 | 0.01467 |

| price band | group | n | mean owners | mean sentiment | propensity |
|---|---|---|---|---|---|
| ≤$5 | non-indie | 7,774 | 68,254 | 0.7246 | 0.00881 |
| ≤$5 | indie | 13,954 | 52,056 | 0.7610 | 0.00915 |
| $5–10 | non-indie | 4,535 | 160,383 | 0.7583 | 0.01359 |
| $5–10 | indie | 7,867 | 77,104 | 0.7903 | 0.01333 |
| $10–20 | non-indie | 3,771 | 267,186 | 0.7797 | 0.01657 |
| $10–20 | indie | 6,872 | 133,753 | 0.8012 | 0.01440 |
| >$20 | non-indie | 2,599 | 580,352 | 0.7652 | 0.01996 |
| >$20 | indie | 1,310 | 437,427 | 0.7827 | 0.01723 |

**Reach:** indie's mean-owners deficit persists in every cohort and every price band without
exception. Age (indie is only 0.5 years newer on average; medians tied at 2020) and price do
not explain it away. **Sentiment:** indie holds a small consistent edge everywhere.
**Propensity:** mixed and near parity in every stratum, consistent with §3.2.

### 3.5 Producer consistency runs against indie

`sql/38_thesis_v2_producer_consistency.sql`. Among developers with at least one hit
(`owners_mid ≥ 500,000`):

| | developers | ever land a hit | rate |
|---|---|---|---|
| Indie | 22,028 | 690 | **3.13%** |
| Non-indie | 8,114 | 625 | **7.70%** |

**Non-indie developers land a first hit roughly 2.5× as often** (7.70 ÷ 3.13 = 2.46).
Conditional on landing one, they repeat more often too: **25.60% of non-indie hitters land a
second hit against 12.17% of indie hitters**, and non-indie hitters average more titles
overall (4.15 vs 1.93) — more shots on goal *and* a higher conversion rate on each.

### 3.6 The counterargument stated in one paragraph, for the record

> Indie games reach fewer people, from developers who succeed less often, and the "engagement"
> half of the case for them cannot be tested at all with this data. Per owner actually
> reached, indie costs **$92.81 per million against non-indie's $61.93 — 50% worse** — and the
> survivorship structure of the data means that comparison flatters indie rather than
> punishing it. The only leg that survives untouched is price, and price at retail is not
> price at licensing. On the yardstick most people instinctively reach for — audience per
> dollar — **the recommendation in this deck is a worse buy, and by a wide margin.**

---

## 4. THE RECONCILIATION — why the recommendation stands anyway

Both yardsticks in §2.4 are correctly computed on the same population with the same price
proxy. They disagree because they measure different things:

| | what it asks | who asks it |
|---|---|---|
| **Cost per owner reached** | "How many people will play this game per dollar?" | A **premium publisher**, monetising unit sales of a title |
| **Titles per $1,000** | "How many reasons not to cancel do I buy per dollar?" | A **subscription**, monetising a fixed monthly fee against a catalogue |

A subscription does not sell copies. It sells continued membership. The unit that keeps a
subscriber subscribed is **the number of credible reasons to open the app this month**, and
that unit is a catalogue slot, not an owner. Slots are what a subscription buys; slots are
what indie is cheap in.

**This is not a rescue of "high engagement" — nothing can rescue that, the data cannot measure
it, and the breadth case does not need it.** It is the narrower, defensible version of the
investment case: **indie is the more efficient way to build catalogue breadth, at the direct
and disclosed cost of reaching fewer players per title.**

Anyone who prefers the per-owner yardstick is making a coherent argument for a different
business — one where a smaller number of larger titles is the right purchase. That argument
should be made explicitly and decided on, not smuggled in through a metric.

---

## 5. THE HONEST EROSION — what these 21 picks actually deliver

The pool-level advantage (§2.4) is not what a real portfolio delivers, because the moment you
select for **recognisability** you select for **price**: recognition and price rise together.
Measured directly on the 21 picks:

| | titles per $1,000 | advantage over non-indie |
|---|---|---|
| Non-indie benchmark | 41.39 | — |
| **This portfolio (21 picks)** | **50.28** | **+21.5%** |
| Whole 201-title qualifying list | 58.62 | +41.6% |
| Indie pool benchmark (994 titles at the quality bar) | 63.47 | +53.3% |

**Arithmetic, in full.** The 21 picks' retail prices sum to **$417.69**:

```
29.99 + 13.39 + 14.99 + 24.99          (Tier 1: Hat in Time, Obra Dinn, Rogue Legacy, Stanley Parable)
+ 14.99 + 29.99 + 19.99 + 19.99 + 14.99 (Tier 2: VA-11 Hall-A, Library Of Ruina, Unpacking, Edith Finch, Journey)
+ 9.99 + 7.49 + 14.99 + 24.99 + 24.99 + 7.99 + 34.99 + 19.99 + 12.99 + 10.99 + 19.99 + 44.99
                                        (Tier 3: Firework … Temtem)
= 417.69
```

1,000 × 21 ÷ 417.69 = **50.28 titles per $1,000**. Against the non-indie benchmark:
50.28 ÷ 41.39 − 1 = **+21.5%**.

**Edge retained:** (50.28 − 41.39) ÷ (63.47 − 41.39) = 8.89 ÷ 22.08 = **40.3%**. **This
portfolio retains 40% of the pool-level breadth advantage.** That is the honest number, and
it is the one to defend — not 53.3%.

**Cutting Temtem alone lifts it to 53.66.** Temtem is $44.99, by a wide margin the worst
titles-per-dollar contribution in the slate: 1,000 × 20 ÷ (417.69 − 44.99) = 1,000 × 20 ÷
372.70 = **53.66 per $1,000 (+29.6% over non-indie)**. It is ranked last on purpose and is the
designated first cut.

**Mean pick price $19.89** (417.69 ÷ 21); median $19.99.

**Caveat 3 applies to every figure in this section.** These are retail-price comparisons
measured identically on both sides, not cost projections.

---

## 6. EVERY FILTER, WITH ITS JUSTIFICATION AND SENSITIVITY

### 6.1 The eligibility screen in full

`sql/30_indie_v2_candidate_screen.sql`:

```sql
is_demo = false
AND app_type = 'game'
AND monetisation_model = 'paid'
AND review_total >= 5000
AND review_positive_ratio >= 0.70
AND owners_mid <= 750000
AND price_usd > 0
AND is_indie = true
AND developer_title_count <= 10
AND app_id NOT IN (tags: 'Sexual Content', 'Nudity', 'Hentai')
```

→ **573 eligible titles**, 42.8% carrying a Metacritic score.

### 6.2 The 5,000-review floor — derived, not inherited

The prior version ran a nine-row sensitivity sweep and **quoted only the first four rows**,
stopping exactly before the curve's later behaviour became visible, then kept the inherited
4,000 floor. The red team caught it. Re-run in full on the rebuilt population
(`sql/28_indie_v2_review_floor_full_sensitivity.sql`) — **all nine rows**:

| floor | 500 | 1,000 | 2,000 | 3,000 | 4,000 | **5,000** | 6,000 | 7,500 | 10,000 |
|---|---|---|---|---|---|---|---|---|---|
| n | 4,486 | 2,766 | 1,626 | 1,112 | 844 | **669** | 531 | 395 | 259 |
| % with Metacritic | 25.0 | 30.0 | 34.2 | 36.2 | 37.7 | **38.7** | 38.8 | 39.0 | 39.4 |
| marginal gain (pp) | — | +5.0 | +4.2 | +2.0 | +1.5 | **+1.0** | **+0.1** | +0.2 | +0.4 |

**Decision: raised from 4,000 to 5,000.** The plateau begins cleanly at 5,000 — the step just
before it still buys **+1.0pp** of Metacritic density; the step just after buys **+0.1pp**, a
**10× collapse in marginal return**. Did not go to 6,000+: the cumulative 6,000–10,000 gain is
**+0.7pp** and costs another **138 titles** (669 → 531).

*Why Metacritic presence is the criterion:* it is an **independent, externally-sourced
recognition signal** that the composite never uses. It is the only quality signal in this
dataset not derived from Steam review behaviour, so it cannot be circular with the ranking.

*(Note: the eligible pool is 573, not the 669 in this table, because the sweep measures the
review floor alone; the final screen also applies the sentiment floor, the owners ceiling, the
paid/priced conditions and the adult-tag exclusion.)*

### 6.3 The 750,000-owners ceiling

Purpose: exclude titles **already widely owned**, on the reasoning that a subscription slot
adds least where the audience already has the game.

Re-checked at the new review floor (`sql/29_indie_v2_owners_ceiling_sensitivity.sql`):

| ceiling | 150,000 | 350,000 | 500,000 | **750,000** | 1,000,000 | 1,500,000 | 3,500,000 |
|---|---|---|---|---|---|---|---|
| n | 49 | 326 | 326 | **573** | (identical to 750k) | — | — |
| % with Metacritic | 22.4 | 34.0 | 34.0 | **42.8** | 42.8 | 40.4→42.3 | 44.3 |

**Kept at 750,000.** Two disclosures: (1) it is **bucket-equivalent to 1,000,000** — n is
identical at both, because `owners_mid` is a step function and no title sits between; the
ceiling is therefore coarser than it looks. (2) Relaxing further **keeps buying Metacritic
density** (40.4% → 42.3% → 44.3% at 1.5M/3.5M) — at the direct cost of the ceiling's entire
purpose. That is a trade made knowingly, not a dominated choice.

### 6.4 The indie definition — the filter that was rebuilt

**What was wrong.** The first definition was `is_indie = true AND is_self_published = true`,
where `is_self_published` is a **literal `developer == publisher` string equality**.

| title | developer | publisher | `is_self_published` |
|---|---|---|---|
| Return of the Obra Dinn | Lucas Pope | **3909** | **False** |
| Papers, Please | Lucas Pope | **3909** | **False** |
| Baba Is You | Hempuli Oy | Hempuli Oy | True |

"3909" is Lucas Pope's own one-man label. **Two of the most canonical independent games ever
made were classified non-indie by a name mismatch.** The same mechanism excluded every indie
that signed with an indie-friendly publisher: What Remains of Edith Finch and Journey
(Annapurna), Unpacking and Temtem (Humble Games), SANABI (NEOWIZ), ABZU (505 Games), ENDER
LILIES, VA-11 Hall-A, Potion Craft, Firework, The Hungry Lamb.

Simultaneously it **admitted** self-published mass-catalogue operations: **EroticGamesClub
(181 titles)**, Choice of Games (163), Boogygames Studios (130), Hosted Games (109), Sokpop
Collective (96).

Wrong at **both** ends: high false-negative rate exactly at the top of the quality
distribution, high false-positive rate across the asset-flip tail. The two flags are also only
weakly associated — P(self-pub | indie) = 54.4% vs P(self-pub | not indie) = 37.6% — so the
second flag added a genuinely different, and wrong, dimension rather than sharpening the
first.

**First replacement tried, and rejected: publisher catalogue size.** `is_indie AND
publisher_title_count ≤ N` passes the hand-check for any N roughly in **[32, 105)**, but at
the smallest passing N it still admits **48% of the whole catalogue** — barely narrower than
the raw flag's 67.6%. Publisher size cannot separate a boutique label (Annapurna, 32 titles)
from a mid-size mainstream one (Nacon, 94 titles, only 4 indie-tagged). **Not adopted, and
recorded as rejected rather than dropped quietly.**

**Adopted: `is_indie = true AND developer_title_count ≤ 10`**, where `developer_title_count`
is the developer's total non-demo game count catalogue-wide. It works because the
mass-catalogue bad actors *are* self-published — the same entity is developer and publisher —
so a huge developer count catches them exactly where a huge publisher count did, while leaving
tiny studios untouched **regardless of whose name is on the publisher line**.

**Hand-check, verified line by line** (`sql/27_indie_definition_v2_sensitivity.sql`):

| title / entity | developer | dev title count | classified |
|---|---|---|---|
| Return of the Obra Dinn | Lucas Pope | 2 | **IN** |
| Papers, Please | Lucas Pope | 2 | **IN** |
| What Remains of Edith Finch | Giant Sparrow | 2 | **IN** |
| Journey | thatgamecompany | 2 | **IN** |
| ENDER LILIES | Live Wire / Adglobe | 1 | **IN** |
| Unpacking | Witch Beam | 2 | **IN** |
| ABZU | Giant Squid | 2 | **IN** |
| SANABI | WONDER POTION | 1 | **IN** |
| Choice of Games | Choice of Games | 163 | **OUT** |
| EroticGamesClub | EroticGamesClub | 181 | **OUT** |
| Boogygames Studios | Boogygames Studios | 130 | **OUT** |
| Hosted Games | Hosted Games | 109 | **OUT** |
| Sokpop Collective | Sokpop Collective | 96 | **OUT** |

**Extended spot-check beyond the required list:** Supergiant Games (5 titles), Vlambeer (5),
Mode 7 (3) all stay **IN** at N=10. **N=2 — the strictest cutoff that still passes the
required hand-check — would have wrongly excluded all three.** Klei Entertainment (12) is
excluded at N=10: an acceptable, named edge case, not required IN by any hand-check item.

**Honestly disclosed limitation.** This narrows the raw `is_indie` population from 67.6% to
**44.8% (54,692 / 122,191)** — **less** narrowing than the broken rule achieved (36.8%).
Developer-catalogue-size fixes **who** is correctly classified as indie; it does not by itself
make "indie" a small segment, because most Steam titles tagged Indie genuinely are made by
1–2-title developers. That is a structural fact about the catalogue, not a modelling failure.
The narrowing to an actionable segment happens downstream in the eligibility screen (573
titles, 0.47%).

**Proof the fix worked:** eight of the wrongly-excluded canonical titles now appear inside the
**top 20** by composite — Unpacking, VA-11 Hall-A, Temtem, SANABI, Edith Finch, ENDER LILIES,
Journey, Potion Craft, Obra Dinn.

### 6.5 The controller-support gate — dropped, and why the original justification was wrong

`has_controller_support = true` was added at Stage 12/16 as a Steam-PC → Xbox-**console**
platform-fit proxy (certification, control-scheme risk). **It is dropped, for one reason only:
Game Pass runs on Windows PC, so a console-fit proxy no longer applies to a keyboard-and-mouse
title.**

**The original justification for dropping it was wrong and is withdrawn.** Stage 20 argued
that dropping the gate was equivalent to "demoting" it, because the Fit model already scores
`has_controller_i` as its strongest positive coefficient (**+0.0387**). The coefficient claim
verifies. The inference does not:

- The whole coefficient range is **[−0.0851, +0.0387]** on a target spanning ~0.70–1.00; Fit
  is percentile-ranked and weighted **0.10**; in-population **R² = −1.34** (worse than
  predicting the mean).
- Direct evidence the demotion is inert: **KovaaK's** sat at rank #11 with `fit_pct = 0.0395`
  (bottom 4% on Fit) and **Verdun** at #19 with `fit_pct = 0.0099` (bottom 1%). A pillar that
  leaves bottom-1%-on-Fit titles inside the top 20 is not "handling" anything.

**Nothing replaces the gate's quality-signal role, and the cost is real and measured:**
Metacritic presence is **40.7%** among controller-supported titles (n=241) against **25.5%**
among no-controller titles (n=165) — a **15.2pp quality gap** admitted knowingly.

Measured cost per tier (`23_indie_v2.md` A-2):

| tier | qualifying n | no-controller n | no-controller % |
|---|---|---|---|
| Anchor | 178 | 45 | 25.3% |
| Depth | 12 | 2 | 16.7% |
| Low-cost option | 11 | 5 | 45.5% |
| **All** | **201** | **52** | **25.9%** |

Two picks lack controller support: **VA-11 Hall-A** and **Temtem**. Both are playable on PC by
construction; the cost is console reach, which under this scope is a bonus, not a gate.

### 6.6 Composite weights and tier rules (carried forward, disclosed as such)

Recognition **0.50** / Headroom **0.40** / Fit **0.10**; qualifying bar **0.60**; Anchor tier =
`review_total ≥ 10,000 OR (Metacritic present AND owners_mid ≥ 350,000)`; Low-cost option =
`price ≤ $10`. **These were carried forward unchanged under standing instruction and were not
re-derived in this pass.** They were checked against the rebuilt 573-title pool and produce a
sane 178/12/11 split. Disclosed as inherited, not as justified.

---

## 7. THE MODEL'S KNOWN LIMITS

### 7.1 The composite is ~90% one variable

Within the 6-value `owners_mid` bucket structure, Recognition (percentile of
`ln(review_total)`) and Headroom (percentile of `ln(review_total) − ln(owners_mid)`) are
**near-perfectly collinear — Spearman = 1.0000 within every bucket with n≥5** (150,000 /
350,000 / 750,000), because `owners_mid` is constant inside a bucket.

- **Pooled R² of the composite against `ln(review_total)` alone: 0.775** (`23_indie_model_v2.json`: 0.7749).
- **In the top 20, `owners_mid` takes only two distinct values: 350,000 and 750,000.**
- Pillar influence on the composite (Spearman): Recognition **0.886**, Headroom **0.828**, Fit
  **0.155**.

**So the composite is, honestly, a log-review-count ranking banded by a near-constant
ownership step — not a multi-factor quality blend.** Headroom moves a title between bands; it
does not order titles within one.

**The cross-artifact tension, and how it is resolved.** `21_indie_thesis.md` warns that
reviews-per-owner is confounded and must not be read as engagement; the scoring composite
leans on the *volume* side of exactly that quantity. Both statements are individually true and
they sit in genuine tension. The resolution adopted: the scoring document now states plainly
that the composite is a review-**volume** ranking, and the thesis stops treating reach and
propensity as two independent lines of evidence. Neither document claims the metric measures
engagement.

**This disclosure changed a pick.** KovaaK's (rank 22, 32,859 reviews — 4th-highest volume in
the screened set, $9.99) outranks three actual picks on composite and would be a cheap slot
under a pure titles-per-dollar reading. It is **excluded** because a training utility
accumulates review volume through a mechanism that does not convert into what a catalogue slot
is for. That is the disclosed degeneracy producing a title the metric likes for a reason the
strategy does not share — caught because the degeneracy was disclosed rather than buried.

### 7.2 The Fit model is weak, and is weighted accordingly

`12_model_v2_fit.json`. Ridge regression (alpha 5.0) on 41 genre/tag/capability features,
target `review_positive_ratio`, n = 60,502.

| measure | value |
|---|---|
| Out-of-sample Pearson r (5 seeds: 42, 7, 123, 2024, 99) | **0.3771 – 0.3883** (mean 0.3843) |
| Out-of-sample R² (same 5 seeds) | 0.1418 – 0.1507 |
| **In-population R² (scoped to the 221 eligible rows in the test fold)** | **−1.3387** |
| Weight in the composite | **0.10** |

**A negative R² in-population means the model does worse than predicting the mean for exactly
the titles being ranked.** It is retained as a 10% tiebreaker and nothing more, and no claim
rests on it.

*Note:* `price_usd` and `is_free` were deliberately **excluded** from the Fit feature set so
that price could not re-enter the composite through the Fit door after being removed from
scoring (see §8).

### 7.3 Coarse ownership data

`owners_mid` takes 12 distinct values catalogue-wide and 6 in the eligible pool (bucket
counts: 10,000 → 2; 35,000 → 2; 75,000 → 1; 150,000 → 31; 350,000 → 254; 750,000 → 283). Every
statement about "owners" is a statement about a bucket midpoint.

---

## 8. WHAT WAS WITHDRAWN, AND WHY

Recorded so a reader can check that corrections were made rather than absorbed.

| # | Withdrawn claim | Why | Replaced by |
|---|---|---|---|
| 1 | **"Indie has higher engagement."** | No playtime data exists — every playtime column is constant zero across 140,077 rows. Not "the proxies disagree"; there is nothing to test with. | Nothing. The leg is deleted, and the breadth case is made without it. |
| 2 | **"Indie propensity runs at ~74% of non-indie's, unconditionally and in every cohort and price band"** (the propensity penalty). | Never stratified by `owners_mid`, the denominator of its own metric. Stratified, it sits at 92–108% — parity. The 82.4% unconditional headline is a composition effect driven by the 10,000-owner bucket. | "Reviews-per-owner does not meaningfully distinguish indie from non-indie once ownership scale is held constant." |
| 3 | **Propensity and reach presented as two converging lines of evidence.** | Within a bucket they are the same measurement rescaled — one line counted twice. | Reach reported once, on its own terms; propensity reported once and excluded from the verdict. |
| 4 | **"Fit compensates for the dropped controller gate."** | Technically true (+0.0387 is Fit's strongest coefficient) and practically empty: Fit is 10%-weighted with in-population R² = −1.34, and bottom-1%-on-Fit titles sat freely in the top 20. | "The gate is dropped because Game Pass runs on PC. Nothing replaces it, and the 15.2pp Metacritic gap is a cost accepted knowingly." |
| 5 | **"Indie developers are not less consistent once they succeed."** | Reverses under the corrected indie definition: 25.60% of non-indie hitters repeat vs 12.17% of indie hitters, and non-indie hitters also carry more titles. | "Non-indie developer consistency is unambiguously stronger on this population." Reported as evidence **against** the recommendation (§3.5). |
| 6 | **The `is_indie AND is_self_published` definition.** | A `developer == publisher` string match. Wrong at both ends (§6.4). | `is_indie AND developer_title_count ≤ 10`, hand-checked. |
| 7 | **The price-band sentiment reversal at >$20** reported in the prior thesis version. | Does not reproduce under the corrected indie definition. | Retracted with the definition that produced it. |
| 8 | **"Cheap" as a scored pillar** (earlier general-population model). | Retail price is a **production-budget** proxy, biased in exactly the dimension being compared. Metacritic presence rises monotonically with price (5.7% at ≤$2 → 22.5% at >$20); qualify rate falls 24.8% → 2.1%. Ranking on inverse price ranks on absence of budget. | Price removed from the composite entirely; carried as a **cost annotation column** only. It does no ranking work anywhere in this recommendation. |
| 9 | **The "four-pillar" composite of the first model.** | Proven and Scarcity were Spearman **−0.762** and cancelled: Scarcity's rank influence on the composite was **0.030**. The brief's central tension was annihilated, not encoded. Result: The Confession, The Horrorscope and BBQ Simulator at the top of the list. | A single Headroom ratio (`ln(reviews) − ln(owners)`) plus a separate absolute Recognition term — complementary (Spearman +0.331), not cancelling. |
| 10 | **The 7-title console port-gap watchlist** (previous run). | Dissolved by the PC rescope. Wandering Sword, SANABI, The Hungry Lamb, Path Of Wuxia and Sanfu now compete on merit; five of them are picks. | Console SKU recorded as a **reach bonus** (14 of 21 picks have one). |

---

## 9. COUNTERPARTY RISK

Four of the strongest candidates sit behind two publishers that lost their entire staff in
2024.

- **Annapurna Interactive** — publisher of **What Remains of Edith Finch** and **Journey** (and
  of lower-ranked Neon White, Gorogoa, Florence). The **entire video-game staff (~24 people)
  resigned en masse in September 2024** after a dispute with owner Megan Ellison over a failed
  spin-off negotiation. [Bloomberg, 12 Sept 2024; Deadline, Sept 2024]. **No report found that
  catalogue rights were sold, lost or disputed** — this is counterparty continuity risk, not a
  confirmed rights blocker.
- **Humble Games** — publisher of **Unpacking** and **Temtem**. **Laid off its entire ~36-person
  staff in July 2024**, widely reported as a de facto shutdown. The company disputed "full
  shutdown," called it a restructure, and later signalled it would keep supporting its existing
  catalogue. [Forbes, 23 July 2024; Game Developer, July 2024; PC Games Insider, July 2024].
  Same caveat: catalogue rights not reported as lost or sold.
- **NEOWIZ** (SANABI): checked specifically; **no evidence of comparable restructuring found**.
  Stated as absence of evidence, not confirmed stability.

**Why this is not a price range.** A distressed rights holder with a dormant catalogue and no
staff may license **cheaply** — a back-catalogue licence is close to free money against an
asset nobody is working. Or it may be **impossible to transact with at all**, because nobody
with signing authority remains. These are not two ends of a spectrum: one is cheap and one is
**binary**, and a binary failure cannot be priced into a bid.

**What the portfolio does about it:**

1. The two **stable** restarts (VA-11 Hall-A, Library Of Ruina) are ordered **ahead** of the
   three distressed ones, so Tier 2 can be worked in order and stopped.
2. A **30-day counterparty-identification condition** is written into Tier 2's removal rule,
   converting an unpriceable risk into a dated go/no-go.
3. Tiers 1 and 3 are populated independently of these publishers, so **17 of 21 picks survive
   all four counterparties falling over**.

### Sizing: no price exists, and none is invented

**No sourced figure for indie-tier or back-catalogue-tier Game Pass minimum guarantees exists
in the public record.** Two searches across two stages found none. The only dated, sourced
figures are AAA-scale — **$5M–$300M day-one deals** and **~$12–15M/month for GTA V**
back-catalogue (Axios, 19 Sept 2023) — and neither is representative of a sub-750k-owner indie
title. **Nothing is extrapolated from them.**

Consequence: **the recommendation is ordered by deal structure** (never-included / rotated-out
/ already-in-service / counterparty-risk-adjusted), **not by price**. Retail price does no
ranking work anywhere. It appears only in the group-level breadth comparison, measured
identically on both groups, carrying Caveat 3.

---

## 10. THE PICKS — availability and status evidence

| Group | Titles | Evidence |
|---|---|---|
| **Never on Game Pass, PC + console confirmed** | A Hat in Time, Return of the Obra Dinn, Rogue Legacy, The Stanley Parable: Ultra Deluxe | Confirmed "Not Included" via subscription tracker (Rogue Legacy via absence of dated evidence despite extensive search) |
| **Rotated out (previously licensed)** | VA-11 Hall-A (added 1 Dec 2020, **PC tier specifically**, left ~30 Nov 2021) · Library Of Ruina (Aug 2021 → gone, date not pinned) · Unpacking (left **~late June 2026**) · What Remains of Edith Finch (≥2019 → gone) · Journey (added July 2024, **PC tier specifically** → gone) | Dated sources per title in `24_availability_indie.json` |
| **Added at some point, no dated exit** | Firework (Jun 2024), A Short Hike (3 Aug), Potion Craft, Chants of Sennaar, CARRION | Current-day status **not** reconfirmed |
| **No Game Pass evidence either way** | The Hungry Lamb, SANABI, Wandering Sword, Path Of Wuxia, Sanfu, Temtem | PC confirmed by construction of the dataset |

**VA-11 Hall-A and Journey are the two clearest precedents in the entire list for exactly the
PC-Game-Pass deal type this scope asks about** — both added and later removed as PC-tier
inclusions. This exact deal shape has been executed twice.

**What could not be verified**, stated plainly: current-day Game Pass status for 9 titles;
whether Journey's PC Game Pass release ever had a console counterpart; Xbox console releases
for The Hungry Lamb, SANABI, Path Of Wuxia, Sanfu, VA-11 Hall-A (absence of evidence, not
confirmed absence); exact departure dates for Library Of Ruina and Edith Finch; whether the
**original** Rogue Legacy was ever on Game Pass (heavily obscured by Rogue Legacy 2's separate,
well-documented Game Pass history — **a named exposure, and the removal trigger for that pick**);
**ranks 26+ were not screened at all.**

### Composition (measured on the 21 picks)

- 11 of 21 carry Metacritic (75–89) — an independent press signal the composite never uses.
- 16 of 21 sit in the 500k–1M owner bucket, against the ceiling.
- Max titles from one developer: **2** (Shiying Studio — Firework and Sanfu; one counterparty
  conversation covers two picks).
- Mean price $19.89, median $19.99.
- PC confirmed 21/21. Console exists for 14/21 (reach bonus, not a gate).

### Concentration, and the bounded remedy

**[MEASURED]** Picks (n=21): Action 19.0%, multiplayer 9.5%, co-op 9.5%. Qualifying list
(n=201): Action 47.3%, multiplayer 27.4%, co-op 23.4%. **The gap is real.**

| band | n | Action | multiplayer | co-op |
|---|---|---|---|---|
| ranks 1–25 (screened) | 25 | 28.0% | 12.0% | 12.0% |
| **ranks 26–60** | 35 | 45.7% | **40.0%** | **34.3%** |
| ranks 61–120 | 60 | 56.7% | 28.3% | 20.0% |
| ranks 121–201 | 81 | 46.9% | 25.9% | 24.7% |

The band immediately below the screen is **the multiplayer peak of the entire list**.
Extending the availability screen from rank 25 to rank 60 is a bounded ask (35 titles) landing
exactly where the gap closes. **14 titles with verified co-op/multiplayer flags sit in ranks
26–60** — Verdun (#26), Deadside (#33), Rhythm Doctor (#36), Your Only Move Is HUSTLE (#39),
Streets of Rogue (#43), Children of Morta (#47, MC 82), Crab Champions (#48), TerraTech (#50),
My Time at Sandrock (#52, MC 80), Contagion (#54), TMNT: Shredder's Revenge (#55), Trailmakers
(#56), LIZARDS MUST DIE (#58), Wobbly Life (#60). **None can be a pick today** — all sit
outside the screen with no availability verdict. That is the cost of closing the gap, not a
gap already closed.

*Temtem's genre strings are Spanish in source (`Aventura`/`Rol`/`Multijugador masivo`), a known
non-English metadata case from `02_cleaning_report.md`, which slightly understates the
Action/RPG share above.*

### Named and deliberately NOT picked

- **KovaaK's** (824270, rank 22, 32,859 reviews, $9.99). Outranks Sanfu, The Stanley Parable
  and CARRION on composite. Excluded on §7.1: the composite is ~90% log review count, and a
  training utility accumulates review volume through a mechanism that does not convert into
  catalogue value. **Excluded.**
- **Milk inside a bag of milk inside a bag of milk** (1392820, rank 17, 26,566 reviews,
  $1.49). **The best titles-per-dollar entry anywhere in the screened set** — the breadth
  thesis taken to its logical limit. Excluding it is in **genuine tension** with the argument
  this portfolio rests on, and that tension is stated, not hidden. Excluded on (1) positioning
  and (2) series duplication (rank 17 and rank 28 are one licensable property contributing two
  rows). **No runtime is asserted for it — there is no playtime data. "Short novelty" is a
  characterisation, not a measured finding. Excluded, reversibly.**
- **Nothing to license:** BlazBlue Entropy Effect (rank 5, ships as "Entropy Effect X"), Halls
  of Torment (rank 21) — both in the subscription today.

---

## 11. TRACEABILITY INDEX

| Figure | Value | Artifact |
|---|---|---|
| Non-demo catalogue | 122,191 | `sql/20_indie_definition_check.sql` |
| Eligible pool | 573 (42.8% MC) | `23_indie_model_v2.json` / `sql/30` |
| Qualifying | 201 | `23_indie_model_v2.json` |
| Screened / picks | 25 / 21 | `24_availability_indie.md` / `25_indie_portfolio.json` |
| Indie price discount | 30.1% mean, 25.0% median, n=48,682 | `21_indie_thesis.md` §(a) / `sql/32` |
| Titles per $1,000 | 63.47 vs 41.39 (1.53×) | `21_indie_thesis.md` §B-5 / `sql/36` |
| Cost per million owners | $92.81 vs $61.93 (1.50×) | same |
| Portfolio breadth | 50.28 per $1,000 (+21.5%); 40% of edge retained | `25_indie_portfolio.md` [DERIVED] |
| Temtem cut | 53.66 per $1,000 | `25_indie_portfolio.md` [DERIVED] |
| Hit-rate ratios | 72.2 / 45.9 / 35.0 / 29.4% | `sql/35` |
| Survivorship exclusion | 36.9% indie vs 35.1% non-indie | `sql/34` |
| Propensity by bucket | 92–108% (n≥30 buckets) | `sql/33` |
| First-hit rate | 3.13% vs 7.70% (2.5×) | `sql/38` |
| Review floor sweep | 9 rows, plateau at 5,000 | `sql/28` |
| Owners ceiling | 750,000, bucket-equivalent to 1M | `sql/29` |
| Indie definition + hand-check | `is_indie AND dev_title_count ≤ 10` | `sql/27`, `23_indie_v2.md` A-1 |
| Composite vs log reviews | R² 0.775 | `23_indie_model_v2.json` |
| Fit model | r 0.3771–0.3883 OOS; in-population R² −1.3387; weight 0.10 | `12_model_v2_fit.json` |
| Controller quality gap | 40.7% vs 25.5% MC | `20_indie_scoring.md`, verified in `22_redteam_indie.md` A-2 |
| Price-band budget bias | MC 5.7% (≤$2) → 22.5% (>$20) | `11_redteam_scoring.md` RT-04 |
| Pillar cancellation | Spearman −0.762; Scarcity influence 0.030 | `11_redteam_scoring.md` RT-02 |
| Console ARPPU | +47.3% ($81.68 ÷ $55.47) | `04_sources.json` (MIDiA 2024 via Plarium) |
| Annapurna / Humble | Sept 2024 / July 2024 | Bloomberg 2024-09-12 / Forbes 2024-07-23 |
| AAA licensing figures (not used for sizing) | $5M–$300M day-one; $12–15M/mo GTA V | Axios 2023-09-19 |

**Tier membership, tier ordering and the rationale text are authored judgments.** Every
*figure* is joined from the source artifacts by `scripts/25_build_indie_portfolio.py`, which
aborts if a named title is missing from either input.
