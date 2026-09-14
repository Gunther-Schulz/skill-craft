#!/usr/bin/env python3
"""register_lint — mechanical register checker for skill markdown.

A CHECKER, not a rewriter: it flags and exits non-zero. It grades the
mechanical half of the prose-form discipline (SKILL.md, Prose form and
the authoring pipeline) — sentence density, em-dash load, and a list of
AI tells. The judgment half (does the pruned text still carry every
obligation) is the fresh-context clause-coverage diff, not this tool.

Checks
  em-dash          em dashes per 1000 words above the band's rate
  sentence-density file mean words-per-sentence above the band's cap
  tell:<id>        a line matching one of TELL_PATTERNS

Frontmatter and fenced code blocks are excluded from every check.

The BAND is the pair of caps a file is graded against. It defaults to
the pstack-derived values below and is overridden per corpus with
--band; the band is a property of the corpus, never of the tool, and
it is stated at the invocation rather than discovered from repo config
so the command that ran always shows what it graded against.

Output   <file>:<line>: <check>: <text>   (stdout)
Exit     0 = clean, 1 = findings, 2 = usage error.
"""

import argparse
import json
import re
import sys
import typing

# --- Thresholds -----------------------------------------------------
# Source: the 2026-09-13 skill-style comparison
# (statiker/dev-notes/skill-style-comparison-2026-09-13.md, Measurements).
# The pstack sample measured 7.9-18.7 words/sentence per file and 0-5 em
# dashes per file; the house sample measured 21.0-48.2 and 18-432. The
# DEFAULT band sits at the top of the pstack band, and --band overrides
# it per corpus.
#
# THE EM-DASH HALF IS A RATE, and that is a shape correction rather than
# a recalibration: an absolute per-file count is not comparable across
# files, because it rises with length while the property it stands for
# does not. Measured over the ethos corpus, the absolute count spreads
# 3.5x (28-98) while the rate holds inside 20.5-27.5 per 1000 words, so
# an absolute cap in any declared band either fires on that corpus's
# next long module or goes vacuous for its short ones.
#
# The default is DERIVED from the same pstack sample the old absolute 5
# came from, not chosen: create-verification carried 5 dashes in 936
# words = 5.34 per 1000, and it was the sample's only file with any. So
# 5.34 IS "the top of the pstack band" restated in the corrected unit,
# and every skill-craft file keeps the verdict it had (all eight fail
# both ways — rates 13.9-32.2, absolutes 16-97). That invariance is a
# battery arm, not a claim.
WORDS_PER_SENT_MAX = 19.0
EM_DASH_PER_1000_MAX = 5.34


class Band(typing.NamedTuple):
    """The two caps a corpus is graded against.

    Passed explicitly from main() down to each check rather than read
    off module globals: a --band that mutated the globals would leave
    the caps keyed to whatever ran last, and a battery arm that set
    them would grade the fixture instead of the build.
    """

    words_per_sent: float
    em_per_1000: float


DEFAULT_BAND = Band(WORDS_PER_SENT_MAX, EM_DASH_PER_1000_MAX)

