# Stage 22 — Red team of the indie rescope and the indie thesis

Two targets: the scoping (Stage 20) and the thesis document (Stage 21). Every figure below
was re-executed against `parquet/`.

**What reproduced exactly** — and this is worth saying before the objections, because it is
most of both artifacts. Stage 20: eligible pool **406** (34.5% metacritic), qualifying
**138**, no-controller share **48/138 = 34.8%**, controller gate **802 → 1,179**, metacritic
**40.7% vs 25.5%** across the gate, indie definition **67.6% / 36.8% / 122,191**. Stage 21:
**every single headline number**, to the decimal — mean price $8.02/$12.24, median
$4.99/$9.54, n=48,682 (23,650/25,032), mean owners 78,008/189,921, p90 75,000/349,957,
sentiment 0.7729/0.7626, propensity 0.00706/0.00956, all four hit rates (9.01/17.71,
1.98/5.64, 0.86/3.05, 0.14/0.44), the full cohort table, the price-band sentiment reversal
at >$20 (0.7638 vs 0.7731), and producer consistency (10.40 / 19.19 / 17.90 / 19.58 against
published 10.40 / 19.18 / 17.90 / 19.55 — rounding only). The arithmetic is sound
throughout. The objections below are about definitions, controls and framing, not errors.

---

# Part A — The scoping

## A-1. The indie definition splits on the wrong axis. It excludes the canonical indies and admits the shovelware factories. **MATERIAL → rebuild the definition.**

`is_self_published` is a **literal `developer == publisher` string equality**. Verified:

| title | developer | publisher | `is_self_published` |
|---|---|---|---|
| Return of the Obra Dinn | Lucas Pope | **3909** | **False** |
| Papers, Please | Lucas Pope | **3909** | **False** |
| Baba Is You | Hempuli Oy | Hempuli Oy | True |

"3909" is Lucas Pope's own one-man label. Two of the most canonical independent games ever
made are classified **non-indie by a string mismatch**, while Baba Is You passes. That is
not a structural signal; it is a name-collision test.

**What the definition excludes** — `is_indie=true`, clearing every other screen, rejected
only for having a publisher:

> What Remains of Edith Finch (MC **89**, Annapurna) · Return of the Obra Dinn (MC **89**) ·
> ENDER LILIES (MC **86**) · Unpacking (MC 83) · ABZU (MC 83) · Temtem (MC 79) ·
> VA-11 Hall-A (MC 77) · Journey · SANABI · Potion Craft · Firework · The Hungry Lamb

Annapurna, Humble, tinyBuild, Devolver-type labels **are** indie publishers. Signing with
one is the definition of indie success, not evidence of not being indie. The screen removes
the segment's best-regarded work.

**What the definition admits** — self-published publishers with large catalogues:

> EroticGamesClub (**180** titles) · Choice of Games (158) · Boogygames Studios (128) ·
> Hosted Games (109) · Sokpop Collective (93) · Cyber Keks (73) · Blender Games (71) ·
> EpiXR Games UG (68) · RewindApp (68)

- **Objection:** the definition asks "did the developer sign a publishing deal?" The
  question that matters is "is this a small independent operation?" Those are different
  axes, and the mismatch is not marginal — it is systematically wrong at **both** ends: high
  false-negative rate exactly at the top of the quality distribution, high false-positive
  rate across the asset-flip tail. `is_indie` and `is_self_published` are also only weakly
  associated (P(self-pub | indie) = 54.4% vs P(self-pub | not indie) = 37.6%), so the second
  flag is adding a genuinely different — and wrong — dimension, not sharpening the first.
- **Evidence:** above; `sql/20_indie_definition_check.sql` reproduces exactly.
- **Resolution:** define indie by **scale**, not by the presence of a publishing deal — the
  `publisher catalogue size ≤ N` alternative the analyst tested and rejected. It was
  rejected for having an arbitrary cutoff, but an arbitrary threshold that is *testable by
  sensitivity* beats a clean binary that is *wrong by construction*; a string match has no
  sensitivity analysis available to it at all. A publisher-title-count rule restores Obra
  Dinn, Edith Finch and Unpacking and excludes the 180-title factories. Report the pool at
  N ∈ {3, 5, 10, 25} and pick from the curve.

