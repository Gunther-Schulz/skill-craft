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
    # DERIVED from the comparison report's own rows, never restated from
    # the tool: create-verification carried 5 em dashes in 936 words, and
    # it was the only pstack file with any, so the top of that band in
    # the rate unit is 5/936*1000. Writing 5.34 here instead would be the
    # fixture reading the value it grades.
    assert rl.EM_DASH_PER_1000_MAX == round(5 / 936 * 1000, 2)
    assert rl.WORDS_PER_SENT_MAX == 19.0
    assert rl.DEFAULT_BAND == rl.Band(19.0, rl.EM_DASH_PER_1000_MAX)


# --- check (a): em dashes -------------------------------------------

# The em-dash fixtures are DERIVED FROM THE BAND, not hardcoded at a
# dash count. Under the old absolute cap "at cap" meant five dashes in
# any file; under a rate it means a count relative to length, so a
# fixture pinned to a number stops testing the moment the band moves —
# which is exactly what happened to the pre-rate version of these two,
# and the battery caught it rather than passing vacuously.
DASH_LINE = "Split the work — then commit.\n"
FILLER_LINE = "The gate reads the index and returns.\n"


def _padded_to_rate(dash_lines, want_over):
    """CLEAN + `dash_lines` dash-carrying lines, padded with dash-free
    filler until the file's em-dash rate sits just OVER or just UNDER
    the default band's cap.

    Filler is short and dash-free so it moves the rate's denominator
    without touching the density or tell checks — a pad that tripped a
    second check would make the arm's red unattributable.
    """
    body = CLEAN + "\n" + DASH_LINE * dash_lines
    fill = 0
    while True:
        text = body + FILLER_LINE * fill
        rate = rl.lint("f.md", text)[1]["em_dashes_per_1000"]
        over = rate > rl.DEFAULT_BAND.em_per_1000
        if over == want_over:
            return text
        if not want_over and fill > 4000:
            raise AssertionError("padding never reached the band")
        fill += 1


EM_DASH_POSITIVE = _padded_to_rate(6, want_over=True)
EM_DASH_AT_CAP = _padded_to_rate(6, want_over=False)


def test_em_dash_fixtures_straddle_the_cap():
    """The fixtures' own arrangement proof: a planted case that could
    not fire returns exactly what a true negative returns, so both
    sides are shown to sit where the arm needs them BEFORE either
    verdict is read."""
    cap = rl.DEFAULT_BAND.em_per_1000
    assert metrics(EM_DASH_POSITIVE)["em_dashes_per_1000"] > cap
    assert metrics(EM_DASH_AT_CAP)["em_dashes_per_1000"] <= cap
    assert metrics(EM_DASH_POSITIVE)["em_dashes"] == \
        metrics(EM_DASH_AT_CAP)["em_dashes"]


def test_em_dash_positive_goes_red():
    assert "em-dash" in classes(EM_DASH_POSITIVE)


def test_em_dash_at_cap_stays_green():
    assert "em-dash" not in classes(EM_DASH_AT_CAP)


def test_em_dash_grades_the_rate_not_the_count():
    """THE PAIR THAT SEPARATES THE TWO SHAPES. Both fixtures carry the
    SAME number of em dashes and differ only in length, so an absolute
    per-file cap would return the same verdict for both. One goes red
    and one stays green, which no count-based predicate can produce —
    the arm dies if the check ever reverts to counting."""
    assert metrics(EM_DASH_POSITIVE)["em_dashes"] == \
        metrics(EM_DASH_AT_CAP)["em_dashes"]
    assert "em-dash" in classes(EM_DASH_POSITIVE)
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
    assert payload["caps"]["em_dashes_per_1000"] == rl.EM_DASH_PER_1000_MAX
    assert payload["findings"]


# --- check (e): the declared band ------------------------------------


def test_band_flag_overrides_the_default():
    """A corpus declares its own band at the invocation and is graded
    against THAT. The same bytes that fail the pstack default pass a
    band wide enough to hold them."""
    findings, _ = rl.lint("f.md", EM_DASH_POSITIVE)
    assert "em-dash" in {f.check for f in findings}
    wide, _ = rl.lint("f.md", EM_DASH_POSITIVE, rl.Band(19.0, 500.0))
    assert "em-dash" not in {f.check for f in wide}


def test_band_flag_still_fires_past_the_declared_band():
    """A declared band is a band, not an exemption: drift past what the
    corpus declared still fires. Without this arm a wide band would be
    indistinguishable from switching the check off."""
    narrow, _ = rl.lint("f.md", EM_DASH_AT_CAP, rl.Band(19.0, 0.0))
    assert "em-dash" in {f.check for f in narrow}


