# Q&A prep — Game Pass portfolio

**Board Q&A, 22 August 2026.** Ten questions, each answerable in about 30 seconds.
Drawn from `15_redteam_portfolio.md` (the red team's own three hostile questions are Q1,
Q2 and Q3 below, verbatim in substance), `16_scoring_v3.md` and `04_context.md`.

**Two rules for the room.** Do not invent a number under pressure — every figure you may
say is in the pitch script's traceability table, and anything outside it gets "I don't have
a sourced figure for that." And when the honest answer is "we cannot answer that yet," give
it, then say exactly what would settle it. That is Q6 and Q10.

---

## Q1. "Six of your picks are games we already had and gave up. Did we drop them, or did they drop us — and if it was us, why are you asking me to buy them back?"

**This is the question. Expect it first.**

> I cannot tell from outside. Either the publisher declined to renew, which means the price
> is above what we would pay — or we declined, which means our own engagement data already
> returned a verdict. No external source establishes which, for any of the six.
>
> That is precisely why they are second in the running order and not first. The three titles
> that lead — A Hat in Time, Obra Dinn, Baba Is You — have no prior run to explain at all.
> And you can settle the restarts internally, in a day, at zero external cost. That is the
> lookup I am asking for.

*If pushed — "so you're recommending games we rejected?"* — Six named picks that stand on
their own scores, with a condition attached: remove any title our own record of its prior
run puts in the bottom quartile of engagement per licensing dollar. The condition is on the
sheet already.

---

## Q2. "You said the catalogue's strongest signal is Action and multiplayer — half the qualifying list — and you brought us a portfolio that is seventeen per cent each. Which is it?"

> Both, and it is a property of the ranking, not an accident. Picks are 17.6% Action and
> 17.6% multiplayer against 53.8% and 33.5% in the 275-title qualifying list.
>
> The mechanism is known: Recognition carries half the weight and review volume runs highest
> for single-player narrative titles, and the Fit component — retargeted onto positive
> review ratio — penalises multiplayer, which carries systematically lower positive ratios.
> We cut Fit from 20% to 10% and that measurably helped: ranks 31–60 went from 16.7%
> multiplayer to 23.3%.
>
> But it did not close the gap, so we withdrew the remedy rather than dress it up. Density
> only doubles past rank 60. Closing this properly means extending the availability screen
> to rank 120, which would surface 22 titles with verified co-op and multiplayer flags —
> SnowRunner, Streets of Rogue, TMNT: Shredder's Revenge, Streets of Rage 4 among them.
> None of them can be a pick today because none has been screened.

*The one correction to make unprompted:* an earlier draft named Deep Rock Galactic:
**Survivor** as a co-op alternate. It has neither flag — it is a single-player roguelite
spin-off. The label was our error, not the data's. It is withdrawn.

---

## Q3. "Fifteen of your seventeen are jammed against your own ownership ceiling. Did you pick these games, or did the threshold pick them?"

> Largely the threshold, and I would rather say so than be caught at it.
>
> Ownership acts only as a three-level step, while Recognition is continuous and weighted
> 0.50. A coarse step cannot offset a continuous term, so the model reliably selects the
> most-owned titles that still clear the ceiling. The ceiling defines the list more than it
> filters it. And because SteamSpy buckets are what they are, a 750,000 ceiling is
> bucket-identical to a 1.5 million one.
>
> So here is what one bucket down looks like: at 500,000 owners, 110 of the 275 qualify, and
> the top of that view is ANIMAL WELL at Metacritic 91 — the highest score anywhere in the
> list — Neon White at 89, Rogue Legacy at 85. Eleven of its top fifteen were never
> availability-screened, so it cannot be turned into a portfolio today. That is the honest
> shape of the alternative.

---

## Q4. "Why do you not know what these cost?"

