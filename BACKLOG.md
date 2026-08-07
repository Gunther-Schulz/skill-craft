# Backlog — skill-craft

Work items for the canon, in two grades: parked (carries its named
missing evidence or trigger) and ready (decision-complete). Items
leave by commit ref or are dropped with a one-line reason. Consumer:
the maintainer's next canon pass (Layer-4 gate applies to every canon
edit; nothing lands from here without it).

- (cleared 2026-08-05, operator backlog-clear GO;
  leaving refs and dispositions in dev-notes/OBSERVATIONS.md
  "2026-08-05 — Consolidation pass" and the clearing commit 64cd292.)
- (dropped 2026-08-06, same day as parked: grilling/frontier-round
  adoption was mis-homed here — operator correction: not skill-craft
  work at any grade. Minted thin as a corpus convention instead
  (dotfiles f3dfa52, CLAUDE.md Recommending & reporting).)

- **READY — skill-lint: mechanical pre-release checker for skill
  files** (booked 2026-08-07, operator GO from the statiker meta
  session; provenance: statiker reviews 8-12, where wrap/term/cite
  defects consumed reviewer findings and edit laps — each check
  below carries a real incident). Design decided: a CHECKER that
  flags, never an auto-formatter (prose reflow can silently
  corrupt quoted blocks, list continuations, inline templates —
  observed hazard class in statiker's `> Superseded` blocks and
  tag templates); trailing-whitespace is the sole auto-fix.
  Checks: (1) wrap >72 chars with a whitelist for unbreakable
  literals — path templates, frontmatter description (statiker
  review-9 NIT6, review-11-era rewrap misses); (2) trailing
  whitespace, auto-fixable; (3) section-cite liveness — a
  parenthetical cite naming a heading ("(The attack)") must
  resolve to a real heading in the file (reviewers ran this grep
  by hand every round); (4) new-term singleton WARN — a
  backticked/capitalized term the diff introduces occurring
  exactly once in the file is an undefined-at-point-of-use
  candidate (statiker review-9 N1 "task system"; warn-not-block,
  false fires expected). Placement: this repo's plugin `tools/`,
  wired into the /release-plugin checklist (the seam every
  release crosses). Verifier: red-first on the real incidents —
  run against statiker SKILL.md at 0aa1891 (must flag the
  review-9 wrap lines) and a planted dead cite + singleton term;
  green on the current file with whitelist. Done-criterion:
  checker in tools/, release-plugin checklist step added, red
  and green runs recorded in dev-notes. Repo-specific content
  checks (statiker's tag-enum/scope-form consistency) are
  explicitly OUT — those live in the consuming repo's tools/.

## Parked — review-regime section (draft-attack-before-release)

- **Mint a review-regime rule set into skill-craft** (operator
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
