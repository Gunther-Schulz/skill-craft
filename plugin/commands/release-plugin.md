---
description: Release the current plugin repo and activate it — checklist, version-bump check, commit+push, marketplace + pin update, operator /reload-plugins handoff, activation verification. Covers the first release of a newly created plugin.
argument-hint: <plugin-repo-path (default: current repo)>
---

Release the plugin in $ARGUMENTS (default: the current repo). The
sequence is mechanical; show each step's executed output.

1. Resolve the repo: it must contain `plugin/.claude-plugin/plugin.json`
   (or `.claude-plugin/plugin.json` at root). Read `name` + `version`;
   find the marketplace and installed pin in
   `~/.claude/plugins/installed_plugins.json`
   (key `<name>@<marketplace>`).
   - No pin entry = FIRST RELEASE (birth branch). Steps 2, 3 and 5
     run as written; step 4 is satisfied vacuously (no pin to
     differ from — paste the version being born). In place of
     step 6: `claude plugin marketplace add <owner>/<repo>` (or the
     environment's marketplace convention), then
     `claude plugin install <name>@<marketplace>` (fully-qualified;
     a bare name fails with "Plugin not found" — measured
     2026-08-20). Then converge the environment's plugin management
     where it has one — mirror pins, adoption roster, doctor/health
     checks; an environment that declares a plugin-birth lane or
     runbook governs the convergence detail — follow it rather than
     improvising. Evidence: the environment's pin/roster entry for
     the new plugin pasted, or "none exists" stated. Rejoin at
     step 7.
2. Repo checklist: if the repo's CLAUDE.md names a pre-push or release
   checklist, run it now.
3. Skill-lint: run the checker shipped at this plugin's root,
   `tools/skill_lint.py` (resolve the root from where this command
   file is installed), over every skill file the release ships —
   each `SKILL.md` plus its `references/*.md`. Paste the output.
   Exit 0 = clean or warnings only; exit 1 = blocking flags (wrap,
   trailing whitespace, dead section-cite), and each one is
   dispositioned — fixed, or recorded as accepted with a reason —
   before proceeding. `--fix` strips trailing whitespace, the only
   auto-fix; wrap and cite findings are always hand-resolved.
   Singleton-term warnings do not block; `--diff-base <ref>` narrows
   them to terms the release introduces.
4. - [ ] Version-bump check: plugin.json `version` differs from the
     installed pin's `version`?
     - NO → CANNOT proceed. The marketplace caches by version — a push
       without a bump does not propagate. Bump per the repo's
       convention first.
     - YES → Evidence: both values pasted.
5. Commit + push per the repo's conventions (AI-attribution trailer).
6. Run `claude plugin marketplace update <marketplace>`, then
   `claude plugin update <name>@<marketplace>`; paste both outputs.
7. - [ ] Pin MOVED: re-read `installed_plugins.json` — `version`
     equals the released version AND `gitCommitSha` equals the pushed
     HEAD?
     - NO → CANNOT proceed to activation. Surface the mismatch.
     - YES → Evidence: the pin entry pasted.
8. - [ ] Dispatch freeze. The window opens at step 7, not at step 9:
     the pin has moved on disk and every running session — INCLUDING
     THIS ONE — still resolves the old copy. A subagent inherits the
     dispatcher's resolution, so a dispatch composed now executes the
     OLD skill silently: a skill carries no version in its own prose,
     so both copies read as the same file. The stale-pin gate does not
     cover this — it fires on the operator's next Skill call in an
     unreloaded session and says nothing about a subagent spawned from
     one.
     - Until step 9 is taken: no further dispatches — OR the brief
       states the served version explicitly, so the executor can report
       the mismatch from its own `(h)` slot.
     - Measured 2026-08-10: an executor loaded dispatch-guards 0.10.13
       while the pin on disk already read 0.10.14, released mid-wave by
       its own dispatcher. It flagged the mismatch instead of reporting
       a clean read; nothing else would have surfaced it.
9. Operator handoff — exactly one action, stated as the turn's final
   line: type `/reload-plugins`. Never `/reload-skills` (it rescans
   already-resolved paths and does not re-read the pin). Every running
   session serves the old version until this step.
10. After the operator confirms: verify activation at the serving
    altitude — for a plugin with a skill, invoke it and read the
    injection's base-directory version; otherwise confirm the
    stale-pin gate stays silent on the next Skill call. Report the
    released version, pin SHA, and activation evidence.
