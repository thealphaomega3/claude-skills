---
name: spritecook
description: "Generate or edit images through SpriteCook (AI game art and image generation) with the local API key helper, in any project. Use when asked to make, edit, recolour or reroll art, sprites, icons or illustrations, or to check SpriteCook credits."
version: 1.0.0
author: Burak
license: MIT
platforms: [macos, windows]
metadata:
  hermes:
    tags: [spritecook, art, image-generation, sprites]
---

# SpriteCook

SpriteCook is reached over HTTP through one helper script. You never touch the key.

- Key: `~/.config/spritecook/api_key (Windows: %USERPROFILE%\.config\spritecook\api_key)` (mode 600). **Never read it into output, print, copy, log or commit it.** The helper reads it itself.
- On Windows use `python` (or `py -3`) in place of `python3`, and `$HOME`/`%USERPROFILE%` in place of `~` in cmd.exe.
- Helper: `~/.config/spritecook/sc.py` (stdlib Python, any `python3`).

```
python3 ~/.config/spritecook/sc.py tools                     # list tool names
python3 ~/.config/spritecook/sc.py get_credit_balance '{}'
python3 ~/.config/spritecook/sc.py <tool_name> '<json arguments>'
```

It prints the tool's result as JSON. Run `tools` first if unsure of a tool's name.

## Uploading a local image (to edit it)

1. `create_asset_upload` with the file's name and content type.
2. PUT the file to the returned URL with `curl -s -o /dev/null -w "%{http_code}" -X PUT --data-binary @file ...`.
3. `finalize_asset_upload`. The returned asset id is what `edit_asset_id` takes.

The upload URL and token are secrets: keep them out of prose, reports and files.

## Generating

`generate_game_art`, defaults that worked well:
`model: gpt-image-2`, `resolution: 2K`, `quality: medium`, `pixel: false` (true for pixel art), `smart_crop: false`, `wait_seconds: 90`.
`bg_mode: white` when you will cut the art out yourself; see the tool's own options for transparent output.
Pass `project_id` to file assets under a SpriteCook project: `list_projects` shows them, `create_project` makes one per codebase. Do not file one project's art under another's.
Download the result's `sprite_url` with curl into your working directory, never into a shared or temp folder another project reads.

## Traps

- **Credits.** A 2K medium edit costs 7 credits, a 4K one 17. Check `get_credit_balance` before a batch and tell Burak if it cannot cover it.
- **One job at a time.** Do not fire generations in parallel.
- **A timeout is not a failure.** The job usually finished: `list_recent_assets`, then `get_asset_metadata` on the newest id, and download its `sprite_url`. Do not regenerate and pay twice.
- **Never pass `style_asset_ids` when editing a finished image.** The model edits the style reference instead of your image; this burned 91 credits once.
- **Art direction is Burak's.** Show him a raw result before spending on a whole batch.
- **One account, every project.** Credits are shared across all projects; say how many a task spent in your report.

## Per-project notes

A project with its own art workflow documents it in its repo; read that before generating, and follow it over the defaults above.

- **Tomebound** (`~/gamedevelopment/tomebound`, SpriteCook project `f4c16c85-3a3c-4d3d-8d78-ccce3f6272de`): the spell-art workflow is `.claude/skills/generate-spell-art/SKILL.md`, with prompts in `style.md` and family notes in `families.md` beside it. Its Python art tools run from `~/.venvs/tomebound-artgen/bin/python` with `PYTHONDONTWRITEBYTECODE=1`, and a changed sprite needs the tiles re-baked (step 10 of that skill).
