# Decisions — portfolio run

## Stage 10 — Scoring

- **`data/reference/web_indie_2025_2026.csv` (the open question GOAL_STATEMENT.md asks
  Simon to settle) does not exist anywhere on this filesystem** — checked with a full-disk
  search before scoring began. Decision: proceeded without it. Since the file cannot be
  read, its potential use to define "winning" is moot in this run regardless of what the
  answer would otherwise have been; no web-sourced list, curated or otherwise, was used to
  define the fit model's target, its features, or any threshold. Every input to the
  scoring model traces to `parquet/fact_games.parquet`, `genres_long`, or `tags_long`. If
  this file is added to the repo in a future run, the question needs re-settling
  explicitly before it is used, per the goal statement's own instruction.

- **Mapped the four "good pick" criteria onto four separately-scored pillars, one axis per
  criterion, rather than one blended metric.** Proven -> percentile of ln(review_total).
  Not-widely-owned -> percentile of -owners_mid. Fits-what-wins -> the out-of-sample-
  validated structural fit score. Cheap -> percentile of -price_usd. review_positive_ratio
  (quality) was deliberately kept as a hard gate (>=0.70) and NOT a fifth scored pillar,
  because scoring on it again after already gating on it would double-count the same
  signal and quietly upweight "quality" relative to the other three criteria without
  saying so.

- **Rejected review_positive_ratio as the "not universally owned" axis's counterpart and
  used raw review_total instead**, after the first scoring pass (quality-ratio as pillar 1)
  produced an "Anchor" tier dominated by titles with as few as 58-300 reviews at $0.99-
  $1.99 — technically passing every screen but not a signal any board could act on with
  confidence. Recognition/proof needed to be about SCALE (how much evidence exists), not
  just direction (was it positive) — ln(review_total) as its own percentile pillar fixed
  this because it directly rewards more evidence, independent of the already-gated
  quality floor.

- **Added a price_usd>0 screen (excluding 4,057 `paid`-labelled rows with price_usd=0)
  after spot-checking the first candidate run and finding "The Elder Scrolls Online -
  Elsweyr" ranked #1** — an MMO expansion with is_free=false but a stale/regional $0
  steamspy price, not a genuinely free listing. Treated as a data defect to exclude, not a
  signal that the title is "free to license."

- **Added an adult-content tag screen (Sexual Content / Nudity / Hentai, excluding 2,836
  titles) after spot-checking the second candidate run and finding shock/meme titles
  ("SEX with HITLER," "Hentai Police," "BOOBS SAGA") in the top 20 by composite score.**
  These titles cleared every quantitative screen (cheap, well-reviewed by volume, low
  owners) because they are cheap and attract ironic/meme-driven positive reviews at
  moderate volume — a case where the metrics were technically satisfied but the underlying
  signal was not what "proven reception" was meant to capture. Framed as a platform-policy
  fit screen (Xbox/Microsoft Store restricts this content far more than Steam does), not a
  taste judgment, so it has an externally defensible justification rather than an ad hoc
  one.

- **Set the ownership ceiling at owners_mid<=750,000, not a rounder number like 500,000 or
  1,000,000**, after spot-checking the buckets on both sides. The 1,000,000-2,000,000 and
  2,000,000-5,000,000 buckets are visibly dominated by already-massive, already-recognized
  franchise names (Starfield, Baldur's Gate 3, Assassin's Creed Origins, Persona 5 Royal)
  that Xbox either already publishes or the market has already reached at scale; the
  500,000-1,000,000 bucket (kept) still contains recognizable-but-not-saturated titles
  (Bloodstained, Tomb Raider: Anniversary, Dead Space remake, TEKKEN 8). Verified the
  eligible-pool size is not sensitive to the exact cutoff within a wide tested range
  (200k-3.5M all land within 16,499-19,732), so the choice of exactly 750,000 vs. a
  neighboring bucket boundary does not materially change downstream conclusions.

- **Excluded the fit model's age-since-release coefficient from the score used to rank
  candidates**, even though it is included in the model that was fit and validated. The
  age term exists only as a right-censoring control (older titles have had more time to
  accumulate reviews, per the dataset's own truncation hazard) — including its
  contribution in the candidate-facing "fit" score would silently reward vintage rather
  than genre/tag/mode fit, which is not what pillar 3 is supposed to measure.

- **Chose NOT to fix a single "top N" and instead set a bar on the composite score
  (0.60)**, per the goal statement's explicit instruction that a fixed count is "an
  admission that no threshold was chosen." Reported the full sensitivity table (0.50
  through 0.75) rather than picking 0.60 and hiding how arbitrary-looking neighboring
  values would have changed the list size, and stated plainly that the model's real
  precision degrades near the bar (Spearman rank stability of 0.56-0.75 under
  re-weighting) even though the top of the list is robust.

