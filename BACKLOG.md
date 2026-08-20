# Backlog — skill-craft

Work items for the canon, in two grades: parked (carries its named
missing evidence or trigger) and ready (decision-complete). Items
leave by commit ref or are dropped with a one-line reason — the
entry MOVES to `## Done` below at closure time, one line with its
grade word and evidence pointer; a stub or strike left in the live
sections is a closure without an exit. Consumer: the maintainer's
next canon pass (Layer-4 gate applies to every canon edit; nothing
lands from here without it).

- **PARKED 2026-08-10 — skill-lint dead-cite still fires on a
  COMMA-SEPARATED identifier list.** Residual of 2b4a32e, surfaced by
  its executor with a run, not a reading: `(SendMessage, WebFetch)`
  still flags — the shipped exclusion is single-token only. Absent
  from both governed corpora today (full-corpus run: zero dead-cites),
  so nothing is blocked. NOT a one-liner, which is why this is parked
  rather than ready: `cite_candidate` deliberately takes
  `head = c.split(",")[0]` so a legitimate cross-file cite
  `(Heading, \`file.md\`)` still resolves, so "exclude comma lists
  whose head is CamelCase" has a real cite shape to preserve. Named
  missing decision: whether a comma list whose FIRST token is a
  CamelCase identifier is ever a cite. Trigger: the shape appearing in
  a governed corpus, or a release blocked by it.
  (Re-checked 2026-08-20, kämmung pass: governed-set skill-lint run,
  zero dead-cite fires — trigger unmet, stays parked.)

## Parked — review-regime section (draft-attack-before-release)

- **PARKED 2026-08-07 — Mint a review-regime rule set into
  skill-craft** (operator
  question, 2026-08-07, statiker meta session #4; parked on a
  named trigger: statiker trial reaches its no-blocker round or
  stabilization grading, whichever first — the convergence
  clause needs the completed series as evidence). Skill-craft is
  the right home: it already owns "Reviewing a skill",
  self-review, and the consolidation criterion, but carries no
  regime for RELEASING edits to dense interlocked skill text.
  Candidate content, evidence-complete parts marked: (a)
  draft-attack-before-release — repairs to a skill executed
  literally by a fresh context are attacked pre-release by a
  fresh context on the draft diff (diff + full file + question,
  no author reasoning), iterated to a no-blocker round, then
  released byte-identical [evidence: statiker reviews 8-12
  release-first cadence 4→2→2→1→1 with every round's blockers
  inside the newest repair vs. draft-attacks 1-5 catching 12
  blockers pre-release; stop-call record in statiker dev-notes].
  (b) trend-over-round reading at each lap seam — blocker counts
  and locations ACROSS rounds, not the last round's findings; a
  flat or rising series with findings concentrated in the newest
  repair layer re-opens the repair FORM (patch vs. coherent
  region rewrite) [evidence: statiker draft-attack cadence
  2→1→2→3→4 under patch-on-patch; form switch at attack 5
  operator-prompted, not self-noticed — the miss that makes the
  rule]. (c) probe-execute external-behavior claims (git,
  filesystem, tool semantics) before shipping them in skill
  text; a widened claim ("and kin") inherits the probe duty for
  each widened member [evidence: attack-5 B2 — the two
  unprobed "kin" were exactly the two ops git does not guard].
  Provenance chain: statiker dev-notes/OBSERVATIONS.md sessions
  #3-#4 (2026-08-07). Consumer: skill-craft maintainer session
  at the trigger; grading input = the statiker series' final
  cadence.

  - (judged 2026-08-08, backlog-work pass, operator GO: stays
    PARKED — the named trigger is unmet, the statiker trial has
    not run. Grading input grew since booking: the R1–R3
    design-attack series ended in a FORM change (executable spec +
    battery, statiker dev-notes 2026-08-08), not a no-blocker
    round — so part (a)'s iterate-to-no-blocker shape now has a
    measured limit (flat series on dense interlocked prose =
    medium wrong, not more rounds), and part (b) is already
    corpus canon (re-entry-seam trend rule). At the trigger,
    re-derive against that record; do not mint as drafted.)
  - (re-checked 2026-08-20, kämmung pass: statiker trial still in
    flight — its dev-notes name the trial close's grading as a
    future consumer. Trigger unmet, stays parked.)

