schema: 2
baseline: 14
added: 1
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
