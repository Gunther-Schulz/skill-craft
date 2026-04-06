# Protocol Conventions Reference

Summary of conventions for writing protocol text that AI actually follows.
For the full specification, see Clippy's CONVENTIONS.md.

## Core principle

AI does not self-enforce. Protocol text must use structural mechanisms to
mandate behavior. Instructions without enforcement are suggestions.

## Language agnosticism

All terminology must be language-agnostic and paradigm-neutral.

- "Component" not "module", "class", "package"
- "Contract" not "type", "interface", "signature"
- "Identifier" not "variable", "field", "property"

Test: does this rule work for C, Python, Go, Haskell, and JavaScript?

## Forcing functions

Temporal keywords mandate sequence:

- **FIRST** — mandates initial action
- **BEFORE** — creates prerequisite
- **THEN** — defines sequence

## Blocking logic

Binary checks with evidence requirements:

```
- [ ] [Check]?
  - NO → CANNOT proceed. [Alternative].
  - YES → Evidence: [Must state HOW verified]
```

Key elements: binary YES/NO, evidence requirement, "CANNOT proceed" (not
"should"), alternative action, clear gate.

## Observable checkpoints

Checkpoints verify actions taken, not internal states.

Observable (works): "Searched codebase?" → Evidence: [locations found]
Introspective (fails): "Feeling confident?" → AI cannot detect own states

## Menus as structural enforcement

Show menu after every response where user has choices. Menu is always last
element. Menu presence is the enforcement mechanism — without it, the user
cannot control the flow.

## Progressive disclosure

Reference detailed guidance from `references/` files rather than inlining
everything. Load at invocation: SKILL.md only. Load on demand: reference files
when the AI needs specific guidance.

## Conceptual vs procedural rules

- **Conceptual** (principles): reference by ID. "C3 compliant?"
- **Procedural** (step-by-step): inline at point of use, even if repeated.

Test: must I follow this step-by-step without judgment? If yes, inline it.
If no, reference it.
