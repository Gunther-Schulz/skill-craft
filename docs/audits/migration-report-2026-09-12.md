# Migration report — BACKLOG.md → ITEMS.md (2026-09-12)

Produced by `lifecycle migrate`. **A DRY RUN**: the source carriers `BACKLOG.md` and `NONE` were READ. They are not edited, not moved and not deleted, and retiring them is a separate act after a human has read this file.

This report DESCRIBES entries — line number, grade word, rule applied. It does not quote their prose.

## The sources this run read, PINNED BY BLOB

The git blob sha of every source, so a later run can tell whether it is looking at the same file. **A re-run whose report already records a DIFFERENT sha answers COULD NOT VERIFY** and writes nothing: a second answer over a third file is indistinguishable from the first one, and every record pointer below already points into the blob named here. Reproduce with `git hash-object <file>`.

source-blob: 143262c12a7fdca093c320f6c91a16f78200b388  (BACKLOG.md)

done-blob: NONE  (NONE)

A report carrying NO blob line predates this check, and an absent record is not a mismatch — it is an unpinned run, which this build says rather than treating as agreement. An absent line FOR ONE PATH is the same answer at source granularity: that carrier has not been migrated into these homes, which is a first migration for it and not a moved source.

## Reconciliation

| quantity | count |
|---|---|
| top-level bullets in `BACKLOG.md` | 13 |
| of those, ENTRIES (bold, or led by a grade-shaped word) | 13 |
| of those, non-entry prose bullets (not migrated) | 0 |
| of those, bullets in a section §4 row 1 CUTS | 0 |
| items written to `ITEMS.md` | 4 |
| of those, CLOSURES routed to `ITEMS-DONE.md` instead | 9 |
| entries reported UNCLASSIFIED or AMBIGUOUS (not written) | 0 |
| archive bodies in `ITEMS-DONE.md` (verbatim) | 9 |
| entries routed to the ledger | 0 |
| RESIDUE items booked (`tend`, from no source entry) | 1 |

**Identity:** 13 entries read = 4 written + 9 closed + 0 unclassified — HOLDS. THREE columns, not two: a closure read out of the source carrier is neither written as an item nor unclassified, and folding it into either would make one of those numbers say something it does not.

**Bullet identity:** 13 top-level bullets = 13 entries + 0 prose + 0 cut — HOLDS. This is the identity that makes 'not migrated' visible: every bullet in the source is in exactly one of the three columns, so a bullet the migration simply did not see would show up as a gap in the sum rather than as nothing at all.

**Conservation (§3.1), computed on the produced files:** items 5 (of which 1 residue) + done 9 = 14; baseline 14 + added 0 − compacted 0 = 14. HOLDS. THE RESIDUE IS IN THIS IDENTITY AND NOT IN THE ONE ABOVE, and the split is the point: a residue item is a BODY in the carrier, so conservation must see it, and it comes from no SOURCE ENTRY, so the reconciliation identity must not — folding it in there would answer COULD NOT VERIFY on every migration after this one.

The bullet count and the archive count use DIFFERENT notions of an entry, deliberately and not accidentally: the archive count is `items_mod.archive_entries`, every line opening `- ` in the archived body, which is the notion the conservation identity uses on both sides of the migration. The entry count above is the migration's own notion. Where the two differ over the same file, the difference is sub-bullets at column zero and is not a lost body.

## The MIGRATION WRITE-RULES (§3.1, blocking and fixed)

**No migrated entry inherits READY.** READY is the desk's judgment that a fresh context could execute an item now, made about a carrier that no longer exists. Every entry below is written NEW.

**Every migrated OPEN entry carries a TYPED blocker.** The typing is the rule, not a detail: "every migrated item is blocked" is satisfied by prose, and prose sits in nobody's court — which is the entry that ages out silently. The three branches:

| branch | blocker | why |
|---|---|---|
| old READY / RECORD | `decision` | the grade returns to the desk for a re-grade; it is not inherited |
| PARKED carrying its named missing evidence | `evidence` | it is already in the MACHINE's court, and converting it to a decision would move a waiting item into the operator's queue for no reason |
| slot-incomplete (everything else) | `decision` | NEW with a decision naming what the desk must supply — never `NONE` |

**Blockers written, PER TYPE.** A total is the number that hides the untyped one, so there is no total here:

| blocker type | entries |
|---|---|
| `decision` | 3 |
| `evidence` | 1 |
| `item-id` | 0 |
| `NONE` | 0 |
| `untyped` | 0 |

`untyped` and `NONE` are both **0**, and either being non-zero is a finding rather than a statistic. Under the closed goal vocabulary nearly every migrated open item is slot-incomplete anyway, so the `decision` count will LOOK like "all" — which is precisely why the criterion is stated per type.

