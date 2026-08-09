# Review questions

**Load when:** reviewing a skill after creating or modifying it —
any skill, including skill-craft itself.

The questions seed the review and do not bound it: trace each
finding's implications past the list, and state findings per item —
file:line for failures. Distinct from the self-review dispatch
(`references/self-review.md`), the fresh-context pass on changes to
skill-craft's own files; the two compose.

1. **Consumer.** Declared — model or tier range? Enforcement
   density matches the declaration: evidence-register principles
   for a top tier, structural instruments (`enforcement.md`) below
   trust tier? Fragile or invariant sequences keep exact steps at
   every tier?

2. **Structure.** Entry SKILL.md; references skill-local;
   maintenance files outside the plugin payload? Mechanical
   conformance (frontmatter schema, packaging) validated via
   plugin-dev / `skills-ref validate`, or the deferral stated — a
   clean architectural pass does not imply clean frontmatter.

3. **Boundary.** Maintenance files never loaded by operational
   files — referenced as write targets only?

4. **Pointer.** Description states what the skill does and when to
   use it (never second person), leading word front-loaded, one
   trigger per genuinely distinct branch, no identity the body
   carries? Invocation choice
   deliberate — model- vs user-invoked, with the prose-invocation
   cost weighed (SKILL.md, Invocation choice)?

5. **Ladder.** In-file vs disclosed decided by branching — what
   every branch needs inline, single-branch material behind
   pointers? Concepts co-located, not scattered? No sediment —
   every line still bearing on what the document does?

6. **No-op test.** Passed clause by clause against the declared
   consumer — no clause the consumer already obeys by default?
   Packed sentences unpacked before grading (SKILL.md, the no-op
   test's clause unit)? Leading words strong enough to beat the
   default?

7. **Salience.** Every strong default carries its scope at or
   before its statement — no carve-out stranded downstream? Every
   load-bearing default owns its own sentence at the seam it
   governs — none buried mid-sentence in a packed enumeration?

8. **Register.** Directive vs evidence follows each rule's action;
   judgment rules with event-shaped firing moments carry anchored
   triggers; imperative form throughout; directive rules rendered
   positive where possible?

9. **Abstraction.** Judged at the skill's declared scope — a
   domain skill correctly domain-bound; only a domain-general skill
   reaching across domains. No baked-in language, paradigm,
   architecture, runtime, or problem domain; states a relationship
   between entities, not a scenario; composes with existing rules;
   at the level of surrounding content? Context-independent —
   correct behavior for a user whose global configuration is empty?

10. **Enforcement.** Must-hold sequences structurally enforced with
    un-fakeable evidence; N/A escapes mechanically verifiable; no
    naked load-bearing judgment (mitigation ladder applied —
    SKILL.md, Enforcement)? The medium question: is any of the
    text itself must-hold machine semantics — text a machine
    reads, not judgment steering — belonging in a mechanism
    rather than either register (SKILL.md, The two registers),
    prose keeping only the principles? The answering measurement
    is a count — the share of the section's lines that are
    machine-read semantics. Successive repair rounds
    concentrating findings in each round's newest text read as
    evidence the medium is wrong (hypothesis, validate by use).

11. **Completion criteria.** Steps end on checkable, demanding
    bounds — "every X accounted for," not "produce a list"?

12. **Evolution.** Improvement journal exists for judgment skills
    and patch-carrying skills; the gap → observation → change cycle
    stated; capability patches carry provenance and a firing log —
    a patch with no logged firing since the last consolidation
    flagged as a cut candidate (the cut itself belongs to
    consolidation)?

13. **Durability.** Operational content classifiable — enforcement
    structure, capability patch, binding? Bindings state their
    validity condition? A consumer-tier move since minting flags
    directive-register patches for re-registering (SKILL.md, the
    era re-grade — the flag lands here, the re-render belongs to
    consolidation)?

14. **Information flow** (orchestrated skills only). Every handoff
    passes what the receiver needs — explicit, format-matched,
    compaction-safe?

15. **Cross-skill consistency** (multi-skill plugins). Every
    assumption one skill encodes about another — field names,
    paths, schemas, status values, invocation syntax — checked
    against the other skill's actual contract, not recalled?

16. **Rendering fidelity** (skills derived from a source spec or
    framework). Every load-bearing source clause survives;
    structural mechanisms render structural; verified by
    clause-level diff from a context that did not write the render?

17. **Evaluation.** Tier 1 measured for any description-triggered
    skill; Tier 2 where the skill forces an observable signature
    (`references/evaluation.md`)? Inspection is not measurement.

After the pass: state whether it surfaced anything new; recommend
another pass, a change of medium, or moving on.
