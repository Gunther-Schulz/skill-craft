#!/usr/bin/env python3
"""Battery for register_lint.py — one planted positive and one clean
control per check, no exceptions.

Every tell pattern is exercised from its own table entry, so a pattern
added without an example fails collection rather than passing silently.

The module is loaded by PATH rather than imported, so REGISTER_LINT can
point the battery at a crippled copy of the tool. That override is what
makes the red-first proof runnable without editing the repo copy: each
mutant reddens only the checks it targets.

    REGISTER_LINT=<scratch>/mutant_no_tells.py python3 -m pytest -q
    REGISTER_LINT=<scratch>/mutant_no_caps.py  python3 -m pytest -q
"""

import importlib.util
import os
import pathlib
import sys

import pytest

TOOL = pathlib.Path(
    os.environ.get(
        "REGISTER_LINT", pathlib.Path(__file__).with_name("register_lint.py")
    )
)

_spec = importlib.util.spec_from_file_location("register_lint", TOOL)
rl = importlib.util.module_from_spec(_spec)
sys.modules["register_lint"] = rl
_spec.loader.exec_module(rl)


# A clean fixture: short imperative sentences, no tells, no em dashes.
CLEAN = """---
name: sample
description: A sample skill used as the lint's negative control.
---

# Sample

Read the manifest before editing. Commit by pathspec. Push nothing.

## Steps

1. Open the file named in the brief.
2. Run the battery. Paste its output.
3. Stop on a red result and report it.

```python
# Code blocks are excluded, so this long, dash-laden — line — with
# "curly" quotes and the word utilize must never raise a finding.
```
"""


def classes(text):
    findings, _ = rl.lint("f.md", text)
    return [f.check for f in findings]


def metrics(text):
    _, m = rl.lint("f.md", text)
    return m


# --- the shared negative control ------------------------------------


def test_clean_fixture_is_green():
    assert classes(CLEAN) == []


# --- calibration pin -------------------------------------------------
# The fixtures below plant literal counts taken from the 2026-09-13
# comparison band (0-5 em dashes, 7.9-18.7 words/sentence), never from
# the tool's own constants: a fixture derived from the value it grades
# moves with a mutant and stays green on the drift it exists to catch.


def test_thresholds_match_the_calibration_band():
    assert rl.EM_DASH_MAX == 5
    assert rl.WORDS_PER_SENT_MAX == 19.0


# --- check (a): em dashes -------------------------------------------

EM_DASH_POSITIVE = CLEAN + "\n" + "Split the work — then commit.\n" * 6
EM_DASH_AT_CAP = CLEAN + "\n" + "Split the work — then commit.\n" * 5


def test_em_dash_positive_goes_red():
    assert "em-dash" in classes(EM_DASH_POSITIVE)
    assert metrics(EM_DASH_POSITIVE)["em_dashes"] == 6


def test_em_dash_at_cap_stays_green():
    assert metrics(EM_DASH_AT_CAP)["em_dashes"] == 5
    assert "em-dash" not in classes(EM_DASH_AT_CAP)


def test_em_dash_control_clean_fixture():
    assert "em-dash" not in classes(CLEAN)
    assert metrics(CLEAN)["em_dashes"] == 0


# --- check (b): sentence density ------------------------------------

DENSE = (
    "# Dense\n\n"
    "The clause that carries the qualifier that carries the exception "
    "that the reader must hold in mind while parsing the rest of this "
    "sentence keeps going well past the point at which any reader would "
    "have to backtrack to recover the subject.\n"
)


def test_density_positive_goes_red():
    found = classes(DENSE)
    assert "sentence-density" in found
    assert metrics(DENSE)["mean"] > 19.0


def test_density_control_clean_fixture():
    assert "sentence-density" not in classes(CLEAN)
    assert metrics(CLEAN)["mean"] <= 18.7


# --- check (c): every tell pattern ----------------------------------