**The done home holds no blocker.** The write-rules are about OPEN items; a blocker in the closure home is a shape finding, not a migration output. This migration writes nothing into the done home but the verbatim archive, so the property holds by construction — and it is CHECKED by the done home's own shape check rather than assumed.

## What a CLOSED entry is (lc-18, lc-19, lc-21)

A source carrier states a closure in three shapes, and this run read all three. A closure written back into the open carrier is the one migration defect that is SILENT — the entry lands looking exactly like work nobody has started.

| shape | disposition |
|---|---|
| a CLOSURE GRADE WORD at the bullet start (`DONE`, `DROPPED`) | archived verbatim to the done home |
| an entry under the carrier's own CLOSURE HEADING | archived verbatim to the done home |
| a closure word standing alone LATER in an ungraded title | **REFUSED** — reported, never written either way |
| an OPEN grade word under the closure heading | **REFUSED** — the word says open and the section says closed |

**Closure heading(s) read:** `## Done` — the source carrier declares no `Closure-home:`, so the default in-carrier closure heading applies: `## Done`.

The heading is stated rather than assumed because the two failures look identical from outside: "no entry sat under a closure heading" and "this run looked under a heading this carrier does not use" both produce a zero here.

**The SECTION decides before the TITLE does, and the order is the rule.** An ungraded entry under a closure heading carries no grade word precisely BECAUSE the heading already said it. Scanning its title for a closure word first would refuse every one of them as ambiguous — a guard firing on legitimate work, which is the repair that trains a reader to discount the warning that will one day be real.

**A date-led bullet with no grade word — `2026-08-23 — title` — is the same precedence, admitted under this same rule.** It is neither bold at the start nor grade-word-led, so outside a closure heading it reads as prose; under one it is the heading's own idiom for a closed entry and archives verbatim like any other (lc-72).

**Closure bodies are archived VERBATIM, at a named line range, and are never re-rendered as items.** A closure's body is the author's own record of what closed and why; re-rendering it into slots would be a paraphrase of a body nobody reads twice. This is a DRY RUN, so the source in `BACKLOG.md` is untouched and the range still resolves.

## Grade-word rules (design §4 row 1, §3.1)

These classify the SOURCE word — which entries are entries, which are closures, and which are unclassifiable. An OPEN grade is then overridden to NEW by the write-rules above; the mapping is kept because it decides UNCLASSIFIED, and because a reader needs to see which word each entry carried.

| source grade word | §4 row 1 says | after the §3.1 write-rules |
|---|---|---|
| `READY` | READY | NEW — §4 row 1: READY→READY (scheduled by cap/head-rule at read time, not by this migration) |
| `RECORD` | READY | NEW — §4 row 1: RECORD→READY-unscheduled; §3.1: the rest are READY and visible, not a separate word |
| `PARKED` | NEW | NEW — §4 row 1: PARKED→PARKED with a typed blocker, or NEW |
| `HANDOFF` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `OPEN` | NEW | NEW — §4 row 1 and §3.1: OPEN→NEW |
| `BUST` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `PARTLY` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `CANDIDATE` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `FINDING` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `NEW` | NEW | NEW — §4 row 1: →NEW with a typed blocker or DROPPED |
| `POINTER` | NEW | NEW — §3.1: POINTER → an item whose body lives elsewhere, referenced |
| `DONE` | DONE | **CLOSED** — §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry |
| `DROPPED` | DROPPED | **CLOSED** — §3.1: `DROPPED` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open carrier, and it never inherits a grade the source did not carry |
| (ungraded) | NEW | NEW — §4 row 1: ungraded → NEW with a typed blocker or DROPPED |
| (ungraded, under a closure heading) | — | **CLOSED** — §4 row 1 + lc-18: ungraded, under the carrier's own closure heading — the heading is the closure statement, and the body is archived verbatim |
| anything else | — | **UNCLASSIFIED**, reported with its grade word and line number (D-f). Never guessed. |

## Outcome per class

| source grade word | → | entries |
|---|---|---|
| `DONE` | CLOSED → the done home | 8 |
| `PARKED` | NEW | 4 |
| `DROPPED` | CLOSED → the done home | 1 |

## Entries by source section

| section | entries |
|---|---|
| Backlog — skill-craft | 1 |
| Parked — review-regime section (draft-attack-before-release) | 3 |
| Done (moved here at closure, with the ref) | 9 |
| Kämmung passes | 0 |

## Closures routed to the done home

9 entry/ies. Each body is in `ITEMS-DONE.md` VERBATIM, under the archive heading, preceded by a comment naming its source line range and the rule that routed it.

