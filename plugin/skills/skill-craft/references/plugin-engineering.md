# Plugin Engineering Reference

Practical guide to packaging Claude Code plugins. Covers the pitfalls the
official docs don't mention.

---

## Two-Layer Structure

A plugin distributed through a marketplace needs two separate layers: the
marketplace (a catalog) and the plugin (the actual extension). Their
`.claude-plugin/` directories must never be mixed.

```
repo-root/                         # ← marketplace root
├── .claude-plugin/
│   └── marketplace.json           # marketplace definition ONLY
├── plugin/                        # ← plugin root
│   ├── .claude-plugin/
│   │   └── plugin.json            # plugin definition ONLY
│   ├── commands/
│   ├── skills/
│   │   └── my-skill/
│   │       └── SKILL.md
│   ├── hooks/
│   │   ├── hooks.json
│   │   └── scripts/
│   └── agents/
├── install.sh                     # optional setup helper
└── README.md
```

When both `plugin.json` and `marketplace.json` exist in the same
`.claude-plugin/` directory, Claude Code reads the wrong one and fails with
a misleading schema validation error (`owner: expected object, received
undefined`).

---

## marketplace.json

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

## plugin.json

Located at `plugin/.claude-plugin/plugin.json`:

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

## Skills

Skills live in `skills/<skill-name>/SKILL.md`. Claude automatically invokes
them based on the `description` field in the frontmatter.

**Naming convention:** Use descriptive names without the plugin prefix. The
namespace already provides context (`my-plugin:code-review`, not
`my-plugin:my-plugin-code-review`). Avoid skill names that share a prefix
with the plugin name — non-namespaced duplicates appear in autocomplete
and cluster with the plugin's namespaced entries.

**Description convention:** Use third-person with specific trigger phrases
in quotes:

```markdown
---
name: code-review
description: This skill should be used when the user asks to "review code",
  "check this PR", "analyze code quality", or requests feedback on
  implementation patterns.
version: 1.0.0
---
```

---

## Commands

Commands live in `commands/<name>.md`. They become slash commands namespaced
under the plugin: `/my-plugin:command-name`.

```markdown
---
description: Does something useful
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: [option1|option2]
---

Handle the command. User argument: $ARGUMENTS
```

`disable-model-invocation: true` means only the user can trigger it (not
the model).

---

## Hooks

Hooks live in `hooks/hooks.json`. Plugin hooks require a `"hooks"` wrapper
key — without it you get `Hook load failed: expected record, received
undefined`.

```json
{
  "description": "What these hooks do",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/my-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Use `${CLAUDE_PLUGIN_ROOT}` for all paths. It resolves to the plugin's
cached install location.

Available events: PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart,
SessionEnd, UserPromptSubmit, PreCompact, Notification.

### Hook scripts — stderr pitfall

Claude Code treats any stderr output from hook scripts as a hook error, even
when the script exits 0. Silence stderr early:

```bash
#!/usr/bin/env bash
exec 2>/dev/null
# ... rest of script
```

```python
#!/usr/bin/env python3
import os, sys
sys.stderr = open(os.devnull, "w")
# ... rest of script
```

---

## Plugin Configuration (.local.md pattern)

Plugins that need user-configurable settings use
`.claude/plugin-name.local.md` files with YAML frontmatter:

```markdown
---
enabled: true
sensitivity: normal
custom_option: value
---
```

Location precedence: project `.claude/plugin-name.local.md` overrides global
`~/.claude/plugin-name.local.md`. Add `.local.md` files to `.gitignore`
(user-specific, not shared).

Reading from hooks: parse the YAML frontmatter with a simple regex in Python
or `sed -n '/^---$/,/^---$/{...}'` in bash. No external dependencies needed.

---

## New Plugin Setup

Minimum steps from empty repo to installable plugin:

1. Create the two-layer directory structure:
   ```
   mkdir -p .claude-plugin plugin/.claude-plugin plugin/skills/my-skill
   ```

2. Write `.claude-plugin/marketplace.json` (marketplace catalog):
   ```json
   {
     "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
     "name": "my-marketplace",
     "owner": { "name": "Your Name" },
     "plugins": [{ "name": "my-plugin", "source": "./plugin" }]
   }
   ```

3. Write `plugin/.claude-plugin/plugin.json` (plugin metadata):
   ```json
   { "name": "my-plugin" }
   ```

4. Write `plugin/skills/my-skill/SKILL.md` (the skill itself)

5. Push to GitHub, then install:
   ```
   claude plugin marketplace add owner/repo
   claude plugin install my-plugin@my-marketplace
   ```

Do NOT put `plugin.json` at the repo root — it conflicts with
`marketplace.json`. The most common first-time mistake.

---

## Installation Flow

### Publishing

Push your repo to GitHub with `.claude-plugin/marketplace.json` at the root.

### Installing

```
/plugin marketplace add owner/repo
/plugin install my-plugin@my-marketplace
/reload-plugins
```

### Updating after changes

```
/plugin marketplace update my-marketplace
/plugin uninstall my-plugin@my-marketplace
/plugin install my-plugin@my-marketplace
/reload-plugins
```

`marketplace update` pulls the latest marketplace.json but does NOT update
already-installed plugins. Must uninstall and reinstall.

### Local development

```bash
claude --plugin-dir ./plugin
```

Loads the plugin directly. Use `/reload-plugins` to pick up changes.

### Session restart note

After installing or reinstalling a plugin, `/reload-plugins` loads the new
skills, commands, and hooks. However, hook errors from the previous load may
persist in the session. If you see stale "hook error" messages after fixing
an issue, restart Claude Code — a fresh session clears them.

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
- Tools where hooks just call an external binary — the plugin adds
  indirection without benefit

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
| Marketplace and plugin have the same name | Skills appear both namespaced and non-namespaced | Use different names (e.g., marketplace `coding-clippy`, plugin `clippy`) |
| `directory` source in `extraKnownMarketplaces` | `owner: expected object, received undefined` on install | Use GitHub source (`/plugin marketplace add owner/repo`) instead |
| `enabledPlugins` in settings.json without `/plugin install` | Plugin doesn't load | Must install via `/plugin install`, not just enable in settings |
| Archive dirs with SKILL.md in repo | Stale skills appear | Delete or rename SKILL.md files outside `plugin/`; they get cloned into marketplace cache |
