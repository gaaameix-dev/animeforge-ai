# html-anime

You draw anime in code. You do not generate video, and you do not open an editor timeline.

1. Read the sheet the user pasted. If they only wrote a logline, build the sheet with `harness/compile.js` (as a Claude Code plugin: `node "${CLAUDE_PLUGIN_ROOT}/harness/sheet-cli.mjs" "<logline>" 8 16:9 indigo ""`) and show it before any drawing.
2. Read the five skills, in the order `skills/html-anime-direct/SKILL.md` names. Each skill owns one subject.
3. Use `films/roof/index.html` for the file shape and the color-dip cut only.

Write the film to `films/<slug>/index.html` at the size on the sheet.

A shot list that does not sum to the runtime is not done. A hex that is not on the sheet is not done. A second sakuga shot is not done.

Done when, in that film's directory, both pass:

```
npx hyperframes lint
npx hyperframes validate
```

## As a Claude Code plugin

`/plugin marketplace add gaaameix-dev/html-anime` then `/plugin install html-anime@html-anime`. The plugin root is `${CLAUDE_PLUGIN_ROOT}`: read `skills/`, `harness/` and `films/roof/` from there, and write the film into the user's project at `films/<slug>/index.html`.
