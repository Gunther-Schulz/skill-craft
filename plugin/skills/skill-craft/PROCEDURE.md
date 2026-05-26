# Skill Design Procedure

How to design Claude Code skills the AI reliably follows. Covers plugin
structure, protocol conventions, skill architecture, evolution, and
reflexivity — everything needed to build a skill that holds together
across many invocations and the AI failure modes catalogued in
`references/anti-patterns.md`.

---

## File categories and the loading boundary

Skill files fall into two categories. The boundary — which files load
during skill use — is the central rule.

### Category 1: Operational files — loaded during skill use

- `SKILL.md` — entry point. Trigger conditions, what to load, dependency
  graph. Every skill has this. Always loaded.
- `PROCEDURE.md` — the core method. Loaded by SKILL.md.
- `references/` — supplementary detail loaded on demand during use.
- Sub-skill files for orchestrators with multiple phases.

### Category 2: Maintenance files — never loaded during skill use

Standard names, used only during skill development and improvement:

- `OBSERVATIONS.md` — improvement journal.
- `VISION.md` — philosophical foundation.
- `ROADMAP.md` — improvement work items.

**Placement.** Maintenance files live outside the plugin payload — the
directory tree that ships as the installed skill. Keep them at the
source-repo level, not in the skill directory. They are part of the
project, not the distributable: a user installing the skill should see
only operational files. The source repo carries both; the installed
skill carries only Category 1.

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

**README.md** sits at the plugin root — for humans deciding whether to
install (a different audience than SKILL.md, which is the AI's
instructions).

Required sections:
- **What it does** — the value in one paragraph. Lead with the problem
  solved, not the mechanism.
- **Installation** — the marketplace add + install + reload-plugins
  commands, copy-pasteable.
- **Usage** — trigger phrases and/or slash command.
- **Files** — a table of plugin files and their roles.

Optional: an **origin story** (the real incident that motivated the
skill) and a brief **phases/features** overview.

A plugin with contributors also needs a **Development** section — the
edit → commit → reinstall cycle, `/reload-plugins`, and version bumps
— which prevents the "I changed the file but nothing happened"
friction.

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

**Multiple skills, and shared content.** A plugin can hold several
skills — each its own `skills/<name>/SKILL.md` directory. Reference
files are **skill-local**: a `SKILL.md` loads files from its own skill
directory, and the plugin root has only the recognized component
directories above — an invented plugin-root `references/` is not a
supported home for shared content. So when several skills would share
the same reference material, there is a structural choice: make it
**one skill** — the orchestrator as `SKILL.md`, the other phases as
sub-files under it, references skill-local — or accept a duplicated
copy per skill. Prefer one skill when the shared material is
load-bearing for all of them; duplicated copies drift. The exact path
mechanics for referencing bundled files belong to the official
`plugin-dev` plugin and the Claude Code docs — confirm there rather
than inventing layout.

For plugin packaging details (marketplace vs plugin separation, hooks pitfalls,
installation flow, common mistakes), see `references/plugin-engineering.md`.

This layer is mechanical. Get it right once and move on.

### Layer 2: Protocol conventions (engineering)

How to write protocol text that AI actually follows. AI does not self-enforce.
Instructions without structural enforcement are suggestions.

Layer 2 groups into five disciplines: **Enforcement mechanics**
(the foundations — un-fakeable artifacts, judgment-call mitigation,
gates), **Output discipline** (communication),
**Boundary discipline** (cross-phase + cross-skill state),
**Authoring discipline** (writing the procedure itself), and
**Portability discipline** (terms, domains, context, rendering).

#### Enforcement mechanics

**The un-fakeable-artifact principle.** A check's evidence must be an
artifact that cannot be produced without doing the work the check
represents. An enumeration — "the cases checked: [list]; results:
[list]" — requires having done the checking; a bare claim — "checked
all edge cases" — is satisfiable whether or not the work happened.
Every enforcement technique below rests on this: require the
un-fakeable artifact, not the claim.

