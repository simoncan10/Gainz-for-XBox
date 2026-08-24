# Indie slate for PC Game Pass — spoken script

**Word count (spoken text only): 422.**
**Runtime: 3 min 15 s at 130 wpm · 2 min 49 s at 150 wpm.**
Budget is three minutes. Under pressure you will speak *slower* than in rehearsal, not
faster — if you are behind at the 2:00 mark, drop the four Tier-1 title names and the nine
words after "and twelve breadth titles". Do not drop the objection.

---

### 0:00 – 0:20 · HOOK  *(Slide 1 — the question)*

> At a fixed quality bar, a thousand dollars of retail price buys **sixty-three** indie
> titles. The same thousand buys **forty-one** non-indie ones. That gap is the entire case
> for this slate. It is not a claim that indie games are better. It is a claim about what a
> subscription actually buys.

*Delivery: land "sixty-three" and "forty-one" hard, then **pause a full beat** before "That
gap." Do not say "we analysed" anything. Do not open with the method.*

---

### 0:20 – 0:45 · TENSION  *(Slide 5 — the yardstick flip)*

> The usual yardstick is owners per dollar. On that yardstick this slate loses, badly — indie
> costs **ninety-three dollars** per million owners reached against **sixty-two**. I will come
> back to that. But a subscription does not sell copies. It sells the reason not to cancel
> this month, and that reason is a catalogue slot, not an owner.

*Delivery: say "loses, badly" flatly and without apology — conceding it early is what buys you
the room. Slow right down on "not an owner."*

---

### 0:45 – 1:40 · THE FUNNEL AND THE FILTERS  *(Slides 2, 3, 4)*

> Here is how twenty-one names came out of a hundred and twenty-two thousand. Five filters:
> paid, five thousand reviews, seventy percent positive, under seven hundred and fifty
> thousand owners, genuinely indie. Five hundred and seventy-three eligible. Two hundred and
> one qualifying. Twenty-five checked by hand against Game Pass. Twenty-one picks.
>
> Trust those filters because we can tell you how the first two failed. Version one ranked
> shovelware at the top — its recognition term cancelled itself out, and its cheap pillar was
> really a filter for no production budget. Then our indie test was a string match. It called
> *Papers, Please* non-indie, because Lucas Pope's label is spelled "three-nine-zero-nine" —
> and it let in a publisher with a hundred and eighty-one asset flips. Both caught, both
> rebuilt, both hand-checked.

*Delivery: the funnel numbers are a **rhythm**, not data — four beats, dropping. Then change
tone completely for "Trust those filters." This is the credibility passage; slow, direct eye
contact, no notes.*

---

### 1:40 – 2:20 · THE PICKS, AND WHAT THEY REALLY DELIVER  *(Slide 6)*

> Twenty-one titles, three jobs. Four clean adds that lead — A Hat in Time, Obra Dinn, Rogue
> Legacy, Stanley Parable. Five restarts Microsoft has already licensed once, including
> Journey and VA-11 Hall-A — both PC-tier deals we have done before. And twelve breadth
> titles, which are the investment case: ENDER LILIES, SANABI, Chants of Sennaar, Wandering
> Sword, and nine more.
>
> Now the honest part. The pool delivers fifty-three percent more breadth per dollar. These
> twenty-one deliver **twenty-one and a half**. We keep forty percent of the edge, because
> recognition and price rise together.

*Delivery: "Now the honest part" — pause before it. Volunteering the erosion is worth more
than the number costs you.*

---

### 2:20 – 3:00 · THE OBJECTION, AND THE ASK  *(Slide 7)*

> The strongest objection, and I will make it for you: indie reaches fewer people — twenty-nine
> to seventy-two percent of non-indie's hit rate — and the "engagement" half of the old story
> is untestable. This dataset has no playtime data, so we withdrew the claim rather than dress
> it up. The answer is that reach per title is not what a subscription optimises.
>
> What I want approved today: open negotiations on the four clean adds and the two stable
> restarts, and extend the availability screen from rank twenty-five to sixty. Temtem is the
> first cut if the budget bites.

*Delivery: "we withdrew the claim rather than dress it up" is the most valuable sentence in
the pitch — say it slowly and stop. Then the ask, plainly, and **stop talking.***

---

## If asked, in one line each

- **"Is that a cost figure?"** No — Steam retail price, measured identically on both groups.
  A comparison, not a cost. No sourced indie-tier Game Pass licence price exists.
- **"Owners?"** Bucketed SteamSpy estimates, not sales.
- **"Engagement?"** No playtime data exists in this dataset. We make no engagement claim.
- **"Does Steam transfer to Game Pass?"** Better than before, since the scope is PC. It still
  does not carry subscriber behaviour, console reach, or in-service merchandising.

---

## Traceability — every number spoken

| Spoken | Exact | Source |
|---|---|---|
| "sixty-three … forty-one" titles per $1,000 | 63.47 vs 41.39 (1.53×) | `21_indie_thesis.md` B-5; `sql/36` |
| "ninety-three dollars … against sixty-two" per million owners | $92.81 vs $61.93 (1.50×) | same |
| "a hundred and twenty-two thousand" | 122,191 non-demo titles | `sql/20_indie_definition_check.sql` |
| "five thousand reviews / seventy percent / seven hundred and fifty thousand owners" | ≥5,000 · ≥0.70 · ≤750,000 | `sql/30_indie_v2_candidate_screen.sql` |
| "five hundred and seventy-three eligible" | 573 (42.8% Metacritic) | `23_indie_model_v2.json` |
| "two hundred and one qualifying" | 201 at composite ≥0.60 | same |
| "twenty-five checked … twenty-one picks" | 25 screened; 21 picks | `24_availability_indie.md`; `25_indie_portfolio.json` |
| "recognition term cancelled itself out" | Spearman(proven, scarcity) = −0.762; Scarcity influence 0.030 | `11_redteam_scoring.md` RT-02 |
| "cheap pillar … no production budget" | Metacritic 5.7% (≤$2) → 22.5% (>$20) | `11_redteam_scoring.md` RT-04 |
| "*Papers, Please* … 3909" | `is_self_published` = developer==publisher string match | `22_redteam_indie.md` A-1 |
| "a hundred and eighty-one asset flips" | EroticGamesClub, 181 titles, admitted by the old rule | `23_indie_v2.md` A-1 |
| "fifty-three percent … twenty-one and a half … forty percent" | +53.3% pool · +21.5% portfolio (50.28/$1,000) · 40.3% of edge retained | `25_indie_portfolio.md` [DERIVED] |
| "twenty-nine to seventy-two percent" | Hit-rate ratios 29.4%–72.2% across four owner thresholds | `sql/35`; `21_indie_thesis.md` |
| "no playtime data" | All playtime columns constant zero, 140,077 rows | `01_profile.md`, `02_cleaning_report.md` |
| "rank twenty-five to sixty" | Ranks 26–60: 40.0% multiplayer vs 12.0% in ranks 1–25 | `25_indie_portfolio.md` |
| "Temtem is the first cut" | $44.99; cutting it lifts 50.28 → 53.66 per $1,000 | `25_indie_portfolio.md` [DERIVED] |

*Full evidence and the counterargument at full strength: `deliverables/indie_evidence_appendix.md`.*
