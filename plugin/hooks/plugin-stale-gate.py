#!/usr/bin/env python3
"""PreToolUse(Skill) gate: WARN when a skill injection comes from a
stale plugin pin. Never blocks — the load proceeds.

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

Deny retired (2026-08-05, operator-raised + measured). The gate
denied in main sessions on the theory that only a deny reaches the
operator, while a warn would let stale rule text into context
unread. Both halves were wrong:

  - The operator-facing channel is `systemMessage`, and it renders
    on the ALLOW path with no `permissionDecision` at all — probed
    live, three variants in one session: bare systemMessage
    (PROBE-A), +additionalContext (PROBE-B), +permissionDecision
    "allow" (PROBE-C). All three surfaced identically, under the
    same "PreToolUse:Skill says:" line the deny had used, and all
    three Skill loads succeeded. The deny bought zero attention.
  - A stale skill is a near-copy of the fresh one; a blocked skill
    is the discipline absent entirely. Observed twice: a fable
    subagent worked around its DENIED skill-craft load by reading
    the mirror by hand, and a main-session deny produced a design
    conversation and no /reload-plugins.

So one rendering serves both contexts, and the `agent_id` branch
that carried the old main/subagent split is gone. Two channels,
two audiences: `systemMessage` tells the OPERATOR the pin moved and
that /reload-plugins (not /reload-skills) re-reads it;
`additionalContext` tells the MODEL its load is the baseline copy
and names the current installPath so it can read the newer source
directly when the delta plausibly matters.

Known imprecision, deliberately left: the pin moves at PLUGIN
granularity while staleness matters at SKILL granularity, so a
release touching only a hook still warns about an unrelated skill.
Under a deny that cost a blocked skill; under a warn it costs one
line of text, which is not worth the SessionStart install-path
snapshot a content-level comparison would need.

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


def stale_pin(payload: dict, installed: dict, baseline):
    """(name, entry, updated) when the invoked skill's plugin pin moved
    after `baseline`, else None. The predicate behind the warning."""
    if payload.get("tool_name") != "Skill":
        return None
    skill = (payload.get("tool_input") or {}).get("skill") or ""
    name, entry = plugin_entry(skill, installed)
    if entry is None or baseline is None:
        return None
    updated = _parse_ts(entry.get("lastUpdated") or "")
    if updated is None or updated <= baseline:
        return None
    return name, entry, updated


def check(payload: dict, installed: dict, baseline) -> str | None:
    """The operator-facing warning text, or None (= stay silent)."""
    hit = stale_pin(payload, installed, baseline)
    if hit is None:
        return None
    name, _entry, updated = hit
    return operator_text(name, updated, baseline)


def operator_text(name: str, updated, baseline) -> str:
    """Rides `systemMessage` — renders to the OPERATOR on the allow
    path (probed 2026-08-05; see module docstring). Names the remedy
    and the near-name command that does NOT perform it."""
    return (
        f"[{SOURCE}] plugin '{name}' pin moved "
        f"{updated.strftime('%Y-%m-%d %H:%M:%S%z')} — after this session's "
        f"baseline ({baseline.strftime('%Y-%m-%d %H:%M:%S%z')}: last "
        "/reload-plugins, else session start). The Skill load PROCEEDS on the "
        "previously resolved version. To serve the new one: /reload-plugins "
        "(/reload-skills does NOT re-read the pin.)"
    )


def model_text(name: str, entry: dict, updated) -> str:
    """Rides `additionalContext` — reaches the MODEL only. Names the
    current installPath so a context that cannot run /reload-plugins
    (any subagent) can still read the newer source directly."""
    install = (entry or {}).get("installPath") or "(installPath unrecorded)"
    return (
        f"[{SOURCE}] plugin '{name}' pin moved "
        f"{updated.strftime('%Y-%m-%d %H:%M:%S%z')}, after this context's "
        "baseline: this Skill load serves the PREVIOUSLY RESOLVED version, "
        "not the pinned one. Current released source, readable directly: "
        f"{install}/skills/. If the newer version plausibly matters for the "
        "task at hand, read it there and say so."
    )


def warn(name: str, entry: dict, updated, baseline) -> None:
    """The one rendering, both contexts: no permissionDecision, ever —
    the Skill load proceeds. Two channels because the two audiences
    need different sentences (docstring)."""
    print(json.dumps({
        "systemMessage": operator_text(name, updated, baseline),
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": model_text(name, entry, updated),
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
        hit = stale_pin(payload, installed, baseline)
        if hit:
            warn(*hit, baseline)
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

    # RED: update (10:19) after session start (08:00), no reload → warn.
    b = session_baseline(transcript(untimed_line, start_line))
    assert b is not None and b.hour == 8
    assert check(skill_call, installed, b) is not None
    # GREEN: reload (10:00) … still before the update (10:19) → warn.
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

    # --- main() level: warn-only, both contexts (2026-08-05).
    # The INVARIANT this file exists to hold since the deny was retired:
    # no output path may carry permissionDecision. Red against the
    # pre-change implementation, which emitted deny for a main session.
    import io
    import os
    from contextlib import redirect_stdout

    install_dir = "/home/g/.claude/plugins/cache/mp/clippy/0.12.1"

    def home_with(last_updated, install_path=install_dir):
        d = tempfile.mkdtemp()
        pdir = os.path.join(d, ".claude", "plugins")
        os.makedirs(pdir)
        e = {"lastUpdated": last_updated}
        if install_path is not None:
            e["installPath"] = install_path
        with open(os.path.join(pdir, "installed_plugins.json"), "w") as fh:
            json.dump({"plugins": {"clippy@coding-clippy": [e]}}, fh)
        return d

    def run_main(raw, home):
        """Feed stdin, capture stdout; Path is redirected so the fixture
        home is read instead of the real one."""
        old_stdin, old_path = sys.stdin, globals()["Path"]

        class _P:
            # `old_path`, not `Path`: the global is patched below, so a
            # late lookup would resolve to this very stub.
            @staticmethod
            def home():
                return old_path(home)

        out = io.StringIO()
        ret, exited, code = None, False, None
        try:
            sys.stdin = io.StringIO(raw)
            globals()["Path"] = _P
            with redirect_stdout(out):
                try:
                    ret = main()
                except SystemExit as exc:
                    exited, code = True, exc.code
        finally:
            sys.stdin, globals()["Path"] = old_stdin, old_path
        return ret, out.getvalue(), exited, code

    t_main = transcript(start_line)                    # baseline 08:00
    stale_home = home_with("2026-08-05T13:20:08.000Z")  # pin moved after
    fresh_home = home_with("2026-08-05T07:00:00.000Z")  # pin older
    call = {"tool_name": "Skill", "tool_input": {"skill": "clippy:clippy"},
            "transcript_path": t_main}

    # (a) THE INVARIANT: stale pin never blocks, in either context.
    # This is the assertion that went red against the deny build.
    for agent in ("a1", "", None):
        raw = json.dumps(call if agent is None else dict(call, agent_id=agent))
        _, out, _, _ = run_main(raw, stale_home)
        assert "permissionDecision" not in out, (agent, out)
        assert "Blocked" not in out, (agent, out)

    # (b) both channels present, each carrying its own audience's text.
    _, out_b, _, _ = run_main(json.dumps(call), stale_home)
    wp = json.loads(out_b)
    hso = wp["hookSpecificOutput"]
    assert hso["hookEventName"] == "PreToolUse", out_b
    # systemMessage → operator: names the remedy and the near-name trap.
    assert wp["systemMessage"] == operator_text(
        "clippy", _parse_ts("2026-08-05T13:20:08.000Z"),
        session_baseline(t_main)), out_b
    assert "/reload-plugins" in wp["systemMessage"], out_b
    assert "/reload-skills does NOT" in wp["systemMessage"], out_b
    assert "PROCEEDS" in wp["systemMessage"], out_b
    # additionalContext → model: names where the newer source sits.
    ctx = hso["additionalContext"]
    assert install_dir + "/skills/" in ctx, ctx
    assert "13:20:08" in ctx, ctx

    # (c) fresh pin → silence, in either context.
    for agent in ("a1", None):
        raw = json.dumps(call if agent is None else dict(call, agent_id=agent))
        assert run_main(raw, fresh_home)[1] == "", agent
    # Missing installPath degrades to the literal placeholder, not a crash.
    _, out_e, _, _ = run_main(
        json.dumps(call),
        home_with("2026-08-05T13:20:08.000Z", install_path=None))
    assert "(installPath unrecorded)/skills/" in out_e, out_e
    # Fail-open survives the new branch: garbage stdin, wrong tool.
    assert run_main("not json", stale_home)[0] == 0
    assert run_main(json.dumps({"tool_name": "Bash"}), stale_home)[1] == ""

    print("plugin-stale-gate: all tests passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _test()
        sys.exit(0)
    sys.exit(main())
