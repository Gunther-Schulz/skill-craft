# Checklist for Reviewing a Skill

**Load when:** Reviewing an existing skill or validating a new one.

**Scope.** This checklist applies when reviewing any skill — including
skill-craft itself. The Self-review mandate (`PROCEDURE.md` Layer 4) is
a separate, finer-grained mechanism: it runs on every commit to
skill-craft's canonical files and adds a cross-pattern test against
`anti-patterns.md` Symptoms. The two compose; this checklist does not
subsume or replace the mandate.

---

Apply after creating or modifying any skill. For any item that fails,
state what's missing before continuing.

- [ ] **Structure.** SKILL.md entry point, standard file names, README
  at root, dependency graph for multi-file skills? Mechanical
  conformance (frontmatter schema, name/character rules, packaging)
  validated via plugin-dev / `skills-ref validate`, or explicitly
  deferred — skill-craft delegates mechanics (`SKILL.md` Companion),
  so a clean architectural review does not imply a clean frontmatter.

- [ ] **Boundary rule.** Maintenance files (OBSERVATIONS, VISION,
  ROADMAP) never loaded by operational files? Only referenced as
  write targets? Located outside the plugin payload, not in the
  skill directory?

- [ ] **Trigger clarity.** SKILL.md description states specific trigger
  phrases in third person?

- [ ] **Density.** SKILL.md under 2,000 words? Detailed content in
  references/ loaded on demand — what moves out judged by the
  derivation trace, not length (per `anti-patterns.md` Procedure-drift)?
  Every sentence changes AI behavior
  (no provenance, restated content, hedging, meta-commentary,
  transitions)? Consider load-time availability before removing
  apparent duplicates. Rules covering the same concern merged into
  fewer, sharper items?

- [ ] **Salience / reading order.** Does every strong default carry its
  scope at or before the point of statement — no carve-out (workflow-vs-
  judgment split, exception, narrowing) stranded downstream where the AI
  reader absorbs the default too late to override it (Scope-precedes-
  default, `PROCEDURE.md`)?

- [ ] **Abstraction.** Judged against the skill's intended scope — a
  domain-specific skill is correctly domain-bound; only a
  domain-general skill must clear the tests across domains. Passes all
  seven tests (five exclusion, two inclusion)? At the same level as
  surrounding content? Uses terminology abstract within that scope?

- [ ] **Protocol conventions.** Imperative form throughout (no second
  person)? Workflow skills: gates use blocking logic (CANNOT + evidence),
  checkpoints observable, choice points surfaced where user has flow
  control, and every conditional dependency between independently-
  dispatchable steps encoded structurally (dependent step's input carries
  the prerequisite's result; artifact cites it) rather than prose-only?
  Judgment skills:
  principles with evidence requirements, deepening mandatory, output
  demonstrates analysis?
  - NO → Add blocking logic / encode dispatch dependencies (workflow) or
    evidence requirements (judgment).

- [ ] **Deepening.** Findings traced to implications beyond the
  checklist? Checklist is floor, not ceiling?

- [ ] **Evolution.** OBSERVATIONS.md exists for skills involving
  judgment? SKILL.md includes evolution instructions (notice gap →
  write observation → propose change)? Skill notices when own
  guidance needs updating?

- [ ] **Durability.** Operational content classifiable under the three
  durability classes (`PROCEDURE.md` Layer 4 "Durability classes")?
  Capability patches carry provenance + a firing log in
  OBSERVATIONS.md — a patch with no logged firing since the last
  consolidation pass is flagged as a cut candidate here (the cut
  itself belongs to consolidation). Bindings state their validity
  condition. A patch-bearing skill without OBSERVATIONS.md fails
  Evolution first, not here. The skill's reason to exist is what it
  enforces or binds, not what it explains — an explanation-only
  skill is itself a retirement candidate as models improve.
- [ ] **Consumer calibration.** Does the skill name its intended
  consuming model/tier, and does prescription density match — brief
  principle + example for top-tier consumers, explicit steps and
  convention lists for cheaper tiers? (Freedom coupling stays
  primary: fragile procedures keep exact steps at every tier. See
  writing-by-skill-type, "Calibrating prescription density".)

- [ ] **Information flow (orchestrated skills only).** Every handoff
  passes what the receiver needs? Data explicit in prompt or on disk?
  Format matches? State survives compaction?

- [ ] **Cross-skill consistency (multi-skill plugins).** Every
  assumption one skill encodes about another — field names, file
  paths, schemas, status values, invocation syntax — matches the
  other skill's actual contract? Checked against the other skill,
  not recalled?

- [ ] **Rendering fidelity (skills that derive content from a source
  spec, framework, or standards doc).** Every load-bearing clause of
  the source survived into the skill text? Structurally-enforced
  source mechanisms render as structural mechanisms, not flattened to
  prose? Verified by a clause-level diff against the source — not by
  re-reading the rendered text?

- [ ] **Evaluation.** Triggering measured (Tier 1) for any
  description-triggered skill, and the behaviour-delta signature
  checked (Tier 2) where the skill forces an observable artifact? See
  `references/evaluation.md`. Inspection is not measurement — a skill
  can read clean and still under-trigger or sit inert.

---

**After running this checklist:** State whether this pass surfaced
anything new. Recommend another pass or moving on.
