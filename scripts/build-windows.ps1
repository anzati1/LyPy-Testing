param(
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$appDir = Join-Path $repoRoot "LyPy"
$venvDir = Join-Path $repoRoot ".venv-build"

if (-not (Test-Path $venvDir)) {
    python -m venv $venvDir
}

$pythonExe = Join-Path $venvDir "Scripts\python.exe"

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r (Join-Path $appDir "requirements.txt")
& $pythonExe -m pip install pyinstaller

$requiredAssets = @(
    "btn_prev.png",
    "btn_play.png",
    "btn_pause.png",
    "btn_next.png",
    "app_icon.png",
    "app.ico"
)

foreach ($asset in $requiredAssets) {
    $assetPath = Join-Path $appDir ("assets\" + $asset)
    if (-not (Test-Path $assetPath)) {
        throw "Missing required asset: $assetPath"
    }
}

Push-Location $appDir
try {
    & $pythonExe -m PyInstaller "lypy.spec" --noconfirm --clean
} finally {
    Pop-Location
}

$builtExe = Join-Path $appDir "dist\LyPy.exe"
if (-not (Test-Path $builtExe)) {
    throw "Build failed: executable not found at $builtExe"
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    if ($env:GITHUB_REF_NAME -and $env:GITHUB_REF_NAME.StartsWith("v")) {
        $Version = $env:GITHUB_REF_NAME
    } else {
        $Version = "dev"
    }
}

$releaseDist = Join-Path $repoRoot "dist"
New-Item -ItemType Directory -Path $releaseDist -Force | Out-Null

$versionedExe = Join-Path $releaseDist ("LyPy-" + $Version + "-windows-x64.exe")
Copy-Item -Path $builtExe -Destination $versionedExe -Force
$latestExe = Join-Path $releaseDist "LyPy-latest-windows-x64.exe"
try {
    Copy-Item -Path $builtExe -Destination $latestExe -Force
} catch {
    Write-Host "Skipped updating LyPy-latest-windows-x64.exe because it is locked."
}

Write-Host "Built executable:"
Write-Host $versionedExe