## A-2. "The Fit model already handles controller support" is technically true and practically empty. **MATERIAL.**

The coefficient claim **verifies**: `has_controller_i = +0.0387` is the single strongest
positive coefficient in `12_model_v2_fit.json`. But the inference from it does not survive.

- The whole coefficient range is **[−0.0851, +0.0387]** on a target (`review_positive_ratio`)
  spanning ~0.70–1.00; Fit is then percentile-ranked and weighted **0.10**; and the model's
  in-population **R² = −1.34** (worse than predicting the mean), carried forward unchanged
  from Stage 15's A-4 finding.
- **Direct evidence the demotion is inert:** **KovaaK's ranks #11** with `fit_pct = 0.0395`
  (bottom 4% of the pool on Fit). **Verdun ranks #19** with `fit_pct = 0.0099` (bottom 1%).
  A pillar that leaves bottom-1%-on-Fit titles inside the top 20 is not "handling" anything.
- The gate's cost is real and the analyst measured it honestly: metacritic **40.7%**
  (controller, n=241) vs **25.5%** (no controller, n=165). Verified exactly.
- **Objection:** dropping the gate is **correct** on PC grounds — that part of the rescope
  is right, and I said in RT-11 that the gate was a *console* proxy. The error is the claim
  that drop and demote are "the same outcome in practice." They are the same outcome only
  because the demotion does nothing. The artifact should say the gate was dropped and
  **nothing replaces it**, then decide whether the measured 15.2pp quality gap is acceptable.
- **Resolution:** if the quality gap matters, use **metacritic presence** as an explicit
  tiebreaker or tier condition — it is a directly measured, independent signal already in
  the data — rather than a 10%-weighted pillar with negative in-scope R².

## A-3. The 48 keyboard-only qualifiers are a different product, and the artifact names the trade without pricing it. **MINOR→MATERIAL.**

34.8% verified. The no-controller cohort is led by **KovaaK's** (an aim trainer, not a
game), **The Room** and **The Room Two** (touch-first mobile ports), **Milk outside a bag of
milk**, **There Is No Game**, **Your Only Move Is HUSTLE** — six of them inside the top 20.
Metacritic presence among the newly admitted 165 is 25.5%. On PC these are all legitimately
playable; the objection is that a PC Game Pass tier led by an aim trainer and two mobile
ports is a positioning decision, not a scoring by-product, and it is not surfaced as one.
**Resolution:** report the no-controller share **per tier**, so the board sees that the
Anchor tier — the tier meant to lead — is where they cluster.

## A-4. The review-floor sensitivity was truncated exactly where it stops supporting the inherited threshold. **MATERIAL.**

The analyst was told to re-derive rather than inherit. It ran the re-derivation, then quoted
four of nine rows:

| floor | 500 | 1,000 | 2,000 | 3,000 | **4,000** | 5,000 | 6,000 | 7,500 | 10,000 |
|---|---|---|---|---|---|---|---|---|---|
| n | 2,057 | 1,302 | 775 | 526 | **406** | 330 | 254 | 196 | 116 |
| metacritic % | 23.2 | 28.1 | **33.4** | **35.4** | **34.5** | **34.2** | **37.0** | **37.2** | **37.9** |

**Bolded four** are the ones quoted ("33.4 / 35.4 / 34.5 / 34.2 … flat-to-noisy"). Correct —
and the range stops at 5,000. At **6,000 / 7,500 / 10,000** metacritic density rises
**monotonically to 37.0 / 37.2 / 37.9%**, a clear 2.5–3.4pp above 4,000.

- **Objection:** "no floor in that range clearly dominates 4,000" is true only because the
  range was cut one row before the answer changes. On the document's **own** stated
  criterion — metacritic-presence density — the data points to **6,000 or higher**. A
  re-derivation that returns the inherited number because it was read selectively is not a
  re-derivation.
- **Resolution:** publish all nine rows, and either move the floor to 6,000 (n=254) or state
  explicitly that pool size was traded against recognition density and name the exchange
  rate. Note this also partially fixes A-5: a higher floor thins the novelty tail.
