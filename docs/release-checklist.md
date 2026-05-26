# LyPy Windows Release Checklist

## Local validation

1. Run `powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Version vX.Y.Z`.
2. Confirm `dist/LyPy-vX.Y.Z-windows-x64.exe` exists.
3. Launch the built `.exe` on a Windows machine without Python installed.
4. Confirm lyrics render, media controls work, and album-gradient updates.
5. Change a setting, restart the app, and confirm it persists.

## CI validation

1. Push a test tag in semver format.
2. Confirm the `release` workflow runs on `windows-latest` and succeeds.
3. Confirm workflow artifact upload contains `LyPy-vX.Y.Z-windows-x64.exe`.
4. Confirm GitHub Release is created with generated release notes.

## First production release

1. Merge release-ready changes into the target branch.
2. Create and push the first release tag (for example `v0.1.0`).
3. Open the created release and verify the executable asset downloads correctly.
4. Run a final smoke test from the downloaded release asset.
