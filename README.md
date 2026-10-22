# NOTE: Due to the ongoing PHP security attacks, NexusUpdater — the update service used by RoscoRadio, RoscoRadioOS, and other Nexus applications — will be temporarily offline effective October 22, 2026.

Service will be restored once we have verified that the NexusUpdater server is not vulnerable and is safe to bring back online.

During this outage, update checks and downloads through NexusUpdater in any Nexus/Rosco app may be unavailable.

As a result, the Online Installer **WILL NOT WORK.** Please download the `.zip` file instead.
When NexusUpdater comes back online, you will receive a notification.


# Rosco Radio

**The long-awaited solution to the endless pile of separate radio apps.**

Rosco Radio (RR) is a Windows-focused radio workspace that brings WebSDR reception, local radio audio, CW/Morse tools, SSTV, radio utilities, session logging, and NexusUpdater into one interface.

## Current versions

- **Latest documented Stable version:** [`v0.1.5`](releases/v0.1.5.md), promoting the Achievements build to Stable.
- **Existing GitHub ZIP releases:** `v0.1.2` Stable and `v0.1.3` Beta.

Use the [online installer](https://github.com/isaaco122606-cpu/Rosco-Radio/releases/tag/Installer) to request the current Stable or Beta build from NexusUpdater. Stable is recommended for normal use. Beta is a separate testing channel and is not necessarily newer than Stable.

NexusUpdater determines the version delivered by the installer. The `rosco-radio` Stable manifest must report `0.1.5` for clients to receive that update.

## Github factory install

The factory distribution starts on Home with an announcement directing users to the current NexusUpdater version under **Updates**. The target version is fetched from the app manifest at startup, rather than hard-coded.

Use the **Build Rosco Radio Github Factory** GitHub Actions workflow to generate the factory ZIP. Extract it and launch `run.bat` (Python 3.12+ required). This workflow generates a build artifact; existing release downloads are unchanged until a factory ZIP is published.

See [factory build and update details](build/FACTORY.md).

## Online installer

Rosco Radio includes a small **NexusUpdater-powered online installer** under [`installer/`](installer/).

The installer does not hard-code a Rosco Radio package URL. Instead, it:

1. contacts `https://nexusupdater.duckdns.org`,
2. asks for the current Stable or Beta manifest,
3. downloads the package published by NexusUpdater,
4. verifies the package SHA-256,
5. installs RR for the current Windows user,
6. keeps the verified ZIP and a backup of an existing install,
7. creates a desktop shortcut and launches Rosco Radio.

Run `RoscoRadio-Online-Installer.bat` normally for **Stable**. Pass `beta` as its first argument to request the **Beta** channel.

## v0.1.5 Stable

The Achievements build is promoted to Stable, with tracking for RX, CW, VOX, serial PTT, UTC announcements, RR AI chaos, CB bait, and completing the Chocolate Broadcast. This release targets the standalone Windows channel through NexusUpdater.

See the [v0.1.5 release notes](releases/v0.1.5.md) for details.

## Earlier releases

### v0.1.2 Stable

Highlights include:

- Redesigned WebSDR workspace: WebSDR page on the left, receiver data on the right.
- Corrected WebSDR frequency/action control sizing.
- CW workspace: Automatic Morse TX on the left, decoded CW on the right.
- SSTV workspace: decoded image on the left, receive engine on the right.
- Local Radio service selection for FRS, Ham, GMRS, and CB handling.
- FRS supports VOX and Serial PTT configuration.
- RX decoder-bus controls moved behind compact settings controls.
- First Time Setup state is stored per Windows user under `%APPDATA%\RoscoRadio`, preventing another user's previous setup from suppressing onboarding.
- NexusUpdater support with version comparison, staged installation, backups, and the user's selected storage directory.

### v0.1.3 Beta

The v0.1.3 Beta introduced Rosco Radio's native **Satellite** workspace backed by an embedded SatDump processing runtime in packaged builds.

SatDump is GPL-3.0 software and retains its own copyright/license requirements. The Beta distribution includes third-party notices and SatDump integration documentation.

## First Time Setup

On a user's first launch, RR opens First Time Setup. Setup state is saved per Windows user rather than machine-wide, so updates keep an existing user's settings while new Windows users still receive onboarding.

## NexusUpdater

Rosco Radio uses **NexusUpdater** to check and install application updates. Matching versions report **Up to date** instead of reinstalling themselves. Update downloads, staging, and backups are stored below the RR storage directory selected during First Time Setup.

The GitHub Actions release workflow also mirrors NexusUpdater packages into GitHub Releases after verifying their hashes, so NexusUpdater remains the source of truth for published builds.

## Running from source

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Then launch:

```bash
python main.py
```

Packaged releases also contain RR media/runtime assets that are intentionally not duplicated as ordinary source files.

## Radio note

Rosco Radio is software, not authorization to transmit. Users are responsible for operating their equipment in accordance with the rules that apply to their radio service and equipment.

## License

See [`LICENSE`](LICENSE). Third-party components may carry their own licenses and notices.
