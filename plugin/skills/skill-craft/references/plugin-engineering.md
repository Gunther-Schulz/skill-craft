# Plugin Engineering Reference

Practical guide to packaging and distributing Claude Code plugins. Covers
what the official `plugin-dev` does not: distribution paths, marketplace
workflow, battle-tested gotchas, and operational knowledge.

For skill formatting, writing style, hooks, commands, MCP servers, agents,
progressive disclosure, and plugin settings (.local.md), see the official
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

Use this when: the plugin is personal, for a team, or not ready for public
release.

### Path B: Official Claude Code marketplace

You submit a PR to the official `claude-plugins-official` repo. Anthropic
reviews and merges. The plugin is available to all Claude Code users.

Use this when: the plugin is polished, general-purpose, and ready for
public use.

### What's the same in both paths

The plugin itself is identical. Same directory structure:

```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── commands/
├── agents/
└── hooks/
```

Same `plugin.json`:

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

Only `name` is required. The name determines the skill namespace — skills
are available as `/my-plugin:skill-name`.

---

## Path A: Private marketplace setup

A private marketplace needs two layers in one repo: the marketplace
(catalog) and the plugin (extension). Their `.claude-plugin/` directories
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

Required fields: `name`, `owner` (with `name`), `plugins` array. Each plugin
entry needs `name` and `source`. The `source` is a relative path starting
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
claude plugin uninstall my-plugin@my-marketplace
claude plugin install my-plugin@my-marketplace
```

Then `/reload-plugins`. Note: `marketplace update` pulls the latest
marketplace.json but does NOT update installed plugins. Must uninstall
and reinstall.

### Publishing later to official marketplace

When ready to publish, submit a PR to `claude-plugins-official` with your
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
- **Marketplace copy** — `~/.claude/plugins/marketplaces/my-marketplace/`.
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
claude plugin uninstall my-plugin@my-marketplace
claude plugin install my-plugin@my-marketplace
/reload-plugins
```

### Session restart note

After installing or reinstalling, `/reload-plugins` loads new skills and
hooks. However, hook errors from the previous load may persist. If stale
"hook error" messages appear after fixing an issue, restart Claude Code.

---

## When NOT to Use a Plugin

**Good fit:**
- Skills, commands, hooks with no external dependencies
- Tools that don't need CLI access outside Claude Code
- Self-contained extensions

**Bad fit (keep as standalone tool):**
- System utilities needing a CLI binary in `$PATH`
- Tools that configure `statusLine` (plugins can only set the `agent` key)
- Scripts with heavy external state that must survive reinstalls
- Tools where hooks just call an external binary

**The test:** If after converting to a plugin, install.sh still handles most
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