*N/A escapes need un-fakeable conditions too.* When a check carries
an N/A clause ("skip if X"), the X condition must itself be
mechanically verifiable from observable state (the diff, the
document, the artifact). Judgment-based N/A conditions ("if small
enough," "if prior coverage applies," "if I judge it redundant") are
fakeable claims — they let the AI escape the check via prose
self-attest. Same shape as the bare-claim failure mode above,
applied to escape clauses; surfaces as the *Skip-rationalization*
anti-pattern (`references/anti-patterns.md`).

**Judgment calls as design risk.** A decision or load-bearing
rule the AI must apply, left without structural backing, fails
latently — the AI acts confidently and inconsistently, error
surfaces downstream. Three mitigations, preference-ordered:

1. **Mechanical criteria.** Compute from observable evidence
   (counts, presence checks, field values, cross-references).
2. **Structural enforcement.** Blocking logic with un-fakeable
   artifact as evidence (judgment stays).
3. **Safety net.** Fail-loud downstream check. Use only when
   (1) and (2) are impossible; document unreliability.

Never leave a decision or load-bearing rule naked.

**Forcing functions.** Temporal keywords mandate sequence:
- **FIRST** — mandates initial action
- **BEFORE** — creates prerequisite
- **THEN** — defines sequence

**Blocking logic.** Binary checks with un-fakeable artifact as
evidence (per "The un-fakeable-artifact principle" above):
```
- [ ] [Check]?
  - NO → CANNOT proceed. [Alternative].
  - YES → Evidence: [Must state HOW verified]
```
Use for workflow skills where sequence matters; for judgment
skills use evidence-backed principles instead (see
`references/writing-by-skill-type.md`).

**Reference loading is a blocking gate, not a pointer.** A skill
that depends on reference files for correct execution must gate
their loading. Use one consolidated load gate at skill activation:
```
- [ ] All load-bearing references loaded this session?
  - NO → CANNOT proceed. Load each now.
  - YES → Evidence: [files + sections read]
```
Applies only to references load-bearing for correct execution;
genuinely-optional references stay on-demand (Layer 3 progressive
disclosure).

**Observable checkpoints.** Verify actions taken, not internal
states. A claim like "checked all edge cases" is unfalsifiable;
**Fix:** require enumeration of what was checked + results — the
un-fakeable artifact.

#### Output discipline

**Communication discipline.** A skill acts on actionable findings
within the same invocation rather than deferring them for the user
to track; defer only what requires out-of-scope structural work.
When presenting a decision, include the skill's recommendation
alongside the question — never a naked question without a take.

#### Boundary discipline

**Commitment consistency across phase boundaries.** When a skill spans phases
(cycles, hand-offs, mode transitions) and a phase produces output another phase
reads as a commitment (recommendation, decision, approved text, locked design,
named option), encode a structural gate at each boundary where the commitment
could be silently revised. Two valid paths through the gate: (a) faithful
execution of the prior commitment, or (b) explicit surface of the change
("Switching from X to Y because Z — confirm?") with operator response required
before proceeding. Silent revision between phases is a discipline violation
regardless of which artifact carries the commitment.

**Information flow in orchestrated workflows.** At every handoff
between skills/agents, data is lost unless verified. For each
handoff point, the receiver must get everything it needs: sender
produces all required data; data passed inline or explicitly
referenced by path; formats match (schema + field names); prompt
compression preserves what downstream consumers need; retries
re-provide the original context, not just the failure details;
persistent state goes to disk (compaction loses
conversation-only state).

#### Authoring discipline

**Conceptual vs procedural rules.** Conceptual rules (principles) are
referenced by ID. Procedural rules (step-by-step) are inlined at point of use,
even if repeated. Test: must I follow this step-by-step without judgment? If
yes, inline it. If no, reference it.

**Every sentence must change behavior.** Skill files have one
reader: the AI in mid-execution. Test: if the sentence were
deleted, would the AI do something different? If no, it is fluff
and belongs elsewhere (OBSERVATIONS.md, commit messages,
README.md). Actionable content may need to exist in both routine
use and on-demand references when load-bearing for routine use.

**Imperative writing style.** Write skill content in imperative
form (verb-first instructions), not second person. Correct: "Read
the configuration file." Incorrect: "You should read the
configuration file." Exception in YAML frontmatter:
`description` uses third-person trigger phrases. Second person
remains correct in user-facing output templates (text the AI
produces FOR the user) and quoted-speech examples.

#### Portability discipline

**Terminology agnosticism.** A procedure must not bake in terms
specific to one variant of the skill's domain. Use scope-neutral
terms rather than variant-specific ones (e.g., for a coding skill,
paradigm-neutral terms across OOP/functional/procedural variants).

**Domain-independence check.** Abstraction is judged against the
skill's intended **scope** — the range it is meant to serve. A
domain-specific skill (a coding skill, a GIS skill, or one that
instantiates a framework for a single domain) is correctly bound to
its domain; only a domain-general methodology skill — skill-craft, a
framework — must reach across unrelated domains. The Layer 4
"Abstraction check" operationalizes this principle as a 7-test
checkpoint before any rule, example, or checkpoint is committed to
procedure or reference files.

**Context-independence check.** Domain-independence verifies the rule
*content* is abstract. This verifies the runtime *behavior* assumes
nothing ambient. A skill must behave correctly regardless of the
user's ambient context — global instruction files, tool settings,
prior-session memory. Test: would this rule still produce correct
behavior for a user whose global configuration is empty? If it
depends on conventions, defaults, or instructions that live outside
the skill, either inline what it needs or make the dependency
explicit and optional. A rule can be fully domain-independent in
wording yet still assume context that exists only for the user who
built it.

**Rendering from a source.** When skill text is derived from a
higher source (framework spec, standards document, parent
methodology), every load-bearing clause of the source must
survive, and structurally-enforced source mechanisms must render
as structural mechanisms (not flattened to prose). Verify by
clause-level diff against the source — not by re-reading the
render (the renderer is blind to its own flattening).

### Layer 3: Skill architecture (design)

How to organize knowledge across files so the skill remains followable
by the AI as it grows.

**File roles.** Each file in a skill serves one of these roles:

- **Procedure** — what to do. The actionable method. Abstract, domain-independent.
  Contains checkpoints, phases, verification steps. Never contains project-specific
  examples or concrete names.

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
  detail available when needed. Reference content is domain-independent like
  procedures — no project-specific evidence. The pattern and fix are
  sufficient; the AI does not need provenance to apply the guidance.

**The separation that matters most: procedure from observations.** The procedure
must be abstract within the skill's intended scope — usable across every project
in that scope, free of any one project's specifics. The observations must contain
real incidents to ground the procedure in reality. Mixing them produces a
procedure that only makes sense for one project, or observations that are too
abstract to be useful.

**Progressive disclosure.** The SKILL.md loads first and tells the AI what else
to read. Reference files load on demand. This matters because context window is
finite — loading everything at invocation wastes context on guidance that may
not be needed. Qualifier: references load-bearing for correct execution are
gated at activation (Layer 2, "Reference loading is a blocking gate"); only
genuinely-optional references load purely on demand.

**Word count.** SKILL.md body: 1,500-2,000 words ideal, 5,000 max. If
exceeding 2,000, move detailed content to `references/`. Each reference
file can be 2,000-5,000+ words (loaded on demand, not at invocation).

**Dependency graph.** When a skill has multiple files, document which files
depend on which. When a parent file changes, its dependents should be checked
for consistency. The SKILL.md is the natural place for this documentation.

### Layer 4: Skill evolution (lifecycle)

How a skill improves through use — the OBSERVATIONS.md cycle and the
disciplines for making each change well. Layer 4 is the machinery of
change; Layer 5 is the noticing that triggers it.

**When a skill includes OBSERVATIONS.md, it has evolution behavior.** The
presence of the file is the signal. SKILL.md must include instructions for
persisting gaps noticed during use:

1. When a gap is noticed (checkpoint missed, failure not covered, pattern
   worth capturing) → write the observation to OBSERVATIONS.md
2. Assess if PROCEDURE.md needs updating based on the new observation
3. Propose changes per Layer 5 "How to surface it" below.

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
what happened. A procedure change prevents it from happening again. A change is
either Path 1 — grounded in an observed incident, which provides the
evidence the change is warranted — or Path 2, a blank-slate
hypothesis, valid only when explicitly marked and validated by use
(full Path 2 techniques in `references/writing-by-skill-type.md`).
What is not valid is an unmarked guess — a change presented as
grounded when it is neither incident-backed nor flagged as a
Path 2 hypothesis.

**Amendment discipline.** When codifying a new failure pattern,
prefer revising existing rules over adding new ones. Decision
sequence: (1) existing rule already addresses it? Revise in place.
(2) Existing content becomes redundant or mergeable? Reduce / merge.
(3) Absorbable by extending an existing rule's scope? Extend (widen
trigger, add gate clause, extend evidence requirement). (4) Only if
none: add a new sub-section.

