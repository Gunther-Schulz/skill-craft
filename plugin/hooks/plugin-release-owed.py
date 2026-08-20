#!/usr/bin/env python3
"""SessionStart banner: this plugin SOURCE REPO is ahead of its
installed pin — a release is owed.

Incident (2026-08-20): the repo accumulated committed versions 2.2.1
and 2.2.2 while the installed pin stayed 2.2.0, so the operator's
/reload-plugins correctly re-read an unmoved pin and served the old
payload.

Direction. This hook and plugin-stale-gate.py guard the two ends of
one pipeline and never overlap:

  - here: committed source AHEAD of the pin — the release step never
    ran, so nothing on disk has the new version yet;
  - stale gate: the pin AHEAD of the running session — the release
    ran, but this session resolved its install path before it.

Channel. A session-start banner, not a commit-time warning: the
commit-time warning is what already existed, and it measurably
decayed — three fires, zero holds, on the incident day itself. A
warning printed beside a commit competes with the commit's own
output and is read once; the owed state persists until the release
happens, so the signal has to persist too, at a moment when acting
on it is the natural next move.

Predicate (computable, per-plugin): the manifest version at
`<cwd>/plugin/.claude-plugin/plugin.json` (else
`<cwd>/.claude-plugin/plugin.json`) differs from the `version` of a
pin entry keyed `<name>@<marketplace>` in
~/.claude/plugins/installed_plugins.json. No manifest = not a plugin
source repo; no pin entry = never installed here, and a FIRST
release is a decision, not an owed act — both stay silent.

Fail-open by design: any exception exits 0 with no output. The hook
never blocks and never exits nonzero. --test runs fixture-based
checks over the same check() the hook calls.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PIN_PATH = Path.home() / ".claude/plugins/installed_plugins.json"

# Manifest locations, in resolution order: the plugin-payload layout
# this repo uses, then a repo that IS the plugin root.
MANIFEST_RELPATHS = (
    "plugin/.claude-plugin/plugin.json",
    ".claude-plugin/plugin.json",
)


def read_manifest(root) -> dict | None:
    """The plugin manifest under `root`, or None when `root` is not a
    plugin source repo."""
    for rel in MANIFEST_RELPATHS:
        path = Path(root) / rel
        if path.is_file():
            return json.loads(path.read_text())
    return None


def pin_entries(name: str, pin_path) -> list[tuple[str, dict]]:
    """(key, entry) for every installed-plugin entry whose key is
    `<name>@<anything>`. Values are LISTS of entries — one per scope —
    so a plugin installed twice yields two rows (verified against the
    real file, 2026-08-20)."""
    installed = json.loads(Path(pin_path).read_text())
    # `.get("plugins", installed)`: tolerate a flat file, as
    # plugin-stale-gate.py does at the same read.
    plugins = installed.get("plugins", installed)
    out = []
    for key, entries in plugins.items():
        if key.split("@", 1)[0] != name:
            continue
        for entry in entries or []:
            out.append((key, entry))
    return out


def check(root, pin_path) -> list[str]:
    """The banner lines — one per pin entry behind the manifest, empty
    when nothing is owed. Both inputs are parameters so the fixtures
    exercise this exact function."""
    manifest = read_manifest(root)
    if not manifest:
        return []
    name = manifest.get("name")
    committed = manifest.get("version")
    if not name or not committed:
        return []
    return [
        f"release owed: {name} committed {committed}, installed "
        f"{entry.get('version')} ({key}) — /release-plugin moves the pin"
        for key, entry in pin_entries(name, pin_path)
        if entry.get("version") != committed
    ]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        root = payload.get("cwd") or os.getcwd()
        for line in check(root, PIN_PATH):
            print(line)
    except Exception:
        return 0  # fail-open: never break session start
    return 0


def _test() -> None:
    import tempfile

    def repo(version, name="skill-craft", nested=True):
        """A plugin source repo fixture; `version=None` writes no
        manifest at all."""
        d = tempfile.mkdtemp()
        if version is None:
            return d
        rel = MANIFEST_RELPATHS[0] if nested else MANIFEST_RELPATHS[1]
        path = Path(d) / rel
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"name": name, "version": version}))
        return d

    def pins(body):
        f = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8")
        f.write(body)
        f.close()
        return f.name

    real_shape = pins(json.dumps({"version": 1, "plugins": {
        "skill-craft@skill-craft-marketplace": [{
            "scope": "user", "version": "2.2.2",
            "installPath": "/home/g/.claude/plugins/cache/x/2.2.2"}],
        "other@mp": [{"version": "9.9.9"}],
    }}))

    cases, failed = [], 0

    def case(label, fn):
        nonlocal failed
        try:
            fn()
            cases.append(f"  [{label}] PASS")
        except AssertionError as exc:
            failed += 1
            cases.append(f"  [{label}] FAIL: {exc}")

    # (a) differ → fires, and the line carries BOTH versions.
    def a():
        out = check(repo("2.2.3"), real_shape)
        assert len(out) == 1, out
        assert "2.2.3" in out[0] and "2.2.2" in out[0], out
        assert "skill-craft@skill-craft-marketplace" in out[0], out
        assert "/release-plugin" in out[0], out
    case("a differ -> fires, both versions in the line", a)

    # (b) equal → silent. Same fixture pair as (a): the ONLY change is
    # the manifest version, so the difference is the predicate's doing.
    def b():
        out = check(repo("2.2.2"), real_shape)
        assert out == [], out
    case("b equal -> silent", b)

    # (c) no manifest → silent (not a plugin source repo).
    def c():
        out = check(repo(None), real_shape)
        assert out == [], out
    case("c no manifest -> silent", c)

    # (d) no pin entry for this name → silent (never installed here).
    def d():
        out = check(repo("2.2.3", name="never-installed"), real_shape)
        assert out == [], out
    case("d no pin entry -> silent", d)

    # (e) malformed pin file → silent, via main()'s fail-open. check()
    # itself raises (loudly, by design); the hook's contract is that
    # main() swallows it and prints nothing.
    def e():
        bad = pins("{not json")
        try:
            check(repo("2.2.3"), bad)
            raise AssertionError("check() should have raised")
        except json.JSONDecodeError:
            pass
        import io
        from contextlib import redirect_stdout
        old_stdin, old_pin = sys.stdin, globals()["PIN_PATH"]
        out = io.StringIO()
        try:
            sys.stdin = io.StringIO(json.dumps({"cwd": repo("2.2.3")}))
            globals()["PIN_PATH"] = bad
            with redirect_stdout(out):
                rc = main()
        finally:
            sys.stdin, globals()["PIN_PATH"] = old_stdin, old_pin
        assert rc == 0 and out.getvalue() == "", (rc, out.getvalue())
    case("e malformed pin file -> silent (main fail-open)", e)

    # Flat-repo layout resolves too (second MANIFEST_RELPATH).
    def f():
        out = check(repo("2.2.3", nested=False), real_shape)
        assert len(out) == 1, out
    case("f flat .claude-plugin layout resolves", f)

    print("\n".join(cases))
    print(f"plugin-release-owed: {len(cases) - failed} passed, {failed} "
          f"failed, 0 skipped")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    if "--test" in sys.argv:
        _test()
        sys.exit(0)
    sys.exit(main())
