schema: 2
baseline: 14
added: 3
compacted: 0

## sc-1
grade: NEW
requirement: PARKED 2026-08-10 — skill-lint dead-cite still fires on a COMMA-SEPARATED identifier list — record: BACKLOG.md:12
goal: UNKNOWN
write-set: UNKNOWN
done-criterion: UNKNOWN
evidence: BACKLOG.md:12-27
blocked-by: decision the missing decision named in the source body: answer it, then re-grade

## sc-2
grade: NEW
requirement: PARKED 2026-08-07 — Mint a review-regime rule set into skill-craft — record: BACKLOG.md:30
goal: UNKNOWN
write-set: UNKNOWN
done-criterion: UNKNOWN
evidence: BACKLOG.md:30-78
blocked-by: evidence false  # the named missing evidence in the source body

## sc-3
grade: NEW
requirement: PARKED 2026-08-20 — self-review load manifest (the load has no compliance artifact) — record: BACKLOG.md:79
goal: UNKNOWN
write-set: UNKNOWN
done-criterion: UNKNOWN
evidence: BACKLOG.md:79-91
blocked-by: decision the missing decision named in the source body: answer it, then re-grade

## sc-4
grade: NEW
requirement: PARKED 2026-08-20 — release lint scope misses command files — record: BACKLOG.md:92
goal: UNKNOWN
write-set: UNKNOWN
done-criterion: UNKNOWN
evidence: BACKLOG.md:92-101
blocked-by: decision the missing decision named in the source body: answer it, then re-grade

## sc-5
grade: PARKED
requirement: 3 tracked file(s) still name the migrated carrier(s) `BACKLOG.md`. A consumer left pointing at a carrier nobody writes any more reads as current until someone notices, and nobody is scheduled to — record: the migration report
goal: tend
write-set: CLAUDE.md, LEDGER.md, dev-notes/OBSERVATIONS.md
done-criterion: no tracked file outside the migration's own outputs names `BACKLOG.md`, or each remaining one is recorded as a declared exemption
evidence: tracked files naming `BACKLOG.md` at migration time: CLAUDE.md, LEDGER.md, dev-notes/OBSERVATIONS.md
blocked-by: decision every consumer migrated or declared exempt

## sc-6
grade: READY
requirement: the cut-candidate predicate cannot separate a patch that had opportunities and caught nothing from one minted last week, and both read as zero firings. daneel hit this live, fixed its own copy, and surfaced it here deliberately rather than editing this repo -- record: daneel BACKLOG.md:198 at blob f99ff84f15b8c8bd2b7b89793b3dddd8252d0376 (pinned inline: daneel is deleting that carrier, and the pin is what keeps this pointer resolving via git cat-file -p)
goal: general-maintenance
write-set: plugin/skills/skill-craft/SKILL.md (Durability classes, Layer 4) and references/review-checklist.md
done-criterion: Durability classes either adopts a run-count discriminator (a rule whose scope no run has entered is unmeasured, not cut-eligible) or records why the current predicate is sufficient here. Either is an exit; silence is not. If adopted, the review-checklist entry at :107 moves with it, and dev-notes/OBSERVATIONS.md:1240-1242 is corrected, since it currently certifies as closed the very gap this reopens.
evidence: MEASURED 2026-09-12 by the dotfiles drainage desk, both sides opened. THIS REPO carries the undefended predicate at plugin/skills/skill-craft/SKILL.md:368 and :478-479 (a mechanism with no firing since the last review is a cut candidate) and references/review-checklist.md:107. DANEEL's fix, for comparison rather than for copying: dev-notes/OBSERVATIONS.md:18-38 -- the reviewer's first question is not did it fire but has anything EXERCISED it yet, how many runs have entered this rule's scope since minting; zero runs plus zero firings carry no information, and such a rule is UNMEASURED rather than depreciating. WHY THIS REPO WOULD NOT HAVE FOUND IT: dev-notes/OBSERVATIONS.md:1240-1242 records the durability cut-candidate gap as CLOSED-ALREADY-SATISFIED because the rule text exists -- so a reviewer here reads the gap as closed, and the defect is in the text that closed it. Instrument note: the sweep for the defect formulation (zero runs / unmeasured / has anything exercised / run count / entered its scope) over this repo returned only unrelated senses of unmeasured; the positive control on the same instrument (cut candidate) returned 6 hits, so that absence is instrument-proven rather than an unread sweep.
blocked-by: decision whether Durability classes adopts the run-count discriminator, or declares the current predicate sufficient with its reason

