# Skill Design Procedure

How to design Claude Code skills that produce good results. Covers plugin
structure, protocol conventions, skill architecture, evolution, and
reflexivity — everything needed to build a skill that works well over time.

---

## File naming convention

Skill files fall into two categories. The boundary between them is the
central naming rule.

### Category 1: Operational files — loaded during skill use

- `SKILL.md` — entry point. Trigger conditions, what to load, dependency
  graph. Every skill has this. Always loaded.
- `PROCEDURE.md` — the core method. Loaded by SKILL.md.
- `references/` — supplementary detail loaded on demand during use.
- Sub-skill files for orchestrators (e.g., Clippy's four SKILL.md files).

The shape of operational files is unconstrained. A skill can have one
PROCEDURE.md or four sub-skills with references directories. The convention
doesn't prescribe how many operational files a skill needs.

### Category 2: Maintenance files — never loaded during skill use

Standard names, used only during skill development and improvement:

- `OBSERVATIONS.md` — improvement journal. Failure patterns from real use.
- `VISION.md` — philosophical foundation. Why the approach matters.
- `ROADMAP.md` — concrete improvement work items.

### The boundary rule

**Category 2 files are never LOADED by Category 1 files.** PROCEDURE.md
never reads from OBSERVATIONS.md. SKILL.md's "Load this now" section never
includes maintenance files. Maintenance files can reference each other and
can reference operational files. The reverse never happens for reading.

**Category 2 files CAN be referenced as write targets.** When a gap is
noticed during skill use, the observation needs a destination. SKILL.md
can say "write new observation to OBSERVATIONS.md" — that's a write
target, not a read dependency. The distinction:
- "Read OBSERVATIONS.md" — loads content, violates boundary
- "Write observation to OBSERVATIONS.md" — write target, acceptable

This prevents the improvement journal from polluting the method while
enabling the evolution cycle (Layer 4) to operate during skill use.

---

## The five layers

Every effective skill addresses five layers. Most skills get layer 1 right and
stop. Skills that work well over time address all five.

### Layer 1: Plugin structure (plumbing)

Directory layout, manifest, auto-discovery, README. The mechanical foundation.

**README.md** sits at the plugin root — the first thing a potential user
sees. It serves a different audience than SKILL.md (which is for the AI).
The README is for humans deciding whether to install.

Required sections:
1. **What it does** — one paragraph explaining the value. Lead with the
   problem it solves or the before/after difference, not the mechanism.
   "Enforces investigation before implementation" not "provides a
   multi-phase workflow with tracker."
2. **Installation** — the marketplace add + install + reload-plugins
   commands, copy-pasteable.
3. **Usage** — trigger phrases and/or slash command. How to invoke it.
4. **Files** — table of plugin files and their roles (operational vs
   maintenance, loaded at invocation vs on demand).

Optional but valuable:
- **Origin story** — why the skill was created. One real incident that
  motivated it. This grounds the README in reality and explains why
  someone should care.
- **Phases/features** — brief description of what the skill does at each
  step. Not the full procedure — just enough to set expectations.

The README does NOT replace SKILL.md. SKILL.md is AI instructions.
README is human documentation. Different audiences, different content.

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

For plugin packaging details (marketplace vs plugin separation, hooks pitfalls,
installation flow, common mistakes), see `references/plugin-engineering.md`.

This layer is mechanical. Get it right once and move on.

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
- Self-reported completion (fragile): "Checked all edge cases?" → AI says
  yes, but evidence is unfalsifiable. Fix: require the evidence to enumerate
  what was checked. Not "checked edge cases" but "checked these specific
  cases: [list]. Results: [list]." The enumeration is observable; the claim
  of completeness is not.

**Menus as structural enforcement.** Show menu after every response where user
has choices. Menu is always last element. Without it, user cannot control flow.

**Conceptual vs procedural rules.** Conceptual rules (principles) are
referenced by ID. Procedural rules (step-by-step) are inlined at point of use,
even if repeated. Test: must I follow this step-by-step without judgment? If
yes, inline it. If no, reference it.

**Language agnosticism.** All terminology must be paradigm-neutral. Use
"component" not "module/class", "contract" not "type/interface", "identifier"
not "variable/field."

**Imperative writing style.** Write all skill content using imperative/
infinitive form (verb-first instructions), not second person. Use objective,
instructional language.

- Correct: "Read the configuration file. Validate input before processing."
- Incorrect: "You should read the configuration file. You need to validate."

The description in YAML frontmatter uses third-person with specific trigger
phrases:

- Correct: `description: This skill should be used when the user asks to
  "create a hook", "add a PreToolUse hook", or mentions hook events.`
- Incorrect: `description: Use this skill when working with hooks.`

This applies to SKILL.md body, PROCEDURE.md, and all reference files.
Second person ("you should", "you need to", "your role") weakens
instruction-following because it positions the AI as recipient rather
than executor.

**Exceptions — second person is correct in:**
- **User-facing output templates** — text the AI produces FOR the user.
  "What would you like to build?" is correct because the AI is speaking
  to a human. The imperative rule applies to instructions for the AI,
  not to output the AI shows to users.
- **Quoted speech examples** — examples of phrases to say or not say.
  "Which do you prefer?" as a bad-pattern example needs to stay in
  second person to illustrate the anti-pattern accurately.

This layer determines whether the skill's instructions are followed or ignored.

### Layer 3: Skill architecture (design)

How to organize knowledge across files so the skill produces good results.

**File roles.** Each file in a skill serves one of these roles:

- **Procedure** — what to do. The actionable method. Abstract, project-agnostic.
  Contains checkpoints, phases, verification steps. Never contains project-specific
  examples or real filenames.

- **Observations** — what goes wrong and what works. Evidence from real incidents,
  abstracted to remove project-specific details. Grounds the procedure in reality.
  Not loaded at invocation — read only when improving the skill itself.

- **Vision** (optional) — the philosophical foundation. Why this approach matters.
  The analogy or principle that the procedure derives from. Not every skill needs
  this; complex skills with non-obvious methodology benefit from it.
  **When present:** SKILL.md should document the VISION → PROCEDURE derivation
  (the dependency table). When PROCEDURE.md is updated, validate the change is
  still covered by VISION.md. If not, either the vision needs expanding or the
  procedure change isn't grounded — present this to the user for decision.

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

**Word count.** SKILL.md body: 1,500-2,000 words ideal, 5,000 max. If
exceeding 2,000, move detailed content to `references/`. Each reference
file can be 2,000-5,000+ words (loaded on demand, not at invocation).

**Dependency graph.** When a skill has multiple files, document which files
depend on which. When a parent file changes, its dependents should be checked
for consistency. The SKILL.md is the natural place for this documentation.

### Layer 4: Skill evolution (lifecycle)

How a skill improves through use.

**When a skill includes OBSERVATIONS.md, it has evolution behavior.** The
presence of the file is the signal. SKILL.md must include instructions for
persisting gaps noticed during use:

1. When a gap is noticed (checkpoint missed, failure not covered, pattern
   worth capturing) → write the observation to OBSERVATIONS.md
2. Assess if PROCEDURE.md needs updating based on the new observation
3. Propose changes with reasoning. Do not change without permission.

This is the write-target rule applied: OBSERVATIONS.md is referenced as a
destination, not loaded as a source.

Skills WITHOUT OBSERVATIONS.md do not need evolution instructions. The
user decides at skill creation whether the skill needs an improvement
journal.

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

**Abstraction check — BEFORE proposing any change to a skill's procedure or
reference files:**

- [ ] Proposed change makes sense in an unrelated codebase?
  - NO → CANNOT add to procedure or references. Rephrase in domain-independent
    terms, or move to observations (where project-specific content belongs).
  - YES → Evidence: [State the domain-independent version of the rule/checkpoint]

A checkpoint about "substring collisions in keyword matching" is project-specific.
A checkpoint about "inputs at decision boundaries for any decision logic" is
project-agnostic. The latter belongs in a skill; the former belongs in an
observation.

---

## Writing procedure content

Not all skills are the same type. The approach to writing PROCEDURE.md depends
on what kind of skill it is.

### Skill types

**Rule-based skills** — checklists, audits, validation procedures. The procedure
is a set of rules that prevent specific failures. Examples: architecture audit
(three-layer checks), bildhauer (five checkpoints at transitions).

**Workflow skills** — orchestrate a multi-phase process. The procedure is a flow
with phases, gates, and routing. Examples: clippy (investigate → implement →
verify), clawdance (design → decompose → build).

**Domain knowledge skills** — encode expertise for a specific domain. The
procedure is "when encountering X, do Y because that's how this domain works."
Examples: gis-utils (CRS safety, geometry conventions), claude-api (SDK patterns).

**Tooling skills** — thin wrappers around a specific workflow or tool. The
procedure is a sequence of steps. Examples: ref (clone a reference repo),
sync-docs (update docs after implementation).

### Writing rule-based procedures

Two paths, depending on whether real incidents exist.

**Path 1: Phenomenon-driven (you have incidents).** A failure happened. The
observation exists or is obvious.

1. Document the observation (what happened, abstracted)
2. Derive the rule from the observation (what would prevent it)
3. The observation grounds the rule — the reason for its existence is traceable

This is how most effective rule-based skills are built. The observation comes
first, the rule follows.

**Path 2: Blank-slate (no incidents yet).** You're writing rules for a new
capability. No failures to learn from. Three techniques:

- **Phenomenon identification.** Before drafting any rule, describe what
  actually goes wrong (or could go wrong) and why. A rule must address the
  root cause, not just one scenario.

- **Proxy detection.** For each element of a rule, ask: does this represent
  the actual condition, or an approximation? "Be careful" is a proxy for a
  specific action. Replace proxies with the precise condition.

- **Non-firing case enumeration.** List at least two cases where the rule
  would NOT fire. For each, decide: should it have? If yes, the trigger is
  too narrow.

Rules from Path 2 are hypotheses. Validate by use, refine through Path 1.

### Writing workflow procedures

Define phases, gates between phases, and what triggers transitions. The key
decisions are: what must be true to advance? What signals completion? What
happens when the user interrupts?

Workflow procedures benefit from menus (layer 2) more than any other type.
The menu IS the flow control — it shows the user where they are and what
they can do next.

**Decision logic within workflow phases.** When a workflow phase produces
design decisions that contain decision logic (classification, matching,
filtering, scoring, routing), apply Path 2 techniques to that logic:
phenomenon identification, proxy detection, and non-firing case enumeration.
A workflow skill's design phase proposing a heuristic is creating an
internal rule — validate it as one, not just as a workflow step.

### Writing domain knowledge procedures

Encode the expertise as concrete rules with context. Not "be aware of CRS
issues" but "BEFORE any geometry operation, verify source and target CRS
match. If they don't, reproject explicitly."

Domain procedures are the most likely to need progressive disclosure — the
full expertise is too large to load at once. Core rules in PROCEDURE.md,
detailed reference material in `references/`.

### Writing tooling procedures

Keep them minimal. State the steps, the expected inputs, the expected outputs.
Tooling skills rarely need observations or evolution — they either work or
they don't. If the tool changes, update the steps.

---

## Anti-patterns

For common skill design mistakes and their fixes, load
`references/anti-patterns.md`. Key patterns: monolithic SKILL.md,
project-specific procedures, checklist as ceiling, findings without
follow-through, skills that never evolve.

---

## Communication rules

### Findings drive action, not reports

A skill that produces actionable findings should act on cheap ones within
the same invocation, not defer them for the user to track. An audit that
lists fixable issues without fixing them is half a skill. A review that
identifies gaps and says "address later" when "later" means "5 minutes
from now" is wasting the user's attention on tracking instead of doing.

Severity classifies impact, not urgency. A low-impact fix that takes
minutes is still worth doing now — deferring it costs more (remembering,
tracking, context-switching) than doing it. Defer only what requires
out-of-scope structural work.

Present all findings with equal clarity. Do not bury low-severity findings
or signal they can be ignored.

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

For the full review checklist with blocking logic, load
`references/review-checklist.md`. Covers: naming, boundary rule, trigger
clarity, writing style, word count, file separation, dependency graph,
progressive disclosure, protocol conventions, deepening, evolution,
reflexivity.

---

## Diminishing returns signal

After each invocation, state whether this pass surfaced anything new or
substantial, and recommend whether another pass is warranted. If the pass
found structural issues, recommend another round. If it found only minor
issues or nothing new, say so and recommend moving on. The user decides —
the skill provides the honest signal with a recommendation.