> Because no sourced per-title price for this tier exists, and I would rather bring you no
> number than an invented one.
>
> The only public figure is from a former Xbox business development lead: $50,000 to over
> $50 million across 500-plus deals, with no breakdown. That is a thousandfold span. It
> excludes no possibility and supports no budget, so I have not presented it as sizing.
>
> The AAA leak numbers are real but the wrong order of magnitude — Assassin's Creed Mirage
> around $100 million, Baldur's Gate 3 around $5 million, GTA V back-catalogue at $12–15
> million a month. Extrapolating downward from those to a sub-million-owner indie is
> speculation.
>
> What I have instead is an execution ordering by deal structure: prior deal exists, port
> exists, status known, counterparty scale. Commit tier by tier and stop when the quotes
> stop making sense. That ordering never uses retail price, deliberately — price in this
> catalogue is a proxy for production budget, and using it would resurrect an error we
> already removed.

---

## Q5. "This is Steam PC data. We sell Xbox consoles."

> Correct, and it is the caveat I would raise myself if you had not.
>
> Console ARPPU runs about 47% higher than PC — $81.68 against $55.47, MIDiA estimates for
> 2024 — and the genre mix differs: shooters dominate PC playtime while sports overtook
> action-adventure on Xbox console in 2024. A Steam-derived genre signal does not
> automatically transfer.
>
> Three things narrow the risk. Every pick is gated on full controller support. All
> seventeen have a shipped Xbox console SKU, so console viability is demonstrated rather
> than assumed. And demographic skew is broadly similar across the two platforms — it is
> spend and genre that differ, not audience age.
>
> What I am not doing is claiming a genre finding transfers. The picks rest on recognition
> volume, which transfers more readily than taste does.

---

## Q6. "Which of these will actually get played? What does the engagement look like?"

**This is the honest "we cannot answer that yet."**

> I cannot answer that, and no part of this analysis pretends to. Every playtime column in
> this dataset is zero. There is no engagement or retention signal in it, and I have made no
> claim about either for any of the seventeen titles.
>
> Two things would settle it, both internal. First, Microsoft's own engagement record for
> the six restart titles during their prior runs — that is a direct read on six of the
> seventeen and it exists today. Second, for the other eleven, nothing external will settle
> it; you would learn it after adding them.
>
> What the data does support is that these are titles a lot of people know about and
> relatively fewer own. Recognition, not engagement. I would rather name that boundary than
> blur it.

---

## Q7. "How did you rank them? Talk me through the model."

**Say this correctly or do not say it at all. It is not a multi-pillar blend.**

> It is Recognition — the percentile of log review volume, weighted 0.50 — banded by a
> three-level ownership step. Inside any one ownership band the ranking is simply
> most-reviewed-first.
>
> I want to be precise about that because we originally described it as a three-pillar
> blend and that was wrong. The Headroom term is review volume minus owners, and SteamSpy
> owners take only five distinct values with three buckets holding nearly the whole pool.
> Within a bucket the correlation between Recognition and Headroom is 1.0000 exactly —
> Headroom is Recognition minus a constant. Its only real job is moving a title between
> bands.
>
> The third component, Fit, carries 10%. Its in-population R² is −1.34, worse than
> predicting the mean, so we cut it from 20% and treat it as a tiebreaker. Its measured
> influence on the final ranking is 0.04. Nothing in the portfolio rests on it.

---

## Q8. "Why seventeen? Why is the bar where it is?"

> The bar is the deliverable, not the count. Two thresholds do the work.
>
> The review floor is 4,000, chosen on a measured elbow: Metacritic presence in the pool
> climbs to 47.3% at 4,000 and is flat within a point all the way to 7,000. We had it at
> 5,000 and moved it down, because 5,000 was costing 164 titles for seven-tenths of a
> percentage point. The composite bar is 0.60, which yields 275 qualifying titles from a pool
> of 802.
>
> Seventeen is not a cap on the ranking. It is what survived the external availability
> screen, which covered thirty titles. The list is 275 long and it is in the pack. Screen
> more and the pick list grows — Dead Space and Lies of P are the next two in line and we
> make no availability claim about either.

---

## Q9. "What if a rights holder says no?"