- **Ownership ceiling:** re-derived correctly and the bucket-equivalence disclosure is
  honest. Verified: n is **identical at 350k and 500k (233)** and **identical at 750k and 1M
  (406)**. 173 of 406 titles (42.6%) sit at the single value `owners_mid = 750,000`.

## A-5. The top-20 drift is real, and the mechanism is not price — it is that the composite is a review-count ranking. **MATERIAL.**

First, the hypothesis the coordinator offered, tested and **rejected**: this is *not* a price
effect. Spearman(composite, price) = **−0.102**; top-20 median price $9.99 against $14.99
for the eligible pool. Mild, not causal.

The actual mechanism, measured: **every one of the top 20 has `owners_mid` ∈ {350,000;
750,000} — two values.** Headroom = `ln(reviews) − ln(owners)` is therefore
`ln(reviews)` minus one of two constants, and Recognition is the percentile of `ln(reviews)`.
So **0.90 of the composite is one variable: log review count.** (This is Stage 15's A-3
finding, now degenerate: two levels instead of three.)

Within a self-published pool capped at 750k owners, the titles with the highest raw review
counts are exactly those with the highest **reviews-per-owner** — short, cheap, memorable,
high-completion, meme-adjacent. That is Refunct (~30 minutes), Milk outside a bag of milk,
KovaaK's, Your Only Move Is HUSTLE, Touhou Mystia's Izakaya. The drift is not a bug in the
tier rules; it is what a review-count ranking selects for in this population.

**The cross-artifact contradiction, and the strongest single finding of this pass:**
`21_indie_thesis.md` devotes its central methodological section to warning that
reviews-per-owner is confounded by community/genre norms, in-client solicitation and
review-bombing, and **varies systematically by segment**. `20_indie_scoring.md` builds
**90% of its composite** on precisely that quantity. The two artifacts cannot both be right.

- **Stated in the rescope's favour:** metacritic presence in the top 20 is **8/20 (40.0%)**
  against 34.5% in the eligible pool. The list is **not** degraded the way v1's was — this
  is drift toward *short and novel*, not toward junk, and that distinction is real.
- **Resolution:** raise the review floor per A-4; and either add a duration/scope proxy the
  data supports or accept and *label* the tilt — "high-completion, high-recall short-form
  titles" is a defensible Game Pass thesis if it is chosen, and indefensible if it is
  arrived at by accident.

---

# Part B — The thesis document

## B-1. The propensity conclusion does not survive the one control that matters. **FATAL to that leg.**

The document controls for **release cohort** and **price band**. It never stratifies by
**owners bucket** — the denominator of its own metric. Doing so:

| `owners_mid` | 10,000 | 35,000 | 75,000 | 150,000 | **350,000** | 750,000 | 1.5M | **3.5M** | 7.5M | **15M** |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 31,209 | 7,234 | 3,674 | 2,565 | 2,119 | 915 | 513 | 311 | 91 | 29 |
| indie as % of non-indie | **71.2** | 79.5 | 88.2 | 86.0 | **100.9** | 93.9 | 90.9 | **102.3** | 95.1 | **103.0** |

Monotone convergence to parity, **reversing in three buckets**. The headline "**73.8%**" is
driven almost entirely by the `owners_mid = 10,000` bucket, which holds **31,209 of 48,682
titles (64.1%)** and where the denominator is a bucket **midpoint for a 0–20,000 range** —
a constant fiction applied to titles whose true ownership varies by orders of magnitude.

Compounding it: the document reports the **mean of ratios** (73.8%). The properly aggregated
**ratio of totals** is 0.01276 / 0.01592 = **80.2%** — a materially smaller gap.

- **Objection:** "indie titles generate reviews at roughly 74% of the non-indie rate per
  estimated owner, **unconditionally and within every age cohort and price band tested**" is
  not supportable. The defensible statement is: *below ~100k owners indie propensity runs
  10–29% lower; at and above ~350k owners the gap closes to zero or reverses.* Since the
  Stage 20 shortlist lives entirely at 350k–750k owners, the propensity penalty **does not
  apply to the titles actually being recommended** — which the document never notices.
- **Severity: FATAL** to the propensity leg, which the verdict calls "the closer of the two
  proxies" and leans on hardest.