| line | source grade word | section | rule |
|---|---|---|---|
| `BACKLOG.md:104-106` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:107-109` | `DROPPED` | Done (moved here at closure, with the re | §3.1: `DROPPED` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the op |
| `BACKLOG.md:110-113` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:114-117` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:118-121` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:122-124` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:125-127` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:128-130` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |
| `BACKLOG.md:131-137` | `DONE` | Done (moved here at closure, with the re | §3.1: `DONE` is the closed vocabulary's own word — a closure MOVES to the done home; it never enters the open  |

## UNCLASSIFIED and AMBIGUOUS — findings for the desk

**None — zero.** Every entry read matched a rule or a closure shape.

## What this migration does NOT carry, named rather than discovered

- **`goal`, `done-criterion` and `evidence` have no rule in §4 row 1.** Only the write-set does ("write-set absent → UNKNOWN"). A slot cannot be empty, so `goal` and `done-criterion` are written `UNKNOWN` at the same width the design gives the write-set, and `evidence` carries the source line range in `BACKLOG.md`. The design gap is reported, not closed here.
- **The PARKED branch of §4 row 1 is unreachable over this carrier.** "PARKED→PARKED with a typed blocker or NEW" turns on a typed blocker, and the old carrier has no blocker slot; no rule in the design derives one from a body. Every PARKED entry therefore takes the NEW branch, and the parked-ness — which court the item waits in — is not carried across. That is the largest single information loss in this migration and it is a decision for the desk, not for the tool.
- **A NARRATIVE section's bold bullets migrate as items, because §4 row 1 states no rule that stops them.** The rule list covers grade words and "ungraded", and a handoff paragraph's bullet is ungraded — so it becomes a NEW item. Only `## Grades` is CUT by name. The per-section table above is where this is visible: a section whose heading is a status narrative rather than a queue contributed entries, and whether that is wanted is the desk's call, not a rule this tool may invent.
- **Live entry BODIES are not carried.** An item's slots are one line each; the old entries are paragraphs. In this DRY RUN the bodies stay in `BACKLOG.md`, and git keeps them either way — but a later act that retires the old carrier drops them to history, and that is worth deciding rather than discovering.

## The migration's own RESIDUE, booked as `tend` items (§3.1b)

A migration leaves consumers of the OLD carrier still pointing at it, and nobody is scheduled to notice — the assumed-delivery class, where a write with no committing actor ACCUMULATES and the only detector is a count of what piled up. The migration is the one party that knows its residue exists at the moment it creates it, so it books it: a `tend` item (the plugin-reserved meta-goal — self-work advances no DOMAIN goal and could not otherwise be booked at all), PARKED on the decision "every consumer migrated or declared exempt".

**3 tracked file(s)** still name `BACKLOG.md` — one item, its `write-set` and `evidence` naming every one of them:

- `CLAUDE.md`
- `LEDGER.md`
- `dev-notes/OBSERVATIONS.md`

SEARCHED: the files git TRACKS (`git grep -l -I -F` over the work tree), fixed-string so a `.` in a basename cannot match any character. EXCLUDED: the source carriers, the successor homes and this report — each of which names the old carrier by construction, so a search without those exclusions would book a residue item for the migration's own output in every repo it ever ran in. An UNTRACKED file naming the carrier is out of scope: it is not a consumer the migration broke.

**What is NOT booked here, each for a stated reason.** The frozen ARCHIVE rides the `done bodies` kind's declared COMPACTION exit (the retire lane, R20/R22) — R22 withdrew every size cap, so there is no line-count tripwire in this system and none is invented here; booking it would re-add a banned cap and double the retire lane. The un-decomposed METHOD FILE rides the FILE SWEEP (§4): no universal marker exists for a tool to key on. No class is claimed twice.

## Where these findings WENT (R3)

**A finding in an audit nobody routes is a finding nobody acts on.** §3.8c bullet 8 sends this report's findings into the carrier as ITEMS via intake, and has the report point at the item ids rather than carrying the findings itself. The table below is READ FROM THE CARRIER at report time — items whose `evidence` slot cites this file — so it cannot go stale against it, and an empty table means the routing has not happened rather than that there was nothing to route.

**None yet.** On the FIRST run of a migration this is expected and says so: the items are added after the report exists, and `lifecycle migrate --report-only` re-renders this section once they do. On any later run an empty table is the finding.

## Ledger

`LEDGER.md` holds 0 line(s). Nothing migrates into the ledger (§3.6, §4 row 1); the acceptance criterion is that this number is zero, and it is printed as a number because "nothing migrated" and "nothing was counted" read the same in prose.

