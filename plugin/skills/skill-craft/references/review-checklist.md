# Checklist for Reviewing a Skill

**Load when:** Reviewing an existing skill or validating a new one.

---

When reviewing, verify each item. For any that fails, state what's
missing before continuing.

- [ ] **README.** Plugin has a README.md at root? Contains: what it does
  (value, not mechanism), installation commands, trigger phrases, files table?
  - NO → Create README.md with required sections.

- [ ] **Naming convention.** Files named per standard? `SKILL.md` for
  entry point, `PROCEDURE.md` for method, `OBSERVATIONS.md` for journal?
  - NO → Rename to standard names.

- [ ] **Boundary rule.** Category 2 files (OBSERVATIONS, VISION, STRATEGY,
  ROADMAP) appear in any Category 1 files (SKILL.md, PROCEDURE.md, references)?
  - YES → Remove. Maintenance files never appear in operational files.

- [ ] **Trigger clarity.** SKILL.md description clearly states when to
  activate? Third-person with specific trigger phrases?
  - NO → Rewrite with explicit trigger phrases.

- [ ] **Writing style.** Imperative/infinitive form throughout? No second
  person ("you should", "your role")?
  - NO → Rewrite to imperative form.

- [ ] **Word count.** SKILL.md body under 2,000 words (5k max)? Detailed
  content in references/?
  - NO → Move heavy content to references/. Keep SKILL.md lean.

- [ ] **Behavior-change test.** Every sentence changes AI behavior? No
  provenance, restated content, named examples, or motivational framing?
  - NO → Remove sentences that fail the test. Consider load-time
    availability before removing apparent duplicates.

- [ ] **File separation.** Procedure project-agnostic? Observations
  grounded in real incidents? Supporting files not loaded at invocation?
  - NO → Separate procedure from observations.

- [ ] **Dependency graph.** SKILL.md documents which files depend on which?
  - NO → Add dependency table.

- [ ] **Progressive disclosure.** SKILL.md tells what to load first and
  what to load on demand? Or everything loads at once?
  - NO → Extract to `references/`. Keep SKILL.md focused.

- [ ] **Protocol conventions.** Instructions use forcing functions?
  Checkpoints observable? Menus where user has choices?
  - NO → Add blocking logic for advisory instructions.

- [ ] **Deepening.** After checklist items, procedure traces findings to
  implications? Or stops at the checklist?
  - NO → Add deepening step.

- [ ] **Evolution path.** Place for observations? Updated based on real
  failures? Or written once?
  - NO → Create OBSERVATIONS.md if the skill involves judgment.

- [ ] **Evolution instructions (if OBSERVATIONS.md exists).** Does SKILL.md
  include the evolution behavior? (notice gaps → write to OBSERVATIONS.md
  → assess procedure change → propose with reasoning)
  - OBSERVATIONS.md exists but no evolution instructions → Add them.
  - No OBSERVATIONS.md → N/A.

- [ ] **Reflexivity.** Skill notices when own guidance needs updating?
  - NO → Add reflexivity rule.

- [ ] **Abstraction level.** Procedure and reference content project-agnostic?
  Checkpoints use domain-independent language? Examples abstract, not from a
  specific codebase?
  - NO → Rephrase abstractly or move project-specific content to observations.
