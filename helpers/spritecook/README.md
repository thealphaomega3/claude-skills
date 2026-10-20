# SpriteCook access for agents

- Key: `~/.config/spritecook/api_key` (mode 600 on macOS/Linux; on Windows `%USERPROFILE%\.config\spritecook\api_key`). Never print, copy, log or commit it.
- Helper: `~/.config/spritecook/sc.py`, stdlib only. It reads the key itself and talks to the SpriteCook MCP endpoint over HTTP.

```
python3 ~/.config/spritecook/sc.py tools                      # list tool names
python3 ~/.config/spritecook/sc.py get_credit_balance '{}'
python3 ~/.config/spritecook/sc.py generate_game_art '{"prompt": "...", "edit_asset_id": "...", "model": "gpt-image-2", "resolution": "2K", "quality": "medium", "wait_seconds": 90}'
```

Traps:
- One job at a time. A 2K gpt-image-2 medium edit costs 7 credits; check the balance first.
- A call that times out may still have finished: `list_recent_assets`, then `get_asset_metadata` on the id, and download its `sprite_url`.
- Never pass `style_asset_ids` when editing a finished image: the model edits the style reference instead of your image.
- Download URLs and upload tokens are secrets too: keep them out of prose and files.
- The Tomebound art workflow is the `generate-spell-art` skill in the repo (`.claude/skills/generate-spell-art/`).
