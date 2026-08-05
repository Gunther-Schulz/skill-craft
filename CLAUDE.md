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

## Governed set (search-before-add scope, PROCEDURE.md Layer 4)

skill-craft's governed set: `plugin/skills/skill-craft/PROCEDURE.md`,
`plugin/skills/skill-craft/SKILL.md`,
`plugin/skills/skill-craft/references/*.md`. Every rule addition,
repair, or amendment scans this set first; the scan (command + hits)
is the edit's placement basis.