## sc-7
grade: READY
requirement: five house skills declare their consumer without the as-of stamp skill-craft's own two-parties section mandates ('with an as-of stamp naming the model era the declaration was last graded against', SKILL.md:33-37): dispatch:8, executor:8, begehung:10, kaemmung:11, statiker:630. Found by the 2026-09-13 skill-style comparison (statiker dev-notes/skill-style-comparison-2026-09-13.md, finding iii.1), each location verified at source by the desk
goal: tend
write-set: dispatch-guards repo (dispatch+executor SKILL.md consumer lines),begehung repo (SKILL.md:10),kaemmung repo (SKILL.md:11),statiker repo (SKILL.md:630 — rides a statiker release seam per its review cadence)
done-criterion: each of the five consumer declarations carries an as-of era stamp in skill-craft:33-37's form; verifier: case-folded grep for 'as of' on each consumer line returns a hit; the statiker edit lands at that repo's next release seam, never as its own release
evidence: skill-craft SKILL.md:33-37 read at the desk 2026-09-13; the five unstamped lines from the comparison report, executor:8 and statiker:630 spot-verified at source same date
blocked-by: NONE

## sc-8
grade: READY
requirement: skill-craft adopts two style disciplines from the 2026-09-13 comparison (statiker dev-notes/skill-style-comparison-2026-09-13.md), operator-decided in the statiker session: (1) STABLE NUMBERED RULE IDS with gaps preserved for cross-referenced rules (pstack unslop:19's habit) — incident basis beyond the comparand: phrase-shaped cross-references have returned false zeros when greped (corpus environment module, 2026-08-23, several lanes); (2) a REGISTER discipline, operator's words: pstack reads 'how i wish skill-craft could force a skill to be written' — short imperative sentences, and the house case-law register recognized as LLM default un-resisted at the surface (measured: 21-48 words/sentence, up to 432 em dashes/file vs pstack 0-5) while its EPISTEMICS (incident provenance, mechanical-vs-hoped labels) stay mandatory: the fix is separating the two — evidence REQUIRED but carried as pointer/sidecar out of the executing reader's path (precedent: statiker's own 2026-08-10 'skill text states decisions cleanly, history in dev-notes'), plus a compose-time density rule and a mechanical AI-tell lint (pstack unslop's bans are largely regex-detectable, so the lint clears the mechanism bar)
goal: tend
write-set: SKILL.md (register + reference-discipline sections),tools or hooks (the tell-lint, red-first per this repo's own discipline)
done-criterion: skill-craft SKILL.md carries both disciplines; the register rule's mechanical slice ships as a lint proven red on a planted tell and green on clean text; existing house skills are NOT retrofitted wholesale — each adopts at its own seam (statiker at a release seam per its cadence rule)
evidence: operator decision 2026-09-13, statiker session 1b204567 ('agreed to your recomends for 1 and 4' + the register direction quoted above); comparison report finding (i).2/(i).3 and the measured register numbers; corpus environment module's phrase-search false-zero incidents 2026-08-23
blocked-by: NONE
amend-reason: 2026-09-13 operator direction: adapt her recipe with the manual pruning replaced by automation — lint-loop for the mechanical half, fresh-context clause diff + evals for the judgment half
amended-done-criterion: 2026-09-13 skill-craft SKILL.md carries both disciplines PLUS the automated prune loop that replaces her manual step (operator, 2026-09-13: full automation at the same level statiker automates design): (1) the tell+density LINT, mechanical and red-first on planted tells, thresholds calibrated on pstack's own measured band (7.9-18.7 words/sentence, 0-5 em dashes — the 2026-09-13 comparison report is the calibration data); (2) the PRUNE LOOP: the drafting LLM iterates against the lint until green — her inner-loop-against-a-harness applied to prose; (3) the SEMANTIC-PRESERVATION gate replacing the human's judgment half: a fresh-context clause-coverage diff (the dispatch skill's enumeration form, ABSENT/WEAKENED per clause, cheap tier) proving the pruned text drops no obligation, plus the eval-skill battery where the skill has one; the lint ships proven red on planted tells and green on clean text; existing house skills adopt at their own seams, never wholesale
