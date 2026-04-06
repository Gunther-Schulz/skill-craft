# Plugin Structure Reference

Summary of Claude Code plugin directory layout and manifest. For the full
specification, see the official plugin-dev skill (plugin-structure).

## Directory layout

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── plugin/
│   └── skills/
│       └── skill-name/
│           ├── SKILL.md     # Required: skill definition + trigger
│           ├── references/  # Optional: loaded on demand
│           └── scripts/     # Optional: helper scripts
├── commands/                # Optional: slash commands (.md files)
├── agents/                  # Optional: subagent definitions (.md files)
└── hooks/                   # Optional: event handlers
    └── hooks.json
```

## Manifest (plugin.json)

Minimal:
```json
{
  "name": "plugin-name"
}
```

Recommended:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief purpose",
  "license": "MIT"
}
```

## SKILL.md format

```markdown
---
name: skill-name
description: When to activate this skill. Be specific about trigger phrases.
version: 1.0.0
---

# Skill Title

Instructions for AI assistant.

## Load this now

What files to read at invocation.

## Core guidance

The skill's method.
```

## Key rules

- SKILL.md must be named exactly `SKILL.md` (not README.md)
- The `description` field in frontmatter is the trigger condition
- Component directories go at plugin root, not inside `.claude-plugin/`
- Use `${CLAUDE_PLUGIN_ROOT}` for portable path references in scripts
- Skills auto-discover: any `SKILL.md` in a `skills/` subdirectory loads