## B-2. Propensity is disclaimed as an engagement proxy and then used as one. **MATERIAL.**

The document states "no proxy constructed from this dataset is engagement, and none is
presented as such." Its verdict then reads: "**the closest measurable stand-ins for
'engagement' do not support** the idea that they engage … players more … per-owner review
activity runs the other way." A disclaimer contradicted by the conclusion it introduces is
not a disclaimer; it is a hedge that lets the claim be made and defended simultaneously.

Worse, **propensity and reach are not independent evidence.** Within a bucket,
`review_total / owners_mid` is review volume divided by a constant — the *same* measurement
as the reach finding, rescaled. The document presents them as two lines converging on one
answer. They are one line, counted twice.

**Resolution:** either delete the propensity leg or restate it as "review volume, banded by
owner bucket," and drop it from the verdict.

## B-3. Survivorship cuts **against** indie. The negative reach finding is **understated**, not overstated. **Credit — but say so.**

The `review_total ≥ 10` floor is itself a survivorship filter, and it bites unevenly:

| group | all paid, priced | in population (≥10 reviews) | excluded | **% excluded** |
|---|---|---|---|---|
| non-indie | 36,998 | 25,032 | 11,963 | **32.3%** |
| indie | 39,338 | 23,650 | 15,688 | **39.9%** |

Indie is the **more heavily survivor-filtered** group by 7.6pp. Recomputing hit rates with
the floor removed:

| threshold | published ratio | **floor removed** |
|---|---|---|
| ≥100k owners | 50.9% | **46.3%** (5.68% vs 12.27%) |
| ≥1M owners | 28.2% | **25.1%** (0.52% vs 2.07%) |

- **Direction and magnitude:** the floor **flatters indie** by roughly **3–5 percentage
  points of ratio**. The true indie reach deficit is *wider* than the document reports.
- **Objection is presentational, not analytical:** the conclusion is conservative, which is
  the right way to be wrong. But the document does not say so, and a hostile reader will
  assume survivorship runs the other way — that failed indies vanish while AAA persists. On
  Steam, delisting is rare and the binding filter is the review floor, which removes indie
  titles *more* often. State it, and the negative finding gets stronger.

## B-4. A hit rate on a 5-level step function cannot carry "28–51%" as a range. **MATERIAL.**

`owners_mid` takes 12 distinct values catalogue-wide. **None of the four thresholds falls on
a bucket boundary:** "≥100,000" resolves to "≥ the 150,000 midpoint" (the 75,000 midpoint
fails it); "≥500,000" resolves to "≥ the 750,000 midpoint." The thresholds are not the
thresholds they are named after.

- **Objection:** the four ratios are four readings of the same handful of bucket edges, not
  samples from a continuum. The direction is sound and robust — indie is genuinely
  under-represented in the upper tail at **every** cut, and that conclusion stands. The
  **"28–51% of non-indie's rate"** framing does not: two significant figures and a range
  imply a resolution the step function cannot deliver.
- **Resolution:** name the bucket midpoint each threshold actually resolves to, present four
  discrete comparisons, and state the conclusion directionally.

## B-5. The yardstick. This is the calculation that flips the sign, and the document does not run it. **MATERIAL — the finding the thesis is missing.**

**Per owner reached**, using the document's own two headline numbers:

| | retail price | mean owners | **cost per million owners** |
|---|---|---|---|
| indie | $8.02 | 78,008 | **$102.81** |
| non-indie | $12.24 | 189,921 | **$64.45** |

**Indie costs 1.60× more per owner reached — a 60% loss per dollar.** The document reports
both inputs (65.5% on price, 41.1% on owners) and never divides them. On the reach yardstick
the cost advantage does **not** compensate, and the negative result is *understated*.

**Per catalogue slot at a fixed quality bar** (`review_total ≥ 4,000`, `ratio ≥ 0.80`):

| | n qualifying | mean price | **titles per $1,000 of retail proxy** |
|---|---|---|---|
| indie | 574 | $15.34 | **65.2** |
| non-indie | 1,351 | $21.72 | **46.0** |

**Indie delivers 1.42× more qualifying catalogue per dollar.**