- **Assigned portfolio tiers (Anchor/Depth/Low-cost option) by an explicit
  review_total/price rule, not by re-slicing the composite score into thirds.** A pure
  score-tercile split would have called several ~65-review, $1 titles "Anchor" purely
  because a extreme cheap/scarcity percentile pulled their average up — not a defensible
  reading of "anchor" for a board pitch. The review_total>=1,000 floor for Anchor ties
  tier membership back to a criterion (scale of proof) a board would recognize as making a
  title safe to lead with.

- **Flagged the Randumb Studios / Chilla's Art / 07th Expansion repeat-qualifier pattern
  as a real producer-level finding, and separately flagged the Kairosoft / KOEI TECMO /
  Square Enix / Nihon Falcom deep-back-catalogue pattern (visible only at the broader
  eligible-pool level, before the composite bar) as interesting but NOT YET DEFENSIBLE** —
  the latter was not composite-ranked or reweighted to test whether it survives the same
  scrutiny as the former, and is reported as an open avenue rather than a finding.

- **Did not attempt to check Game Pass availability for any title.** Per the hard limits,
  this is not in the dataset and must be checked externally, per title, with a source and
  a date. Every row in `10_candidates.csv` carries
  `screen_gamepass_availability=PENDING_EXTERNAL_CHECK` rather than a guess.

## Stage 11 — Red team

- **Verdict: REBUILD.** Full findings in `artifacts/11_redteam_scoring.md`. Not contested
  — every fatal finding (RT-01 through RT-05) reproduced on independent verification in
  Stage 12 before being fixed. This is recorded rather than summarized away because the
  Stage-10 model's failure mode (a composite that cancels the exact tension the brief
  asked for) is the kind of thing that looks fine until someone actually checks it, and
  the checking is the point.

## Stage 12 — Scoring rebuild

- **Verified the coordinator-forwarded "reported yield" before using it, per explicit
  instruction not to trust it any more than the critic trusted Stage 10.** Direct query
  confirmed pool=926 is the count WITHOUT `has_controller_support=true` applied, even
  though the rebuild spec's own bulleted list instructs adding that gate, and confirmed
  Temtem and ICARUS (both in the reported top-10) have `has_controller_support=false` and
  therefore cannot appear in a correctly-gated pool. Chose to implement the gate
  literally, as the spec states it (pool=638, not 926), and to document the discrepancy
  rather than either (a) silently reproducing the ungated number to match what was
  "expected," or (b) silently dropping the gate to match the reported number. Either of
  those would have repeated exactly the failure mode this whole exercise exists to catch
  — an unverified number quietly becoming the record.