For **multi-file rule corpora** (a spec rendered into multiple
files, or a framework with instance renders), the decision
sequence applies across ALL homes the concept exists in — a rule
restated in N files with different framings is the reduce/merge
case in (3), not a clean parallel structure. Scan every home
before adding a new sub-section anywhere; fragmenting the same
rule across multiple homes with restated emphasis is its own
failure shape (cross-file fragmentation). On amendment to a rule
in a multi-file corpus, audit each home for stale or now-redundant
restatement.

**Two reflexivity mechanisms — different stages.** Layer 5 "How to
surface it" governs Mechanism 1: AI notices a gap, proposes a
change, user decides. The Self-review mandate below governs
Mechanism 2: AI dispatches a subagent to verify already-committed
changes against the existing ruleset; AI executes recovery on
blocking findings, because the action being corrected is its own
commit, not a proposed rule.

**Self-review mandate.** Every change to skill-craft's canonical
files (`PROCEDURE.md`, `references/*.md`, `SKILL.md`) triggers one
self-review — one subagent for the whole change — **before
commit**. The authoring AI dispatches a fresh-context subagent
against the proposed changes (working tree, staged diff, or
inline-described in brief). The subagent loads skill-craft, reads
the changed text freshly, and applies these checks:

1. **Universal rule application** — for each canonical rule in
   skill-craft (Layer 2 principles, Layer 4 disciplines,
   anti-patterns), test the changed text against it. A violation
   is a blocking finding.
