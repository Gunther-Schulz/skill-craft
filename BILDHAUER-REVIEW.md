# Bildhauer Review — First Pass

*2026-04-06. First bildhauer pass on skill-craft v1.0.0.*

## Findings

### F1: SKILL.md missing dependency graph — FIX NOW

The guide (Layer 3) explicitly says: "document which files depend on which" and
"the SKILL.md is the natural place for this documentation." Our SKILL.md doesn't
do this. Bildhauer's SKILL.md has a dependency table. Ours should too.

### F2: Guide doesn't use its own Layer 2 — FIX NOW

The review checklist in GUIDE.md is advisory, not enforced. No gates, no blocking
logic, no "CANNOT proceed." For a guide about writing effective protocols, this is
a credibility gap. The checklist items should be observable checkpoints, not just
questions.

### F3: Layers 4 and 5 could merge — DISCUSS

Reflexivity is the detection mechanism; evolution is the process. They could be one
layer ("skill maintenance") with reflexivity as the trigger and the improvement
cycle as the response. This would simplify the mental model from 5 to 4 layers.

Counter-argument: keeping them separate emphasizes reflexivity explicitly, which
was the motivation for adding it. Merging risks reflexivity becoming a footnote
in the evolution section.

## Assessment

Structure is sound. File separation follows its own advice (procedure-like guide
separate from observations, references loaded on demand). The content is
project-agnostic. Progressive disclosure works. The two concrete gaps (F1, F2) are
fixable without structural change.
