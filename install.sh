#!/usr/bin/env bash
# macOS/Linux counterpart: symlinks each skill into ~/.claude/skills.
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/.claude/skills ~/.config/spritecook
for d in "$repo"/skills/*/; do ln -sfn "${d%/}" ~/.claude/skills/"$(basename "$d")"; echo "linked $(basename "$d")"; done
cp "$repo"/helpers/spritecook/* ~/.config/spritecook/
