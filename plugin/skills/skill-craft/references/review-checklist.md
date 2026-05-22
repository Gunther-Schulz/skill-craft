# Checklist for Reviewing a Skill

**Load when:** Reviewing an existing skill or validating a new one.

---

Apply after creating or modifying any skill. For any item that fails,
state what's missing before continuing.

- [ ] **Structure.** SKILL.md entry point, standard file names, README
  at root, dependency graph for multi-file skills?

- [ ] **Boundary rule.** Maintenance files (OBSERVATIONS, VISION,
  ROADMAP) never loaded by operational files? Only referenced as
  write targets? Located outside the plugin payload, not in the
  skill directory?

- [ ] **Trigger clarity.** SKILL.md description states specific trigger
  phrases in third person?

- [ ] **Density.** SKILL.md under 2,000 words? Detailed content in
  references/ loaded on demand? Every sentence changes AI behavior
  (no provenance, restated content, hedging, meta-commentary,
  transitions)? Consider load-time availability before removing
  apparent duplicates. Rules covering the same concern merged into
  fewer, sharper items?

- [ ] **Abstraction.** Judged against the skill's intended scope — a
  domain-specific skill is correctly domain-bound; only a
  domain-general skill must clear the tests across domains. Passes all
  seven tests (five exclusion, two inclusion)? At the same level as
  surrounding content? Uses terminology abstract within that scope?

- [ ] **Protocol conventions.** Imperative form throughout (no second
  person)? Workflow skills: gates use blocking logic (CANNOT + evidence),
  checkpoints observable, menus where user has choices? Judgment skills:
  principles with evidence requirements, deepening mandatory, output
  demonstrates analysis?
  - NO → Add blocking logic (workflow) or evidence requirements (judgment).

- [ ] **Deepening.** Findings traced to implications beyond the
  checklist? Checklist is floor, not ceiling?

- [ ] **Evolution.** OBSERVATIONS.md exists for skills involving
  judgment? SKILL.md includes evolution instructions (notice gap →
  write observation → propose change)? Skill notices when own
  guidance needs updating?

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
