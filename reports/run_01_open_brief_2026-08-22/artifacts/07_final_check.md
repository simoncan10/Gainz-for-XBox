# Stage 7 — Final numerical traceability and honesty check

Scope: `deliverables/pitch_script.md`, `deliverables/qa_prep.md`, `artifacts/05_theses_final.json`.
Numerical traceability and honesty only. Strategy, sequencing and thesis structure not re-opened.

**Result: PASS, subject to two required one-line fixes and two minor ones. All four are in
`pitch_script.md`. `qa_prep.md` passes clean.**

---

## 1. Traceability of spoken numbers

I inventoried every figure spoken aloud and checked each against the trace table, then checked
each table row against the artifacts. **The table is complete and correct with one omission.**

Verified present and correctly sourced: 500+ deals (`gp-deal-cost-range`); $29.99→$22.99
(Xbox Wire, primary); $840M and 28×; F1's top-decile shape; ~650 titles; ~$1B sweep; 0.025pp;
30M / $168 / 60% / $30.24M; $750K; ARPPU ~48%. No table row is unsupported by an artifact.

**Omission — "six weeks" (spoken twice, and in the ask) is not in the trace table**, and it
narrows the artifact's range: T2's `first_step` in `05_theses_final.json` specifies a **6–8 week**
audit. The script commits the board to the optimistic end. *Fix: say "six to eight weeks", or add
a table row noting six is the floor.*

Rhetorical restatements ("a hundred games buys you ninety bad ones") reduce to F1 and need no
separate row. `$21.8B` appears only in `qa_prep.md`, not in speech — correctly out of the table.

## 2. Break-even arithmetic — re-derived, exact

```
300,000 × $168            = $50,400,000
      × 60%               = $30,240,000   ✓ spoken as "thirty million dollars a year"
$1.5M ÷ 24 months × 12    =    $750,000   ✓ per title-year
$750,000 ÷ $30,240,000    = 0.0248015…pp  ✓ rounds to 0.025pp
```
Spoken version matches exactly. **The rounding is not doing hidden work, and runs against the
speaker's own case:** 0.0248 → 0.025 raises the bar ~0.8%, implying a $1.512M break-even price
against the $1.5M actually assumed. Conservative.

Cross-check: 20 titles × 2 years × 0.0248pp = **0.992pp ≈ 1.0pp**, and 20 × 2 × $750K = **$30M** —
reconciling precisely with the $30M / 1.0pp hurdle carried from v2. The unit chain is coherent
end to end. `qa_prep` Q2's worked example also checks (50 title-years × 0.025 = 1.25pp; 2pp clears
at 1.6×, 0.5pp fails by exactly 2.5×).

## 3. Withdrawn claims — none reappear

- **Engagement / playtime:** absent. No such word or implication anywhere in the script.
  `qa_prep` adds an explicit trap-refusal ("every playtime column in the source is constant zero").
- **Per-title causal claim:** absent. "Per title-year" is a *cost* normalisation, not an effect
  attribution, and `qa_prep`'s second trap-refusal states the tranche-level limit correctly.
- **Annual programme figure:** absent. The `$1B` is explicitly a one-time full sweep, not the
  withdrawn $90M/yr, and `qa_prep` Q9 refuses to name an annual figure under direct pressure —
  the right behaviour at exactly the point it would be most tempting.

## 4. Required fixes

### FIX 1 — the 30M subscriber figure is spoken as disclosed fact. **Required.**
Spoken: *"One point of churn, **on thirty million subscribers**, is three hundred thousand people."*
No hedge. Microsoft does not disclose this. `04_sources.json` `gp-subscribers-estimate-2026` is a
**secondary aggregator estimate, confidence LOW**, band 30–34M. The trace table notes the inputs
are unsourced; the board hears a flat number.
*Fix: "on an estimated thirty million subscribers".* One word, no rhythm cost.

### FIX 2 — "licensable" asserts a rights clearance the analysis has not done. **Required.**
Spoken: *"Around six hundred and fifty proven titles **screen through as licensable** back-catalogue."*
`05_decision_tree.md` line 43 states plainly that 646–652 is *"before netting, before rights, and
before a console-penetration screen this dataset cannot support."* The screen excluded free-to-play,
recent and Microsoft-owned/structurally-unavailable publishers — it did **not** establish rights
availability. `qa_prep` Q9 gets this right; the script overstates it.
*Fix: "screen through as candidates".* The $1B that follows is then correctly framed as a ceiling.

### FIX 3 — $840M / 28× spoken as point estimates. **Should fix.**
Both rest on an unsourced 10M-Ultimate-subscriber assumption. The verified range is
**$420M–$1.26B → 14×–42×**. The trace table discloses the range; the speech does not, and the
delivery note makes 28× "the number they will remember". `qa_prep` Q4 already uses the range
correctly, so the script contradicts its own prep on the same figure.
*Fix: "somewhere between four hundred million and one and a quarter billion a year — fourteen to
forty times any licensing programme anyone would ask you for."* Still lands; survives challenge.

### FIX 4 — "six weeks" vs the artifact's 6–8. **Minor.** See §1.

**Checked and found acceptable, no change needed:** "roughly four-fifths or more" for F1's 78–93%
(Indie 78.4% and Sports 78.1% sit just under four-fifths, but "roughly" carries it and M7 requires
this be spoken as a shape, never to a decimal — correctly observed).

## 5. `qa_prep.md`

**Passes.** Contains three genuine non-answers, not one: Q5 *"Not cleanly, no"* on whether the
audit can recover the price-action cost; Q7 *"I don't have one, and the analysis says so
explicitly"* on studio investment; Q10 *"the one I can't fix"* on internal greenlight skill.
Each names what would settle it.

No contradiction with `05_theses_final.json`. I verified the two positions that changed last:
Q2's positive branch ("skip the experiment entirely and size a standing programme") matches the
final artifact's Branch A; Q5's demotion of the price comparison matches *"per N2 the price-action
comparison is NO LONGER a prior falsifier — it is an input"*. Both N1 and N2 are closed in the
artifact and reflected accurately in the prep.

One trivial note: Q3 says "a tenth of a percent" where the figure is 0.138%; the deck elsewhere
says 0.14%. Rounds in the flattering direction by a hair. Not worth changing.

---

## Verdict

**PASS.** The arithmetic is exact, the unit chain reconciles end to end, the rounding is
conservative, no withdrawn claim has reappeared, and the population-transfer limitation is
conceded by the speaker in the RISK section rather than left for the board to raise — it is given
sixty of the script's four hundred words and the delivery note tells the speaker to concede it
"with your chin up".

Fix the four figures listed. Two are single words (`estimated`, `candidates`), one is a phrase
swap already used correctly in `qa_prep`, and one is a range restored. None touches the argument.
