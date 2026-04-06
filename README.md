# skill-craft

A Claude Code skill plugin for designing effective skills and plugins.

Covers five layers of skill design: plugin structure, protocol conventions,
skill architecture, evolution, and reflexivity. Complemented by the official
`plugin-dev` plugin for formatting and writing style.

## Installation

```
claude plugin marketplace add Gunther-Schulz/skill-craft
claude plugin install skill-craft@skill-craft-marketplace
/reload-plugins
```

## Usage

Triggers on: "create a skill", "design a plugin", "write a protocol",
"review a skill", "improve a skill", or discussions about skill architecture.

## Files

| File | Role | Loaded |
|------|------|--------|
| `SKILL.md` | Entry point, trigger conditions, dependency graph | At invocation |
| `PROCEDURE.md` | The skill design method (self-contained) | At invocation |
| `OBSERVATIONS.md` | Improvement journal (failure patterns) | Only when improving skill-craft |
| `references/plugin-engineering.md` | Plugin packaging and distribution | On demand |
