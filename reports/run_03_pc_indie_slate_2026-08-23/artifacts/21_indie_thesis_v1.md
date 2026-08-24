# Stage 21 — Testing the indie thesis: cheaper, and higher engagement?

**The claim under test:** indie games are better investments for Game Pass because they
are (a) cheaper and (b) have high user engagement.

This is a separate, even-handed test of that claim — not a defense of the Stage 20
shortlist. It uses a broader population than the shortlist (see below) because the
question is whether indies differ *as a class*, not whether the already-curated
finalists look different.

**Population** (`sql/21_thesis_population.sql`): non-demo, paid, priced titles with
≥10 reviews (Valve's own minimum for a review score to exist at all) — **n = 48,682**.
**Group definition:** the same operational indie definition chosen in Stage 20
(`is_indie=true AND is_self_published=true`) — **indie n = 23,650**; everyone else —
**non-indie n = 25,032** (includes 73 titles with a NULL `is_indie` flag, folded into
non-indie per the non-English-metadata floor documented in `02_cleaning_report.md`).

## What cannot be tested, stated plainly

**Engagement cannot be measured in this dataset.** Every playtime column in
`steamspy_stage` is constant zero across all 140,077 rows (`01_profile.md`,
`02_cleaning_report.md`) — there is no session length, no retention curve, no time-spent
signal anywhere in this data, for indie or non-indie titles. No proxy constructed from
this dataset is engagement, and none is presented as such below. What follows tests the
**nearest measurable things** and states explicitly, for each, what it does and does not
tell you.

## (b) "High engagement" — the nearest measurable proxies

**Review propensity** = `review_total / owners_mid` — reviews left per estimated owner.

*What it might tell you:* a rough, noisy signal of how motivated a game's owners are to
write something down. *What it does NOT tell you:* nothing about session length, return
visits, or time spent — a player can leave one review after finishing a game once and
never touch it again, or play 500 hours and never review it. *Known confounders,
stated up front:* (1) **community/genre norms** — some genres and audiences review far
more actively than others regardless of engagement (competitive/strategy communities
skew vocal; casual/mobile-adjacent genres skew quiet); (2) **solicitation** — larger
studios and live-service titles frequently prompt players in-client to leave a review,
which larger non-indie publishers can afford to instrument more systematically;
(3) **controversy** — review-bombing inflates review count for reasons that have nothing
to do with genuine engagement, and is not evenly distributed across the catalogue;
(4) `owners_mid`'s coarse bucketing (documented since `01_profile.md`) adds noise to the
denominator for both groups symmetrically, which should not bias the *group comparison*
but does widen the noise band on any single title's propensity value.

**Review sentiment** = `review_positive_ratio` — the share of reviews that are positive.
*What it tells you:* a quality-perception signal among people who chose to review.
*What it does NOT tell you:* engagement, or even necessarily overall satisfaction among
non-reviewers — reviewers are self-selected.

Both are reported below, labelled for exactly what they are, alongside reach (`owners_mid`)
and hit rate, which speak to *scale*, not engagement, but bear on the "better investment"
half of the claim regardless.

## (a) "Cheaper" — tested directly

**Confirmed, and it is the strongest, cleanest result in this analysis.** Mean price:
indie $8.02 vs. non-indie $12.24 (indie **34.5% cheaper** on mean). Median: indie $4.99
vs. non-indie $9.54 (indie **47.7% cheaper** at the median) — n=48,682, `sql/22_thesis_
headline_comparison.sql`. This holds in every price band by construction and in every
release-year cohort (see the controlled table below).

**What this does and does not establish, stated explicitly:** retail price on Steam is
**not** Game Pass licensing cost. A cheaper storefront price is a reasonable directional
signal (lower production budgets tend to command lower licensing minimums), but this
dataset contains no licensing-fee data, and no better proxy exists in it either —
`is_self_published` and developer/publisher title counts are already baked into the
indie *definition* itself (Stage 20), so using them again here as a "better cost proxy"
would be circular, not an independent check. **The "cheaper" claim is well-supported at
the retail-price level and unverifiable at the licensing-cost level with this data.**

## Full comparison, unconditional

| | n | mean owners | p90 owners | mean sentiment | mean propensity | mean price | mean release yr |
|---|---|---|---|---|---|---|---|
| **Indie** | 23,650 | 78,008 | 75,000 | **0.7729** | 0.00706 | **$8.02** | 2019.9 |
| **Non-indie** | 25,032 | **189,921** | **349,957** | 0.7626 | **0.00956** | $12.24 | 2019.5 |
| Indie as % of non-indie | — | 41.1% | 21.4% | +1.4pp | 73.8% | 65.5% | +0.4 yr |

**Hit rate** at successive `owners_mid` thresholds (`sql/23_thesis_hit_rates.sql`):

| threshold | indie (n=23,650) | non-indie (n=25,032) | indie as % of non-indie rate |
|---|---|---|---|
| ≥100k owners | 9.01% | 17.71% | 50.9% |
| ≥500k owners | 1.98% | 5.64% | 35.1% |
| ≥1M owners | 0.86% | 3.05% | 28.2% |
| ≥5M owners | 0.14% | 0.44% | 31.8% |

Indie titles reach roughly **half to a third** the hit rate of non-indie titles at every
threshold tested, consistently. Median `owners_mid` is tied at 10,000 for both groups —
this is **not** informative (both groups have the bulk of their titles in SteamSpy's
bottom bucket, per the known resolution hazard); the mean and the hit-rate table, which
are driven by the upper tail, are the metrics that actually distinguish the groups here.

## Controlling for confounders

Indie titles in this population skew only **0.4 years newer on average** (mean release
year 2019.9 vs 2019.5; **median tied at 2020 for both groups**) — a real but modest age
gap, smaller than assumed going in. Indie titles are, by the comparison above, also
substantially cheaper. Both could in principle explain away the reach/propensity gaps.
They do not.

**By release-year cohort** (`sql/24_thesis_cohort_and_price_control.sql`):

| cohort | group | n | mean owners | %≥100k | mean sentiment | mean propensity |
|---|---|---|---|---|---|---|
| ≤2018 | non-indie | 8,763 | 257,362 | 27.15% | 0.7116 | 0.00735 |
| ≤2018 | indie | 7,836 | 122,888 | 15.67% | 0.7215 | 0.00653 |
| 2019–2021 | non-indie | 6,873 | 136,631 | 13.89% | 0.7665 | 0.01035 |
| 2019–2021 | indie | 7,343 | 53,704 | 6.99% | 0.7689 | 0.00744 |
| 2022–2024 | non-indie | 9,016 | 88,233 | 9.58% | 0.8061 | 0.01071 |
| 2022–2024 | indie | 8,347 | 48,734 | 4.30% | 0.8243 | 0.00713 |

The reach gap and propensity gap **persist in every cohort**, at similar or larger
relative magnitude than the unconditional figures — age does not explain them away.
Sentiment's small indie edge also persists in every cohort.

**By price band** (same query): reach and propensity gaps persist in every band from
≤$5 up to >$20, though the gap **narrows sharply at the top**: in the >$20 band, mean
owners are 545,267 (non-indie) vs 485,713 (indie) — far closer than at lower price points
— and **sentiment reverses**: indie 0.7638 vs non-indie 0.7731 in that band alone, the
only band where indie does not lead on sentiment. Price does not explain the gaps away
either, but it visibly compresses them at the premium end, where the remaining "indie"
titles in this dataset (self-published *and* priced above $20) are a much smaller,
likely atypical slice (n=841 vs n=23,650 overall).

## Producer consistency

Among developers with **at least one hit** (`owners_mid≥100,000`, `sql/25_thesis_
producer_consistency.sql`): **10.40% of indie developers (1,575/15,143) ever land one**,
against **19.18% of non-indie developers (2,936/15,307)** — indie developers are roughly
**half as likely to ever produce a hit at all.** But conditional on landing one, the
repeat-hit rate is close: **17.90% of indie hitters repeat vs. 19.55% of non-indie
hitters** — a small, not decisive, gap. **Indie developers are not less consistent once
they succeed; they succeed less often in the first place.**

## Verdict — clearly separated from the scoring rescope above

**(a) Cheaper: TRUE, well-supported.** Indie titles cost 35–48% less at retail,
consistently, across every stratification tested. The one honest caveat: retail price is
not licensing cost, and this dataset cannot bridge that gap.

**(b) Higher engagement: NOT SUPPORTED — the measurable proxies point the other way.**
Engagement itself is unmeasurable here and this is stated as a limit, not sidestepped.
Of the two nearest measurable things:

- **Review propensity** (the closer of the two proxies to "engaged, vocal community")
  favors **non-indie**, not indie — indie titles generate reviews at roughly **74% of
  the non-indie rate per estimated owner**, unconditionally and within every age cohort
  and price band tested.
- **Review sentiment** does favor indie, by a small, real, and fairly robust margin
  (+1.0 to +1.4 percentage points, holding in most strata) — but it reverses at the
  premium price band, and sentiment measures quality perception among reviewers, not
  engagement.
- **Reach and hit rate** — not part of the original claim, but directly relevant to
  "better investment" — favor non-indie decisively: indie titles reach roughly 21–41%
  of non-indie's audience on average and hit meaningful ownership thresholds at
  roughly a third to a half the rate, holding after controlling for age and price.

**Net assessment:** the thesis is **half right**. The cost advantage is real and large.
The engagement advantage, to the extent it can be approximated at all with this data, is
not supported by the two nearest measurable proxies — one is roughly neutral-to-favorable
for indie (sentiment, small and reversing at premium prices) and the other favors
non-indie (propensity, consistently and substantially). Combined with a reach
disadvantage that persists after controlling for the two most obvious confounders, the
strongest honest counterargument is: **indie titles are cheaper, but the closest
measurable stand-ins for "engagement" do not support the idea that they engage
proportionally-owning players more than non-indie titles do — if anything, per-owner
review activity runs the other way, and indie titles reach a meaningfully smaller
audience at every scale tested.** This does not mean indie titles are bad Game Pass
picks — Stage 20's shortlist stands on its own screening logic — but "cheap and highly
engaging" as a blanket justification for an indie-first strategy is not what this
dataset shows; "cheap, and reasonably well-liked by the smaller audience they reach" is
the defensible version of the claim.
