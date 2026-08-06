# Skill-craft — repo-local instructions

## Rule-corpus edits

When editing skill-craft, anneal-framework spec, or instance
skills (clippy / daneel / etc.): invoke the `skill-craft` skill
via the Skill tool BEFORE the edit.

Apply Edit-as-Pareto-improvement: name what the edit reduces or
consolidates. If nothing — the addition is suspect per the
Additive reflex anti-pattern (skill-craft/references/anti-patterns.md).

**Recursion check**: rule-edit subagent PASS may self-validate.
Pause + re-read before push.

## Role files

Defaults and forms come from `~/.claude/CLAUDE.md` ("Per-project
accretion" — project file roles; "Insurance mechanisms" — the ledger),
and are not restated here. What this repo carries:

- `LEDGER.md` — this repo's on-disk ledger. Read its tail before
  re-deriving anything that may already be settled.
- `BACKLOG.md` — future work, in the parked and ready grades.
- `PLAN.md` — the 2.0.0 rewrite charter; carrier for that design
  session's settled decisions.
- `dev-notes/` — maintenance artifacts, kept outside the plugin
  payload. `OBSERVATIONS.md` is the incident record that grounds canon
  changes; eval results live in dated subdirectories.
- `README.md` — humans and the public, never operating knowledge.

Boundary: an incident and its abstraction → `dev-notes/OBSERVATIONS.md`;
a decision and its why → `LEDGER.md`; a work item → `BACKLOG.md`; a
standing rule → this file. A rationale that lives only in a commit
message is the drift this split exists to stop.

## Governed set (search-before-add scope, SKILL.md Amendment discipline)

skill-craft's governed set: `plugin/skills/skill-craft/SKILL.md`,
`plugin/skills/skill-craft/references/*.md`. Every rule addition,
repair, or amendment scans this set first; the scan (command + hits)
is the edit's placement basis.