# --- Tell patterns --------------------------------------------------
# (id, regex, example). The example is the battery's planted positive:
# test_register_lint.py asserts every entry's example fires its own id,
# so a pattern cannot enter this table without a red-proven fixture.
TELL_PATTERNS = [
    (
        "hedge-stack",
        r"\b(?:could|may|might|can)\s+(?:potentially|possibly|perhaps|conceivably)\b",
        "This could potentially break the build.",
    ),
    (
        "delve",
        r"\bdelv(?:e|es|ed|ing)\b",
        "Delve into the configuration before editing.",
    ),
    (
        "worth-noting",
        r"\b(?:it(?:'s|\s+is)\s+worth\s+noting|it\s+is\s+important\s+to\s+note|"
        r"it\s+should\s+be\s+noted)\b",
        "It is worth noting that the cache resolves at start.",
    ),
    (
        "epoch-opener",
        r"\bin\s+(?:today's|an?\s+increasingly|the\s+ever[-\s]evolving|"
        r"the\s+fast[-\s]paced)\b",
        "In today's fast-paced release cycle, tests matter.",
    ),
    (
        "intensifier-stack",
        r"\b(?:very|really|extremely|incredibly|highly|truly)\s+"
        r"(?:very|really|extremely|incredibly|highly|truly|significantly|important)\b",
        "The gate is really very important here.",
    ),
    (
        "ai-vocab",
        r"\b(?:crucial|pivotal|tapestry|testament|vibrant|garner|showcase|"
        r"myriad|realm|holistic|synerg(?:y|ies|istic))\b",
        "The manifest is a testament to careful packaging.",
    ),
    (
        "fancy-is",
        r"\b(?:serves\s+as|stands\s+as|boasts|acts\s+as\s+a)\b",
        "The hook serves as the enforcement point.",
    ),
    (
        "not-just-but",
        r"\bnot\s+(?:just|only|merely)\b[^.!?\n]{1,60}\bbut\b",
        "The lint is not just a formatter but a gate.",
    ),
    (
        "superficial-ing",
        r",\s+(?:highlighting|ensuring|showcasing|fostering|reflecting|"
        r"underscoring|emphasizing|enabling)\b",
        "The battery runs first, ensuring the check is red.",
    ),
    (
        "vague-attribution",
        r"\b(?:experts\s+(?:believe|agree|say)|studies\s+show|"
        r"research\s+suggests|industry\s+reports|some\s+would\s+argue|"
        r"it\s+is\s+widely\s+(?:believed|accepted))\b",
        "Studies show that shorter sentences read faster.",
    ),
    (
        "chatbot",
        r"(?:\bI\s+hope\s+this\s+helps|\bLet\s+me\s+know\s+if\b|"
        r"\bOf\s+course!|\bCertainly!|\bGreat\s+question)",
        "Let me know if the release step fails.",
    ),
    (
        "filler",
        r"\b(?:in\s+order\s+to|due\s+to\s+the\s+fact\s+that|"
        r"at\s+the\s+end\s+of\s+the\s+day|when\s+it\s+comes\s+to|"
        r"for\s+all\s+intents\s+and\s+purposes)\b",
        "Run the battery in order to prove the check.",
    ),
    (
        "generic-conclusion",
        r"\b(?:the\s+future\s+looks|game[-\s]changer|paradigm\s+shift|"
        r"revolutioniz(?:e|es|ing)|take\s+it\s+to\s+the\s+next\s+level)\b",
        "This release is a game-changer for the corpus.",
    ),
    (
        "plain-word",
        r"\b(?:utiliz(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|"
        r"numerous|in\s+the\s+event\s+that|commence(?:s|d)?|"
        r"leverag(?:e|es|ed|ing))\b",
        "Utilize the pathspec form to commit.",
    ),
    (
        "sycophantic",
        r"\b(?:you(?:'re|\s+are)\s+absolutely\s+right|great\s+point|"
        r"excellent\s+question|happy\s+to\s+help)\b",
        "Great point, the gate does fire there.",
    ),
    (
        "second-person",
        r"\b(?:you\s+should|you'll\s+want\s+to|you\s+can\s+simply|"
        r"you\s+may\s+wish\s+to|feel\s+free\s+to)\b",
        "You should read the manifest first.",
    ),
    (
        "curly-quote",
        r"[‘’“”]",
        "The rule calls it a “gate”.",
    ),
    (
        "emoji-heading",
        r"^#{1,6}\s.*[\U0001F300-\U0001FAFF✅❌✨⚠⭐]",
        "## Release checklist \U0001F680",
    ),
]

SENTENCE_END = re.compile(r"[.!?](?=\s|$)")
FENCE = re.compile(r"^\s*(?:```|~~~)")
EM_DASH = "—"

