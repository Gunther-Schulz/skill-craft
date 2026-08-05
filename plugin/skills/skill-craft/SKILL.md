---
name: skill-craft
description: This skill should be used when the user asks to "create a skill", "design a plugin", "write a protocol", "review a skill", "improve a skill", or discusses skill architecture, plugin structure, protocol conventions, or how to make skills effective. Also activate when discussing failures in existing skills that suggest the skill itself needs updating.
license: MIT
---

# Skill Craft

Activated when designing, reviewing, or improving Claude Code skills and
plugins.

## Load this now

- [ ] `PROCEDURE.md` and `references/anti-patterns.md` loaded this session?
  - NO → CANNOT proceed. Load each now.
  - YES → Evidence: [files + sections read]

## File dependencies

| Document | Purpose | Derived from | When changed, also check |
|---|---|---|---|
| `PROCEDURE.md` | The skill design method — five layers, protocol conventions, review checklist | First principles + observed patterns | `references/review-checklist.md` (operationalizes Layer rules — Durability, Consumer calibration) and `references/anti-patterns.md` (cites PROCEDURE sections) |
| `references/plugin-engineering.md` | Plugin packaging: marketplace structure, hooks, installation, common mistakes | Battle-tested plugin development | `commands/release-plugin.md` and `hooks/*` (operationalize §Activation's pin model — sync on Activation changes) |
| `references/anti-patterns.md` | Common skill design mistakes and fixes | Observed failures | Loaded at activation per "Load this now"; applied at drafting and at validation |
| `references/review-checklist.md` | Full skill review checklist with blocking logic | Procedure layers | Nothing — standalone reference |
| `references/writing-by-skill-type.md` | Type-specific authoring guidance for new skills (Path 2 techniques, judgment/workflow/domain-knowledge/tooling procedures) | Skill type patterns | Loaded on demand when designing a new skill |
| `references/evaluation.md` | How to evaluate a skill — Tier 1 triggering, Tier 2 behaviour-delta signature, Tier 3 isolated grade | Anthropic measurement guidance + un-fakeable-artifact principle | Loaded on demand when designing or validating a skill |
| `references/self-review.md` | The Layer-4 self-review mandate machinery — five checks, recovery path, discipline-citation, accept-with-rationale / defer-to-observations commit conventions | Layer 4 self-review mandate | Loaded on demand when dispatching the self-review subagent or executing its findings |

When updating PROCEDURE.md, check that its grounding observations still
hold. When adding observations, check if the procedure should change.

## Companion: official plugin-dev

Skill-craft covers design methodology (five layers, protocol conventions,
evolution). The official `plugin-dev` plugin (`plugin-dev@claude-plugins-official`)
covers mechanics (frontmatter format, hooks syntax, agent definitions,
skill-development structure, plugin settings).

When building or scaffolding a plugin, use both:
- Skill-craft for **what** to build and **how to structure** it
- Plugin-dev skills for **formatting** and **Claude Code conventions**

Check the available-skills list for `plugin-dev:` sub-skills (e.g.
`plugin-dev:skill-development`) — their presence is the observable signal
it is installed. If present, invoke the relevant ones alongside
skill-craft guidance. If absent, suggest installation:

```
claude plugin install plugin-dev@claude-plugins-official
```

Offer to run this for the user if they agree. The official plugin
provides authoritative guidance on Claude Code conventions that
skill-craft's `references/plugin-engineering.md` covers only partially.

## When advising on skill design

Apply all five layers from the procedure:
1. Plugin structure (plumbing)
2. Protocol conventions (engineering)
3. Skill architecture (design)
4. Skill evolution (lifecycle)
5. Skill reflexivity (self-awareness)

Most skill authors get layer 1 right (directory layout) and layer 2 partially right (some checkpoints). Layers 3-5 are where skills succeed or fail over time.

## Reflexivity

When a gap is noticed in skill-craft's own guidance during any use,
design, or review, apply Layer 5 reflexivity from PROCEDURE.md
("When to suggest a skill update" + "How to surface it"). Observations
go to `dev-notes/OBSERVATIONS.md` (maintainer-side, outside the
plugin payload).
