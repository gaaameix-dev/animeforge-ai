Read AGENTS.md and follow it. The skills are in `skills/`.

## Plugin

This repo is also a Claude Code plugin and its own marketplace (`.claude-plugin/`).

```
/plugin marketplace add gaaameix-dev/html-anime
/plugin install html-anime@html-anime
```

- `skills/` holds the five skills. The plugin loads them automatically; `/html-anime:sheet` builds a shot sheet.
- When installed as a plugin, `harness/`, `films/roof/` and `skills/` live under `${CLAUDE_PLUGIN_ROOT}`. Read them from there, not from the user's project root.
- Write films into the user's project, at `films/<slug>/index.html`, never into the plugin folder.
