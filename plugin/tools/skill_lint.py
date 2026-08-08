#!/usr/bin/env python3
"""skill-lint — mechanical pre-release checker for skill files.

A CHECKER, not a formatter: it flags and exits non-zero. The single
auto-fix is trailing whitespace, and only under an explicit --fix.
Prose reflow is never automated — it silently corrupts quoted blocks,
list continuations and inline templates.

Checks
  wrap         line longer than 72 columns, minus the unbreakable
               whitelist (frontmatter, fenced code, table rows, and
               lines whose longest single token already overflows)
  trailing-ws  trailing space or tab (auto-fixable with --fix)
  dead-cite    a parenthetical naming a section, e.g. "(The attack)",
               that resolves to no heading in the same file
  singleton    WARN-only: a backticked term used exactly once in the
               file — an undefined-at-point-of-use candidate. False
               fires are expected; --diff-base narrows it to terms
               the diff introduces.

Output   <file>:<line>: <check>: <text>   (stdout; summary on stderr)
Exit     0 = clean, or warnings only.  1 = blocking findings.
"""

import argparse
import os
import re
import subprocess
import sys

MAX_WIDTH = 72
BLOCKING = ("wrap", "trailing-ws", "dead-cite")

CODE_SPAN = re.compile(r"`([^`\n]+)`")
PARENTHETICAL = re.compile(r"\(([^()]{2,60})\)")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
TRAILING_PAREN = re.compile(r"\s*\([^()]*\)\s*$")
CITE_FORBIDDEN = set(";:!?`|=/\\<>[]{}#*.")


class Finding:
    def __init__(self, path, line, check, text):
        self.path = path
        self.line = line
        self.check = check
        self.text = text

    def __str__(self):
        return f"{self.path}:{self.line}: {self.check}: {self.text}"

    @property
    def blocking(self):
        return self.check in BLOCKING


def scan_structure(lines):
    """Classify each line: in frontmatter, in a fenced block."""
    fm = [False] * len(lines)
    fence = [False] * len(lines)
    i = 0
    if lines and lines[0].strip() == "---":
        fm[0] = True
        i = 1
        while i < len(lines):
            fm[i] = True
            if lines[i].strip() == "---":
                i += 1
                break
            i += 1
    in_fence = False
    for n in range(i, len(lines)):
        if lines[n].lstrip().startswith("```"):
            fence[n] = True
            in_fence = not in_fence
            continue
        fence[n] = in_fence
    return fm, fence


def unbreakable(line):
    """True when no rewrap could bring the line under the limit.

    A path template, URL or other whitespace-free literal that already
    overflows on its own is not the author's to fix.
    """
    indent = len(line) - len(line.lstrip())
    longest = max((len(tok) for tok in line.split()), default=0)
    return indent + longest > MAX_WIDTH


def check_wrap(path, lines, fm, fence, out):
    for n, line in enumerate(lines):
        if len(line) <= MAX_WIDTH:
            continue
        if fm[n] or fence[n]:
            continue
        if line.lstrip().startswith("|"):  # markdown table row
            continue
        if unbreakable(line):
            continue
        out.append(Finding(path, n + 1, "wrap",
                           f"{len(line)} cols (limit {MAX_WIDTH}): "
                           f"{line.strip()[:60]}"))


def check_trailing(path, lines, out, fix):
    hits = []
    for n, line in enumerate(lines):
        if line != line.rstrip():
            hits.append(n)
    for n in hits:
        state = "fixed" if fix else "trailing whitespace"
        out.append(Finding(path, n + 1, "trailing-ws", state))
    if fix and hits:
        return [line.rstrip() for line in lines]
    return None


def headings(lines, fence):
    """Normalized heading forms, full and minus a trailing parenthetical."""
    forms = []
    for n, line in enumerate(lines):
        if fence[n]:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        full = normalize(m.group(1))
        forms.append(full)
        short = normalize(TRAILING_PAREN.sub("", m.group(1)))
        if short and short != full:
            forms.append(short)
    return [f for f in forms if f]


def normalize(text):
    text = text.replace("`", "").replace("*", "").replace("_", "")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text.rstrip(".:,;")


