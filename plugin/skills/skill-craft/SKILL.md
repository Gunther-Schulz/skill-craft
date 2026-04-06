---
name: skill-craft
description: This skill should be used when the user asks to "create a skill", "design a plugin", "write a protocol", "review a skill", "improve a skill", or discusses skill architecture, plugin structure, protocol conventions, or how to make skills effective. Also activate when discussing failures in existing skills that suggest the skill itself needs updating.
version: 1.0.0
license: MIT
---

# Skill Craft

**Instructions for AI assistant.** Activated when designing, reviewing, or improving Claude Code skills and plugins.

## Load this now

Read `GUIDE.md` and `OBSERVATIONS.md` from this skill's directory. The guide defines how to design effective skills. The observations document what goes wrong when skills are poorly designed — read them to calibrate judgment before advising.

For plugin directory layout and manifest details, see `references/plugin-structure.md`.
For protocol text conventions (forcing functions, blocking logic, checkpoints), see `references/protocol-conventions.md`.

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
