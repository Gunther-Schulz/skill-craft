---
name: skill-craft
description: This skill should be used when the user asks to "create a skill", "design a plugin", "write a protocol", "review a skill", "improve a skill", or discusses skill architecture, plugin structure, protocol conventions, or how to make skills effective. Also activate when discussing failures in existing skills that suggest the skill itself needs updating.
version: 1.0.0
license: MIT
---

# Skill Craft

Activated when designing, reviewing, or improving Claude Code skills and
plugins.

## Load this now

Read `PROCEDURE.md` from this skill's directory. Self-contained —
everything needed to design, review, or improve a skill.

## File dependencies

| Document | Purpose | Derived from | When changed, also check |
|---|---|---|---|
| `PROCEDURE.md` | The skill design method — five layers, protocol conventions, review checklist | First principles + observed patterns | Nothing — it's a leaf |
| `references/plugin-engineering.md` | Plugin packaging: marketplace structure, hooks, installation, common mistakes | Battle-tested plugin development | Nothing — standalone reference |
| `references/anti-patterns.md` | Common skill design mistakes and fixes | Observed failures | Nothing — standalone reference |
| `references/review-checklist.md` | Full skill review checklist with blocking logic | Procedure layers | Nothing — standalone reference |

When updating PROCEDURE.md, check that its grounding observations still
hold. When adding observations, check if the procedure should change.

## When advising on skill design

Apply all five layers from the procedure:
1. Plugin structure (plumbing)
2. Protocol conventions (engineering)
3. Skill architecture (design)
4. Skill evolution (lifecycle)
5. Skill reflexivity (self-awareness)

Most skill authors get layer 1 right (directory layout) and layer 2 partially right (some checkpoints). Layers 3-5 are where skills succeed or fail over time.

## Reflexivity rule

When a gap is noticed during use — through discussion, reviewing another
skill, or observing a failure — in this skill's own guidance (incomplete,
contradicted, or improvable):

1. Write the observation to the improvement journal (OBSERVATIONS.md)
2. Suggest the specific change to PROCEDURE.md or references/ with reasoning
3. Do not change silently. The user decides.

This applies to all skills. If designing or reviewing any skill reveals
a gap in skill-craft's guidance itself, surface it.
