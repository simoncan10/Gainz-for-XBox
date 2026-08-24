# Stage 6 — Red-team verification, round 2

Narrow pass against `05_theses_v2.json` and Round 2 of `05_responses.md`. Conceded objections
are not re-litigated. Three questions only: did the concessions change the theses or only the
prose; are the new numbers sound; did anything new and unsupported enter.

---

## 1. Did the concessions actually change the theses?

Round 1's failure mode — conceding an objection's form while leaving its substance standing —
does not recur. I checked each of the six numbered objections by grepping v2 for the original
figure and confirming it survives only inside an explicit "v1 claimed X, corrected to Y"
retrospective, never as a live claim.

| Obj | v1 figure | Status in v2 | Real or cosmetic |
|---|---|---|---|
| **R1** | $90M/yr steady state; pool 1,160; "roughly 5%" | All three **absent as live claims**. A `no_steady_state` field states no annual figure is offered and that a board-facing one "would be fabricated". Title count re-derived from design, not inventory. | **Real** |
| **R4** | base rate 1.01% as T3's load-bearing leg | T3 withdrawn. T3-prime carries **no base-rate claim at all**; 12.59% survives only as the falsifier's benchmark, explicitly bounded as a ceiling. | **Real** |
| **R5** | two central deal prices ($1.0M / $1.5M) | Single stated price: $1.5M. 20 × $1.5M = **$30M**. Verified. | **Real** |
| **R6** | "~0.5% of segment revenue" | Gone. $30M / $21.8B = **0.1376% ≈ 0.14%**, stated correctly, and stated as *strengthening* the materiality objection. | **Real** |
| **R9** | "$9-18M/yr, payback inside a year" | **Struck entirely.** Replaced with "no dollar return and no payback period is quoted, because any such figure would be computed against a base whose value this thesis exists to establish." | **Real** |
| **R12** | rollback cited as evidence *for* catalogue | Inverted. Now T2's **first named deliverable**, with a sensitivity range. | **Real** |

Also genuinely fixed and checked: **R7** (hurdle and falsifier both now in annual churn;
windows extended to 24 months so treatment outlives readout; 90-day reading demoted to an
interim indicator), **R8** ("per-title" struck from T2's causal claim; per-title randomisation
added as precondition (d) with the correct observation that it is free before signature and
impossible after), **R10** (claim is now unambiguously an escalation gate), **R11** ($50M
removed, not re-anchored; explicitly labelled an unanchored judgement).

**R3 was rebutted in part, and the rebuttal is correct.** I asserted the selection rule was
backwards. v2 answers that recognition and penetration are separable, and that Steam ownership
is not Xbox console penetration — so a 1M+ Steam title may have low console penetration and be
exactly the right pick. That is right, and my R3 implicitly transferred penetration across
platforms in the same breath as complaining about population transfer. The remedy is conceded
in full and the pool is declared unsizable from this data. **Objection withdrawn as stated;
remedy accepted.**

The self-audit in Round 2 (`05_responses.md`) that names O1 and O4 as concessions in form only
is accurate and volunteered. Assessed on the record, this is a real revision.

---

## 2. Are the new numbers sound?

Re-derived from `parquet/` rather than accepted.

**12.59% ceiling decomposition — VERIFIED EXACTLY.**
```
n_class=842  n_hits=106  pct=12.59
band 1M–5M = 92   band 5M–20M = 13   band 20M+ = 1
```
92 + 13 + 1 = 106 ✓; 92/106 = 86.8% ≈ **87%** ✓; 106/842 = **12.59%** ✓. The bound is correct
and it is the right bound to draw: reaching 1M owners is not returning a studio commitment, and
the class conditions on titles that shipped from publishers already holding 20+ titles. v2
volunteering this against its own corrected number is the strongest single move in the revision.

