# Ledger — skill-craft

The repo's on-disk ledger: one line per entry, append-only,
chronological. Facts with their basis, decisions with their why (and
the rejected alternative where it is not obvious), open questions.
Absence of an entry never reads as settled. Form and trigger:
`~/.claude/CLAUDE.md`, "Insurance mechanisms" — not restated here.

Consumer: the next session working in this repo, read before
re-deriving anything that may already be settled. The split against
the other role files is declared in `CLAUDE.md`.

Seeded 2026-08-06 from `git log` over the preceding three weeks, and
deliberately thin: only decisions whose rationale lived ONLY in a
commit message were lifted. Anything already carried by
`dev-notes/OBSERVATIONS.md`, `BACKLOG.md` or `PLAN.md` stayed there.

- 2026-07-26 DECIDED (24bf274, v1.0.69): the voice-terms alias (evidence-voice / directive-voice) dropped from "The two registers" — a grep across this corpus and the operator stack found the terms in ZERO operational files (maintainer journals exempt), so the alias failed the density test. This SUPERSEDES 05991bc's B1 keep-as-alias disposition, on that new evidence; the canonical-term obligation's surface-the-substitution duty was discharged once in 05991bc's commit body and is not owed as permanent rule text.
- 2026-07-26 FACT + DECIDED (7f6ae18, v1.0.70): the Tier 2 arm-contamination check in `references/evaluation.md` is Path-1 grounded in an EXTERNAL incident — DietrichGebert/ponytail's agentic benchmark (`benchmarks/results/2026-06-18-agentic.md`, "A contamination bug we found in our own numbers"), where a plugin SessionStart hook fired on the no-skill baseline arm and shrank a real -54% delta to a false ~4%, nearly published. The class fails toward false-inert, which is the reading Tier 2 acts on. Rejected: reading a clean coined-terms grep as proof of a clean arm — hence the no-hit branch is written in evidence register, not as a clearance. `dev-notes/OBSERVATIONS.md:1415` cites the check but carries none of this grounding.
- 2026-08-05 ACCEPTED (7d7a741, v1.1.0): three known limitations in the release-activation machinery, operator-accepted — not defects to re-litigate. (a) `README.md`'s Files table "Loaded" column mixes load-timing with component-kind values across three rows; a separate section costs more than it clarifies at this size. (b) `plugin-update-reminder.py`'s PATTERN matches the command string inside quotes and comments; it is a reminder-only hook, so a false fire is one harmless context line. (c) A bare skill name colliding with a like-named plugin would gate a user-level skill by that plugin's pin; verified no such collision exists today, and the failure direction is a one-keystroke reload.
- 2026-08-06 DECIDED (a3edc4c, operator correction): skill-craft stays PURE CRAFT — workflow and reporting conventions (the grilling / frontier-round format) are not skill-craft work at ANY backlog grade; they mint into the operator corpus instead (dotfiles f3dfa52). Rejected: parking it here as a future canon item, which is where it had been filed. `BACKLOG.md` carries the drop line; `dev-notes/OBSERVATIONS.md:1420` still points at "the parked grilling-variant BACKLOG item" and is stale.
- 2026-08-06 DECIDED (e11b75d, operator release GO): 2.0.0 released immediately as an old→new replacement — only the new canon visible, history preserved by git. This SUPERSEDES `PLAN.md`'s trial gate, which still reads "The installed 1.2.0 pin IS the freeze" and "2.0.0 releases only after a real trial: producing at least one real skill well" (PLAN.md:16-19); b039d23's "No release: installed pin stays 1.2.0" is likewise historical. OPEN: the named trial — the anneal-successor lift from statiker — has not run, and `PLAN.md` is unamended, so it reads as a live gate to anyone who opens it.
- 2026-08-06 DECIDED (21d4348, v2.0.1): `commands/` sits OUTSIDE skill-craft's governed set (`CLAUDE.md` declares that set as `plugin/skills/skill-craft/SKILL.md` + `references/*.md`), so a fix there is surfaced to the operator per the reflexivity rule but mandates NO self-review dispatch. Applied when `/eval-skill`'s raw `$ARGUMENTS` substitution was repaired: the argument now resolves to a bare skill name once, in Step 1, rather than being re-substituted at seven separate use points — one home for the resolution instead of relying on the reader to remember it.
- 2026-08-20 DECIDED (operator GO "GO" + "make it live"): 2.2.0 canon
  pass drains both carriers in one release — OBSERVATIONS entries
  08-09→08-20 (8 annotated: invariance widening, amendment inverse
  direction, trigger-anchor tests, unbound-reference test, lever trio,
  eval deltas ×4, birth branch, era-re-grade citation reconciled) and
  5 BACKLOG entries left by ref. Basis per edit: fresh placement scans
  (zero concept hits, control 5), current-text re-reads; premise rot
  caught: backlog named "release-plugin SKILL.md" — target is the
  command file; birth branch landed inside step 1 to keep step-number
  citations (3, 8) stable. Discharges the banner's owed retirement
  pass (booked ~3 vs closed ~0 → 5 closures this commit).
- 2026-08-20 ADDENDUM (operator question "should this be persisted /
  is that how we should work?"): the pass's premise re-judgment
  recorded as method evidence — edit targets re-read in current
  state, placement scans run fresh, one rotted premise caught
  (release-plugin SKILL.md -> command file); two LABEL-graded
  evidence pointers (begehung a2e552c grade; "reviews leave no
  durable mark" vs self-review.md) opened only on operator prompt,
  both held. Class for the corpus fire-rate review: stored-entry
  re-read under-fires on INLINE execution and on evidence-pointer
  premises — sharpen proposed to the operator; if minted, it lands
  in dotfiles routing.md with its JOURNAL line, not here.
- 2026-08-20: booked opus lane commit d05e690 (release-owed
  SessionStart banner + hooks.json wiring + 2.2.3 bump) —
  integrated after dispatcher verification (6/6 --test, live
  fire/no-fire pair on the real pin, hooks.json parse, trailer
  claim). G1 channel decision: model-facing stdout, precedent the
  backlog banner; systemMessage copy rejected as the decaying
  operator-nag channel. Mint provenance + reach limit:
  dev-notes/OBSERVATIONS.md, same-day mint entry (1392991).
