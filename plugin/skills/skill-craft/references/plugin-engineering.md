# Plugin Engineering Reference

**Load when:** packaging, releasing, or installing a plugin;
setting up a marketplace; diagnosing activation or stale-pin
behavior.

Practical guide to packaging and distributing Claude Code plugins.
Covers
what the official `plugin-dev` does not: distribution paths, marketplace
workflow, battle-tested gotchas, and operational knowledge.

For skill formatting, writing style, hooks, commands, MCP servers,
agents,
progressive disclosure, and plugin settings (.local.md), see the
official
`plugin-dev` plugin (`plugin-dev@claude-plugins-official`).

---

## Distribution: ask the user first

Before creating a plugin, ask: **will this be published to the official
Claude Code marketplace, or distributed via a private GitHub repo?**

Both paths use the same plugin structure. The difference is how the
marketplace layer works.

### Path A: Private GitHub repo (local marketplace)

Host a marketplace in a GitHub repo. Full control over distribution.
The plugin can be published to the official marketplace later without
restructuring.

Use this when: the plugin is personal, for a team, or not ready for
public
release.

### Path B: Official Claude Code marketplace

You submit a PR to the official `claude-plugins-official` repo.
Anthropic
reviews and merges. The plugin is available to all Claude Code users.

Use this when: the plugin is polished, general-purpose, and ready for
public use.

### What's the same in both paths

