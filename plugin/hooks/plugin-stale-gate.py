#!/usr/bin/env python3
"""PreToolUse(Skill) gate: block skill injections from a stale plugin pin.

Incident (2026-08-05): a plugin released several versions mid-session,
`claude plugin update` moved the pin, the operator ran /reload-skills
("no changes") — and the next Skill invocation silently served the
session-start version. A running session serves the install path it
resolved at its own start or at its last /reload-plugins; nothing
announces the mismatch, and the operator may not even know an update
happened (another session can move the pin). The near-name command is
the trap: /reload-skills rescans already-resolved paths and never
re-reads the pin; /reload-plugins re-reads it (verified live both
ways in one session — 0.9.97 served after /reload-skills, 0.12.1
immediately after /reload-plugins).

Predicate (computable, per-plugin): the invoked skill's OWN plugin
has pin `lastUpdated` LATER than the session's last /reload-plugins
marker (else the session's first transcript timestamp). Updates to
unrelated plugins never block. A no-op `claude plugin update` does
NOT move lastUpdated (verified 2026-08-05), so a pin-move fire
corresponds to a real version change.

Fail-open by design: missing field, unreadable file, or parse error
exits silently — the gate must never break Skill use on harness
drift. --test runs fixture-based red/green checks.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SOURCE = "skill-craft/plugin-stale-gate"
# Split literal: this file's own text must never contain the marker,
# or a session that Reads/Writes this file plants a phantom "reload"
# in its transcript and silently disarms the gate there.
RELOAD_MARKER = "<command-name>/reload-plugins</" + "command-name>"


def _parse_ts(s: str):
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    # Always aware: a naive timestamp compared against an aware one
    # raises, which would breach the fail-open promise.
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def session_baseline(transcript_path: str, session_id: str | None = None):
    """Timestamp of the session's last /reload-plugins user command,
    else the first timestamped transcript line — scoped to
    `session_id`'s own records when given: a resumed session reuses
    its transcript file, and the prior life's timestamps and reloads
    must not leak into this process's baseline. Falls back to
    unscoped records when the scope matches nothing. None =
    unknowable."""
    # String probes are a cheap pre-filter only (both serializations);
    # the parsed record is the authority on session membership.
    sid_probes = ((f'"sessionId":"{session_id}"',
                   f'"sessionId": "{session_id}"') if session_id else None)
    first = last_reload = None          # scoped (= unscoped when no sid)
    first_any = last_reload_any = None  # unscoped fallback
    try:
        with open(transcript_path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                has_marker = RELOAD_MARKER in line
                scoped_hint = (sid_probes is None
                               or any(p in line for p in sid_probes))
                if not (has_marker or first_any is None
                        or (scoped_hint and first is None)):
                    continue
                try:
                    rec = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
                scoped = (session_id is None
                          or rec.get("sessionId") == session_id)
                ts = _parse_ts(rec.get("timestamp") or "")
                if ts is None:
                    continue
                if first_any is None:
                    first_any = ts
                if scoped and first is None:
                    first = ts
                # Genuine slash-command records carry message.content as a
                # STRING; tool_result records are also type "user" but carry
                # content as a LIST — a grep/Read echoing the marker must
                # not advance the baseline (that would disarm the gate).
                # No startswith: real command records may lead with a
                # <local-command-caveat> prefix before the command tag.
                content = (rec.get("message") or {}).get("content")
                if (has_marker and rec.get("type") == "user"
                        and isinstance(content, str)):
                    last_reload_any = ts
                    if scoped:
                        last_reload = ts
    except OSError:
        return None
    if first is not None:
        return last_reload or first
    return last_reload_any or first_any


def plugin_entry(skill_name: str, installed: dict):
    """The installed-plugin entry owning `skill_name`, or (None, None).
    `plugin:skill` resolves by prefix; a bare name matches a plugin of
    the same name; user-level skills match nothing."""
    if not skill_name:
        return None, None
    cand = skill_name.split(":", 1)[0]
    plugins = installed.get("plugins", installed)
    for key, entries in plugins.items():
        if key.split("@", 1)[0] == cand and entries:
            # Multi-scope installs: judge by the most recent pin move.
            return cand, max(entries,
                             key=lambda e: e.get("lastUpdated") or "")
    return None, None


def check(payload: dict, installed: dict, baseline) -> str | None:
    """Return the deny reason, or None (= stay silent)."""
    if payload.get("tool_name") != "Skill":
        return None
    skill = (payload.get("tool_input") or {}).get("skill") or ""
    name, entry = plugin_entry(skill, installed)
    if entry is None or baseline is None:
        return None
    updated = _parse_ts(entry.get("lastUpdated") or "")
    if updated is None or updated <= baseline:
        return None
    return (
        f"plugin '{name}' pin moved {updated.strftime('%Y-%m-%d %H:%M:%S%z')} — "
        f"AFTER this session's baseline ({baseline.strftime('%Y-%m-%d %H:%M:%S%z')}: "
        "last /reload-plugins, else session start). The session still serves "
        "the previously resolved version; this Skill injection would be stale. "
        "Operator: type /reload-plugins, then retry the Skill call. "
        "(/reload-skills does NOT re-read the pin.)"
    )


def deny(reason: str) -> None:
    msg = f"[{SOURCE}] Blocked: {reason}"
    print(json.dumps({
        "systemMessage": msg,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": msg,
        },
    }))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Skill":
            return 0
        installed_path = Path.home() / ".claude/plugins/installed_plugins.json"
        installed = json.loads(installed_path.read_text())
        baseline = session_baseline(payload.get("transcript_path") or "",
                                    payload.get("session_id"))
        reason = check(payload, installed, baseline)
        if reason:
            deny(reason)
    except Exception:
        return 0  # fail-open: the gate must never break Skill use
    return 0


def _test() -> None:
    import tempfile

    marker_line = json.dumps({
        "type": "user", "timestamp": "2026-08-05T10:00:00.000Z",
        "message": {"content": RELOAD_MARKER},
    })
    start_line = json.dumps({
        "type": "user", "timestamp": "2026-08-05T08:00:00.000Z",
        "message": {"content": "hello"},
    })
    untimed_line = json.dumps({"type": "last-prompt"})
    # Assistant/tool lines quoting the marker must NOT advance the baseline.
    quoted_line = json.dumps({
        "type": "assistant", "timestamp": "2026-08-05T11:00:00.000Z",
        "message": {"content": "docs mention " + RELOAD_MARKER},
    })

    def transcript(*lines):
        f = tempfile.NamedTemporaryFile(
            "w", suffix=".jsonl", delete=False, encoding="utf-8")
        f.write("\n".join(lines) + "\n")
        f.close()
        return f.name

    installed = {"plugins": {
        "clippy@coding-clippy": [{"lastUpdated": "2026-08-05T10:19:00.000Z"}],
        "other@mp": [{"lastUpdated": "2026-08-01T00:00:00.000Z"}],
    }}
    skill_call = {"tool_name": "Skill", "tool_input": {"skill": "clippy:clippy"}}

    # RED: update (10:19) after session start (08:00), no reload → deny.
    b = session_baseline(transcript(untimed_line, start_line))
    assert b is not None and b.hour == 8
    assert check(skill_call, installed, b) is not None
    # GREEN: reload (10:00) … still before the update (10:19) → deny.
    b = session_baseline(transcript(start_line, marker_line))
    assert b.hour == 10 and check(skill_call, installed, b) is not None
    # GREEN: reload after the update → pass.
    late = marker_line.replace("10:00:00", "10:30:00")
    b = session_baseline(transcript(start_line, late))
    assert b.minute == 30 and check(skill_call, installed, b) is None
    # Quoted marker in an assistant line does not advance the baseline.
    b = session_baseline(transcript(start_line, quoted_line))
    assert b.hour == 8
    # RED (B1, self-review 2026-08-05): a tool_result echoing the marker
    # is type "user" with LIST content — must NOT advance the baseline.
    poison_line = json.dumps({
        "type": "user", "timestamp": "2026-08-05T11:00:00.000Z",
        "message": {"content": [
            {"type": "tool_result", "content": "log: " + RELOAD_MARKER}]},
    })
    assert session_baseline(transcript(start_line, poison_line)).hour == 8
    # A genuine command record with a caveat PREFIX still counts.
    prefixed = json.dumps({
        "type": "user", "timestamp": "2026-08-05T10:40:00.000Z",
        "message": {"content":
                    "<local-command-caveat>x</local-command-caveat>\n"
                    + RELOAD_MARKER},
    })
    assert session_baseline(transcript(start_line, prefixed)).minute == 40
    # Unrelated plugin fresh → pass; unknown/user-level skill → pass.
    assert check({"tool_name": "Skill", "tool_input": {"skill": "other:x"}},
                 installed, b) is None
    assert check({"tool_name": "Skill", "tool_input": {"skill": "keep-warm"}},
                 installed, b) is None
    # Bare skill name matching its plugin resolves.
    assert check({"tool_name": "Skill", "tool_input": {"skill": "clippy"}},
                 installed, b) is not None
    # Fail-open: no baseline, wrong tool, empty payload.
    assert check(skill_call, installed, None) is None
    assert check({"tool_name": "Bash"}, installed, b) is None
    assert check({}, installed, b) is None
    assert session_baseline("/nonexistent/path.jsonl") is None
    # N1: a naive timestamp normalizes to aware UTC — no TypeError.
    naive = json.dumps({"type": "user", "timestamp": "2026-08-05T08:00:00",
                        "message": {"content": "hi"}})
    b2 = session_baseline(transcript(naive))
    assert b2.tzinfo is not None
    assert check(skill_call, installed, b2) is not None
    # N3: resumed transcript — the prior life's records must not set
    # the baseline when session_id is given.
    old_life = json.dumps({"type": "user", "sessionId": "AAA",
                           "timestamp": "2026-08-05T08:00:00.000Z",
                           "message": {"content": "old"}})
    new_life = json.dumps({"type": "user", "sessionId": "BBB",
                           "timestamp": "2026-08-05T12:00:00.000Z",
                           "message": {"content": "new"}})
    t = transcript(old_life, new_life)
    assert session_baseline(t).hour == 8             # unscoped: old life
    b3 = session_baseline(t, "BBB")
    assert b3.hour == 12                             # scoped: this life
    assert check(skill_call, installed, b3) is None  # 10:19 < 12:00
    assert session_baseline(t, "ZZZ").hour == 8      # no match: fallback
    print("plugin-stale-gate: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _test()
        sys.exit(0)
    sys.exit(main())
