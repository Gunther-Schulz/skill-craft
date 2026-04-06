# Skill Design Procedure

How to design Claude Code skills that produce good results. Covers plugin
structure, protocol conventions, skill architecture, evolution, and
reflexivity — everything needed to build a skill that works well over time.

---

## File naming convention

Standard file names enforce consistency across all skills. Use these exact
names when the role exists.

**Mandatory:**
- `SKILL.md` — entry point. Trigger conditions, what to load, dependency
  graph. Every skill has this.
- `PROCEDURE.md` — the core method. The self-contained document with the
  skill's actual instructions. SKILL.md tells the AI to load this.

**Optional (standard names):**
- `OBSERVATIONS.md` — improvement journal. Failure patterns from real use.
  Not loaded during normal skill operation — exists for maintaining the
  skill itself.
- `VISION.md` — philosophical foundation. Only for complex skills with
  non-obvious methodology.
- `STRATEGY.md` — connects observations to principle. Rare.
- `ROADMAP.md` — concrete improvement work items. Rare.
- `references/` — detail files loaded on demand by PROCEDURE.md.

**Self-containment rule:** PROCEDURE.md does not reference other files. Load
it and you have everything needed to use the skill. SKILL.md references
PROCEDURE.md. PROCEDURE.md references nothing.

**Exception:** Orchestrator skills (like a composer that delegates to
sub-skills) reference their sub-skills by design. This is the only case
where PROCEDURE.md references other files.

**Supporting files are never loaded at invocation.** OBSERVATIONS.md,
VISION.md, STRATEGY.md, ROADMAP.md exist alongside for skill maintenance
and evolution. They are not referenced by PROCEDURE.md and not loaded when
the skill is used. They are read only when improving the skill itself.

---

## The five layers

Every effective skill addresses five layers. Most skills get layer 1 right and
stop. Skills that work well over time address all five.

### Layer 1: Plugin structure (plumbing)

Directory layout, manifest, auto-discovery. The mechanical foundation.

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: {"name": "plugin-name"}
├── plugin/
│   └── skills/
│       └── skill-name/
│           ├── SKILL.md     # Required: trigger + instructions
│           └── references/  # Optional: loaded on demand
├── commands/                # Optional: slash commands (.md)
├── agents/                  # Optional: subagent definitions (.md)
└── hooks/                   # Optional: event handlers
```

Key rules:
- SKILL.md must be named exactly `SKILL.md`
- The `description` field in YAML frontmatter is the trigger condition — be
  specific about trigger phrases
- Component directories go at plugin root, not inside `.claude-plugin/`
- Use `${CLAUDE_PLUGIN_ROOT}` for portable path references in scripts
- Skills auto-discover: any `SKILL.md` in a `skills/` subdirectory loads

This layer is well-documented by the official plugin-dev toolkit. Get it right
once and move on.

### Layer 2: Protocol conventions (engineering)

How to write protocol text that AI actually follows. AI does not self-enforce.
Instructions without structural enforcement are suggestions.

**Forcing functions.** Temporal keywords mandate sequence:
- **FIRST** — mandates initial action
- **BEFORE** — creates prerequisite
- **THEN** — defines sequence

**Blocking logic.** Binary checks with evidence requirements:
```
- [ ] [Check]?
  - NO → CANNOT proceed. [Alternative].
  - YES → Evidence: [Must state HOW verified]