The plugin itself is identical — same directory shape (see "Plugin
layout" below for the full tree, key rules, and README structure),
same `plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Your Name"
  }
}
```

Only `name` is required. The name determines the skill namespace —
skills
are available as `/my-plugin:skill-name`.

---

## Plugin layout (a skill's mechanical foundation)

The directory shape every skill plugin follows. Get it right once and
move on — bloat in skill-craft's method has historically clustered
here, so the detail lives in this reference, not in `SKILL.md`.

### Directory tree

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: {"name": "plugin-name"}
├── plugin/
│   └── skills/
│       └── skill-name/
│           ├── SKILL.md     # Required: trigger + instructions
│           └── references/  # Optional: loaded on demand
├── commands/                # Optional: slash commands (.md)
├── agents/                  # Optional: subagent definitions (.md)
└── hooks/                   # Optional: event handlers
```

### Key rules

- SKILL.md must be named exactly `SKILL.md`.
- The `description` field in YAML frontmatter is the trigger condition
  — be specific about trigger phrases.
- Component directories go at the plugin root, not inside
  `.claude-plugin/`.
- Use `${CLAUDE_PLUGIN_ROOT}` for portable path references in scripts.
- Skills auto-discover: any `SKILL.md` in a `skills/` subdirectory
  loads.

### README.md (human audience, not the AI)

README sits at the plugin root, for humans deciding whether to install
— a different audience than `SKILL.md` (the AI's instructions).

Required sections:
- **What it does** — the value in one paragraph. Lead with the problem
  solved, not the mechanism.
- **Installation** — the marketplace add + install + reload-plugins
  commands, copy-pasteable.
- **Usage** — trigger phrases and/or slash command.
- **Files** — a table of plugin files and their roles.

Optional: an **origin story** (the real incident that motivated the
skill) and a brief **phases/features** overview.

A plugin with contributors also needs a **Development** section — the
edit → commit → reinstall cycle, `/reload-plugins`, and version bumps
— which prevents the "I changed the file but nothing happened"
friction.

---

## Path A: Private marketplace setup

A private marketplace needs two layers in one repo: the marketplace
(catalog) and the plugin (extension). Their `.claude-plugin/`
directories
must never be mixed.

```
repo-root/                         # ← marketplace root
├── .claude-plugin/
│   └── marketplace.json           # marketplace definition ONLY
├── plugin/                        # ← plugin root
│   ├── .claude-plugin/
│   │   └── plugin.json            # plugin definition ONLY
│   ├── skills/
│   │   └── my-skill/
│   │       └── SKILL.md
│   └── ...
└── README.md
```

### marketplace.json

Located at `.claude-plugin/marketplace.json` in the repo root:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-marketplace",
  "description": "Short description",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "What the plugin does",
      "source": "./plugin"
    }
  ]
}
```

Required fields: `name`, `owner` (with `name`), `plugins` array. Each
plugin
entry needs `name` and `source`. The `source` is a relative path
starting
with `./`.

### Step-by-step setup

1. Create the two-layer directory structure:
   ```
   mkdir -p .claude-plugin plugin/.claude-plugin plugin/skills/my-skill
   ```

2. Write `.claude-plugin/marketplace.json` (marketplace catalog)

3. Write `plugin/.claude-plugin/plugin.json` (plugin metadata)

4. Write `plugin/skills/my-skill/SKILL.md` (the skill)

5. Push to GitHub, then install:
   ```
   claude plugin marketplace add owner/repo
   claude plugin install my-plugin@my-marketplace
   /reload-plugins
   ```

Do NOT put `plugin.json` at the repo root — it conflicts with
`marketplace.json`. The most common first-time mistake.

### Updating after changes

```
claude plugin marketplace update my-marketplace
claude plugin update my-plugin@my-marketplace
```

Then `/reload-plugins`. See "Activation" below for the two-pin
model.

### Publishing later to official marketplace

When ready to publish, submit a PR to `claude-plugins-official` with
your
`plugin/` directory. The marketplace.json wrapper is not needed — the
official repo is the marketplace. No restructuring of the plugin itself.

---

## Path B: Official marketplace submission

Submit a PR to the `claude-plugins-official` GitHub repo. The plugin
directory goes under `plugins/my-plugin/` in that repo. No separate
marketplace.json needed — the official repo handles the catalog.

```
claude-plugins-official/
├── .claude-plugin/
│   └── marketplace.json           # Anthropic maintains this
└── plugins/
    └── my-plugin/                 # ← your PR adds this
        ├── .claude-plugin/
        │   └── plugin.json
        ├── skills/
        └── ...
```

After merge, users install with:
```
claude plugin install my-plugin@claude-plugins-official
```

---

## Local development (both paths)

Test without the marketplace cycle:

```bash
claude --plugin-dir ./plugin
```

Loads the plugin directly. Use `/reload-plugins` to pick up changes.

### Edit the source repo, not the cache

Installed plugins exist in three locations:

- **Source repo** — the Git repository (e.g., `~/dev/user/my-plugin/`).
  This is where edits belong.
- **Marketplace copy** —
  `~/.claude/plugins/marketplaces/my-marketplace/`.
  Cloned from the source repo. Read-only in practice — changes here are
  overwritten by `marketplace update`.
- **Cache copy** — `~/.claude/plugins/cache/my-marketplace/my-plugin/`.
  Copied from the marketplace on `plugin install`. Read-only — changes
  here are overwritten by reinstall.

**BEFORE editing any plugin file:** Verify the file path points to the
source repo, not the marketplace or cache copy. Edits to cache or
marketplace files are silently lost on the next update/reinstall cycle.

When reviewing or improving a plugin during a conversation, the AI
reads from cache (that's what's loaded). But all writes must go to
the source repo. After editing, commit in the source repo, then:

```
claude plugin marketplace update my-marketplace
claude plugin update my-plugin@my-marketplace
```

Then `/reload-plugins`. See "Activation" for the two-pin model.

Stage only the files the edit touched (avoid `git add -A`); commit
message names what changed.

### Fast iteration: symlink the cache

The reinstall flow above is correct for distribution but slow for heavy
iteration on a plugin's own skills. The cache is a real copy of the
plugin folder; Claude Code reads from it directly. Replace the copy
with a symlink to the source plugin folder to pick up edits without
reinstalling:

```bash
rm -rf ~/.claude/plugins/cache/<mp>/<plugin>/<version>
ln -s /path/to/repo/plugin \
      ~/.claude/plugins/cache/<mp>/<plugin>/<version>
```

After this, edits to source files are visible to Claude Code on
`/reload-plugins` alone — no version bump, no reinstall.

Idempotent dev-link script template (drop into the plugin repo as
`dev-link.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_PLUGIN="$REPO_DIR/plugin"
VERSION=$(jq -r .version "$SRC_PLUGIN/.claude-plugin/plugin.json")
PLUGIN_NAME=$(jq -r .name "$SRC_PLUGIN/.claude-plugin/plugin.json")
MARKETPLACE_NAME=$(jq -r .name "$REPO_DIR/.claude-plugin/marketplace.json")
CACHE_DIR="$HOME/.claude/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION"
mkdir -p "$(dirname "$CACHE_DIR")"
rm -rf "$CACHE_DIR"
ln -s "$SRC_PLUGIN" "$CACHE_DIR"
```

Reads name and version from the manifests so it stays in sync if either
changes. Re-run after `claude plugin uninstall` or after bumping the
version in `plugin.json` (the cache path includes the version).

The standard reinstall flow takes over again whenever uninstall runs
or version bumps. The symlink is a dev-mode override, not a
distribution mechanism — end users install normally via the
marketplace.

### Activation

Two pins govern what version Claude Code actually runs:

- **Marketplace clone** (`~/.claude/plugins/marketplaces/<mp>/`) —
  the catalog of available versions. Updated by `claude plugin
  marketplace update` or a direct `git pull` in the clone.
- **Installed pin** (`~/.claude/plugins/installed_plugins.json`) —
  the version Claude Code reads on load. Updated by `claude plugin
  update <plugin>@<mp>`.

Three activation actions, each with a different reach:

| Action | Picks up |
|---|---|
| `/reload-plugins` (alone) | Same-version skill/hook/setting changes at the currently-pinned version. Re-reads the installed pin but does not bump it. |
| `claude plugin update` + `/reload-plugins` | Version-bump activation. `update` bumps the pin; `/reload-plugins` re-reads the pin so subsequent skill invocations resolve to the new installPath. (Ignore the CLI's "Restart to apply changes" message — conservative guidance; `/reload-plugins` is the activation step.) |
| Session restart | Equivalent to `/reload-plugins` for pin re-reads. Use when hook errors from a prior load persist (those don't clear on `/reload-plugins`) or when a fresh process is otherwise desired. |
| `/reload-skills` | **Nothing here** — rescans skill files at already-resolved paths; never re-reads the pin. The near-identical name is the trap: a session keeps serving the old version through it (verified live). |

So: both same-version edits and version bumps activate via
`/reload-plugins` once the respective on-disk change is in place
(cache symlink update for dev-link, `claude plugin update` for
pin bump). The pin is the resolution point — changing it and
then re-reading via `/reload-plugins` activates the new version
in the running session.

A session may not know the pin moved at all — another session can
move it. This plugin mechanizes the sequence and the catch: the
`/release-plugin` command (the flow above end-to-end), a PreToolUse
gate denying Skill calls whose own plugin's pin moved after the
session's last `/reload-plugins`, and a PostToolUse reminder after
`claude plugin update|install`.

Caveat (unverified this session; expected behavior per the
pin-resolution model): skills already invoked in the current
session may have loaded reference files into their working
context before the bump. `/reload-plugins` re-reads the pin but
is not expected to retroactively re-resolve already-loaded
references. Fresh skill invocations after `/reload-plugins`
should load from the new pin; in-flight skill work may carry
stale content from the prior version until next invocation.

Hook errors from a previous load also persist across
`/reload-plugins`; restart clears them.

---

## When NOT to Use a Plugin

**Good fit:**
- Skills, commands, hooks with no external dependencies
- Tools that don't need CLI access outside Claude Code
- Self-contained extensions

**Bad fit (keep as standalone tool):**
- System utilities needing a CLI binary in `$PATH`
- Tools that configure `statusLine` (plugins can only set the `agent`
  key)
- Scripts with heavy external state that must survive reinstalls
- Tools where hooks just call an external binary

**The test:** If after converting to a plugin, install.sh still handles
  most
of the setup, the plugin layer is adding complexity without value.

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| marketplace.json and plugin.json in same `.claude-plugin/` | `owner: expected object, received undefined` | Separate into marketplace root + plugin subdirectory |
| hooks.json without `"hooks"` wrapper | `Hook load failed: expected record, received undefined` | Wrap events under `{"hooks": {...}}` |
| Hook script writes to stderr | Hook error on every message | Add `exec 2>/dev/null` (bash) or silence stderr (python) |
| Changed plugin on GitHub but not reinstalled | Old behavior persists | `marketplace update` + uninstall + reinstall |
| Marketplace and plugin have the same name | May cause duplicate autocomplete entries (cosmetic) | Use different names if possible |
| `directory` source in `extraKnownMarketplaces` | `owner: expected object, received undefined` | Use GitHub source (`/plugin marketplace add owner/repo`) |
| `enabledPlugins` in settings.json without `/plugin install` | Plugin doesn't load | Must install via `/plugin install`, not just enable |
| Archive dirs with SKILL.md in repo | Stale skills appear | Delete SKILL.md files outside `plugin/`; they get cloned into cache |