2. **Format consistency** — does the change match adjacent
   entries' format?
3. **Overlap or conflict** — with existing rules; is the
   relationship articulated?
4. **Coverage** — does the change catch what it targets?
5. **Substance of any Fix prescription** — does it specify a
   concrete next action?

Findings ranked blocking / notable / nit. Recovery path:

1. **Blocking** — AI fixes (or reverts the change) without operator
   round-trip.
2. **Notable / nit** — AI surfaces each finding to the operator with
   a recommendation (fix-shape proposed). Operator decides per
   finding: fix-now, accept-with-rationale, or defer-to-
   observations. AI does not self-classify or auto-fix.

**Discipline-citation in recommendations.** When a reviewer finding
cites a discipline (Edit-as-Pareto-improvement / Naked-judgment
anti-pattern / Skip-rationalization anti-pattern / no-theater /
equivalent framework practices), the AI's recommendation cites the
discipline and names its verdict. Classifiable structural-enforcement
candidate → ship-now (n=1). Undefendable alternative per no-theater
→ cut. A proposed AI deviation produces an additional
`operator-decision-required` line citing the alternative — the
deviation surfaces explicitly, not as an equal-weight option.

For accept-with-rationale decisions, AI adds an `Accepted-finding:`
line in the commit message body citing the finding's file:line and
the operator's reason; commit-body-only because the audit trail must
live in git history permanently. For defer-to-observations, AI logs
to the relevant OBSERVATIONS.md (of the corpus the finding cites).
AI commits only after every finding has a recorded disposition.

Reviewing before commit keeps git history clean — bad commits never
enter the record.

**Iterative narrowing of rule or mechanism proposals.** Before
adding any rule, mechanism (subagent, hook, artifact form,
check step), or other corpus addition:

1. **Classify the failure**: *gap* (no existing rule/mechanism
   covers), *unloaded* (exists, never loaded), or
   *loaded-but-inert* (loaded, didn't fire). Fixes differ:
   unloaded → fix loading; loaded-but-inert → sharpen trigger
   or add structural enforcement; gap → minimum novel content.
2. **Enumerate** existing rules/mechanisms in the surface area;
   for each, name what would be lost by extending it to cover
   the failure shape. If the answer is "nothing load-bearing,"
   extend rather than add. Subtract what's covered.
3. **Re-apply** — single pass misses sub-parts.

Complete when further narrowing would lose content no existing
rule or mechanism covers.

**Before applying a patch, check for drift.** Before adding
guidance to a checkpoint: re-read the checkpoint; ask whether the
addition makes it clearer or heavier. If heavier, the addition
belongs in `references/`. If the checkpoint already has 2+ "when
X, also check Y" additions, consolidate rather than patch.

**Abstraction check — BEFORE proposing any change.** Operational
test of Layer 2 "Domain-independence". The change must pass all
of these against the skill's scope:

Exclusion (none of these baked into the change):
1. Specific language
2. Specific paradigm (OOP, functional, procedural)
3. Specific architecture (pipeline, MVC, REST)
4. Single language/runtime
5. Single problem domain

Inclusion (must hold):
6. States an abstract relationship between entities, not a
   specific scenario
7. Composes with existing rules (if standalone, may be a specific
   instance of a more general rule that should be amended instead)

Plus: at the same abstraction level as surrounding content.

**Fix:** rephrase using scope-neutral terminology; if
scenario-shaped, extract the underlying relationship; if
project-specific, move to observations.

**Signal that consolidation may be done.** Two consecutive review
cycles surface only minor wording fixes (typos, phrasing tweaks)
and no structural reorganization (new sub-sections, layer
reshuffling, anti-pattern additions). At that point another
consolidation pass returns diminishing returns; subsequent
observations are deferred until a structural finding surfaces.

### Layer 5: Skill reflexivity (self-awareness)

Noticing — during any use, design, or review of a skill — that
guidance itself needs updating, and surfacing it as a suggestion.
Layer 5 is the trigger for change; Layer 4 is the machinery that
makes it. Reflexivity reaches the skill's own guidance, conventions
that would help other skills, and skill-craft itself.

**When to suggest a skill update.** During any conversation where a
skill is being used, designed, or reviewed — if the experience reveals
that the skill's own guidance is incomplete, contradicted, or could be
improved — surface it (see "How to surface it" below).

**What triggers a reflexivity suggestion:**
- A skill failure that the guide should have prevented but didn't
- A design pattern that works well but isn't documented in the guide
- A convention from one skill that would benefit others
- A contradiction between the guide's advice and what actually works
- An observation in one skill that generalizes across skills

**How to surface it.** State the specific gap, the evidence (what
happened that revealed it), and the proposed change to the guide.
Do not make the change. The user decides whether and how to
incorporate it.

---

## When designing a new skill

Identify the skill type (rule-based, workflow, domain knowledge,
judgment, tooling). Then load
`references/writing-by-skill-type.md` for type-specific authoring
guidance — full Path 2 techniques (phenomenon identification, proxy
detection, bidirectional trigger check, widen by principle),
workflow-phase decision logic, judgment-procedure structure
(principles with evidence requirements, layers, deepening),
domain-knowledge progressive disclosure, and tooling minimalism.
Not needed for reviewing or iterating existing skills.

---

## Anti-patterns

For common skill design mistakes — each with the symptoms that spot
it and the fix — load `references/anti-patterns.md`.

---

## Checklist for reviewing a skill

Run after creating or modifying any skill — not optional. Load
`references/review-checklist.md` and verify all 11 items: structure,
boundary rule, trigger clarity, density, abstraction, protocol
conventions, deepening, evolution, information flow, cross-skill
consistency, rendering fidelity.

---

## After creating or modifying a skill

**The source repo is the single source of truth.** All edits — skill
files, observations, references, plugin.json — happen in the source
repo (e.g., `~/dev/<org>/<plugin>/`). Never edit files in the
marketplace clone directly. The marketplace clone under
`~/.claude/plugins/marketplaces/` is a read-only mirror that gets
updated by pulling from GitHub.

After any change to skill files:

1. **Edit in the source repo.** All file writes target the source repo,
   not the marketplace clone.
2. **Run the review checklist against the changes.** Load
   `references/review-checklist.md` and verify all 11 items against what
   was just edited. State which items pass and which fail, with
   file:line evidence for each failed item. CANNOT proceed to commit
   until all items pass or failures are explicitly accepted with
   reasoning stated.
3. **Commit and push** the source repo. Stage only the changed files.
   Use a descriptive commit message.
4. **Update the marketplace clone.** Find the matching directory under
   `~/.claude/plugins/marketplaces/` (its git remote matches the source
   repo) and pull from the correct branch. This is the catalog Claude
   Code reads available versions from.
5. **Run `claude plugin update <plugin>@<marketplace>`** to bump the
   installed pin in `~/.claude/plugins/installed_plugins.json`. The
   marketplace pull alone does not change which version is active.
6. **Tell the user to run `/reload-plugins`** to re-read the
   installed pin and activate the change — see
   `references/plugin-engineering.md` "Activation". Same handoff
   for same-version edits and version bumps; session restart only
   needed if hook errors from a prior load persist.

This applies to both new skills and edits to existing skills. Do not
consider the work done until both the marketplace clone is pulled and
the installed pin is bumped. Operator handoff: `/reload-plugins`.

