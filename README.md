# skill-craft

> Skills the AI actually follows.

You write a skill. The AI ignores half of it — skips the reference
it was told to read, hits a checkpoint and breezes past it. The
skill says "check all edge cases" and the AI says "checked" without
checking. And the half it does read costs context on every turn,
whether or not it fires. Skill-craft engineers against both.

A Claude Code plugin for designing skills that hold at a cost worth
paying. Every skill declares its consumer — the model tier that
executes it — and that declaration sets the enforcement density:
evidence-register principles for top-tier consumers, structural
instruments (un-fakeable artifacts, blocking gates, load manifests)
below trust tier. The economics — pointer wording, invocation
choice, term selection, the model-relative no-op test — apply at
every tier. The methodology ships with its tooling: an evaluation
harness (`/eval-skill`), a mechanical release-and-activation
sequence (`/release-plugin`), and hooks that catch stale plugin
pins in running sessions — a plugin update activates only on
`/reload-plugins`; until then every running session silently serves
the old version.

skill-craft is the meta-discipline. The
[Anneal framework](https://github.com/Gunther-Schulz/anneal-framework)
is built using its mechanisms; framework instances
([Clippy](https://github.com/Gunther-Schulz/coding-clippy),
[DANEEL](https://github.com/Gunther-Schulz/daneel)) inherit those
mechanisms downstream.

## The method

- **The two parties** — writer and declared consumer; enforcement
  density follows the declaration
- **Economics** — the two loads, context pointers, invocation
  choice, term selection, the no-op test, pruning
- **The two registers** — directive vs evidence, chosen by consumer
  and mechanism
- **Enforcement** — un-fakeable artifacts; the tier-conditional
  instrument toolbox
- **Lifecycle** — durability classes, fire-based retirement, the
  era re-grade, amendment discipline
- **Evaluation** — triggering measured, behaviour-delta signature,
  isolated grade

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
| `SKILL.md` | The canon — two-party spine, economics, registers, enforcement, lifecycle | At activation |
| `references/enforcement.md` | The instrument toolbox — blocking logic, load gates, boundary and handoff checks | On demand |
| `references/anti-patterns.md` | Skill-design failure shapes — symptoms + fixes | On demand |
| `references/review-checklist.md` | The review questions | On demand |
| `references/evaluation.md` | Tier 1 triggering, Tier 2 behaviour-delta, Tier 3 grade | On demand |
| `references/self-review.md` | The pre-commit fresh-context self-review dispatch | On demand |
| `references/plugin-engineering.md` | Plugin packaging: marketplace, hooks, installation | On demand |
| `references/writing-by-skill-type.md` | Type-specific authoring (judgment, workflow, domain-knowledge, tooling) | On demand |
| `commands/release-plugin.md` | `/release-plugin` — mechanical release + activation sequence, ends at the operator's `/reload-plugins` | Command |
| `hooks/plugin-stale-gate.py` | Warns (never blocks) when a Skill call's own plugin pin moved after the session's last `/reload-plugins` — the load proceeds on the stale copy, the operator gets the fix, the model gets the newer source's path | Hook (automatic) |
| `hooks/plugin-update-reminder.py` | After `claude plugin update`/`install`: running sessions serve the old version until `/reload-plugins` | Hook (automatic) |
| `dev-notes/OBSERVATIONS.md` | Improvement journal — maintainer-side, outside plugin payload | Never |

## License

MIT
