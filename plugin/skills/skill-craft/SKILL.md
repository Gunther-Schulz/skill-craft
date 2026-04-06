---
name: skill-craft
description: This skill should be used when the user asks to "create a skill", "design a plugin", "write a protocol", "review a skill", "improve a skill", or discusses skill architecture, plugin structure, protocol conventions, or how to make skills effective. Also activate when discussing failures in existing skills that suggest the skill itself needs updating.
version: 1.0.0
license: MIT
---

# Skill Craft

**Instructions for AI assistant.** Activated when designing, reviewing, or improving Claude Code skills and plugins.

## Load this now

Read `GUIDE.md` from this skill's directory. It is self-contained — everything
needed to design, review, or improve a skill is in that one file.

`OBSERVATIONS.md` is the skill-craft improvement journal. Read it only when
improving skill-craft itself, not when designing other skills.

## File dependencies

| Document | Purpose | Derived from | When changed, also check |
|---|---|---|---|
| `GUIDE.md` | The skill design method — self-contained, five layers, anti-patterns, review checklist | First principles + observed patterns | `OBSERVATIONS.md` (observations ground the guide) |
| `OBSERVATIONS.md` | Failure patterns from real skill design incidents (improvement journal) | Real usage | `GUIDE.md` (new observations may warrant guide changes) |

When updating GUIDE.md, check that OBSERVATIONS.md still grounds it. When adding observations, check if the guide should change.

## When advising on skill design

Apply all five layers from the guide:
1. Plugin structure (plumbing)
2. Protocol conventions (engineering)
3. Skill architecture (design)
4. Skill evolution (lifecycle)
5. Skill reflexivity (self-awareness)

Most skill authors get layer 1 right (directory layout) and layer 2 partially right (some checkpoints). Layers 3-5 are where skills succeed or fail over time.

## Reflexivity rule

When this skill is active and you notice — through discussion, through reviewing another skill, or through observing a skill failure — that the guidance in this skill's own files is incomplete, contradicted, or could be improved: say so. Suggest the specific change to GUIDE.md or OBSERVATIONS.md with reasoning. Do not make the change silently. The user decides.

This applies to all skills, not just this one. If while designing or reviewing any skill you notice that the skill-craft guidance itself has a gap, surface it.
