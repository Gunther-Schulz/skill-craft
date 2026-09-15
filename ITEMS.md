schema: 2
baseline: 14
added: 6
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

## sc-10
grade: READY
requirement: WHERE A SANCTIONED MECHANISM'S OUTPUT IS FULLY DESCRIBED, THE DESCRIPTION COMPETES WITH THE MECHANISM, and the competition is won by whichever is cheaper at the moment of use, which is always the hand-built version. A route stays sanctioned only where the hand-built look-alike is impossible or fails SOFTLY; where it fails TERMINALLY the description is a trap laid by the documentation for its most careful readers. MOVED HERE from statiker st-70 on the operator's venue decision of 2026-09-15: the general form belongs at skill-craft truth-level, not at statiker's, which is where it was first measured. Provenance record: statiker dev-notes/OBSERVATIONS.md 2026-09-14, the look-alike quote block entry, GENERAL FORM paragraph and its DRAIN DISPOSITION
goal: general-maintenance
write-set: plugin/skills/skill-craft/SKILL.md,dev-notes/OBSERVATIONS.md
done-criterion: The rule lands as an AMENDMENT to the existing un-fakeable-artifact guidance (SKILL.md:354-360), NOT as a new bullet, and the shape was decided at the sending desk so this one verifies rather than derives: the un-fakeable-artifact rule already reasons about what a consumer can produce WITHOUT doing the work; this is its mirror, what a consumer can produce INSTEAD of invoking the mechanism. The clause states the test a describing passage must pass: NAME the failure mode of the hand-built look-alike, and where that failure is terminal either drop the description or state the terminal consequence beside it. Verifier: the amended passage, applied to the motivating incident, forbids the passage that caused it
evidence: ONE incident, real and costed: the statiker scoped run's arm 2, 2026-09-14, was one keystroke from the sanctioned route, took the described look-alike instead, and lost the remainder of its loop; the penalty was terminal and unrecoverable. TRANSFER PAST THAT CASE IS ARGUED RATHER THAN ASSUMED: the mechanism is that a describing passage and its mechanism compete on cost at the moment of use, which holds for any skill document whose reader executes under momentum, and statiker is merely where it was first measured. Marked as ONE observation: the reach beyond this case is a hypothesis validated by use, per this repo's own two-paths rule. GOAL SLOT chosen by the foreign desk and owned by this repo's reader
blocked-by: NONE

## sc-11
grade: READY
requirement: the register lint's sentence splitter reads a terminatorless bulleted list as ONE sentence, so the worst-offender headline can name a non-sentence: measured 2026-09-15 in statiker's lap-C scope pass, where :611's reported 229-word sentence is nine bulleted entry forms, 3 of 56 findings were this artifact, and one sat inside a block that ships verbatim and is forbidden to reword - a scope taken from the headline would have rewritten it. Record: statiker docs/audits/2026-09-15-lapC-tighten-scope.md (8d73d35), booked by statiker-9c
goal: general-maintenance
write-set: plugin/,tools/
done-criterion: the splitter segments on bullet-item boundaries (or excludes terminatorless list items from run-on counting) so a bulleted list is never counted as one sentence; red-first: a fixture of the statiker :611 shape (multi-bullet, no terminal periods) goes from one 200+w finding to zero list-artifact findings while a genuine 100w prose sentence in the same fixture still fires; the worst-offender headline names only true sentences
evidence: statiker docs/audits/2026-09-15-lapC-tighten-scope.md at 8d73d35: lint and an independent splitter agreed on 229w@611 (shared coordinate), body read shows nine bulleted forms with no terminal periods; two more of the 56 same artifact
blocked-by: NONE