def test_band_reaches_the_density_half_too(tmp_path):
    p = tmp_path / "d.md"
    p.write_text(DENSE, encoding="utf-8")
    assert rl.main([str(p)]) == 1
    assert rl.main([str(p), "--band", "500", "500"]) == 0
    assert rl.main([str(p), "--band", "0", "500"]) == 2
    assert rl.main([str(p), "--band", "19"]) == 2


def test_default_band_preserves_every_skill_craft_verdict():
    """THE INVARIANCE ARM the recalibration owes.

    The em-dash check changed UNIT, so the default had to move with it,
    and a default chosen loosely would silently re-grade the corpus the
    tool ships inside. For each of skill-craft's own operational files
    the old predicate (absolute count over 5) and the new one (rate over
    the pstack-derived cap) must return the SAME verdict.

    This computes the old predicate here rather than importing the old
    build: the pre-change rule was `total > 5`, four tokens, and
    restating it is exact. The arm would be vacuous if every file were
    clean, so it asserts the population is non-trivial and that at
    least one file actually trips — a run over nothing reads exactly
    like a run that agreed.

    WHAT THIS ARM DOES NOT ESTABLISH, stated because an assurance
    wider than its predicate is what stops anyone looking. Every file
    in this set sits 2.6x to 6.0x ABOVE the cap (rates 13.9-32.2
    against 5.34), so any cap in [0, 13.88) returns these same
    verdicts. The arm therefore shows that NOTHING CROSSED ZERO on
    the real sample; it does not discriminate the cap's VALUE, and a
    wrong default anywhere under 13.88 would pass it unchanged. What
    pins the value is the derivation above
    (test_thresholds_match_the_calibration_band, read off the
    comparison report's own rows) plus the constructed boundary pair
    below — and a constructed case proves the arithmetic, never the
    sample. Both are needed and neither substitutes for the other.

    It also compares the em-dash finding's PRESENCE, not the finding
    line. The reported line is where the dash budget is crossed, and
    the budget is now length-relative, so that anchor legitimately
    moves: measured over this set it moved on 6 of 8 files while
    counts and check classes held. An arm written against exit codes
    alone would have called that "identical" — exit is two-valued, so
    findings can move inside the red set and never show.
    """
    import pathlib

    home = pathlib.Path(rl.__file__).resolve().parents[1] / "skills" / "skill-craft"
    files = sorted(home.glob("**/*.md"))
    assert len(files) >= 8, f"population collapsed to {len(files)}"

    tripped = 0
    for f in files:
        raw = f.read_text(encoding="utf-8")
        findings, m = rl.lint(str(f), raw)
        new_fires = "em-dash" in {x.check for x in findings}
        old_fires = m["em_dashes"] > 5          # the pre-rate predicate
        assert new_fires == old_fires, (
            f"{f.name}: verdict moved — old(count {m['em_dashes']}>5)"
            f"={old_fires}, new(rate {m['em_dashes_per_1000']:.1f}>"
            f"{rl.DEFAULT_BAND.em_per_1000})={new_fires}")
        tripped += new_fires
    assert tripped > 0, "no file tripped either predicate — arm is vacuous"


def test_cap_value_discriminates_at_the_boundary():
    """The arm the real sample cannot give: a CONSTRUCTED pair placed
    either side of the default cap.

    The invariance arm above runs over files 2.6x-6x past the cap, so
    it cannot tell a right default from a wrong one. This one can — it
    fails if the cap moves in either direction by more than the gap
    between the two fixtures. It proves the arithmetic and says
    nothing about whether 5.34 is the right band for any real corpus;
    that claim rests on the derivation from the pstack sample.
    """
    cap = rl.DEFAULT_BAND.em_per_1000
    head = "---\nname: s\ndescription: d\n---\n\n# S\n\n"
    filler = "The gate reads the index and returns.\n"

    def at(target_rate, dashes=3):
        """A body carrying `dashes` dashes at approximately `target_rate`."""
        words_needed = int(dashes / target_rate * 1000)
        body = head + "Split it — now.\n" * dashes
        while len(body.split()) < words_needed:
            body += filler
        return body

    just_under = at(cap * 0.8)
    just_over = at(cap * 1.25)
    assert "em-dash" not in {f.check for f in rl.lint("u.md", just_under)[0]}
    assert "em-dash" in {f.check for f in rl.lint("o.md", just_over)[0]}

    # ARRANGEMENT PROOF: both fixtures carry the same dash count and
    # differ only in length, so the pair is separable by a rate and by
    # nothing else. Without this, a pair that could not straddle the
    # cap would return exactly what a correct pair returns.
    assert rl.lint("u.md", just_under)[1]["em_dashes"] == \
        rl.lint("o.md", just_over)[1]["em_dashes"]
    assert rl.lint("u.md", just_under)[1]["em_dashes_per_1000"] < cap
    assert rl.lint("o.md", just_over)[1]["em_dashes_per_1000"] > cap
