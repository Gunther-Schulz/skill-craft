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
3. - [ ] Version-bump check: plugin.json `version` differs from the
     installed pin's `version`?
     - NO → CANNOT proceed. The marketplace caches by version — a push
       without a bump does not propagate. Bump per the repo's
       convention first.
     - YES → Evidence: both values pasted.
4. Commit + push per the repo's conventions (AI-attribution trailer).
5. Run `claude plugin marketplace update <marketplace>`, then
   `claude plugin update <name>@<marketplace>`; paste both outputs.
6. - [ ] Pin MOVED: re-read `installed_plugins.json` — `version`
     equals the released version AND `gitCommitSha` equals the pushed
     HEAD?
     - NO → CANNOT proceed to activation. Surface the mismatch.
     - YES → Evidence: the pin entry pasted.
7. Operator handoff — exactly one action, stated as the turn's final
   line: type `/reload-plugins`. Never `/reload-skills` (it rescans
   already-resolved paths and does not re-read the pin). Every running
   session serves the old version until this step.
8. After the operator confirms: verify activation at the serving
   altitude — for a plugin with a skill, invoke it and read the
   injection's base-directory version; otherwise confirm the
   stale-pin gate stays silent on the next Skill call. Report the
   released version, pin SHA, and activation evidence.
