#!/usr/bin/env python3
"""PostToolUse(Bash) reminder after `claude plugin update|install`.

Companion to plugin-stale-gate.py (same incident, 2026-08-05): the
pin moves on disk, every running session keeps serving its
previously resolved version, and the activation step is
operator-side — so the moment the pin moves is the moment to say so,
in the session that moved it. The hook never judges; one line of
context next to the tool result. Fail-open on any parse error.
"""
from __future__ import annotations

import json
import re
import sys

PATTERN = re.compile(r"\bclaude\s+plugin\s+(?:update|install)\b")

REMINDER = (
    "If that `claude plugin update`/`install` succeeded, the pin moved on "
    "disk — and every RUNNING session (this one included) keeps serving "
    "the version it resolved at its own start or last /reload-plugins. "
    "Activation is the operator typing /reload-plugins — never "
    "/reload-skills (rescans already-resolved paths; does not re-read "
    "the pin). Proof at the serving altitude: the base-directory line of "
    "a fresh Skill injection."
)


def check(payload: dict) -> str | None:
    if payload.get("tool_name") != "Bash":
        return None
    command = (payload.get("tool_input") or {}).get("command") or ""
    if PATTERN.search(command):
        return REMINDER
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        reminder = check(payload)
        if reminder:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": reminder,
                }
            }))
    except Exception:
        return 0  # fail-open: never break the workflow
    return 0


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert check({"tool_name": "Bash", "tool_input": {
            "command": "claude plugin update clippy@coding-clippy"}}) is not None
        assert check({"tool_name": "Bash", "tool_input": {
            "command": "cd /x && claude  plugin install a@b && echo ok"}}) is not None
        assert check({"tool_name": "Bash", "tool_input": {
            "command": "claude plugin list"}}) is None
        assert check({"tool_name": "Bash", "tool_input": {
            "command": "claude plugin marketplace update mp"}}) is None
        assert check({"tool_name": "Skill"}) is None
        assert check({}) is None
        print("plugin-update-reminder: all tests passed")
        sys.exit(0)
    sys.exit(main())