**652-title pool — essentially correct, cause misdiagnosed.**
727 after the ≤2022 and non-free screens ✓; the five named publishers total 75 in that screened
set ✓; 727 − 75 = 652 ✓. Counting directly I get **650**, because two rows carry a NULL
publisher that a `NOT IN` filter silently drops. My original 646 additionally excluded
PlayStation Publishing (4 titles in the screened set), which v2 omits from its exclusion list —
Sony will not license back catalogue non-exclusively into Game Pass, so 646 is the tighter
figure. Range 646–652; immaterial exactly as claimed. The stated cause ("publisher-string
matching") is wrong — it is NULL handling plus the PlayStation omission. Cosmetic.

**$420M / $840M / $1,260M — arithmetic exact, and conservative.**
5M/10M/15M × $7.00/month × 12 = $420M / $840M / $1,260M ✓. Multiples check: ÷$90M = 4.7× and
14× ✓; ÷$30M = 14× and 42× ✓. The $7.00 is exact ($29.99 → $22.99). Testing my unsourced 10M
assumption across a range instead of adopting it was the right response, and the range excludes
the concurrent PC Game Pass cut ($16.49 → $13.99), so it understates the total price deployment.

**New $30M hurdle — VERIFIED.** 300,000 × $168 = $50.4M/pp gross; at 60% margin $30.24M/pp;
$30M ÷ $30.24M = **0.99pp ≈ 1.0pp** ✓, and correctly denominated on contribution margin rather
than gross. M8's range caveat is carried into `assumptions`.

No new number failed to reproduce.

---

## 3. New unsupported claims

Three entered with the revision. Two are material, and both sit in the new sequencing logic —
which is where the coordinator suspected they would be, and where they are.

### N1 — the decision tree has no branch for good news. **MATERIAL.**
T1 fires "**IF and only if** T2's retrospective **cannot** identify the catalogue-to-retention
effect." So the $30M tranche is triggered by *ignorance* and blocked by *success*. Consider the
state of the world in which the retrospective works and shows a large positive catalogue effect
— the outcome most favourable to catalogue investment. Under v2, T1 does not run (condition 1
fails), the $90M/yr steady state has been withdrawn, and `no_steady_state` forbids offering an
annual figure. I searched v2 for any branch handling a successful, positive retrospective:
**there is none.** The analysis has left itself unable to recommend anything in the one scenario
where its own mechanism is vindicated.

This is the over-correction, and it is narrow and cheap to fix: add the branch. If the
retrospective identifies a positive effect, the correct next step is not a 20-title experiment
— it is to size a programme off the measured effect, using the pool recomputation R1 already
specifies. One paragraph.

*Resolution:* state all three branches explicitly — retrospective positive → size a programme
from the measured effect; retrospective null/inadequate → the $30M instrumented tranche;
retrospective negative, or price cheaper per retained subscriber → drop the catalogue argument.

### N2 — the price-action trigger is not decidable by the audit as scoped. **MATERIAL.**
Audit question (5) — "what did the April 2026 price action cost per retained subscriber?" — is
promoted to a binary gate on $30M. But the rollback was a **universal price change with no
holdout**. Recovering cost-per-retained-subscriber requires a counterfactual churn path at
$29.99. There is an interrupted time series (increase late 2025, rollback April 2026), which
gives partial identification, but it is confounded with the July 2026 restructuring, ordinary
catalogue turnover, competitor launches and seasonality. This is the same identification problem
v2 correctly concedes for the 500-deal retrospective at R8 — and it is not flagged here.

Worse, the threshold it is compared against (~$100) is itself the product of three unsourced
assumptions stacked multiplicatively: 30M subscribers (low-confidence third-party), $14 blended
ARPU (derived from list prices, mix unknown), 60% margin (unsourced). v2 treats a noisy internal
estimate versus an assumption stack as a clean binary decidable in six to eight weeks.

*Resolution:* demote (5) from a gate to an input. It is still the highest-value question in the
audit — that judgement is right and I stand behind R12 — but it should be reported with its
identification caveat and a range, not used as a threshold test against a number carrying three
unsourced inputs.

### N3 — "20 titles is set by experimental design". **MINOR.**
`size.basis` states 20 is "the minimum block giving a detectable tranche-level effect". No power
calculation appears anywhere in the run. The reasoning is also inverted: with a ~10% holdout on
~30M subscribers, statistical power comes from the *subscriber* n, not the title count — 1.0pp
is trivially detectable whether the tranche holds 5 titles or 50. Title count sets treatment
**dose**, and the dose required to move annual churn by 1.0pp is precisely the unknown the whole
exercise exists to measure. So 20 cannot be derived from experimental design. This is an
improvement on v1's inventory-share justification, which was false; it is still an assertion.
*Resolution:* say plainly that 20 is a bounded judgement, as T3-prime's threshold now honestly does.

### N4 — "nine-figure studio commitment". **MINOR.**
T3-prime's bound compares the modal 1M–5M hit against "a nine-figure studio commitment", while
v2 elsewhere correctly declines to assert Xbox acquisition prices ("I do not have their
acquisition prices and do not assert them"). Hedged with "plausibly"; note the inconsistency.

---

## 4. Is "$0 today" honest, or unfalsifiable caution?

Genuinely supported, with one qualification.

It is **not** analyst reflex, because it does not rest on "we need more data." It rests on two
specific findings that survived verification: Microsoft has already run a 500+ deal catalogue
programme (R2), and deployed $420M–$1.26B/year against churn via price months ago (R12). Both
point at internal evidence that is **free, already collected, and demonstrably not yet
consulted** by this analysis. Recommending a $30M experiment before asking two zero-cost
questions of existing data would be indefensible, and v2 is right to refuse. Recommending
measurement is the safe answer in general; here it happens also to be the correct one, and the
distinguishing test is that v2 names exactly which two internal numbers would change the
recommendation and states that neither is substitutable by anything in this dataset.

The qualification is N1. A recommendation of $0 is credible once. What makes it *unfalsifiable*
is that no outcome of the audit currently leads back to a commitment — success blocks T1,
failure triggers only a bounded experiment, and the steady state has been withdrawn with no path
to reinstating it. Add the positive branch and "$0 today" becomes a genuine sequencing decision
with a stated payoff. Leave it out and a board is entitled to ask what result would ever cause
this analysis to say yes.

I also record that v2's `null_option_assessment` now states plainly that with the base rate
corrected "the null option does NOT clearly win" on the studio side and that the analysis
cannot say whether studio investment is a good idea. Conceding that the correction destroyed
its own preferred conclusion, rather than quietly re-deriving it, is the correct behaviour.

---

## Final verdicts

**T2 — retention-attribution capability, rank 1: STANDS.**
Correctly promoted. "Per-title" struck from the causal claim; the circular payback figure
struck; the retrospective-on-500-deals and the price-versus-catalogue comparison added as
audit questions (4) and (5). The $8M remains an unsourced internal estimate and is labelled as
one, gated behind a $0 audit that tests its own load-bearing assumption before money moves.
The one required change is N2: report question (5) with its identification caveat and a range,
not as a binary gate.

**T1 — conditional $30M licensing tranche, rank 2: STANDS NARROWED.**
The arithmetic is now correct throughout ($30M, 0.14%, 1.0pp, 24-month windows, single deal
price), the steady state is properly withdrawn, and precondition (d) on per-title randomisation
before signature is a genuine improvement that did not exist in v1. It cannot go to a board
until the conditional logic is repaired: **add the positive-retrospective branch (N1)** and
**demote the price trigger from gate to input (N2)**. Drop the "experimental design"
justification for 20 titles (N3) and call it a judgement.

**T3-prime — escalation gate on irreversibility, rank 3: STANDS NARROWED.**
Substantially smaller and substantially more honest than T3. No base-rate claim, no dollar
threshold, the falsifier re-benchmarked against the corrected 12.59%, and the bound on that
figure verified exactly against the data. It now recommends process rather than capital, which
is all the evidence supports. Fix N4's unsourced "nine-figure".

**On the set:** v1 had two fatal objections. Both are properly dead — one by withdrawal of the
number, one by withdrawal of the argument. What remains is a correctly sequenced, honestly
sized, mostly-$0 recommendation with one repairable hole in its decision tree. That is a
materially stronger document than v1, and the strategist's self-audit of its own Round 1
failures is accurate rather than defensive. **Iteration 3 should be spent on N1 and N2 only.**

---

## The three questions a hostile board member will ask about the revised position

**1. "What would this audit have to find for you to actually recommend we spend something?"**
*Honest answer as v2 currently stands: nothing.* A positive retrospective blocks T1; a null one
buys a $30M experiment; the annual programme has been withdrawn with no route back. This is N1,
and it is the question that exposes it. The answer must become: a positive retrospective sizes a
programme off the measured effect — at which point the pool recomputation named in R1 becomes
the gating work, not the churn question.

**2. "You just told me the number you used to argue against studio investment was wrong by a
factor of twelve. Why should I trust the rest of it?"**
The honest answer is that this one was caught by an independent reviewer re-running the query,
not by the analysis's own self-critique — which had already conceded the identical error one leg
over and left this one standing. The defensible response is the record: every load-bearing
figure in v2 has now been re-derived from source by a second party, and the reference-class table
goes into the deck whichever way it points. The correction is also volunteered against the
analysis's own preferred conclusion, which is the evidence that the process works.

**3. "We changed the price months ago. Why is a Steam dataset telling us anything about that?"**
It isn't, and v2 now says so. The highest-value output of this entire run is an internal
comparison — what the April 2026 rollback cost per retained subscriber, against a ~$100
contribution-margin hurdle — that uses no Steam data at all. The honest framing is that the
Steam analysis established a boundary (no engagement signal exists, and the console population
differs on genre and spend) and that the boundary is what redirects the question inward. A board
is entitled to note that this is a modest return on the exercise, and `materiality_objection_answered`
should keep conceding it rather than arguing the point.
