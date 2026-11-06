---
description: Plan an anime end to end with AnimeForge AI — brief, story, script, characters, storyboard, audio and edit list
argument-hint: <idea or brief> [duration] [language] [16:9|9:16]
---

Use the `animeforge-ai` skill to plan this: $ARGUMENTS

Work in stages, and stop for approval only where the skill says to:

1. **Brief** — title, logline, genre, tone, audience, platform, runtime, language, aspect ratio, delivery target. Fill defaults yourself (20–30s proof-of-concept, 16:9) when the user gave nothing.
2. **Story** — premise, stakes, conflict, beats, ending or hook.
3. **Script** — scene headings, action, dialogue with speaker labels, approximate shot timings.
4. **Characters** — a character bible with identity anchors for every recurring character.
5. **World and art direction** — locations, lighting, color script, continuity rules.
6. **Storyboard** — shot by shot: size, angle, movement, action, setting, duration, continuity anchors, image/video prompt, negative prompt.
7. **Animation, voice, music, edit** — direction notes, cue sheets, an edit decision list, export settings.
8. **QA** — run `references/production-checklist.md` from the skill folder and report what is planned vs generated vs verified.

Write the package to `animeforge/<slug>/` in the user's project: `brief.md`, `story.md`, `script.md`, `characters.md`, `storyboard.md`, `audio.md`, `edit.md`. Keep every hex, name and duration consistent across the files.

If no image, video, voice or editing tool is connected, say plainly that nothing has been rendered and hand over production-ready prompts instead.
