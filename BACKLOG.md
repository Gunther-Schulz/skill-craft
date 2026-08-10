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

- **READY 2026-08-10 — unbound-reference test: the object-side
  sibling of the named-moment lever** (operator GO from the
  full-corpus review request; incident record and fix-pattern
  evidence: dev-notes/OBSERVATIONS.md 2026-08-10, third lever
  entry). Design decided: (1) SKILL.md gains the test beside the
  no-op test (both are per-clause authoring tests): every
  load-bearing definite reference either has a unique in-scope
  referent or names its selector — the tell is a definite article
  over a noun with siblings in the consumer's environment; the fix
  binds to the invariant object, never a container, section, or
  label that usually coincides with it. (2) review-checklist.md
  gains the matching item with the hot-noun grep named as the
  candidate instrument (grading stays judgment). Verifier: Layer-4
  self-review; dry-run against the four evidence incidents (each
  older wording fails the test, each repaired wording passes).
  Done when both files carry it, self-review dispositions recorded,
  release ships it — natural bundle with the named-moment READY
  entry below (same files, one release). Consumer: the next
  skill-craft canon session.

- **READY 2026-08-10 — named-moment lever, three canon
  applications** (operator GO by booking question on the presented
  findings; incident record and derivation:
  dev-notes/OBSERVATIONS.md 2026-08-10, the two lever entries —
  the trigger-anchor gap and the application sweep). Design
  decided per finding: (1) REVIEW MARK — reviews record a dated
  journal line naming the commit ref reviewed; the medium re-ask
  ("machine-read semantics belonging in a mechanism?") is owed per
  section grown since the previous mark and its verdict lands in
  the review record — the owed re-ask becomes readable, not
  remembered. (2) ERA STAMP — the consumer declaration (SKILL.md,
  The two parties) carries an as-of stamp naming the model era it
  was last graded against; Lifecycle's era re-grade and checklist
  13's "moved since minting" then diff against the stamp — the
  binding staleness discipline applied to the canon's own
  declaration. (3) MINOR — a delist flip's commit names its
  re-measurement (Invocation choice). Also in scope, same
  provenance: the trigger-anchor clause itself gains the two tests
  (observable referent; visible absence) per the first
  observation. Each lands per amendment discipline with the
  Layer-4 self-review; verifier: the self-review's clause-level
  findings plus a constructed dry-run per finding (a review
  without a mark, a declaration without a stamp — each now
  visibly non-compliant). Done when all four land in the canon
  with self-review dispositions recorded and the release ships
  them. Consumer: the next skill-craft canon session.

- (left 2026-08-08 by commit baf064a + the integration commit
  beside it; red target re-pinned to 40bcc73 after the booked sha
  measured green — dispositions and runs in dev-notes 2026-08-08
  "skill-lint landed". Original entry kept below for the record.)
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