@pytest.mark.parametrize(
    "pattern_id,example",
    [(pid, example) for pid, _rx, example in rl.TELL_PATTERNS],
    ids=[pid for pid, _rx, _ex in rl.TELL_PATTERNS],
)
def test_every_tell_pattern_has_a_red_example(pattern_id, example):
    planted = f"# Planted\n\n{example}\n"
    assert f"tell:{pattern_id}" in classes(planted)


@pytest.mark.parametrize(
    "pattern_id",
    [pid for pid, _rx, _ex in rl.TELL_PATTERNS],
    ids=[pid for pid, _rx, _ex in rl.TELL_PATTERNS],
)
def test_every_tell_pattern_stays_green_on_clean(pattern_id):
    assert f"tell:{pattern_id}" not in classes(CLEAN)


# --- the quoted-span exemption (second-person only) ------------------
# The discriminating pair: the same words go red unquoted and green
# quoted, so the exemption is shown to act on quoting rather than on
# the words. The boundary case below fixes its reach: another tell
# inside quotes still fires.


def test_second_person_fires_unquoted():
    doc = "# T\n\nYou should read the manifest first.\n"
    assert "tell:second-person" in classes(doc)


def test_second_person_is_exempt_inside_double_quotes():
    doc = '# T\n\nThe template reads "You should read the manifest first".\n'
    assert "tell:second-person" not in classes(doc)


def test_second_person_is_exempt_inside_backticks():
    doc = "# T\n\nThe template reads `You should read the manifest first`.\n"
    assert "tell:second-person" not in classes(doc)


def test_other_tells_still_fire_inside_quotes():
    doc = '# T\n\nThe note says "delve into the manifest".\n'
    assert "tell:delve" in classes(doc)


def test_only_second_person_is_quote_exempt():
    assert rl.QUOTE_EXEMPT == {"second-person"}


def test_pattern_table_size_is_in_the_specified_band():
    assert 10 <= len(rl.TELL_PATTERNS) <= 20


def test_pattern_ids_are_unique():
    ids = [pid for pid, _rx, _ex in rl.TELL_PATTERNS]
    assert len(ids) == len(set(ids))


# --- exclusions ------------------------------------------------------


def test_frontmatter_is_excluded():
    doc = (
        "---\n"
        "description: You should utilize this — it delves — into things.\n"
        "---\n\n"
        "Read the file. Commit by pathspec.\n"
    )
    assert classes(doc) == []


def test_code_blocks_are_excluded():
    doc = "# T\n\nRead the file.\n\n```\nYou should delve — utilize — this.\n```\n"
    assert classes(doc) == []


def test_findings_carry_a_line_number():
    doc = "# T\n\nRead the file.\nYou should delve into it.\n"
    findings, _ = rl.lint("f.md", doc)
    assert findings, "expected at least one finding"
    assert all(isinstance(f.line, int) and f.line > 0 for f in findings)
    assert any(f.line == 4 for f in findings)


# --- CLI contract ----------------------------------------------------


def test_exit_zero_on_clean(tmp_path):
    p = tmp_path / "clean.md"
    p.write_text(CLEAN, encoding="utf-8")
    assert rl.main([str(p)]) == 0


def test_exit_one_on_findings(tmp_path):
    p = tmp_path / "dirty.md"
    p.write_text(DENSE, encoding="utf-8")
    assert rl.main([str(p)]) == 1


def test_exit_two_on_missing_file(tmp_path):
    assert rl.main([str(tmp_path / "nope.md")]) == 2


def test_exit_two_on_no_argument():
    assert rl.main([]) == 2


def test_json_output_is_parseable(tmp_path, capsys):
    import json

    p = tmp_path / "dirty.md"
    p.write_text(DENSE, encoding="utf-8")
    rl.main([str(p), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["caps"]["em_dashes"] == rl.EM_DASH_MAX
    assert payload["findings"]
