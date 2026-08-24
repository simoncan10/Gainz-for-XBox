# Goal statement — Gainz-for-XBox

Paste this at the top of any agent run. Every agent gets it, unchanged.

---

## THE DECISION

The Xbox / Microsoft board must decide **which specific games to add to the Game Pass
portfolio**. Not whether to add games. Not how much to spend in aggregate. Which titles.

The answer is a **ranked shortlist of named titles**. Any output that does not contain
specific game names and app_ids has failed the brief, however well-reasoned it is.

## REQUIRED OUTPUT SHAPE

- **A ranked list of every title that clears the bar.** No fixed count. The games are being
  scored, so the score decides membership — a cap on top of a ranking is arbitrary and adds
  nothing the ranking did not already say. If 40 titles qualify, the list has 40 titles.
- **The bar itself is the thing that must be justified.** State the qualifying threshold and
  why it sits there — a defensible cutoff is the real deliverable, and it must survive the
  same scrutiny as any other number. "Top N" is not a threshold; it is an admission that no
  threshold was chosen.
- **Each row carries:** app_id, name, developer, score, review count, owners range, and the
  status of every screen it passed.
- **Group the qualifying list into tiers** by role (anchor / depth / low-cost option) so it
  can be read as a portfolio rather than a leaderboard. Tiers are a way of reading the list,
  not a way of shortening it.
- **The pitch highlights a handful; the list is the deliverable.** Whatever gets spoken
  aloud is an illustration of the list, and the spoken selection must follow a stated rule
  rather than taste.
- **One sentence per title** on why it is in the list, tracing to a finding
- **One stated rule** for what would remove a title from the list
- **One named alternative per tier** — the next title down, in case a pick turns out to be
  unavailable. These live on the Q&A sheet, not in the spoken pitch, so they cost no words
  but are ready when someone asks "what if the rights are tied up?"

## THE PICKS MUST COME FROM THE DATASET

Every recommended title must originate in the Steam snapshot in `data/raw/super raw/`.
No title may be introduced from web research, industry press, or general knowledge.
If a game is not in the data, it cannot be recommended — however obviously good it looks.

Web research is still allowed, but only in these two roles:

1. **To EXCLUDE a candidate.** Game Pass availability is not in the dataset, so it must be
   checked per title with a source and a date. This removes titles from a list the data
   produced; it never adds one.
2. **To ARGUE for the picks.** Market context, Xbox's strategic position, what recent
   breakouts have in common — this supports the case for titles the data already chose.

The test: **could this title have been found without the internet?** If no, it is out.
A web-sourced title is a violation of the brief even if it would have been a better pick,
because the assignment is to demonstrate what the data can produce.

> **Open question for Simon to settle before running:**
> `data/reference/web_indie_2025_2026.csv` is hand-curated from gaming press and sits in
> the repo. It is your data in the sense that you built it, but web-sourced in origin.
> Decide explicitly whether it may be used to define what "winning" looks like (it never
> supplies picks either way, since those come from the snapshot). Write the decision into
> this file and into DECISIONS.md — an examiner will ask, and "we thought about it and
> chose X because Y" is a much better answer than discovering the ambiguity in the room.

## WHAT COUNTS AS A GOOD PICK

A title belongs on this list if it is:

1. **Proven** — enough review volume that its reception is a real signal, not noise
2. **Not already on Game Pass** — subscription value is access to what people don't have
3. **Not already widely owned** — recognition should be high, ownership low. These pull in
   opposite directions and the tension is the interesting part of the problem
4. **Aligned with what the evidence says wins** in this catalogue
5. **Cheap relative to the alternative** — back-catalogue licensing, not development

## OUT OF SCOPE — DO NOT RECOMMEND

These are excluded by the board's situation, not by preference. Do not propose them,
and do not propose them in disguise.

- **Studio acquisition, studio funding, or new studio formation.** Microsoft closed or
  divested Ninja Theory, Double Fine and Compulsion in July 2026 and reoriented around
  flagship franchises. This door is shut.
- **Pricing changes.** Game Pass Ultimate already moved $19.99 → $29.99 → $22.99. Not the
  question being asked.
