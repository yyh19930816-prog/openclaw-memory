$env:PATH = $env:PATH + ";C:\Program Files\Git\cmd"
$TOKEN     = "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"
$USER      = "yyh19930816-prog"
$REPO      = "openclaw-memory"
$REMOTE    = "https://${USER}:${TOKEN}@github.com/${USER}/${REPO}.git"
$BACKUP    = "C:\Users\Administrator\.openclaw\backup-repo"
$TODAY     = Get-Date -Format "yyyy-MM-dd"
$NOW       = Get-Date -Format "yyyy-MM-dd HH:mm"
$KEEP_DAYS = 30

function Copy-SourceFiles($destDir) {
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    New-Item -ItemType Directory -Force -Path "$destDir\workspace" | Out-Null
    New-Item -ItemType Directory -Force -Path "$destDir\workspace\memory" | Out-Null
    New-Item -ItemType Directory -Force -Path "$destDir\hud" | Out-Null
    $wsrc = "C:\Users\Administrator\.openclaw\workspace"
    if (Test-Path $wsrc) {
        foreach ($f in @("MEMORY.md","AGENTS.md","HEARTBEAT.md","TOOLS.md","SOUL.md")) {
            $fp = "$wsrc\$f"
            if (Test-Path $fp) { Copy-Item $fp "$destDir\workspace\" -Force }
        }
        if (Test-Path "$wsrc\memory") {
            Copy-Item "$wsrc\memory\*" "$destDir\workspace\memory\" -Recurse -Force -EA SilentlyContinue
        }
    }
    if (Test-Path "D:\TRAE\F1\claw_evolution.json") { Copy-Item "D:\TRAE\F1\claw_evolution.json" "$destDir\" -Force }
    if (Test-Path "D:\TRAE\F1\claw_gui_red.py")     { Copy-Item "D:\TRAE\F1\claw_gui_red.py" "$destDir\hud\" -Force }
    $tr = "C:\Users\Administrator\.cursor\projects\c-Users-Administrator-openclaw\agent-transcripts"
    if (Test-Path $tr) {
        New-Item -ItemType Directory -Force -Path "$destDir\cursor-transcripts" | Out-Null
        Copy-Item "$tr\*" "$destDir\cursor-transcripts\" -Recurse -Force -EA SilentlyContinue
    }
}

Copy-SourceFiles "$BACKUP\latest"

$snapshotDir = "$BACKUP\snapshots\$TODAY"
Copy-SourceFiles $snapshotDir

if (Test-Path "$BACKUP\RESTORE.md") { Copy-Item "$BACKUP\RESTORE.md" "$BACKUP\latest\" -Force -EA SilentlyContinue }

$snapshotsRoot = "$BACKUP\snapshots"
if (Test-Path $snapshotsRoot) {
    $cutoff = (Get-Date).AddDays(-$KEEP_DAYS)
    Get-ChildItem $snapshotsRoot -Directory | Where-Object {
        try { [datetime]$_.Name -lt $cutoff } catch { $false }
    } | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -EA SilentlyContinue }
}

$snapshots = @()
if (Test-Path $snapshotsRoot) {
    $snapshots = Get-ChildItem $snapshotsRoot -Directory | Sort-Object Name -Descending | Select-Object -ExpandProperty Name
}

$lines = @("# OpenClaw Backup Timeline","","Keep last $KEEP_DAYS days. Paste RESTORE.md to Cursor AI to recover memory.","","## Latest","[latest/RESTORE.md](./latest/RESTORE.md)","","## Snapshots","","| Date | Link |","|------|------|")
foreach ($s in $snapshots) { $lines += "| $s | [view](./snapshots/$s/RESTORE.md) |" }
$lines += "","Last backup: $NOW | $($snapshots.Count) snapshots"
$lines -join "`n" | Out-File -FilePath "$BACKUP\TIMELINE.md" -Encoding UTF8 -Force

Set-Location $BACKUP
git remote set-url origin $REMOTE 2>$null
git add -A
$st = git status --porcelain
if ($st) {
    git commit --trailer "Made-with: Cursor" -m "backup $NOW"
    git push origin main 2>&1 | Out-Null
    Write-Host "DONE: pushed to GitHub"
} else {
    Write-Host "DONE: no changes"
}
