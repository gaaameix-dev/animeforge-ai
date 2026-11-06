<h1 align="center">AnimeForge AI</h1>

<p align="center">
  <b>An anime showrunner, screenwriter, storyboard artist and animation director in one skill.</b>
</p>

<p align="center">
  <a href="https://gaaameix-dev.github.io/animeforge-ai/"><img src="https://img.shields.io/badge/site-gaaameix--dev.github.io%2Fanimeforge--ai-111?style=flat-square" alt="Site"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111?style=flat-square" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/for-Claude%20Code-111?style=flat-square" alt="Claude Code">
</p>

AnimeForge AI turns an idea, a prompt, a novel or a manga concept into a production-ready anime package: brief, story, timed script, character bibles, world and art direction, a shot-by-shot storyboard with ready-to-use prompts, animation and audio direction, an edit decision list, and a QA pass.

It is a **skill**, not a renderer. It plans and directs; it never claims a frame, a voice track or an export exists unless a connected tool confirms it. With no generation tool attached it hands you production-ready prompts and assembly instructions instead.

## Install

Claude Code, from this repo as a plugin marketplace:

```
/plugin marketplace add gaaameix-dev/animeforge-ai
/plugin install animeforge-ai@animeforge-ai
```

Then, in any project:

```
/animeforge-ai:plan a 30-second original Hindi anime trailer, night city, red moon
```

Claude.ai / other hosts: drop `skills/animeforge-ai/` into your skills folder, or upload the folder as a skill ZIP. The skill is one `SKILL.md` plus `references/production-checklist.md`.

## What it covers

| Stage | Output |
| --- | --- |
| A — Brief | Title, logline, genre, tone, platform, runtime, language, aspect ratio |
| B — Story | Premise, stakes, conflict, beats, ending or episode hook |
| C — Script | Scene headings, action, dialogue, timings |
| D — Characters | Character bible with identity anchors and reference-sheet needs |
| E — World | Locations, lighting, color script, continuity rules |
| F — Storyboard | Shot size, angle, movement, action, duration, prompt, negative prompt |
| G — Animation | Blocking, timing, spacing, effects, 2D and 3D direction |
| H — Audio | Voice profiles, dialogue script, ambience, SFX, music brief, mix notes |
| I — Production | Uses only tools that actually exist, tracks job ids, verifies outputs |
| J — Edit | Edit decision list, titles, subtitles, grade, export settings |
| K — QA | Continuity, pacing, lip-sync, rights, aspect ratio — as a severity list |

Thirteen modes come with it: Idea, Story, Script, Character, Storyboard, 2D Anime, 3D Anime, Action, Voice & Audio, Trailer, Episode, Production, Revision.

## Layout

```
skills/animeforge-ai/SKILL.md                       the skill
skills/animeforge-ai/references/production-checklist.md   QA checklist
.claude-plugin/                                     plugin + marketplace manifests
commands/plan.md                                    /animeforge-ai:plan
index.html                                          the page at the Pages URL
```

## License

MIT. See [LICENSE](LICENSE).
