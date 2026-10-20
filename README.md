# claude-skills

Burak's personal Claude Code skills, one folder each under `skills/`.

| Skill | What it does |
| --- | --- |
| `tyt-deneme-analizi` | Turkish TYT/YKS deneme sheet to a designed visual analysis page |
| `no-mistakes` | Drives the no-mistakes validation pipeline before pushing |
| `spritecook` | SpriteCook image generation through a local key helper |

## Windows setup

Prerequisites: Git, Python 3 on `PATH` (for `spritecook` and `tyt-deneme-analizi`), Claude Code.

```powershell
git clone https://github.com/thealphaomega3/claude-skills.git $HOME\claude-skills
powershell -ExecutionPolicy Bypass -File $HOME\claude-skills\install.ps1
```

This creates junctions in `%USERPROFILE%\.claude\skills`, so `git pull` updates the skills in place.
Restart Claude Code afterwards.

Then, only if you use `spritecook`, save your key (never committed) to `%USERPROFILE%\.config\spritecook\api_key`.
`no-mistakes` also needs the `no-mistakes` CLI installed on Windows.

## macOS / Linux

```bash
git clone https://github.com/thealphaomega3/claude-skills.git ~/claude-skills && ~/claude-skills/install.sh
```

## Not included

- `synced/`: managed by Claude itself, it re-syncs per account.
- `popbook-*`: project skills, they live in the Popbook repo.