- **The sign of the answer depends entirely on the yardstick.** A subscription monetises
  breadth against a fixed fee — many reasons not to cancel — not units per title. On
  breadth-per-dollar indie wins by 42%; on reach-per-title it loses by 60%. **The document
  scores indie exclusively on the second and never names the first.**
- **Does this rescue the thesis? Partly, and not the claim as stated.** It rescues *"indie is
  the right buy for a subscription"* — on breadth-per-dollar it is, by a real margin, and
  that is the business Xbox is actually in. It does **not** rescue *"indie has higher
  engagement,"* which remains unsupported and, per the dataset's constant-zero playtime
  columns, unmeasurable. The document's verdict answers a question about per-title
  performance that a subscription does not ask.
- **Caveat applying to both rows:** each uses retail price as a licensing proxy, which RT-04
  established is a **production-budget** proxy. Both are directional only, and neither should
  be spoken as a cost figure.

## B-6. Producer consistency: correct, with an unstated nuance that runs against indie. **MINOR.**

Reproduces (10.40 / 19.19 / 17.90 / 19.58). Unreported: indie hitters carry **more** titles
than non-indie hitters (mean **2.75 vs 2.59**) — more shots on goal — and **still** repeat
less often. Controlling for catalogue size would **widen** the repeat gap, not close it.
"Not decisive" is fair; "**indie developers are not less consistent once they succeed**" is
slightly generous to indie and should be softened.

---

# Verdicts

**Scoping (Stage 20): REBUILD.** Not for the rescope's logic — dropping the console gate is
correct, and the honesty about Headroom's degeneracy and the controller quality gap is
better than most of this run. Rebuild because the **definition is the scope**, and it is
wrong at both ends (A-1): it excludes Obra Dinn, Edith Finch, Unpacking and Journey on a
string mismatch while admitting 180-title asset-flip publishers. Two further changes:
publish the full nine-row floor sensitivity and move the floor to 6,000 (A-4), and stop
claiming Fit compensates for the dropped gate (A-2).

**Thesis document (Stage 21): the negative conclusion is CORRECTLY COMPUTED BUT INCORRECTLY
REASONED — overstated on one leg, understated on another, and mis-framed overall.**

- **Overstated: propensity.** Does not survive stratification by owners bucket; converges to
  parity and reverses above 350k owners — the range where the shortlist actually sits (B-1).
  This leg should be withdrawn from the verdict.
- **Understated: reach and hit rate.** Survivorship runs against indie (B-3), and the
  document's own numbers imply a 60% per-owner cost disadvantage it never computes (B-5).
  Both make the negative finding stronger than stated.
- **Mis-framed: the yardstick.** Reach-per-title is not the objective a subscription
  optimises. On breadth-per-dollar the sign reverses and indie wins by 42% (B-5). This does
  not rescue "higher engagement" — nothing can, the data cannot measure it — but it does
  rescue the investment case the thesis was convened to test.

**The defensible one-line verdict the document should have reached:** *indie titles are
substantially cheaper and reach a smaller audience; per owner that is a losing trade, per
catalogue slot it is a winning one, and since a subscription buys catalogue slots, the
cost advantage is real — but "high engagement" is not a claim this dataset can support in
either direction.*

---

# The three questions a hostile board member will ask

1. **"Your own thesis paper says reviews-per-owner is confounded and unreliable. Your
   scoring model is 90% reviews-per-owner. Which of your two documents should I believe?"**
   Both are defensible in isolation and they contradict each other. Fix before the room:
   either the thesis softens its warning or the composite stops resting on the metric.

2. **"You've excluded What Remains of Edith Finch and Return of the Obra Dinn from an
   *indie* portfolio — and included a publisher with 180 titles. Explain the definition."**
   The honest answer is that `is_self_published` is a developer-equals-publisher string
   match and Lucas Pope's label is called "3909." That answer cannot be given in a board
   room. Rebuild the definition first.

3. **"You told me indie is cheaper. You also told me it reaches 41% of the audience. That's
   a worse deal per player — so why is this the recommendation?"**
   Because a subscription buys catalogue slots, not players per title: 65.2 qualifying
   titles per $1,000 against 46.0. That is the winning answer and it is not in either
   document. Put it in the pitch before someone else does the division.
