# Rosco Radio releases

## Stable v0.1.2

GitHub release asset name: `RoscoRadio-v0.1.2.zip`

NexusUpdater package SHA-256:

`e1f19f7729ad48289bbbafa793e7e31490162db98d3d8e6f223715662458f3ae`

This is the current Stable branch/build.

## Beta v0.1.3

GitHub release asset name: `RoscoRadio-v0.1.3-beta.zip`

NexusUpdater package SHA-256:

`da0c1013a5375d06310c7467b631d4bad91769c887a099b8abbf87561d7294d3`

The Beta adds Rosco Radio's Satellite workspace and bundled SatDump processing runtime in packaged builds. SatDump is GPL-3.0 software; see the Beta branch third-party notice and satellite integration documentation.

## Online installer

The release publisher also attaches:

- `RoscoRadio-Online-Installer.ps1`
- `RoscoRadio-Online-Installer.bat`

Installer SHA-256 values for the current repository versions:

- PowerShell: `4957f769c7e890754db25f70741212c5b6ec330f9d7e41614fbc68699a213a4f`
- Batch launcher: `c7d86fa11d84c8ac3696ba146c7f343d05024522db465ab33334e0f2f31e7f58`

The installer queries NexusUpdater at runtime, verifies the published package checksum, and therefore does not need to be rebuilt for every RR release.

## Publishing

`.github/workflows/publish-release.yml` mirrors NexusUpdater builds into GitHub Releases. The workflow supports `stable` and `beta`; Beta is automatically marked as a prerelease.
