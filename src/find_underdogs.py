"""Cross-reference our full indie candidate universe against the top-50 winning
profile to find "underdogs": games that statistically fit the same DNA as the
Steam top-50 breakouts (data/processed/top50_indie_reference.csv /
top50_match_profile.csv, built by build_top50_datasheet.py) but have NOT yet
broken out commercially and are NOT already on Xbox Game Pass - i.e. plausible,
under-the-radar Game Pass acquisition targets rather than games subscribers
likely already own or can already get.

Reuses profile_fit_score from indie_candidates_scored.csv as the similarity
metric. That score is a naive-Bayes log-likelihood ratio against the winner
cohort, validated at AUC 0.939 in-sample / 0.950 held-out (see
build_top50_datasheet.py) - a statistically grounded "how much does this game
look like a top-50 winner" measure, not an ad hoc one.

Underdog filter, applied to indie_candidates_scored.csv (85,632 rows):
  - in_winner_cohort == 0      (excludes games that already broke out: >=8
                                 review_score, >=20,000 reviews, >=1,000,000
                                 owners - these are winners, not underdogs)
  - in_top50_reference == 0   (excludes the top-50 set itself)
  - evidence_tier == "high"    (>=5,000 reviews - enough signal that the
                                 review_score is trustworthy, not a fluke)
  - review_score >= 6          (excludes games that fit the profile's tags but
                                 are actually poorly received)
  - ranked by profile_fit_score descending (similarity to the winning profile)

gamepass_status is then attached from GAMEPASS_STATUS_OVERRIDES: a hand-checked
lookup (web search, see reports/logs/session_log_2026-08-21.md entry 4 for sources
and date), since indie_candidates_scored.csv has no such column and the game's
own metadata predates most Xbox ports. Rows already confirmed on Game Pass are
kept in the output (visible, flagged) but excluded from the final top-5 pick.

Output: data/processed/underdog_candidates.csv - the full filtered/ranked pool
(not just 5), so the next 5 are visible if any pick later turns out to already
be on Game Pass.
"""
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "data" / "processed" / "indie_candidates_scored.csv"
DST = PROJECT_ROOT / "data" / "processed" / "underdog_candidates.csv"

MIN_REVIEW_SCORE = 6
REQUIRED_EVIDENCE_TIER = "high"
TOP_N = 5

# Hand-checked via web search (dates below), not derivable from data/raw.
# status: "not_on_gamepass" | "on_gamepass" | "unverified"
GAMEPASS_STATUS_OVERRIDES = {
    "418030": ("not_on_gamepass", "Subsistence - PC-only, no Xbox port found; checked 2026-08-21"),
    "526160": ("not_on_gamepass", "The Wild Eight - purchasable on Xbox store, but not in Game Pass catalogue; checked 2026-08-21"),
    "1159690": ("on_gamepass", "Voidtrain - added to Xbox Game Pass day-one, 2025-11-07 (Pure Xbox / Xbox Wire)"),
    "393420": ("not_on_gamepass", "Hurtworld - no Game Pass listing found; checked 2026-08-21"),
    "951440": ("not_on_gamepass", "Volcanoids - PC-only, devs have only discussed a future console port; checked 2026-08-21"),
    "250400": ("not_on_gamepass", "How to Survive - no current Game Pass listing found; checked 2026-08-21"),
}


def main():
    with SRC.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    pool = [
        r for r in rows
        if r["in_winner_cohort"] == "0"
        and r["in_top50_reference"] == "0"
        and r["evidence_tier"] == REQUIRED_EVIDENCE_TIER
        and int(r["review_score"] or 0) >= MIN_REVIEW_SCORE
    ]
    pool.sort(key=lambda r: -float(r["profile_fit_score"]))

    for r in pool:
        status, note = GAMEPASS_STATUS_OVERRIDES.get(r["app_id"], ("unverified", ""))
        r["gamepass_status"] = status
        r["gamepass_note"] = note

    picks = [r for r in pool if r["gamepass_status"] != "on_gamepass"][:TOP_N]
    for r in pool:
        r["is_top5_pick"] = int(r in picks)

    cols = list(pool[0].keys()) if pool else []
    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(pool)

    print(f"underdog pool (fit profile, not yet a winner, evidence_tier={REQUIRED_EVIDENCE_TIER}, "
          f"review_score>={MIN_REVIEW_SCORE}): {len(pool)} games")
    print(f"wrote {len(pool)} rows to {DST}\n")
    print(f"Top {TOP_N} picks (excludes anything already on_gamepass):")
    for r in picks:
        print(f"  {r['app_id']:>8}  {r['name']:<30}  fit={r['profile_fit_score']:>6}  "
              f"reviews={r['total']:>6}  owners={r['owners_range']}  {r['gamepass_status']}")


if __name__ == "__main__":
    main()
