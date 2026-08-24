# Q&A prep — ten questions, 30-second answers

Drawn from `06_redteam_v2.md` (hostile-question list §"The three questions", objections N1–N4,
R2/R3/R6/R8/R12) and `05_theses_final.json` (`what_this_analysis_cannot_tell_the_board`).

**Rules for the room:** answer in three sentences. Concede fast where the concession is real —
every one of these was conceded in the analysis already, so conceding out loud costs nothing and
buys the rest. If you do not know, say "I don't know" and then say what would settle it. Never
invent a number; the traces are in `pitch_script.md`.

---

### 1. "This is Steam PC data. Why is it telling us anything about Xbox console subscribers?"
*(the single most likely question — redteam_v2 §"three questions", Q3)*

It isn't, and I won't pretend otherwise. Console players spend about half again as much per
paying user and the genre mix is different — PC skews shooter, console now skews sports, and the
sports evidence here is a measurement artifact, thirty-one titles. What the Steam work
established is a **boundary**: no retention signal exists in any external dataset, which is
precisely why the recommendation points inward at data you own rather than outward at mine.

### 2. "What would this audit have to find for you to recommend we actually spend something?"
*(redteam_v2 §"three questions", Q1 — the N1 hole, now closed. Know this answer cold.)*

A retrospective effect above **0.025 percentage points of annual churn per title-year** at
$1.5M/24-month terms. Above that, you skip the experiment entirely and size a standing programme
straight off the measured effect. Concretely: two points of churn across a fifty-title
cohort-year clears comfortably; half a point across the same cohort fails by two and a half
times — and I'm telling you both today, before I've seen the data.

### 3. "Why not just spend the $30 million? It's 0.14% of the segment. The delay costs more than the money."
*(R6 materiality)*

You're right that it's immaterial — more immaterial than my first draft admitted; it's a tenth of
a percent of a twenty-one-point-eight-billion segment. But the six weeks are not the cost; the
cost is buying a twenty-title experiment while a five-hundred-deal one sits unread, and then
having no way to interpret the result against it. If the retrospective works, the $30M tranche
is never needed at all — that's the saving.

### 4. "We already fixed churn in April with price. Why are we discussing catalogue?"
*(R12 — note this inverts my own earlier draft, and say so)*

Because you spent somewhere between four hundred and twenty million and one-point-two-six
billion a year to do it and you don't know what it bought per retained subscriber. My earlier
draft cited the rollback as *support* for catalogue spending; that ran backwards, and it's
withdrawn — the rollback is evidence that price is your revealed lever, and catalogue now has to
beat it. The audit is the first thing that would let you compare the two.

### 5. "Can the audit even recover what the price action cost per retained subscriber?"
*(N2 — the honest answer is partly no)*

Not cleanly, no. It was a universal price change with no holdout, so there's no counterfactual
churn path at $29.99, and the interrupted time series is confounded with the July restructuring,
catalogue turnover and seasonality. So I report it as a **range with its caveat, as an input, not
a trigger** — and the fix is forward-looking and free: instrument the *next* price action with a
regional or cohort holdout.

### 6. "Your studio base rate was wrong by a factor of twelve. Why should I trust anything else?"
*(redteam_v2 §"three questions", Q2)*

Because it was caught, in writing, by an independent reviewer re-running the query, and corrected
*against* the conclusion I preferred — the corrected number weakened my own argument and I
published it anyway. One percent was the all-Steam rate; the right reference class, premium
titles from established publishers, is 12.59%. Every load-bearing figure in the deck has since
been re-derived from source by a second party, and the reference-class table goes in whichever
way it points.

### 7. "So what's your recommendation on studio investment? We closed three studios in July."
*(T3 withdrawn — do not overreach here)*

I don't have one, and the analysis says so explicitly. The quantitative case against studio
investment collapsed when the base rate was corrected, and I'm not going to rebuild it from
three outcome-selected breakout titles. What survives is process, not capital: route any
commitment whose exit cost can't be reversed within a fiscal year to this board as an escalation,
with the corrected reference class and July's exit costs attached.

### 8. "Doesn't the top-decile concentration argue for buying only hits — which are the expensive ones?"
*(F1 + R3)*

It argues against buying breadth, yes. But Steam ownership is not Xbox console penetration, and
those separate cleanly — the right pick is high recognition and *low* console penetration, which
is a title your subscribers know and haven't played on your platform. That screen cannot be built
from this dataset at all, which is exactly why I'm not naming an annual programme figure today.

### 9. "How big is the programme if the rule clears? Give me a number."
*(R1 — the $90M/yr steady state is withdrawn; do not reinstate it under pressure)*

I won't, because the term that sets it — the pool after netting against the five hundred titles
already in Game Pass, after rights, after a console screen — is genuinely unknown. The
order-of-magnitude ceiling is around six hundred and fifty screened titles at a million and a
half, so roughly a billion for a one-time full sweep; a standing programme is bounded well below
that. A figure any more precise than that from this evidence base would be fabricated.

### 10. "Where is this analysis simply wrong or blind, in your own view?"
*(the one you cannot fully answer — answer it straight)*

Three places. **Engagement**: there is no playtime data anywhere in this dataset, so nothing here
measures retention — the entire mechanism is asserted, not shown. **Owners**: they're bucketed
SteamSpy estimates, with eighty-three percent of the catalogue in one bottom bucket, so
concentration is a shape rather than a measured share. **And the one I can't fix**: whether your
greenlight process picks better than the reference-class rate — that's the pivot the whole studio
question turns on, and it's an internal fact I've never seen.

---

## Two traps to refuse

- **A per-title effect number.** A single randomised holdout identifies one *tranche-level*
  average effect. Per-title effects inside a shared catalogue are self-selected — the people who
  chose to play title X were the more engaged subscribers anyway. Say "correlational, and I'll
  label it as such."
- **Engagement or playtime.** Every playtime column in the source is constant zero. If a question
  presumes engagement data, correct the premise before answering.