```
Key: "CANNOT proceed" (not "should"), evidence requirement, alternative action.

**Observable checkpoints.** Verify actions taken, not internal states.
- Observable (works): "Searched codebase?" → Evidence: [locations found]
- Introspective (fails): "Feeling confident?" → AI cannot detect own states

**Menus as structural enforcement.** Show menu after every response where user
has choices. Menu is always last element. Without it, user cannot control flow.

**Conceptual vs procedural rules.** Conceptual rules (principles) are
referenced by ID. Procedural rules (step-by-step) are inlined at point of use,
even if repeated. Test: must I follow this step-by-step without judgment? If
yes, inline it. If no, reference it.

**Language agnosticism.** All terminology must be paradigm-neutral. Use
"component" not "module/class", "contract" not "type/interface", "identifier"
not "variable/field."

This layer determines whether the skill's instructions are followed or ignored.

### Layer 3: Skill architecture (design)

How to organize knowledge across files so the skill produces good results.

**File roles.** Each file in a skill serves one of these roles:

- **Procedure** — what to do. The actionable method. Abstract, project-agnostic.
  Contains checkpoints, phases, verification steps. Never contains project-specific
  examples or real filenames.

- **Observations** — what goes wrong and what works. Evidence from real incidents,
  abstracted to remove project-specific details. Grounds the procedure in reality.
  Read at skill invocation to calibrate judgment.

- **Vision** (optional) — the philosophical foundation. Why this approach matters.
  The analogy or principle that the procedure derives from. Not every skill needs
  this; complex skills with non-obvious methodology benefit from it.

- **Strategy** (optional) — connects observations to principle. Distills the
  problem being solved and validates that the approach addresses it.

- **Roadmap** (optional) — concrete improvement work items grounded in observed
  failures. Where the skill is going next.

- **References** — detailed guidance loaded on demand, not at invocation.
  Checklists, examples, schemas. Keeps the main skill focused while making
  detail available when needed.

**The separation that matters most: procedure from observations.** The procedure
must be project-agnostic to work in any codebase. The observations must contain
real incidents to ground the procedure in reality. Mixing them produces a
procedure that only makes sense for one project, or observations that are too
abstract to be useful.

**Progressive disclosure.** The SKILL.md loads first and tells the AI what else
to read. Reference files load on demand. This matters because context window is
finite — loading everything at invocation wastes context on guidance that may
not be needed.

**Dependency graph.** When a skill has multiple files, document which files
depend on which. When a parent file changes, its dependents should be checked
for consistency. The SKILL.md is the natural place for this documentation.

### Layer 4: Skill evolution (lifecycle)

How a skill improves through use.

**When a failure becomes an observation.** A failure during skill use reveals a
gap in the procedure. Before adding it to observations, ask: is this a one-time
mistake or a pattern? A pattern is worth documenting. A one-time mistake is not
— unless it reveals a class of failures the procedure doesn't address.

**When an observation becomes a procedure change.** An observation describes
what happened. A procedure change prevents it from happening again. The
observation should exist before the procedure change — it provides the evidence
that the change is warranted. Procedure changes without grounding observations
are guesses about what might go wrong.

**When the procedure is stable.** A procedure stabilizes when new observations
produce only detail-level findings on content that was already structurally
validated. This is diminishing returns — the same phenomenon as in Bildhauer
observation 22. The procedure is refined enough when another pass wouldn't
change its structure, only its surface.

**The improvement cycle:**
```
Use skill → notice failure → abstract to pattern →
add observation → assess if procedure needs change →
if yes: update procedure, grounded in observation →
use skill again
```

### Layer 5: Skill reflexivity (self-awareness)

The skill should notice when its own guidance needs updating.

**When to suggest a skill update.** During any conversation where a skill is
being used, designed, or reviewed — if the experience reveals that the
skill-craft guidance itself is incomplete, contradicted, or could be improved —
surface it as a suggestion. Not an automatic change. A specific suggestion with
reasoning, for the user to decide.

**What triggers a reflexivity suggestion:**
- A skill failure that the guide should have prevented but didn't
- A design pattern that works well but isn't documented in the guide
- A convention from one skill that would benefit others
- A contradiction between the guide's advice and what actually works
- An observation in one skill that generalizes across skills

**How to surface it:** State the specific gap, the evidence (what happened that
revealed it), and the proposed change to the guide. Do not make the change.
The user decides whether and how to incorporate it.

---

## Anti-patterns

### Monolithic SKILL.md

Everything in one file. Works for trivial skills. Fails when the skill grows
because the AI loads the entire file at invocation, wasting context on guidance
that isn't needed yet.

**Fix:** Extract reference material to `references/` subdirectory. Keep SKILL.md
focused on trigger conditions, what to load, and the core method.

### Procedure with project-specific examples

The procedure contains real filenames, service names, or code patterns from a
specific project. It only makes sense in that project. Porting it to another
codebase requires rewriting the examples.

**Fix:** Procedure is abstract. Observations contain the real incidents.

### Checklist without deepening

The procedure has a checklist of N items. The AI performs all N and reports
findings. Issues outside the N categories are not found. The checklist becomes
the ceiling of the investigation.

**Fix:** After each phase, take each finding and trace its implications. What
else must be true if this finding exists? The checklist seeds the investigation;
findings expand it beyond the checklist categories.

### Findings without follow-through

The audit finds a problem and moves to the next checklist item. The implications
of the finding are never traced. Adjacent issues that the finding predicts are
never looked for.

**Fix:** Each finding is a lead. Follow it until it stops producing new findings.
Then move to the next checklist item.

### Skill that never evolves

The skill was written once and never updated. Failures during use are worked
around rather than incorporated as observations or procedure changes.

**Fix:** Establish the improvement cycle (layer 4). Every failure is a candidate
observation. Every observation is a candidate procedure change.

---

## Communication rules

### Questions always carry a recommendation

When a skill presents a decision to the user, it must include the skill's
recommendation alongside the question. Never present a naked question without
a take on the answer. The user may disagree — that's the point. But the skill
should do the analysis and commit to a position, giving the user something to
react to rather than an open-ended evaluation to perform.

This applies to design decisions during skill use, options during investigation,
and any moment where the skill could either ask "what do you think?" or say
"I recommend X because Y — does that work?"

---

## Checklist for reviewing a skill

When reviewing an existing skill or designing a new one, verify each item.
For any item that fails, state what's missing before continuing.

- [ ] **Naming convention.** Are files named per the standard? `SKILL.md` for
  entry point, `PROCEDURE.md` for the method, `OBSERVATIONS.md` for the journal?
  - NO → Rename to standard names.

- [ ] **Self-containment.** Is PROCEDURE.md self-contained? Does it reference
  no other files (unless this is an orchestrator skill)?
  - NO → Inline referenced content into PROCEDURE.md or move to SKILL.md.

- [ ] **Trigger clarity.** Does the SKILL.md description clearly state when the
  skill should activate? Would the AI know from the description alone?
  - NO → SKILL.md description is too vague. Rewrite with explicit trigger phrases.

- [ ] **File separation.** Is the procedure project-agnostic? Are observations
  grounded in real incidents? Are supporting files not loaded at invocation?
  - NO → Identify which files mix concerns. Separate procedure from observations.

- [ ] **Dependency graph.** Does SKILL.md document which files depend on which
  and what to check when a parent changes?
  - NO → Add dependency table to SKILL.md.

- [ ] **Progressive disclosure.** Does the SKILL.md tell the AI what to load
  first and what to load on demand? Or does everything load at once?
  - NO → Extract reference material to `references/`. Keep SKILL.md focused.

- [ ] **Protocol conventions.** Do instructions use forcing functions? Are
  checkpoints observable? Do menus appear where the user has choices?
  - NO → Identify advisory instructions that should be gates. Add blocking logic.

- [ ] **Deepening.** After checklist items, does the procedure trace findings
  to their implications? Or does it stop at the checklist?
  - NO → Add deepening step after each phase or checklist section.

- [ ] **Evolution path.** Is there a place for observations? Has the skill been
  updated based on real failures? Or was it written once?
  - NO → Create OBSERVATIONS.md. If it already exists and is empty, the skill
    hasn't been maintained.

- [ ] **Reflexivity.** Does the skill notice when its own guidance needs updating?
  Or does it only apply to the work at hand?
  - NO → Add reflexivity rule to SKILL.md.