def cite_candidate(content):
    """A parenthetical that reads as a section cite, not as prose.

    Deliberately narrow: the check blocks, so a false fire costs more
    than a miss. Excluded are all-caps identifiers, filenames and
    paths, anything sentence-punctuated, and anything over six words.
    """
    c = content.strip()
    if not c or not c[0].isupper():
        return None
    if not any(ch.islower() for ch in c):
        return None  # ALL_CAPS identifier, e.g. (USAGE_ERROR)
    if any(ch in CITE_FORBIDDEN for ch in c):
        return None  # backtick catches cross-file cites: (Heading, `file.md`)
    words = c.split()
    if len(words) > 6:
        return None
    if any(len(w) == 1 and w.isupper() for w in words):
        return None  # placeholder prose, e.g. (A invokes B, B invokes C)
    lead = re.match(r"[A-Za-z]+", words[0]).group(0)
    if len(lead) > 1 and lead.isupper():
        return None  # acronym-initial prose, e.g. (AI-attribution trailer)
    head = c.split(",")[0].strip()
    return normalize(head) or None


def check_cites(path, lines, fm, fence, out):
    forms = headings(lines, fence)
    for n, line in enumerate(lines):
        if fm[n] or fence[n] or line.lstrip().startswith("#"):
            continue
        for m in PARENTHETICAL.finditer(line):
            cand = cite_candidate(m.group(1))
            if not cand:
                continue
            if any(h.startswith(cand) or cand.startswith(h) for h in forms):
                continue
            out.append(Finding(path, n + 1, "dead-cite",
                               f"({m.group(1)}) matches no heading here"))


def terms(lines, fm, fence):
    """Backticked terms -> [line numbers], outside frontmatter and fences."""
    found = {}
    for n, line in enumerate(lines):
        if fm[n] or fence[n]:
            continue
        for m in CODE_SPAN.finditer(line):
            t = m.group(1).strip()
            if len(t) < 3 or not any(ch.isalnum() for ch in t):
                continue
            found.setdefault(t, []).append(n + 1)
    return found


def base_terms(path, ref):
    """Terms in the file at `ref`; None when the blob cannot be read."""
    repo = os.path.dirname(os.path.abspath(path)) or "."
    try:
        top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        root = top.stdout.strip()
        rel = os.path.relpath(os.path.abspath(path), root)
        blob = subprocess.run(["git", "-C", root, "show", f"{ref}:{rel}"],
                              capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, OSError):
        return None
    lines = blob.stdout.split("\n")
    fm, fence = scan_structure(lines)
    return set(terms(lines, fm, fence))


def check_singletons(path, lines, fm, fence, out, diff_base):
    known = None
    if diff_base:
        known = base_terms(path, diff_base)
        if known is None:
            print(f"{path}: --diff-base {diff_base}: no blob, "
                  "reporting all singletons", file=sys.stderr)
    for term, where in sorted(terms(lines, fm, fence).items()):
        if len(where) != 1:
            continue
        if known is not None and term in known:
            continue
        out.append(Finding(path, where[0], "singleton",
                           f"WARN `{term}` used once — defined at use?"))


def lint(path, fix, diff_base):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    lines = raw.split("\n")
    fm, fence = scan_structure(lines)

    out = []
    check_wrap(path, lines, fm, fence, out)
    fixed = check_trailing(path, lines, out, fix)
    check_cites(path, lines, fm, fence, out)
    check_singletons(path, lines, fm, fence, out, diff_base)

    if fixed is not None:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(fixed))
    return sorted(out, key=lambda f: (f.line, f.check))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Mechanical pre-release checker for skill files.")
    ap.add_argument("files", nargs="+", metavar="FILE")
    ap.add_argument("--fix", action="store_true",
                    help="strip trailing whitespace in place (the only fix)")
    ap.add_argument("--diff-base", metavar="REF",
                    help="report singleton terms only when absent at REF")
    args = ap.parse_args(argv)

    findings = []
    for path in args.files:
        if not os.path.isfile(path):
            print(f"{path}:0: read: not a file", file=sys.stderr)
            return 1
        findings.extend(lint(path, args.fix, args.diff_base))

    for f in findings:
        print(f)

    counts = {}
    for f in findings:
        counts[f.check] = counts.get(f.check, 0) + 1
    blocking = sum(1 for f in findings if f.blocking and
                   not (args.fix and f.check == "trailing-ws"))
    tally = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"
    print(f"skill-lint: {len(args.files)} file(s); {tally}; "
          f"blocking={blocking}", file=sys.stderr)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
