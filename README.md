# skill-craft

> Skills the AI actually follows.

You write a skill. The AI ignores half of it — reads `SKILL.md`, skips
`PROCEDURE.md`, hits a checkpoint and breezes past it. The skill says
"check all edge cases" and the AI says "checked" without checking.
This is the failure mode skill-craft engineers against.

A Claude Code plugin for designing skills that work as written. Five
layers of structural enforcement — un-fakeable artifacts, forcing
functions, blocking gates — so the AI's behavior matches what the
skill says, not what it pattern-completes.

skill-craft is the meta-discipline. The
[Diligence framework](https://github.com/Gunther-Schulz/diligence-framework)
is built using its mechanisms; framework instances
([Clippy](https://github.com/Gunther-Schulz/coding-clippy),
[DANEEL](https://github.com/Gunther-Schulz/daneel)) inherit those
mechanisms downstream.

## The five layers

1. **Plugin structure** — directory layout, manifest, auto-discovery
2. **Protocol conventions** — un-fakeable artifacts, forcing functions, blocking gates
3. **Skill architecture** — file roles, progressive disclosure, dependency graph
4. **Skill evolution** — the observations-cycle and amendment discipline
5. **Skill reflexivity** — noticing during use that guidance itself needs updating

Layers 3-5 are where skills succeed or fail over time.

## Companion: plugin-dev

skill-craft covers **methodology** — what to build and how to structure
it. The official `plugin-dev` plugin (install:
`claude plugin install plugin-dev@claude-plugins-official`) covers
**mechanics** — frontmatter format, hooks syntax, agent definitions.
Use both when building a plugin.

## Installation

```bash
claude plugin marketplace add Gunther-Schulz/skill-craft
claude plugin install skill-craft@skill-craft-marketplace
```

Run `/reload-plugins` in Claude Code to activate.

## Triggers

- "create a skill" / "design a plugin" / "write a protocol"
- "review a skill" / "improve a skill"
- Discussions about skill architecture

## Files

| File | Role | Loaded |
|------|------|--------|
| `SKILL.md` | Entry point, trigger conditions, dependency graph | At invocation |
| `PROCEDURE.md` | The skill design method (self-contained, five layers) | At invocation |
| `references/anti-patterns.md` | Common skill design mistakes — symptoms + fixes | At validation time |
| `references/review-checklist.md` | Full skill review checklist with blocking logic | On demand |
| `references/plugin-engineering.md` | Plugin packaging: marketplace, hooks, installation | On demand |
| `references/writing-by-skill-type.md` | Type-specific authoring (judgment, workflow, domain-knowledge, tooling) | On demand |
| `dev-notes/OBSERVATIONS.md` | Improvement journal — maintainer-side, outside plugin payload | Never |

## License

MIT