- **Retargeted Fit to `review_positive_ratio` rather than dropping it entirely**, though
  RT-05 offered both options ("either drop Fit, or retarget it at something Proven does
  not already measure"). Quality is not encoded anywhere else in the v2 composite
  (Recognition and Headroom are both built from `review_total`/`owners_mid` only), so a
  retargeted Fit adds real, non-redundant information at a reduced 20% weight, rather than
  losing a pillar's worth of signal entirely. Excluded `price_usd` from Fit's own features
  (not just from the composite) specifically so price could not re-enter the ranking
  through the Fit door — a retargeted-but-still-price-fed Fit model would have undone the
  rebuild spec's "take price out of the score entirely" instruction by a side channel.

- **Excluded `is_indie_i` from the v2 feature set, keeping only `genre_Indie`** — RT-05
  found the two perfectly collinear in v1 (identical -0.1155 coefficients), meaning
  "indie" was being counted twice under two different feature names.

- **Reused the owners_mid<=750,000 ceiling exactly as instructed ("KEEP") without
  re-deriving its justification from scratch**, but added the RT-09 honesty correction
  that it is a coarse, bucket-driven cut (only 6 distinct owners_mid values in this pool;
  no value exists between 750,000 and 1,499,999, so 750k and 1M ceilings are provably
  identical). Chosen over silently repeating v1's "sensitivity table" that reported the
  same count twice without explaining why.

- **Chose an elbow in Metacritic presence, not a round number or a percentile of the
  eligible pool, to justify `review_total>=5,000`** specifically. Metacritic coverage is
  the one signal in this dataset that is genuinely independent of review count itself (a
  press outlet reviewing a game is a different act from a player self-selecting into
  leaving a Steam review), so using it to locate where a recognition floor "pays for
  itself" is a materially different and stronger argument than reusing Valve's own
  review-count-nuance threshold (the exact mistake RT-06 identified in v1).

- **Recalibrated the Anchor/Depth/Low-cost tier thresholds to the v2 population's own
  distribution rather than reusing v1's absolute review-count numbers.** Checked first:
  reusing v1-style thresholds (e.g. 1,000 or 10,000 reviews) against a population whose
  own Proven floor is now 5,000 would have made Anchor ~90% of the qualifying list again —
  the identical defect RT-07 flagged, just relabeled. Set Anchor at review_total>=20,000
  (roughly the qualifying list's own 74th percentile) OR (metacritic present AND
  owners_mid>=350,000), verified this produces a genuinely three-way split (131/74/10)
  rather than one tier swallowing the list.

- **Reported reweighting stability as top-30 Jaccard overlap, not full-pool Spearman**,
  per RT-10's finding that Spearman across hundreds of rows is nearly blind to reordering
  at the extreme, which is the only region a shortlist decision actually uses.

- **Collapsed serialized chapters into one licensable property per (developer,
  heuristic-base-title) for the monoculture check's franchise-concentration count only —
  never to drop or merge rows in the deliverable CSV.** The goal statement requires one
  row per app_id with its own app_id; collapsing chapters in the diversity diagnostic
  and then separately reporting "213 distinct properties from 215 qualifying rows"
  keeps both requirements satisfied rather than trading one off against the other.

- **Kept v1's outputs (`10_scoring.md`, `10_candidates.csv`, `10_model.json`) in place,
  unmodified, alongside v2** rather than overwriting them, per the explicit instruction
  that the v1-to-v2 progression is itself part of the deliverable — a red-teamed model
  that visibly changed in response to specific, reproduced findings is stronger evidence
  than a clean rebuild with no paper trail of what was wrong and why.

## Stage 15 — Red team of v2 rebuild + portfolio

- **Recorded, without editorializing, that the Stage-15 critic conceded its own Stage-11
  reported yield (926) was wrong** and that the Stage-12 analyst's independent
  verification of it was the correct handling. Not our finding to take credit for, and not
  a finding to bury either — it belongs in the record because it demonstrates the
  verify-before-trusting discipline worked in both directions across stages, not just
  analyst-to-critic.

## Stage 16 — Scoring v3

- **Scoped this stage strictly to what the coordinator named** (A-4 reweight, A-3
  disclosure, the B-5 echo, the cheap A-2 floor fix, and the Deep Rock Galactic: Survivor
  data-quality check) and explicitly declined to act on Part B of
  `15_redteam_portfolio.md` (B-1 through B-6 — traceability wording, Tier 1 lead
  ordering, Tier 3/4 relabelling, the concentration remedy, sizing framing) even though
  several of those findings are well-evidenced. The coordinator's instruction was "do not
  reopen anything else," and Part B belongs to a downstream portfolio-construction stage
  this session does not own the output file for. Silently fixing it anyway would exceed
  the mandate; silently ignoring that it exists would be worse — so it is named here as
  explicitly out of scope for this stage, not resolved and not forgotten.

- **Adopted the critic's own suggested reweighting (Recognition 0.50 / Headroom 0.40 /
  Fit 0.10) rather than deriving an independent alternative**, since A-4's argument (a
  pillar with negative in-population R² cannot carry 20%) is correctly reasoned and the
  proposed split is a modest, defensible correction rather than an extreme one (Fit still
  contributes; it is no longer load-bearing). Considered dropping Fit to 0% instead
  (which RT-05/A-4 both floated as an option) and rejected it: Fit's out-of-sample
  Pearson r (0.377–0.388) is still positive, significant, and non-redundant with
  Recognition/Headroom (unlike v1's Fit, which restated Recognition) — a small non-zero
  weight uses that real signal without letting a weak model drive the ranking, which a
  0% weight would waste and a 20% weight would over-trust.

- **Verified the A-3 within-bucket collapse myself before writing anything into either
  scoring document**, rather than accepting the critic's Spearman=1.0000 claim on its
  reported precision alone. Reproduced it exactly on the v2 pool (three buckets, n=31/
  243/360, each 1.0000 to four decimal places) and additionally checked it on the new v3
  pool (six buckets, including two with n<5 left unreported per the same n>=5 convention
  used throughout this run) — confirmed it holds under the floor change too, so the
  disclosure is not specific to a pool that happens to no longer exist after the A-2 fix.

- **Wrote the A-3 finding as an inline correction block into the existing
  `12_scoring_v2.md`, rather than only into the new `16_scoring_v3.md`**, per the explicit
  instruction to write it "plainly into 12_scoring_v2.md and DECISIONS.md." The
  alternative — leaving v2's original claim ("complementary, not cancelling") standing
  uncorrected in its own file while only the newer v3 document carries the honest
  version — would let a reader who opens v2 alone (a real risk, since v1 and v2 are both
  kept in place as part of the documented progression) walk away with the disproven
  claim.

- **Did not attempt to re-derive Headroom from a different formula to "fix" A-3.** The
  critic was explicit that this finding "cannot be fixed, only documented," and
  independent verification agreed: the coarseness is in `owners_mid` itself (5-6 distinct
  values catalogue-wide in this pool, a SteamSpy bucket-midpoint limitation documented
  since `01_profile.md`), not in how the ratio is computed from it. Any reformulation
  using the same column would inherit the same step-function structure. Building a
  finer-grained ownership estimate is a data-acquisition problem, not a scoring-formula
  problem, and is out of scope for a scoring stage working from this dataset.

- **Reported the B-5 echo (60.0% of the v3 qualifying list sits in the 750k-owner bucket)
  as a stated property of the scoring design, without recomputing or presenting the
  200k–500k-ceiling sensitivity view B-5 suggested.** That sensitivity view is properly a
  portfolio-stage question (does the board want to see a lower-ceiling alternative
  portfolio), and producing it here would have meant partially reopening Part B under
  cover of "just an echo." Named the mechanism (Recognition continuous and dominant vs.
  ownership as a coarse pre-screen) instead, which is the scoring-stage's own
  responsibility to state.

- **Moved the review-count floor from 5,000 to 4,000 rather than defending 5,000.**
  Checked for a reason to keep 5,000 despite the critic's finer-grained table (round
  number, matches an earlier informal target, etc.) and found none that survives the
  coordinator's explicit "it is where the critic put it is not a reason" instruction —
  4,000 is where the metacritic-presence curve's own elbow sits, verified independently,
  and the larger resulting pool (802 vs 638) has no identified offsetting cost. This is
  the "cheap fix" the coordinator characterized it as: unlike A-3/A-4, there was no
  principled reason available to prefer the more expensive option.

