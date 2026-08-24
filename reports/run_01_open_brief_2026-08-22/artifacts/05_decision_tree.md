# Game Pass catalogue investment — decision tree

One page. Every branch ends in an action, including the ones that spend money.

---

## START — approve today: **$0**

Run a **6–8 week internal audit**. It costs nothing and uses data Microsoft already holds. Five questions:

1. Does retention attribution already exist internally?
2. Is console telemetry retained at sufficient grain to build it?
3. Can a randomised subscriber holdout be run legally in the main markets?
4. **Can the catalogue-to-retention effect be measured retrospectively from the existing 500+ Game Pass deals?** ← *the question that decides everything below*
5. What did the April 2026 price rollback cost per retained subscriber? *(reported as a range with its caveat — an input, not a trigger; see footnote)*

**Why $0 first:** Microsoft has already run 500+ catalogue deals and already spent an estimated $420M–$1.26B/year against churn on price. Both are large natural experiments, already paid for, sitting unanalysed. Buying a $30M experiment before reading them would be indefensible.

---

## Then follow Q4's answer

### ▶ BRANCH A — the retrospective WORKS and the effect is POSITIVE
*Trigger: effect statistically distinguishable from zero and visible on licence **expiries**, not only on additions. Expiry timing was set by contracts signed years ago, so it is closer to exogenous.*

**Do NOT run the experiment — you already have the answer.** Instead:

1. Spend **~$1–2M / 8–12 weeks** on the pool recomputation: net the candidates against Game Pass's existing ~500 titles, sweep rights availability, apply the console-penetration screen.
2. Size a standing annual programme with this rule:

> **Break-even = 0.025 percentage points of annual churn per title-year.**
> 1pp of annual churn = 300,000 subscribers × $168 × 60% margin = **$30.24M/year**.
> A $1.5M licence over 24 months = **$750K per title-year**.
> $750K ÷ $30.24M = **0.0248pp**.

**Above 0.025pp per title-year → licensing pays. Scale to the pool ceiling.**
**Below → it does not pay at $1.5M. Negotiate price down or stop.**

*Worked shape:* 0.5pp measured across a 50-title cohort-year = 0.01pp/title = $302K against a $750K cost → **fails at 2.5×**. 2.0pp across the same cohort = 0.04pp/title = $1.21M against $750K → **clears comfortably**.

**Annual spend** = (titles licensable per year) × (price), capped where marginal effect drops below marginal price, bounded above by the netted pool. Order of magnitude only: 650 Steam-screened titles × $1.5M ≈ **$975M** for a one-time full sweep — so a standing programme is bounded in the high hundreds of millions in the limit, and realistically well below.

**Why no annual figure is named today:** the netted pool is the term that sets it, and it is genuinely unknown — 646–652 is *before* netting, *before* rights, and *before* a console-penetration screen this dataset cannot support. Branch A is also **better-founded than today's estimate**, because a working retrospective replaces the three unsourced inputs in the rule above (30M subscribers, $14 ARPU, 60% margin) with measured internal values.

---

### ▶ BRANCH B — the retrospective returns NULL or cannot identify the effect
*Trigger: title selection was non-random, no holdout ever existed, effect indistinguishable from zero.*

**Approve the $30M tranche** — 20 titles, 24-month windows. An experiment is what you buy when observation has failed.

Four preconditions, all before signature:
- **(a)** net the pool against titles already in Game Pass
- **(b)** confirm rights and pricing on ~60 candidates before committing to 20
- **(c)** screen on high recognition × **low console penetration** — never on Steam rank
- **(d)** write **per-title randomisation** (staggered territory/date windows) into the licence terms — *free before signature, impossible after*

**Kill rule:** no significant 12-month churn difference vs. control, or cost per retained subscriber-year above ~$100 contribution margin → stop, do not continue.

*20 titles is a bounded judgement, not a derivation. Power comes from subscriber n, not title count; title count sets dose, and the required dose is the unknown being measured.*

---

### ▶ BRANCH C — the retrospective shows a NEGATIVE or negligible effect
*Or: the price-action range sits clearly below the ~$100 hurdle.*

**Drop the catalogue argument.** Commit no catalogue capital, redirect the renewal book to cost reduction on existing deals, report the finding. This is a legitimate terminal outcome, not a failed analysis.

---

## Separately, and independent of all three branches

**Studio-side capital (T3-prime):** route any commitment carrying permanent headcount, or whose exit cost cannot be absorbed within one fiscal year, to the board as an **escalation** — not a prohibition — with the corrected reference-class hit rate attached.

> **Use 12.59%, not 1.01%.** The whole-Steam base rate is the wrong reference class for a studio commitment by 12.5×.
> **Bound it every time:** 87% of those hits (92 of 106) reach only 1–5M owners, and the class conditions on titles that shipped from publishers already holding 20+ titles. Reaching 1M owners is not returning a studio-scale commitment. 12.59% is a **ceiling**, not an estimate.

No dollar threshold is proposed — a content-licensing price ceiling cannot calibrate an equity threshold, and no FY27 envelope figure is available here.

---

### Footnote — why Q5 is an input, not a trigger

The April 2026 rollback was a **universal price change with no holdout**. There is no clean counterfactual churn path at $29.99. The interrupted time series is confounded with the July 2026 restructuring, catalogue turnover, competitor launches and seasonality — partial identification at best. The ~$100 hurdle it would be compared against is itself three unsourced assumptions stacked. So it is reported **with bounds, never as a point estimate**, and it weights the branches rather than deciding them.

**What would make it decidable, at no cost:** run the **next** price action with a regional or cohort holdout. That yields a directly identified cost per retained subscriber and settles price-vs-catalogue permanently.