- **PARKED 2026-08-20 — self-review load manifest (the load has no
  compliance artifact).** From the load-list change's round-3
  review (N4): self-review.md's reader is the dispatcher, so its
  loads reach the reviewer only by brief transcription — a skipped
  check is visible via the per-check line, a skipped load leaves
  no absence. Pre-formulated fix in OBSERVATIONS "2026-08-20 —
  Review-machinery obligations without compliance artifacts": a
  one-line load manifest at the file head, pasted into the brief,
  echoed in the report. Named missing decision: manifest form (and
  whether review-checklist.md's per-pass wording adopts the
  "N passes, one axis per pass" mechanism in the same edit).
  Trigger: the next edit of self-review.md or review-checklist.md.

- **PARKED 2026-08-20 — release lint scope misses command files.**
  From the 2.2.0 self-review (finding n3): /release-plugin step 3
  lints "each SKILL.md plus its references/*.md", so
  plugin/commands/*.md never pass through skill_lint — the command
  file's own pre-existing wrap flag was invisible to every release
  it shipped in (fixed by hand in 2.2.0). Named missing decision:
  whether command files join the release lint set (they are
  operator-facing steps, not skill prose — wrap rules may differ).
  Trigger: the next command-file edit, or a release shipping one.

## Done (moved here at closure, with the ref)

- **DONE** 2026-08-05 — backlog cleared, operator GO; refs and
  dispositions in dev-notes/OBSERVATIONS.md "2026-08-05 —
  Consolidation pass" and clearing commit 64cd292.
- **DROPPED** 2026-08-06 — grilling/frontier-round adoption mis-homed
  here (operator correction: not skill-craft work at any grade);
  minted thin as a corpus convention instead (dotfiles f3dfa52).
- **DONE** 2026-08-08 — skill-lint checker (booked f25a748): landed by
  baf064a + integration commit; red target re-pinned to 40bcc73
  after the booked sha measured green; dispositions and runs in
  dev-notes 2026-08-08 "skill-lint landed". Body: git (f25a748).
- **DONE** 2026-08-20 — /release-plugin birth branch (2.2.0 canon
  pass): landed in release-plugin step 1, plugin-engineering
  pointer, first-release description trigger. Body: git +
  OBSERVATIONS annotation.
- **DONE** 2026-08-20 — eval-method deltas (2.2.0 canon pass): all four
  landed in evaluation.md Tier 2 — ablation arm, staged probes,
  series limitation, control-arm definition. Body: git +
  OBSERVATIONS annotation.
- **DONE** 2026-08-20 — history-hedge costume (2.2.0 canon pass):
  Pruning names the costume with the deletion check; checklist
  item 5 carries the paired question. Body: git + OBSERVATIONS.
- **DONE** 2026-08-20 — unbound-reference test (2.2.0 canon pass):
  beside the no-op test, three-site fold included; checklist
  item 18 with the hot-noun grep. Body: git + OBSERVATIONS.
- **DONE** 2026-08-20 — named-moment lever (2.2.0 canon pass): review
  mark, era stamp, flip-measurement line, trigger-anchor tests
  all landed. Body: git + OBSERVATIONS.
- **DONE** 2026-08-20 — self-review canon load names
  review-checklist.md (booked same day from the fresh-text-note
  review's gap 3; operator settled: joins). Landed by d7f9a4b —
  fresh-text rule bound at the five-checks seam, three review
  rounds dispositioned in the commit body. Successor question
  (load manifest) parked above.

## Kämmung passes

2026-08-20 — diagnosis: blocked exit (7 closure stubs + 1 closed
  body in live sections; drainage itself healthy — 5 closed by the
  2.2.0 pass; the banner's "closed ~0" was the undeclared closure
  dialect, not missing drains). Reconciliation: before = 11 bodies
  (7 stubs, 1 closed body, 3 parked); moved to Done = 8; kept
  (parked, re-checked against the world by executed check) = 3;
  dropped = 0. Baseline for the next measurement.
