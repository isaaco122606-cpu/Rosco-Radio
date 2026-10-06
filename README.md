# Rosco Radio

**The long-awaited solution to the endless pile of separate radio apps.**

Rosco Radio (RR) is a Windows-focused radio workspace that brings WebSDR reception, local radio audio, CW/Morse tools, SSTV, radio utilities, session logging, and NexusUpdater into one interface.

## Current versions

- **Stable:** `v0.1.2`
- **Beta:** `v0.1.3`

The Stable build is the recommended version for normal use. The Beta build contains newer features that are still being tested.

## v0.1.2 Stable

Highlights include:

- Redesigned WebSDR workspace: WebSDR page on the left, receiver data on the right.
- CW workspace: Automatic Morse TX on the left, decoded CW on the right.
- SSTV workspace: decoded image on the left, receive engine on the right.
- Local Radio service selection for FRS, Ham, GMRS, and CB handling.
- FRS supports VOX and Serial PTT configuration.
- RX decoder-bus controls moved behind compact settings controls.
- First Time Setup state is stored per Windows user under `%APPDATA%\RoscoRadio`, preventing another user's previous setup from suppressing onboarding.
- NexusUpdater support with version comparison, staged installation, backups, and the user's selected storage directory.

## v0.1.3 Beta

The Beta adds Rosco Radio's native **Satellite** workspace backed by an embedded SatDump processing runtime in packaged builds.

SatDump is GPL-3.0 software and retains its own copyright/license requirements. The Beta distribution includes third-party notices and SatDump integration documentation.

## First Time Setup

On a user's first launch, RR opens First Time Setup. Setup state is saved per Windows user rather than machine-wide, so updates keep an existing user's settings while new Windows users still receive onboarding.

## NexusUpdater

Rosco Radio uses **NexusUpdater** to check and install application updates. Matching versions report **Up to date** instead of reinstalling themselves. Update downloads, staging, and backups are stored below the RR storage directory selected during First Time Setup.

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