# Patterns exempt inside a quoted span. Scoped to second-person only:
# a skill quotes user-facing output and speech, where second person is
# correct (SKILL.md, Imperative form). Every other tell still fires in
# quotes, because quoting a tell does not stop it being one.
QUOTE_EXEMPT = {"second-person"}
QUOTED_SPAN = re.compile(r"`[^`\n]*`|\"[^\"\n]*\"|“[^”\n]*”")


class Finding:
    def __init__(self, path, line, check, text):
        self.path = path
        self.line = line
        self.check = check
        self.text = text

    def __str__(self):
        return f"{self.path}:{self.line}: {self.check}: {self.text}"

    def as_dict(self):
        return {"line": self.line, "check": self.check, "text": self.text}


def body_lines(raw):
    """Return [(lineno, text)] with frontmatter and fenced code removed."""
    lines = raw.split("\n")
    out = []
    i = 0
    # frontmatter: a --- fence on line 1 closing on a later ---
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break
    in_fence = False
    while i < len(lines):
        text = lines[i]
        if FENCE.match(text):
            in_fence = not in_fence
            i += 1
            continue
        if not in_fence:
            out.append((i + 1, text))
        i += 1
    return out


def check_em_dash(path, body, words, band=DEFAULT_BAND):
    """One finding at the line carrying the em dash that crosses the cap.

    `words` is the body word count the density check reports, reused
    here so the rate's denominator is the same number the output names
    — a rate whose divisor nobody can see is not checkable from the
    report.

    A file under 1000 words is graded on its own rate, not exempted:
    the cap is per 1000 words, and a 300-word file carrying 4 dashes is
    at 13.3 and over any pstack-derived band. Zero words yields no
    finding, because the rate is undefined rather than infinite — the
    could-not-verify case, and an empty body has no prose to grade.
    """
    findings = []
    total = 0
    overflow_line = None
    budget = band.em_per_1000 * words / 1000.0 if words else None
    for lineno, text in body:
        n = text.count(EM_DASH)
        if n and overflow_line is None and budget is not None \
                and total + n > budget:
            overflow_line = lineno
        total += n
    rate = (total / words * 1000.0) if words else 0.0
    if budget is not None and total > budget:
        findings.append(
            Finding(
                path,
                overflow_line,
                "em-dash",
                f"{rate:.1f} em dashes per 1000 words, cap "
                f"{band.em_per_1000:.1f} ({total} dashes in {words} words)",
            )
        )
    return findings, total, rate


def split_sentences(body):
    """Join body lines, split on sentence enders, keep a start line each.

    Mirrors the comparison report's crude instrument (words divided by
    count of [.!?] followed by whitespace) so the calibration band
    transfers, and adds the start line so a finding can be located.
    """
    pieces = []
    offset_map = []  # (char_offset, lineno) at each line start
    buf = []
    pos = 0
    for lineno, text in body:
        offset_map.append((pos, lineno))
        buf.append(text)
        pos += len(text) + 1
    joined = "\n".join(buf)

    def line_of(offset):
        found = offset_map[0][1] if offset_map else 1
        for start, lineno in offset_map:
            if start <= offset:
                found = lineno
            else:
                break
        return found

    start = 0
    for m in SENTENCE_END.finditer(joined):
        end = m.end()
        chunk = joined[start:end]
        if chunk.strip():
            pieces.append((line_of(start + len(chunk) - len(chunk.lstrip())), chunk))
        start = end
    tail = joined[start:]
    if tail.strip():
        pieces.append((line_of(start + len(tail) - len(tail.lstrip())), tail))
    return pieces


