# Links every skill in this repo into %USERPROFILE%\.claude\skills using
# directory junctions (no admin rights or Developer Mode needed), and
# installs the SpriteCook helper. Re-run after `git pull` only if you added a skill.
$ErrorActionPreference = 'Stop'
$repo   = $PSScriptRoot
$target = Join-Path $env:USERPROFILE '.claude\skills'
New-Item -ItemType Directory -Force -Path $target | Out-Null

Get-ChildItem (Join-Path $repo 'skills') -Directory | ForEach-Object {
    $link = Join-Path $target $_.Name
    if (Test-Path $link) {
        $item = Get-Item $link -Force
        if ($item.LinkType) { $item.Delete() }
        else { Write-Warning "$link exists and is a real folder; skipping (move it away to link)."; return }
    }
    New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
    Write-Host "linked $($_.Name)"
}

$sc = Join-Path $env:USERPROFILE '.config\spritecook'
New-Item -ItemType Directory -Force -Path $sc | Out-Null
Copy-Item (Join-Path $repo 'helpers\spritecook\*') $sc -Force
if (-not (Test-Path (Join-Path $sc 'api_key'))) {
    Write-Host "Put your SpriteCook key in $sc\api_key (the key is never stored in this repo)."
}
