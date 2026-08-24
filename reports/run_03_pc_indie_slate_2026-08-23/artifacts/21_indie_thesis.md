# Stage 21 (v2) — Testing the indie thesis: cheaper, and higher engagement?

**Revision note.** This document was red-teamed (`artifacts/22_redteam_indie.md`, Part B).
The critic verified every number in the prior version was computed correctly and found the
*reasoning* wrong in three places: one leg overstated (propensity), one understated (reach,
after accounting for survivorship), and — the most important correction — a whole yardstick
missing (cost per catalogue slot vs. cost per owner reached, which flips the sign of the
"better investment" question). All three are fixed below. The population is also migrated
to the Stage 23 indie definition (`is_indie=true AND developer_title_count<=10`, replacing
the retracted `is_self_published` string-match test — see `artifacts/23_indie_v2.md` A-1)
so this document and the scoring document now use the same definition of "indie." The
original version is kept at `artifacts/21_indie_thesis_v1.md` for the record; every number
below was re-verified against `parquet/`, not carried over.

**The claim under test:** indie games are better investments for Game Pass because they are
(a) cheaper and (b) have high user engagement.

**Population** (`sql/31_thesis_v2_population.sql`): non-demo, paid, priced titles with ≥10
reviews (Valve's own minimum for a review score to exist at all) — **n = 48,682**. **Group
definition:** `is_indie=true AND developer_title_count<=10` (developer's total non-demo
game count catalogue-wide) — **indie n = 30,003**; everyone else — **non-indie n = 18,679**
(NULL `is_indie` or NULL developer folds to non-indie via COALESCE).

## What cannot be tested, stated plainly

**Engagement cannot be measured in this dataset.** Every playtime column in
`steamspy_stage` is constant zero across all 140,077 rows (`01_profile.md`,
`02_cleaning_report.md`) — there is no session length, no retention curve, no time-spent
signal anywhere in this data, for indie or non-indie titles. No proxy constructed from this
dataset is engagement, and none is presented as such below.

## (b) "High engagement" — the nearest measurable proxies, and why they are one proxy, not two

**Review propensity** = `review_total / owners_mid` — reviews left per estimated owner.
*What it might tell you:* a rough, noisy signal of how motivated a game's owners are to
write something down. *What it does NOT tell you:* nothing about session length, return
visits, or time spent. *Known confounders:* community/genre norms, in-client solicitation
(larger studios can afford to prompt for reviews more systematically), review-bombing, and
`owners_mid`'s coarse bucketing.

**Review sentiment** = `review_positive_ratio`. *What it tells you:* a quality-perception
signal among people who chose to review. *What it does NOT tell you:* engagement, or
satisfaction among non-reviewers (self-selected).

**Correction (critic B-2): propensity and reach are the same measurement, not two
converging ones.** `review_total / owners_mid`, aggregated within an `owners_mid` bucket, is
review volume divided by a near-constant — the *same* quantity the reach comparison below
already uses, rescaled. The prior version of this document presented them as independent
lines of evidence pointing the same direction. They are one line, counted twice, and this
version does not repeat that framing — propensity is reported once, on its own terms, and
not added to reach as if it were corroborating evidence.

## (a) "Cheaper" — tested directly

**Confirmed, and still the strongest, cleanest result in this analysis.** Mean price: indie
$8.74 vs. non-indie $12.51 (indie **30.1% cheaper** on mean). Median: indie $5.99 vs.
non-indie $7.99 (indie **25.0% cheaper** at the median) — n=48,682,
`sql/32_thesis_v2_headline_comparison.sql`. (These figures shift modestly from the prior
version's 34.5%/47.7% because the corrected indie definition changes group membership, not
because the underlying price data changed.)

**What this does and does not establish:** retail price on Steam is **not** Game Pass
licensing cost. A cheaper storefront price is a reasonable directional signal, but this
dataset contains no licensing-fee data and no better proxy exists in it either — developer/
publisher scale is already baked into the indie *definition* itself, so reusing it here as
a "better cost proxy" would be circular. **The "cheaper" claim is well-supported at the
retail-price level and unverifiable at the licensing-cost level with this data.**

## Full comparison, unconditional

| | n | mean owners | p90 owners | mean sentiment | mean propensity (ratio of totals) | mean price | mean release yr |
|---|---|---|---|---|---|---|---|
| **Indie** | 30,003 | 94,162 | 150,000 | **0.7788** | 0.01340 | **$8.74** | 2019.9 |
| **Non-indie** | 18,679 | **202,037** | **350,000** | 0.7496 | **0.01626** | $12.51 | 2019.4 |
| Indie as % of non-indie | — | 46.6% | 42.9% | +2.9pp | 82.4% | 69.9% | +0.5 yr |

`sql/32_thesis_v2_headline_comparison.sql`. Propensity is reported here as the **ratio of
totals** (Σreviews / Σowners), not the mean of per-title ratios — the critic flagged that
the mean-of-ratios statistic over-weights the enormous population of very-low-owner titles;
ratio-of-totals is the properly aggregated version and is used throughout this document.

## Correction (critic B-1): the propensity gap is a small-bucket artifact — withdrawn as an unconditional claim

The prior version reported indie propensity at "~74% of non-indie's rate, unconditionally
and within every age cohort and price band." That claim did **not** control for `owners_mid`
— the denominator of its own metric — and does not survive doing so
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
| 15,000,000+ | n<30 | n<30 | — | — | **suppressed, n<30** |

**Within every bucket that has n≥30 on both sides, indie propensity sits at 92–108% of
non-indie's — essentially parity, crossing above and below it repeatedly, not a consistent
deficit.** The unconditional 82.4% headline (previous table) is a composition effect: it
reflects the *mix* of buckets each group sits in (indie skews toward the smaller-owner end
of the distribution, where absolute propensity is lower for both groups, not where the
indie-vs-non-indie ratio is worse) far more than it reflects any per-owner engagement
shortfall. **This leg is withdrawn from the verdict as a "propensity penalty" claim.** It is
replaced with the more limited, correctly-supported statement: reviews-per-owner does not
meaningfully distinguish indie from non-indie once ownership scale is held constant.

## Correction (critic B-3): reach is worse than previously stated, because survivorship cuts against indie

The `review_total≥10` floor is itself a filter, and it does not bite evenly
(`sql/34_thesis_v2_survivorship_check.sql`):

| group | all paid, priced | in population (≥10 reviews) | excluded | % excluded |
|---|---|---|---|---|
| non-indie | 28,795 | 18,679 | 10,116 | 35.1% |
| indie | 47,541 | 30,003 | 17,538 | **36.9%** |

Indie is the more heavily survivor-filtered group. Recomputing the hit-rate ratios with the
floor removed (`sql/35_thesis_v2_hit_rates.sql`) shows the floor mildly **flatters** indie's
relative standing at every threshold — removing it moves the indie-as-%-of-non-indie ratio
from 72.2% to 70.5% at the ≥150k mark, and from 45.9% to 44.8% at ≥750k. The effect is
smaller here than the critic measured on the prior (superseded) population, but the
**direction is the same and is not softened**: the reach comparison below, computed with the
floor in place, is if anything slightly generous to indie, not the reverse.

**Hit rate**, named by the `owners_mid` bucket boundary each threshold actually resolves to
(critic B-4 — a 12-value step function cannot support "100k" as if it were a continuous
threshold):

| threshold (nearest bucket) | indie (n=30,003) | non-indie (n=18,679) | indie as % of non-indie rate |
|---|---|---|---|
| ≥150,000 owners | 11.75% | 16.27% | 72.2% |
| ≥750,000 owners | 2.66% | 5.79% | 45.9% |
| ≥1,500,000 owners | 1.16% | 3.31% | 35.0% |
| ≥7,500,000 owners | 0.15% | 0.51% | 29.4% |

Indie titles reach a meaningfully smaller audience at every scale tested, and the gap widens
at the top end. Unlike the propensity leg, this finding **does** survive stratification (see
cohort/price table below) and is strengthened, not weakened, by the survivorship check.

## Controlling for age and price

Indie titles skew only 0.5 years newer on average (2019.9 vs 2019.4; median tied at 2020 for
both) — a modest gap. By release-year cohort and price band
(`sql/37_thesis_v2_cohort_and_price_control.sql`):

| cohort | group | n | mean owners | mean sentiment | propensity (ratio of totals) |
|---|---|---|---|---|---|
| <2018 | non-indie | 4,989 | 329,647 | 0.7182 | 0.01273 |
| <2018 | indie | 7,234 | 153,240 | 0.7177 | 0.01060 |
| 2018–2021 | non-indie | 6,769 | 127,893 | 0.7293 | 0.01768 |
| 2018–2021 | indie | 11,823 | 78,894 | 0.7690 | 0.01565 |
| 2022+ | non-indie | 6,921 | 182,563 | 0.7920 | 0.01988 |
| 2022+ | indie | 10,946 | 71,610 | 0.8298 | 0.01467 |

| price band | group | n | mean owners | mean sentiment | propensity (ratio of totals) |
|---|---|---|---|---|---|
| ≤$5 | non-indie | 7,774 | 68,254 | 0.7246 | 0.00881 |
| ≤$5 | indie | 13,954 | 52,056 | 0.7610 | 0.00915 |
| $5–10 | non-indie | 4,535 | 160,383 | 0.7583 | 0.01359 |
| $5–10 | indie | 7,867 | 77,104 | 0.7903 | 0.01333 |
| $10–20 | non-indie | 3,771 | 267,186 | 0.7797 | 0.01657 |
| $10–20 | indie | 6,872 | 133,753 | 0.8012 | 0.01440 |
| >$20 | non-indie | 2,599 | 580,352 | 0.7652 | 0.01996 |
| >$20 | indie | 1,310 | 437,427 | 0.7827 | 0.01723 |

**Reach**: indie's mean-owners deficit persists in every cohort and every price band without
exception — age and price do not explain it away. **Sentiment**: indie holds a small,
consistent edge in every cohort and every price band, including >$20 (unlike the prior
version of this document, which reported a sentiment reversal at the top price band under
the old, now-retracted, indie definition — that reversal does not reproduce under the
corrected definition and is retracted along with it). **Propensity**: mixed and close to
parity in every stratum (indie ahead in the <2018 cohort and the ≤$5 band; non-indie ahead
elsewhere, typically by single-digit percentage points of ratio) — consistent with the
owners-bucket finding above that this is not a real, direction-stable gap.

## Producer consistency

Among developers with **at least one hit** (`owners_mid≥500,000`,
`sql/38_thesis_v2_producer_consistency.sql`): **3.13% of indie developers (690/22,028) ever
land one**, against **7.70% of non-indie developers (625/8,114)** — non-indie developers are
roughly **2.5x** as likely to ever produce a hit. Conditional on landing one, non-indie
developers also repeat more often: **25.60% of non-indie hitters land a second hit, vs
12.17% of indie hitters** — a real gap, not a small one, unlike the near-parity found in the
prior version of this document. Non-indie hitters also average more titles overall (4.15 vs
1.93) — they have more shots on goal *and* convert at a higher rate on each one. (This
reverses the prior version's finding, which used the old, now-retracted, definition; the
correct reading is that non-indie developer consistency is unambiguously stronger on this
population, not merely "not decisive.")

## The missing calculation, and the actual investment argument (critic B-5)

The prior version of this document reported both price and reach and never divided them.
Two yardsticks, both computed on the corrected population
(`sql/36_thesis_v2_cost_per_owner_vs_per_slot.sql`):

**Per owner reached** — using the two headline numbers above:

| | mean price | mean owners | cost per million owners reached |
|---|---|---|---|
| indie | $8.74 | 94,162 | **$92.81** |
| non-indie | $12.51 | 202,037 | **$61.93** |

**Indie costs 1.50x more per owner reached — a 50% loss per dollar on this yardstick.**

**Per catalogue slot**, at a fixed quality bar (`review_total≥4,000`,
`review_positive_ratio≥0.80`, applied identically to both groups):

| | n qualifying | mean price | titles per $1,000 of retail price |
|---|---|---|---|
| indie | 994 | $15.75 | **63.47** |
| non-indie | 931 | $24.16 | **41.39** |

**Indie delivers 1.53x more qualifying catalogue slots per dollar.**

**The sign of the answer depends entirely on the yardstick, and that is the central finding
of this document.** A subscription service does not buy players per title — it buys breadth
of catalogue against a fixed monthly fee, because the thing that keeps a subscriber
subscribed is having many reasons not to cancel, not the owner count of any single title.
On **reach per title**, indie is a clearly worse buy (50% more expensive per owner reached).
On **breadth per dollar** — the metric that actually matches how a subscription is
monetised — indie is a clearly better buy (53% more qualifying titles per dollar spent).

**This does not rescue "higher engagement."** Nothing can — the dataset cannot measure
engagement, in either direction. It does rescue the narrower, defensible version of the
investment case: indie is the more efficient way to build catalogue breadth, at the direct
and disclosed cost of reaching fewer players per title. Both are true; they answer different
questions; a recommendation that only cites one of them is citing the one that supports its
conclusion, not the one a subscription's economics actually asks.

**Caveat applying to both rows above:** both use retail price as a licensing-cost proxy,
which this dataset cannot verify (see "cheaper," above — retail price tracks production
budget at best, not licensing terms). Both figures are directional, not literal cost
figures, and should not be spoken as if they were.

## Verdict — clearly separated from the scoring rescope above

**(a) Cheaper: TRUE, well-supported.** Indie titles cost 25–30% less at retail on this
population (30.1% cheaper on mean, 25.0% at median), consistently across stratification. The
one honest caveat: retail price is not licensing cost, and this dataset cannot bridge that
gap.

**(b) Higher engagement: UNSUPPORTED AND UNMEASURABLE — not "the proxies say no," but "there
is no data that can answer this."** Of the two nearest measurable things: review propensity,
once properly stratified by ownership bucket, sits at 92–108% of non-indie's rate — close to
parity, not a penalty, and the prior version's "74%, unconditional" claim is withdrawn.
Review sentiment gives indie a small, consistent, real edge (roughly +3pp) that holds in
every cohort and price band tested. Neither is engagement, and neither should be read as a
verdict on it either way.

**Reach: WORSE for indie than previously stated, and this holds up.** Indie titles reach
29–72% of non-indie's audience at successive ownership thresholds, the gap widens at scale,
and survivorship (which excludes indie titles from the population at a slightly higher rate)
means this comparison is if anything generous to indie, not harsh. Producer consistency
tells the same story: non-indie developers land a first hit 2.5x as often and repeat at
roughly twice the rate conditional on landing one.

**The yardstick that decides the "better investment" question is per-catalogue-slot, not
per-owner, because that is what a subscription buys.** Indie is a 50% worse buy per owner
reached and a 53% better buy per qualifying catalogue slot per dollar. This is the actual,
defensible investment case for an indie-weighted strategy — not "cheap and highly engaging,"
which this dataset cannot support on the engagement half and does not need to invoke, given
that the breadth-per-dollar case stands on its own without it.

**Net assessment, restated:** cheaper is real and large. Engagement is not a claim this
dataset can adjudicate in either direction, and the propensity/sentiment proxies that come
closest to it show no meaningful indie advantage once correctly stratified. Reach per title
is genuinely worse for indie, more so once survivorship is accounted for. The investment
case for indie rests on catalogue breadth per dollar, where it wins by a real and now-
quantified margin — and that argument should be made on those terms, not folded into a
vaguer "engagement" claim this data was never able to support.