def check_density(path, body, band=DEFAULT_BAND):
    sentences = split_sentences(body)
    words = sum(len(text.split()) for _, text in sentences)
    count = max(len(sentences), 1)
    mean = words / count
    findings = []
    if mean > band.words_per_sent:
        worst_line, worst = 1, ""
        for lineno, text in sentences:
            if len(text.split()) > len(worst.split()):
                worst_line, worst = lineno, text
        findings.append(
            Finding(
                path,
                worst_line,
                "sentence-density",
                f"file mean {mean:.1f} words/sentence, cap "
                f"{band.words_per_sent:.1f} (longest sentence here: "
                f"{len(worst.split())} words)",
            )
        )
    return findings, {"words": words, "sentences": len(sentences), "mean": mean}


def check_tells(path, body):
    findings = []
    for pattern_id, pattern, _example in TELL_PATTERNS:
        rx = re.compile(pattern, re.IGNORECASE)
        exempt = pattern_id in QUOTE_EXEMPT
        for lineno, text in body:
            subject = (
                QUOTED_SPAN.sub(lambda m: " " * len(m.group(0)), text)
                if exempt
                else text
            )
            m = rx.search(subject)
            if m:
                findings.append(
                    Finding(path, lineno, f"tell:{pattern_id}", repr(m.group(0)))
                )
    return findings


def lint(path, raw, band=DEFAULT_BAND):
    body = body_lines(raw)
    # Density runs FIRST: it owns the word count, and the em-dash rate
    # divides by that same number rather than recounting. Two counts of
    # "the words in this file" would drift apart on the first change to
    # either, and the report would name one while the verdict used the
    # other.
    density_findings, metrics = check_density(path, body, band)
    dash_findings, dash_total, dash_rate = check_em_dash(
        path, body, metrics["words"], band)
    tell_findings = check_tells(path, body)
    findings = dash_findings + density_findings + tell_findings
    findings.sort(key=lambda f: (f.line, f.check))
    metrics["em_dashes"] = dash_total
    metrics["em_dashes_per_1000"] = dash_rate
    return findings, metrics


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="register_lint.py",
        description="Grade one markdown file against the prose-form discipline.",
    )
    parser.add_argument("file", help="markdown file to lint")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--band",
        nargs=2,
        type=float,
        metavar=("WORDS_PER_SENT", "EM_DASHES_PER_1000W"),
        help="the band THIS corpus is graded against, overriding the "
             "pstack-derived default. The band is a property of the "
             "corpus, not of the tool: a corpus whose idiom is "
             "deliberately dense declares its own and is graded against "
             "it, while drift past that band still fires. Stated at the "
             "invocation by the corpus that owns it — this tool reads no "
             "repo config, so the band is always visible in the command "
             "that ran.",
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    band = DEFAULT_BAND if args.band is None else Band(*args.band)
    if band.words_per_sent <= 0 or band.em_per_1000 < 0:
        print(
            "register_lint: --band takes a positive words/sentence and a "
            "non-negative em-dashes/1000w",
            file=sys.stderr,
        )
        return 2
    try:
        with open(args.file, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"register_lint: cannot read {args.file}: {exc}", file=sys.stderr)
        return 2

    findings, metrics = lint(args.file, raw, band)
    if args.json:
        print(
            json.dumps(
                {
                    "file": args.file,
                    "findings": [f.as_dict() for f in findings],
                    "metrics": {
                        "em_dashes": metrics["em_dashes"],
                        "em_dashes_per_1000": round(
                            metrics["em_dashes_per_1000"], 2),
                        "words": metrics["words"],
                        "sentences": metrics["sentences"],
                        "mean_words_per_sentence": round(metrics["mean"], 2),
                    },
                    "caps": {
                        "em_dashes_per_1000": band.em_per_1000,
                        "words_per_sentence": band.words_per_sent,
                    },
                },
                indent=2,
            )
        )
    else:
        for finding in findings:
            print(finding)
        print(
            f"{args.file}: {len(findings)} finding(s); "
            f"{metrics['em_dashes']} em dashes "
            f"({metrics['em_dashes_per_1000']:.1f}/1000w); "
            f"{metrics['mean']:.1f} words/sentence over "
            f"{metrics['sentences']} sentences",
            file=sys.stderr,
        )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
