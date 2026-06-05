# skill-craft vs Anthropic Agent-Skills guidelines — audit

**Date:** 2026-06-05
**Auditor method:** Anthropic's guidelines were cold-extracted by an *isolated* agent that never saw skill-craft (so its categories aren't anchored to skill-craft's vocabulary), then mapped against skill-craft. This is clippy's separate-checker / isolation lever applied to the audit itself.
**Anthropic sources:** `agentskills.io/specification`; platform.claude.com Agent-Skills *overview* + *best-practices*; the engineering post "Equipping agents for the real world with Agent Skills"; the shipped `anthropics/skills` repo — especially **skill-creator** (Anthropic's own meta-skill, the true head-to-head twin), plus `docx`/`pptx` as *practice* samples.
**skill-craft scope audited:** all 6 operational files — `SKILL.md`, `PROCEDURE.md`, `references/{anti-patterns, plugin-engineering, review-checklist, writing-by-skill-type}.md` (1653 lines total).

---

## 0. The reframe (read this first)

skill-craft **deliberately occupies the PHILOSOPHY band and delegates the MECHANICS band to `plugin-dev`** — stated outright in `SKILL.md:31-51` ("the official plugin-dev plugin … covers mechanics (frontmatter format, hooks syntax, … skill-development structure)") and `plugin-engineering.md:7-9` ("For skill formatting, writing style, hooks … progressive disclosure … see the official plugin-dev plugin").

Consequence: "validate skill-craft against Anthropic's guidelines" is two operations, not one — and the split is exactly the tier‑1 / band‑3 line.

- **MECHANICS band** — the platform contract (frontmatter schema, name charset/limits, packaging, MCP tool-naming). Anthropic *is* an oracle here; conformance is binary. Most of these are *intentionally out of skill-craft's scope* → the mechanics audit is "does it delegate cleanly + dogfood," not "does it teach the schema."
- **PHILOSOPHY band** — degree of enforcement, conciseness, scripts-vs-prose, evaluation strategy. Anthropic is *an opinion* here, with a known bias (its corpus is deterministic-document-skill heavy). A skill-craft/Anthropic difference is **not automatically a defect** — verdict is `aligned` / `defensible-divergence` / `unjustified-drift`.

**Headline:** Mechanics = clean-by-delegation with one worth-fixing gap. Philosophy = *not in tension* — skill-craft is the most elaborated independent re-derivation of Anthropic's own principles, plus genuine extensions. **One real strategic gap: evaluation** (§4) — needs an explicit decision, not silence.

---

## 1. MECHANICS band — categorical verdicts

| Anthropic rule (source) | skill-craft state | Verdict |
|---|---|---|
| YAML frontmatter + body (SPEC) | `SKILL.md` conforms | ✅ conforms |
| `name`/`description` required, valid charset/limits (SPEC, BEST 1.x) | `name: skill-craft` valid; `description` 1 sentence | ✅ conforms (dogfood); schema *taught* by delegation to plugin-dev |
| `description` is third person (BEST 2.2) | `SKILL.md:3` third person; **mandated** at `PROCEDURE.md:284` + `review-checklist:27` | ✅ conforms — *more faithfully than Anthropic's own docx/pptx* (which violate it; see Appendix B-1) |
| SKILL.md body small (BEST 3.2 ≤500 lines / 3.3 <5k tokens) | `SKILL.md` 70 lines | ✅ conforms |
| References one level deep (BEST/SPEC 3.6) | not taught; own graph SKILL→PROCEDURE→references (~2 hops) | ⚠️ minor gap (not taught; soft oracle) |
| TOC for long reference files (BEST >100 / CREATOR >300 lines, 3.7) | `PROCEDURE.md` 675 lines, **no TOC**; `anti-patterns` 317, `plugin-engineering` 335 — none have TOC | ⚠️ gap (low; clear `##` headers mitigate; oracle is soft — Anthropic violates sibling rules) |
| Size metric (lines/tokens) | skill-craft uses **words**: "1,500–2,000 ideal, 5,000 max" (`PROCEDURE.md:389`) ≈ ~6.6k tokens at ceiling | ⚠️ minor drift (ceiling looser than Anthropic's 5k-token / 500-line) |
| Validate frontmatter with reference validator (`skills-ref validate`, 7.1) | **absent** — 12-item `review-checklist` + the "after creating/modifying" steps (`PROCEDURE.md:638-674`) never invoke schema validation | ⚠️ **moderate gap** — the only mechanics finding worth acting on |
| MCP fully-qualified tool names (5.9), forward slashes (4.4), packaging (7.2) | not covered (forward slashes used in practice) | ➖ delegated / N/A |

**The one to act on:** skill-craft delegated mechanics to plugin-dev but its own review process doesn't *hand off* to that validation. The 12-item checklist *looks* complete, so a malformed frontmatter passes skill-craft review silently. Fix: add a "run plugin-dev / `skills-ref validate`" gate to `review-checklist`, **or** state in the checklist that mechanical conformance is validated elsewhere. Right now the delegation boundary is invisible at the point of review.

---

## 2. PHILOSOPHY band — reconciliation

### 2a. Strong alignment / skill-craft is the more-developed version

| Anthropic principle | skill-craft | Read |
|---|---|---|
| **Degrees of freedom** — match freedom to task fragility (BEST 6.3) | Layer 2: "Match the mechanism to the work: deterministic/workflow → structural enforcement; judgment → evidence-backed principles, not gates" (`PROCEDURE.md:133`), operationalized into a 5-type typology (`writing-by-skill-type.md`) | **Aligned + extends.** skill-craft independently re-derives Anthropic's own principle and makes it a procedure. |
| **Concise; Claude is smart; challenge every token** (6.1–6.2) | "Every sentence must change behavior" (`PROCEDURE.md:265`); **Edit-as-Pareto-improvement** "a rule edit must show fewer words OR more coverage" (`anti-patterns:119`); **Additive reflex** "default on ambiguous rule-need: do nothing" (`anti-patterns:142`) | **Aligned, sharper.** skill-craft turns conciseness into a *forcing function* (Pareto edit). |
| **Imperative form** (CREATOR 6.4) | mandated (`PROCEDURE.md:281`, `review-checklist:47`) | **Aligned, exact.** |
| **Avoid heavy-handed all-caps MUST/ALWAYS** (CREATOR 6.5) | "Tone becomes adversarial ('CANNOT proceed', 'do not generate') — the procedure is arguing with the AI's tendencies instead of stating principles" listed as a **drift symptom** (`anti-patterns:65`) | **Aligned** — for *judgment* contexts; reserved CANNOT-proceed gates for *workflow* skills (the type split). |

### 2b. skill-craft resolves an Anthropic internal contradiction

The cold extraction found Anthropic contradicts itself on **enforcement strength** (Appendix B-6): CREATOR calls all-caps MUST a "yellow flag, explain the why"; BEST says "use stronger language like 'MUST filter'." skill-craft **dissolves** the conflict by conditioning on skill type — structural CANNOT-proceed gates for workflow skills, evidence-backed principles (no loud MUSTs) for judgment skills. A genuine improvement over a flat contradiction.

### 2c. Already-internalized critiques

- The "validator-mode register leaks into judgment skills" failure → guarded by **"Scope precedes default"** (`PROCEDURE.md:272`) and the **Salience/reading-order** checklist item (`review-checklist:35`).
- skill-craft's own anti-bloat doctrine (Procedure drift, Rule elaboration creep, Additive reflex) *is* Anthropic's conciseness ethos, self-applied.

### 2d. skill-craft extensions with no Anthropic analog (net value-add)

Five-layer model (plumbing → protocol → architecture → evolution → reflexivity); the un-fakeable-artifact / blocking-logic enforcement theory; Layer-4 evolution (OBSERVATIONS cycle, amendment discipline, **self-review subagent mandate**, iterative narrowing); Layer-5 reflexivity; the Category-1/2 loading boundary; rendering-from-source fidelity (`Unverified render`, `Edit-without-spec-origin` anti-patterns). These serve the *judgment/process/longevity* domain Anthropic's guidance barely addresses.

### 2e. Minor philosophy gaps

- **"Pushy" descriptions to counter under-triggering** (CREATOR 2.6) — not addressed. Cheap potential value-add.
- **Plan-validate-execute / verifiable intermediate outputs** (BEST 5.10–5.11) — present in spirit (un-fakeable artifacts) but not named as a script pattern (skill-craft skills rarely bundle scripts; defensible).

---

## 3. Dogfooding tensions (skill-craft vs its own rules)

1. **675-line PROCEDURE.md vs its own "Procedure exceeds 200 lines" drift symptom** (`anti-patterns:62`) and "the procedure should fit on a screen" (`anti-patterns:80`). Partly defensible — skill-craft is a *domain-general framework* (its own Abstraction notes flag frameworks as the special case) and it *has* pushed detail to 4 reference files. But the symptom is stated bluntly and the artifact exceeds it 3×. Worth an explicit accept-with-rationale or a re-derivation pass.
2. **Layer-4 density** — e.g. the discipline-citation closed-set (`PROCEDURE.md:495-514`) is exactly the "Rule elaboration creep" shape (`anti-patterns:125`: body exceeds principle+test+fix, sub-shapes elaborate the same principle) it warns against. Running skill-craft on skill-craft would flag it.

Neither is a correctness defect; both are proportionality findings — the same lens skill-craft (and Anthropic's "concise is key") would apply to any other skill.

---

## 4. The evaluation gap — the one with teeth (+ proposed gate)

### 4a. The gap

Anthropic's guidance is heavily **measurement-driven**: build evals *first* (8.1), **≥3 scenarios** (8.2, countable), establish a **baseline with/without** the skill (8.3), **Claude-A/Claude-B** iteration (8.5), test **across models** (8.9), plus skill-creator's whole benchmark / trigger-rate / description-optimization harness (`run_loop.py`, `aggregate_benchmark`, held-out test selection 8.15).

**skill-craft has none of it** — confirmed across all 6 files. Its quality model is entirely *static review + incident evolution*: `review-checklist` (12 items), the self-review subagent mandate, Path 1/Path 2, the OBSERVATIONS cycle. Rigorous — but a different epistemology: **review/derivation, not measurement.** And the divergence is currently **silent** — skill-craft never mentions evaluation, neither to adopt nor to reject it.

### 4b. Why a naive port fails — and the reconciliation

Anthropic's assertion-based evals fit *deterministic/tooling* skills. They fail skill-craft's *judgment* domain — and Anthropic agrees: "don't force assertions onto subjective skills" (8.12); skill-creator allows "just vibe" grading for subjective skills. So the gap can't be closed by importing the harness. It closes by re-expressing evaluation in skill-craft's **own** idiom — the tier-1 / un-fakeable-artifact / isolation machinery this very audit is built on.

### 4c. Proposed: a 3-tier lightweight eval gate (proportional by skill type)

A judgment skill still has a **tier-1-able slice**. Decompose:

- **Tier 1 — Triggering rate (mechanical, always).** Triggering is a function of the `description` = external, measurable, the purest tier-1 oracle even for a judgment skill. Adopt skill-creator's approach wholesale: ≥N realistic *should-trigger* queries + ≥M tricky *should-NOT-trigger* near-misses, run each ×3, report trigger rate. skill-craft has **zero** triggering validation today — this is the cheapest, highest-value adoption and it is fully mechanical. (Closes Anthropic 8.2/8.11/8.15 for the part that genuinely applies.)

- **Tier 2 — Behavior-delta signature (with/without baseline, observable).** You cannot assert "the judgment was correct," but you *can* define the skill's **observable signature** — the artifacts it is *supposed* to force — and check that with-skill runs produce it and without-skill runs don't. For a judgment skill the signature is the discipline's required evidence: enumerated findings carrying location + impact + classification (`writing-by-skill-type:147`); for skill-craft itself, a completed `review-checklist` with file:line per item. This is the un-fakeable-artifact principle applied to *eval design*: don't measure "good judgment," measure "did the forced artifact appear, and only with the skill on." (Closes Anthropic 8.3 in skill-craft's idiom.)

- **Tier 3 — Isolated qualitative grade (the residue).** The irreducibly-subjective quality ("was the analysis insightful, the cut correct") gets the clippy/skill-creator treatment: an **isolated grader subagent** that didn't author the skill or run the eval reads the with/without outputs blind and scores. Not categorical — but isolation lowers the floor. Reserve for high-stakes / widely-used judgment skills.

### 4d. Proportionality (which skill gets which tier)

| Skill type | Tier 1 (trigger) | Tier 2 (signature delta) | Tier 3 (isolated grade) |
|---|---|---|---|
| Tooling / workflow (deterministic) | yes | yes — use Anthropic's full assertion evals | rarely |
| Judgment | **yes (mandatory, cheap)** | when the skill forces an observable signature | high-stakes only |
| skill-craft itself | yes | yes (the review-checklist *is* the signature) | yes |

### 4e. The decision this forces

Either (a) adopt the gate above — minimally Tier 1 for every skill, Tier 2 where a signature exists — added as a short **"Evaluation" discipline** (new `references/evaluation.md` or a Layer-4 subsection), **or** (b) explicitly state-and-justify the review-over-measurement stance, citing Anthropic 8.12's own concession for subjective skills. Either closes the gap. Silence does not — and silence is currently the state.

Recommendation: **(a), scoped to Tier 1 + Tier 2.** Triggering validation is pure upside skill-craft simply lacks; the signature-delta check is just the un-fakeable-artifact principle pointed at the skill's own output, so it's idiomatic rather than borrowed. Tier 3 only where stakes justify it.

---

## 5. Caveats (oracle instability)

The cold extraction surfaced **10 internal Anthropic contradictions** (Appendix B). Several "guidelines" are therefore *soft oracles* — Anthropic violates its own rule in shipped skills:
- 500-line limit → `docx/SKILL.md` is 590 lines.
- Third-person description → `docx`/`pptx` open imperative/second-person.
- TOC threshold → BEST says >100, CREATOR says >300 lines.
- Progressive disclosure / one-level references → `docx` inlines everything, zero `.md` references.

Findings dinged against these were down-weighted accordingly. Also: philosophy-band verdicts are the auditor's read — that band exists precisely because the calls are the maintainer's to set.

---

## Appendix A — full cold-extracted Anthropic checklist
*(banded MECHANICS/PHILOSOPHY, source-cited; ~80 items across frontmatter, description/triggering, progressive disclosure, file structure, scripts/determinism, content style, packaging/validation, evaluation. Stored separately from this audit; regenerate via the isolated-extraction method in the header.)*

## Appendix B — Anthropic's 10 internal "doc-says vs practice-shows" contradictions
1. Third-person description rule violated by shipped docx/pptx.
2. 500-line limit treated as hard rule but docx is 590 lines.
3. docx ships everything inline despite the docs' own progressive-disclosure/one-level-reference mandate.
4. TOC threshold conflicts: BEST >100 lines vs CREATOR >300 lines.
5. `name` validation split across sources (SPEC has consecutive-hyphen + dir-match; platform docs have XML-tag + reserved-word) — no single source is complete.
6. Enforcement strength contradictory: CREATOR "all-caps MUST is a yellow flag" vs BEST "use stronger language like MUST."
7. `license`/`compatibility`/`metadata`/`allowed-tools` exist only in SPEC, absent from the platform overview/best-practices schema.
8. The repo's `spec/` file is a stub redirect to agentskills.io — the authoritative contract lives off-repo.
9. "Evaluation-first" mandated but "no built-in way to run these evaluations"; skill-creator's eval JSON schema differs field-for-field from the best-practices eval schema.
10. Reserved-word ban is name-only; descriptions are unconstrained (docs don't clarify).