> Every tier has a named alternate, already checked, with its status stated.
>
> For the clean three: ANIMAL WELL — Metacritic 91, the highest in the qualifying list, solo
> developer, and in the lower ownership bucket the portfolio is short of. It is an alternate
> and not a pick for one reason: it was never availability-screened.
>
> For the restarts: Marvel's Guardians of the Galaxy, screened, Xbox SKU confirmed. It is an
> alternate rather than a pick because the counterparty changed — Embracer bought the studio
> and the IP from Square Enix in 2022, so the prior yes came from a company that no longer
> holds the rights, and the Marvel licence adds a second rights holder we never screened.
>
> For the breadth tier: The Stanley Parable: Ultra Deluxe, never screened.
>
> The specific refusals we would expect first: Obra Dinn is one person and one person can
> simply say no; Persona 3 Reload is a still-selling $69.99 SKU from a large publisher and is
> the likeliest title on the list to price itself out. It is ranked last in its tier for
> exactly that reason.

---

## Q10. "Why isn't Wandering Sword — or Journey, or SANABI — a pick? They score higher than half your list."

**The second honest "not yet," with a dated resolution.**

> Because the thing we would be buying has not been shown to exist. Those seven are a
> watchlist and I have labelled them as explicitly not a buy.
>
> SANABI is rank 6 — higher than most of the portfolio — and its Xbox version rests on a
> single source. Six of the seven have an unverified Xbox SKU; two of those sit at low source
> confidence. "No evidence found" from one search is not a finding, in either direction. Our
> own removal rule cannot even be evaluated on them, which is exactly why they are not picks.
>
> They are disciplined by promotion, not removal: a native Xbox console SKU confirmed by two
> independent dated sources, or one primary source — publisher or Microsoft Store. Then the
> title moves into the breadth tier and competes on merit.
>
> One has a date already. Wandering Sword's console release is set for 21 January 2027. If
> it ships, it promotes. If it slips again, it drops off, because then it is open-ended
> rather than diarisable.

---

## Fast-reference card

| If they ask | The number | Where it comes from |
|---|---|---|
| Funnel | 122,191 → 802 → 275 → 30 screened → **17** + 7 watchlist | `02_cleaning_report.md`, `16_scoring_v3.md`, `13_availability.md`, `17_portfolio_final.json` |
| Xbox SKU coverage | 17/17 picks confirmed; 6/7 watchlist unverified | `13_availability.json`; verified in `15_redteam_portfolio.md` B-3 |
| Clean spine | 3/3 never on Game Pass, 3/3 Xbox SKU, no blocker | `13_availability.md` Group D |
| Concentration | picks 17.6% Action / 17.6% MP / 11.8% co-op; list 53.8% / 33.5% / 24.4% | `17_portfolio_final.md` §Concentration |
| Rank-band gradient | MP by band: 13.3% (1–30), 23.3% (31–60), 38.3% (61–120) | `17_portfolio_final.md` §Concentration |
| Ownership ceiling | 60.0% of the 275 in the top bucket vs 48.1% of the 802; 15 of 17 picks | `17_portfolio_final.md` §Ownership ceiling |
| Sensitivity one bucket down | 110 of 275 at ≤500k owners; 11 of its top 15 never screened | `17_portfolio_final.md` §Ownership ceiling |
| Model | Recognition 0.50, banded by a 3-level ownership step; within-bucket Spearman = 1.0000; Fit 0.10, R² −1.34, influence 0.04 | `16_scoring_v3.md` Fix 1 & Fix 2 |
| Review floor | 4,000; Metacritic presence 47.3%, flat to 7,000 | `16_scoring_v3.md` §Cheap fix |
| Deal-cost range | $50K–$50M+ across 500+ deals, no breakdown — **context, not sizing** | MacIntyre via TweakTown, 2025-07-13 |
| AAA anchors (say only to reject them) | ACM ≈$100M, Jedi Survivor ≈$300M, BG3 ≈$5M; GTA V $12–15M/mo | Axios, 2023-09-19 |
| Console vs PC | ARPPU +47.3% ($81.68 vs $55.47) | MIDiA 2024 estimates via Plarium, `04_context.md` §5 |
| Studio closures | Ninja Theory, Double Fine, Compulsion — 6 July 2026 | Tech Times, 2026-07-06 |
| Subscriber count | **Do not quote.** ~30–34M is a third-party aggregator estimate, not disclosed by Microsoft | `04_context.md` §1 |
| Engagement / retention | **No such data exists here.** Every playtime column is zero | `GOAL_STATEMENT.md` |
| Owners | **Bucketed SteamSpy estimates, never sales** | `01_profile.md` |