- **Confirmed Deep Rock Galactic: Survivor's flags are correct by reading the raw
  category and tag strings directly**, rather than assuming either "the flags must be
  wrong, the hazard is documented" or "the downstream label must be wrong, trust the
  pipeline." The raw data is unambiguous, English-language, and contains no co-op or
  multiplayer marker of any kind for this specific app_id, while the base game (a
  different app_id) correctly does — this is a genuinely single-player spin-off, not a
  localization casualty. Logged as a closed data-quality check with no action needed,
  rather than either silently correcting a downstream document this stage doesn't own or
  silently agreeing the flags might be wrong without checking.

---

## Stage 14 — Portfolio construction (2026-08-22)

- **Built the portfolio by JOINING the two upstream artifacts in code
  (`scripts/14_build_portfolio.py`) rather than transcribing titles by hand.** The script
  keys `12_candidates_v2.csv` and `13_availability.json` on `app_id` and calls `sys.exit`
  if a portfolio title is absent from either. Traceability is therefore a property of the
  build, not a claim in the prose — a hand-typed list can drift from its sources between
  edits and this one cannot.

- **Accounted for all 30 availability-screened titles explicitly: 24 picks + 5 stated
  exclusions + 1 named alternate (Marvel's Guardians of the Galaxy).** Verified in code
  that the union of picks, exclusions and that alternate equals the 30 app_ids in
  `13_availability.json`. Nothing was dropped silently, which is the failure mode a board
  detects by asking "what happened to number 11?"

- **Restricted portfolio PICKS to the availability-screened top 30, and drew every tier
  ALTERNATE from ranks 31+ with its missing verdict stated on the row.** Stage 13 screened
  only the top 30, so a pick from rank 32 would carry an availability claim nobody made.
  Making ranks 31+ the alternates satisfies the goal statement's "one named alternative per
  tier" while keeping the unverified status visible rather than laundered.

- **Did not invent a per-title licensing price, and did not extrapolate downward from the
  AAA figures.** Used the one sourced range that genuinely spans this tier (MacIntyre,
  $50K to over $50M across 500+ deals, TweakTown 2025-07-13) and stated that no public
  breakdown of its low versus high end exists. Made the recommendation robust to that gap
  by ordering the tiers on **deal structure** — prior deal exists / port exists / status
  known / counterparty scale — so the board can commit tier by tier and stop where the
  quotes stop making sense.

- **Refused retail price as the cost ordering, per RT-04.** Stage 11 established that price
  in this catalogue is a monotone proxy for production budget and press coverage
  (Metacritic presence 5.7% → 22.5% across price bands), so ordering cost by sticker price
  would resurrect exactly the error the rebuild removed. The price column survives in the
  JSON only under the name `price_usd_retail_not_licence_cost`.

- **Ranked Unpacking (v2 rank 3) above Phoenix Wright (v2 rank 1) inside Tier 1.** The tier
  is ordered by executability, not composite: Unpacking left Game Pass roughly two months
  ago, which is the warmest counterparty relationship in the top 30. Recorded because it is
  the one place the portfolio order visibly departs from the score order, and an examiner
  will ask whether that was deliberate.

- **Attached the "check Microsoft's internal record of the prior run" condition to Tier 1
  as a removal RULE, never as the headline.** The forbidden outcome is recommending
  measurement instead of action; six named titles with a condition attached is action. Kept
  the six as picks that stand even if the board declines the check.

- **Placed Journey in Tier 4 rather than Tier 1** even though it is confirmed rotated out,
  because press coverage framed its July 2024 addition specifically as *PC* Game Pass and
  Stage 13 could not confirm a native Xbox console SKU. A restart only earns Tier 1's cost
  advantage if the SKU it restarts exists.

- **Held Marvel's Guardians of the Galaxy as an alternate rather than a Tier 1 pick**
  despite a clean rotated-out verdict: the counterparty changed (Embracer bought
  Eidos-Montréal and the IP from Square Enix in 2022), so the prior yes was given by a
  company that no longer holds the rights, and the licensed Marvel property adds a second
  rights holder this analysis never screened.

- **Reported the portfolio's own genre concentration against the 215-title list rather than
  in isolation**, and named the remedy titles. Portfolio: Action 4/24 (16.7%), multiplayer
  4/24 (16.7%). Qualifying list: Action 50.7%, multiplayer 30.7% (n=215). The top-30 slice
  is materially more singleplayer-narrative than the list it came from. Named five co-op /
  multiplayer titles from ranks 40–58 as the remedy rather than describing the gap
  abstractly, per FORBIDDEN OUTCOMES §3 and §4.

### Portfolio structures generated and rejected

Six structures were built out before one was chosen.

1. **Reuse the CSV's own Anchor / Depth / Low-cost score tiers.** *Rejected:* those tiers
   are score bands, not roles. Anchor is 131 of 215 titles and answers "how recognisable,"
   which the composite already answered. The task asked for tiers where each has a job; a
   score band's job is to restate the ranking.
2. **Tiers by availability status** (rotated_out / clean / unknown / port-gapped).
   *Rejected in pure form, adopted in substance.* Status is a fact about a title, not a job
   in a portfolio. The chosen structure keeps the same partition but defines each tier by
   what it does for the board — restart a proven deal, lead the pitch, buy breadth, stay
   visible — with the status as the tier's evidentiary basis rather than its name.
3. **One title per genre, twelve genres.** *Rejected:* it would have forced the exclusion of
   Phoenix Wright, Danganronpa 2 and Edith Finch (all Adventure) purely to fill a Racing or
   Sports slot from further down an unscreened list. Manufactures diversity by discarding
   the strongest evidence. The concentration is instead reported honestly with named
   remedies.
4. **Cost tiers by retail price band** ($0–5 / $5–20 / $20+). *Rejected on RT-04 grounds* —
   see above. This is the rejected structure most likely to be proposed in the room, which
   is why it is recorded rather than merely avoided.
5. **Two tiers: "sign now" and "diarise."** *Rejected:* it collapses the distinction between
   a lapsed deal with a warm counterparty and a cold licence with a fresh one, which is the
   single most decision-relevant difference in the evidence, and it leaves the board no way
   to stop partway.
6. **All 215 qualifying titles grouped into role tiers.** *Rejected:* 185 of them have no
   availability verdict, so 86% of that portfolio would rest on an unmade claim. The
   ranked 215 remains the deliverable in `12_candidates_v2.csv`; the portfolio is the
   screened subset that can be acted on tomorrow morning.

---

## Stage 17 — Final portfolio, rebuilt on v3 (2026-08-22)

Responses to `15_redteam_portfolio.md` Part B. Every objection is conceded, bounded or
rebutted — none dismissed.

- **B-2 (T1 leads on executability, not desirability) — CONCEDED in full.** The clean spine
  now leads and the restarts follow, relabelled "cheapest to execute, pending one internal
  check." The critic is right that this costs nothing: the six restart titles keep their
  cost advantage, their removal rule and their place in the portfolio. What changes is that
  the board no longer hears "buy back six games we gave up" as the opening sentence.

- **B-3 (under-sold T3, over-sold T4) — CONCEDED in full, and the headline changed.** 17
  picks + a 7-title watchlist, not 24 picks. Verified in code: 17/17 picks have a confirmed
  Xbox SKU, and 6/7 watchlist entries do not. Tier 3's strength is now stated positively
  (8/8 confirmed Xbox SKU, only current status open, both branches already resolved by its
  own removal rule) rather than hedged. The watchlist carries a **promotion trigger** rather
  than a removal rule, because the picks' removal rule is inoperative on six of its seven
  entries — which is the reason they are not picks.

- **B-4 (the concentration remedy does not work; one alternate misdescribed) — CONCEDED,
  and the remedy replaced rather than repaired.** Deep Rock Galactic: Survivor is withdrawn;
  Stage 16 confirmed the dataset flags are correct and our label was the error, and that is
  stated in the artifact rather than quietly dropped. The v2 "extend to rank 60" remedy is
  withdrawn: measured on v3, ranks 31-60 are 23.3% multiplayer against 13.3% in ranks 1-30 —
  an improvement over v2's 16.7%/16.7%, confirming the coordinator's hypothesis that cutting
  Fit to 10% reduced the sentiment tilt, but still not where the density is. The position is
  now that the concentration is an **accepted, explained property** of a Recognition-led
  ranking, with the mechanism named (Recognition 0.50 plus Fit's residual sentiment tilt),
  and the only intervention that would actually work costed honestly: extend the screen to
  rank 120, which would surface 22 titles with **verified** co-op and multiplayer flags,
  none of which can be a pick today. Every one of those 22 flags is asserted in the build
  script rather than trusted from a label — the specific failure that produced the v2 error.

- **B-5 (the ceiling defines rather than filters) — CONCEDED, stated as a design property.**
  60.0% of the qualifying list versus 48.1% of the pool, 15 of 17 picks in the top bucket.
  The mechanism is now given completely, including the half the v2 artifact omitted: the
  ownership term is only a three-level step and cannot offset a continuous 0.50-weighted
  Recognition term. The 200k-500k sensitivity the critic asked for is computed and reported
  (110 of 275 titles; 11 of its top 15 never screened), which is what makes the honest
  answer to "did you pick these, or did the threshold pick them?" available in the room.

- **B-6 (the $50K-$50M range is not a range) — CONCEDED.** Removed from the sizing section
  entirely and relabelled Q&A context. The sizing section now states plainly that no
  defensible per-title price exists and offers the execution ordering instead, which is what
  the portfolio actually delivers.

- **B-1 (traceability claim overstated; two rank methods) — CONCEDED.** All ranks now derive
  from a single method: position in `16_candidates_v3.csv`, with the sort order asserted in
  code rather than assumed. The availability JSON's `rank` field is v2 and is never used as
  a rank. The claim is restated as "every figure is joined, never typed; tier membership,
  ordering and rationale are authored judgments."

- **Carried the A-3 disclosure into the portfolio's own opening, not just the scoring
  artifact.** The composite is described everywhere as "Recognition, banded by a three-level
  ownership step," never as a multi-pillar blend. This matters more downstream than upstream:
  the scoring document's readers already know how it was built, and the board's do not.

- **Flagged Dead Space (v3 rank 20, MC 87) and Lies of P (v3 rank 21) as top-ranked but
  unscreened, and did NOT pick them.** The floor move to 4,000 and the reweight brought both
  into the v3 top 30, but Stage 13 screened the *v2* top 30 and never touched them. Naming
  them as the first two titles any screen extension should cover is more useful than either
  silently omitting them or asserting an availability status nobody checked.

- **Kept all 24 v2 titles in the document rather than dropping the seven that became
  watchlist entries.** Withdrawing them would have hidden the exposure the critic found;
  relabelling them keeps it visible and gives the board a named trigger for each.
