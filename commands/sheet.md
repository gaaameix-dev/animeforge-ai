---
description: Turn a logline into an html-anime shot sheet (holds, one sakuga shot, closed color script)
argument-hint: <logline> [seconds 8|12|20] [16:9|9:16] [indigo|eclipse|noon|festival]
allowed-tools: Bash(node:*), Read, Write
---

Build the shot sheet for this brief: $ARGUMENTS

Run the compiler that ships with this plugin:

```
node "${CLAUDE_PLUGIN_ROOT}/harness/sheet-cli.mjs" "<the logline>" 8 16:9 indigo "<their dialogue or empty>"
```

Rules:

- Pick `seconds` from 8, 12 or 20 and `aspect` from 16:9 or 9:16. Default to 8 and 16:9 when the user did not say.
- Pick `script` only from indigo, eclipse, noon or festival. Do not invent a palette.
- Put their dialogue in the last argument, in the language they wrote it, or leave it empty. Do not translate.
- If the compiler prints an error, fix the arguments and run it once more.

Show the sheet as-is in a fenced block, then ask whether to draw it. Do not write any film files yet — drawing is `/html-anime:draw` or the html-anime-direct skill's job.
