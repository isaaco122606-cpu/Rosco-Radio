# Rosco Radio v0.1.3 Beta

This branch tracks the current Rosco Radio Beta line.

## Added in v0.1.3 Beta

- Native Rosco Radio **Satellite** workspace.
- Embedded SatDump processing runtime in packaged Beta builds.
- Satellite output stored under the RR storage directory.
- SDR probing and recorded/baseband processing routed through RR's interface.
- Same v0.1.2 UI/FTS fixes carried forward into Beta.
- New **Time Station** Beta workspace with a guided setup tree.
- Time Station setup asks, in order: license status, K1-style radio interface, clock synchronization confirmation, Local vs UTC, then station details.
- Scheduled ten-minute station-identification audio uses VOX-first Local Radio TX audio.
- GMRS recurring one-way Time Station RF remains preview-only in RR Beta; amateur scheduled VOX requires operator-responsibility acknowledgement.

## Package

Current Time Station test package:

`RoscoRadio-v0.1.3-beta-TimeStation.zip`

SHA-256:

`f75a864a99bbbad63f0e909abc882fbe78626f906113735d22338dee22332e06`

See `TIME_STATION.md` for the setup tree and station-ID behavior.

## Third-party component

The packaged Beta contains SatDump as a separate processing backend invoked by Rosco Radio. SatDump is GPL-3.0 software and retains its upstream copyright/license obligations. See `SATELLITE_THIRD_PARTY_NOTICE.txt`.