- **Building new games.** The ask is what to ADD to the portfolio, from what exists.
- **Measurement, audits, instrumentation, or "gather more data first" as the headline
  recommendation.** See FORBIDDEN OUTCOMES.

## FORBIDDEN OUTCOMES

These are the ways this analysis fails while appearing rigorous. Any of them means the
run must be redone, not accepted.

1. **Recommending measurement instead of action.** "Run an audit first", "instrument it
   and revisit", "we cannot say until we have engagement data" — these are the safest
   possible answers for an analyst and they answer a question nobody asked. If the
   evidence is weak, name the picks anyway and mark the confidence low. A low-confidence
   named list beats a high-confidence refusal.
2. **Recommending nothing.** "Spend $0" is not an available answer. The board has already
   decided to add titles; the only question is which.
3. **A strategy with no names in it.** Frameworks, decision trees, thresholds and staged
   gates are supporting material at most. They are not the deliverable.
4. **A monoculture.** Five titles from one micro-genre is one bet made five times. If the
   evidence genuinely points to one genre, say so explicitly and defend the concentration
   as deliberate — but check first whether it is a real finding or just the ranking metric
   restating its own inputs.

## CONSTRAINTS ON HONESTY

These are not in tension with the above. Name the picks AND state the limits.

- There is **no engagement or playtime data** in this dataset. Every playtime column is
  zero. Claim nothing about retention or session length.
- **Owners are bucketed SteamSpy estimates**, not measured sales.
- **Review counts are self-selected** and vary by genre, price and audience size.
- The data is **Steam PC**; the recommendation is for **Xbox console**. Console ARPPU is
  roughly 48% higher and the genre mix differs. State this before the board does.
- **Game Pass availability is not in the dataset.** It must be checked externally, per
  title, with a source and a date.
- Prices in `games.csv` are **99.1% EUR**, not USD. Use the steamspy price column.
- `release_date` is right-truncated (nothing after Oct 2024) and 20.4% missing.

## EVERY NUMBER NEEDS A REASON AND A SOURCE

No figure appears anywhere — pitch, slides, appendix, Q&A — without both. A number is
allowed only if it falls into one of these three categories, and it must be labelled as
which one:

| Type | What backs it | What must be recorded |
|---|---|---|
| **Measured** | A query against the dataset | The `.sql` file that produced it, and n |
| **Sourced** | An external publication | Source name, URL, publication date, and whether it is primary, secondary or an estimate |
| **Derived** | Arithmetic on the above | The full calculation written out, and every input traced to a Measured or Sourced figure |

Rules that follow from this:

- **If it cannot be attributed, it cannot be said.** Not softened, not hedged, not put in
  the appendix — removed. A figure that sounds right is the most dangerous kind, because
  nobody questions it.
- **Every query gets saved.** A number computed in a throwaway command exists nowhere and
  is therefore unsourced, even if it is correct.
- **Report n alongside every statistic.** A median over 11 titles is not a finding.
- **Estimates are labelled as estimates**, every time they are stated. "Roughly 30 million
  Game Pass subscribers" is only sayable as an estimate — Microsoft does not disclose it.
- **Inferred is not measured.** Owners are bucketed SteamSpy ranges, not sales. Say which.
- **Rounding may not do hidden work.** If rounding changes what a number implies, show the
  unrounded figure too.
- **Withdrawn numbers stay withdrawn.** If a figure was cut during review, it does not
  return later because it sounds good aloud. This is the most common way an unsourced
  number re-enters a finished deliverable.

Maintain a **traceability table** at the foot of the pitch script listing every spoken
figure and what backs it. If a number is in the speech but not the table, it is not ready.

## AUDIENCE AND FORMAT

The Microsoft / Xbox board. The deliverable is a **spoken pitch**, kept brief, with slides
behind it and a Q&A sheet. The board is not an audience for a mystery: name the titles
early, then justify them.

## THE TEST

Read the output and ask: **could someone act on this tomorrow morning?**

If it names five games and someone could start making calls about them, it passed.
If it describes what should be considered, or what should be measured first, or under
what conditions a decision could later be made — it failed, and no amount of rigour in
the supporting analysis changes that.
