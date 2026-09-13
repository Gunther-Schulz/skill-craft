# This repo had NO legacy closure home. The absence was STATED at
# migration time (`--from-done NONE`), never inferred from a missing
# file: the archive below is empty because there was nothing to
# archive, which is a different fact from nothing having been read.

schema: 2

## sc-8
grade: DONE
requirement: skill-craft adopts two style disciplines from the 2026-09-13 comparison (statiker dev-notes/skill-style-comparison-2026-09-13.md), operator-decided in the statiker session: (1) STABLE NUMBERED RULE IDS with gaps preserved for cross-referenced rules (pstack unslop:19's habit) — incident basis beyond the comparand: phrase-shaped cross-references have returned false zeros when greped (corpus environment module, 2026-08-23, several lanes); (2) a REGISTER discipline, operator's words: pstack reads 'how i wish skill-craft could force a skill to be written' — short imperative sentences, and the house case-law register recognized as LLM default un-resisted at the surface (measured: 21-48 words/sentence, up to 432 em dashes/file vs pstack 0-5) while its EPISTEMICS (incident provenance, mechanical-vs-hoped labels) stay mandatory: the fix is separating the two — evidence REQUIRED but carried as pointer/sidecar out of the executing reader's path (precedent: statiker's own 2026-08-10 'skill text states decisions cleanly, history in dev-notes'), plus a compose-time density rule and a mechanical AI-tell lint (pstack unslop's bans are largely regex-detectable, so the lint clears the mechanism bar)
goal: tend
write-set: SKILL.md (register + reference-discipline sections),tools or hooks (the tell-lint, red-first per this repo's own discipline)
done-criterion: skill-craft SKILL.md carries both disciplines; the register rule's mechanical slice ships as a lint proven red on a planted tell and green on clean text; existing house skills are NOT retrofitted wholesale — each adopts at its own seam (statiker at a release seam per its cadence rule)
evidence: operator decision 2026-09-13, statiker session 1b204567 ('agreed to your recomends for 1 and 4' + the register direction quoted above); comparison report finding (i).2/(i).3 and the measured register numbers; corpus environment module's phrase-search false-zero incidents 2026-08-23
blocked-by: NONE
amend-reason: 2026-09-13 operator direction: adapt her recipe with the manual pruning replaced by automation — lint-loop for the mechanical half, fresh-context clause diff + evals for the judgment half
amended-done-criterion: 2026-09-13 skill-craft SKILL.md carries both disciplines PLUS the automated prune loop that replaces her manual step (operator, 2026-09-13: full automation at the same level statiker automates design): (1) the tell+density LINT, mechanical and red-first on planted tells, thresholds calibrated on pstack's own measured band (7.9-18.7 words/sentence, 0-5 em dashes — the 2026-09-13 comparison report is the calibration data); (2) the PRUNE LOOP: the drafting LLM iterates against the lint until green — her inner-loop-against-a-harness applied to prose; (3) the SEMANTIC-PRESERVATION gate replacing the human's judgment half: a fresh-context clause-coverage diff (the dispatch skill's enumeration form, ABSENT/WEAKENED per clause, cheap tier) proving the pruned text drops no obligation, plus the eval-skill battery where the skill has one; the lint ships proven red on planted tells and green on clean text; existing house skills adopt at their own seams, never wholesale
closed-reason: 2026-09-13 both disciplines carried in SKILL.md, register_lint + battery landed (58 tests, 5-mutant red-first), mandated fresh-context review run with all 11 findings dispositioned in d23a95a's body; one repair lap consumed, as the mint-form rule priced
closed-ref: ec230ce, 0822772, d23a95a, 46c2ffc

## sc-9
grade: DONE
requirement: generalize statiker's review-cadence conclusion into skill-craft doctrine (operator, 2026-09-13, statiker session: every small edit does not need review, before a release definitely — and generalize it): fresh-context review attaches to the DELIVERY SEAM, not the edit. For version-pinned payloads (plugins) the seam is the RELEASE: small conduct-prose edits ride unreviewed, machine-read semantics and the accumulated delta are reviewed once at the seam, an oversized delta splits into parallel class lanes at that one seam. For live-on-write carriers (a corpus CLAUDE.md, hooks on an execution path) the EDIT is the seam, so per-edit gates stand there. Supersedes the unconditional per-edit self-review reading of the Self-review clause for pinned payloads
goal: tend
write-set: SKILL.md (Self-review clause plus a cadence clause in Lifecycle or Reviewing)
done-criterion: SKILL.md states the seam-attached cadence with the pinned/live-on-write split; the Self-review clause carries the qualifier; provenance cites statiker's checkpoint rule (2026-08-16), its 2026-09-13 tightening, and the release-batching incident (three releases, no consuming run, 28 wake-ups)
evidence: statiker CLAUDE.md checkpoint bullet incl. this date's tightening (commit 8d69a9a); statiker release-batching decision 2026-09-11 (ledger 7e0572f); operator decision this date, statiker session 1b204567
blocked-by: NONE
closed-reason: 2026-09-13 seam-attached cadence landed in Reviewing a skill; Self-review bullet re-keyed from per-commit to per-release; machine-read semantics mandatory at the seam
closed-ref: 11479cf

## Archive (pre-migration)


<!-- CLOSURES READ FROM THE `--from` CARRIER ITSELF (lc-18/lc-19). The
     design modelled closures as a separate `--from-done` FILE; a real
     carrier states them in its own `## Done` section or with a closure
     grade word. These bodies are VERBATIM from the source, at the line
     ranges named beside each one, and they are archived rather than
     written as items: a closure that migrates back as open work is the
     one migration defect that is silent. -->

<!-- BACKLOG.md:104-106 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-05 — backlog cleared, operator GO; refs and
  dispositions in dev-notes/OBSERVATIONS.md "2026-08-05 —
  Consolidation pass" and clearing commit 64cd292.

<!-- BACKLOG.md:107-109 — §3.1: `DROPPED` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DROPPED** 2026-08-06 — grilling/frontier-round adoption mis-homed
  here (operator correction: not skill-craft work at any grade);
  minted thin as a corpus convention instead (dotfiles f3dfa52).

<!-- BACKLOG.md:110-113 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-08 — skill-lint checker (booked f25a748): landed by
  baf064a + integration commit; red target re-pinned to 40bcc73
  after the booked sha measured green; dispositions and runs in
  dev-notes 2026-08-08 "skill-lint landed". Body: git (f25a748).

<!-- BACKLOG.md:114-117 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — /release-plugin birth branch (2.2.0 canon
  pass): landed in release-plugin step 1, plugin-engineering
  pointer, first-release description trigger. Body: git +
  OBSERVATIONS annotation.

<!-- BACKLOG.md:118-121 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — eval-method deltas (2.2.0 canon pass): all four
  landed in evaluation.md Tier 2 — ablation arm, staged probes,
  series limitation, control-arm definition. Body: git +
  OBSERVATIONS annotation.

<!-- BACKLOG.md:122-124 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — history-hedge costume (2.2.0 canon pass):
  Pruning names the costume with the deletion check; checklist
  item 5 carries the paired question. Body: git + OBSERVATIONS.

<!-- BACKLOG.md:125-127 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — unbound-reference test (2.2.0 canon pass):
  beside the no-op test, three-site fold included; checklist
  item 18 with the hot-noun grep. Body: git + OBSERVATIONS.

<!-- BACKLOG.md:128-130 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — named-moment lever (2.2.0 canon pass): review
  mark, era stamp, flip-measurement line, trigger-anchor tests
  all landed. Body: git + OBSERVATIONS.

<!-- BACKLOG.md:131-137 — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry -->
- **DONE** 2026-08-20 — self-review canon load names
  review-checklist.md (booked same day from the fresh-text-note
  review's gap 3; operator settled: joins). Landed by d7f9a4b —
  fresh-text rule bound at the five-checks seam, three review
  rounds dispositioned in the commit body. Successor question
  (load manifest) parked above.

