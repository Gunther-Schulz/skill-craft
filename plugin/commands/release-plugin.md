---
description: Release the current plugin repo and activate it — checklist, version-bump check, commit+push, marketplace + pin update, operator /reload-plugins handoff, activation verification.
argument-hint: <plugin-repo-path (default: current repo)>
---

Release the plugin in $ARGUMENTS (default: the current repo). The
sequence is mechanical; show each step's executed output.

1. Resolve the repo: it must contain `plugin/.claude-plugin/plugin.json`
   (or `.claude-plugin/plugin.json` at root). Read `name` + `version`;
   find the marketplace and installed pin in
   `~/.claude/plugins/installed_plugins.json` (key `<name>@<marketplace>`).
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
8. Operator handoff — exactly one action, stated as the turn's final
   line: type `/reload-plugins`. Never `/reload-skills` (it rescans
   already-resolved paths and does not re-read the pin). Every running
   session serves the old version until this step.
9. After the operator confirms: verify activation at the serving
   altitude — for a plugin with a skill, invoke it and read the
   injection's base-directory version; otherwise confirm the
   stale-pin gate stays silent on the next Skill call. Report the
   released version, pin SHA, and activation evidence.
