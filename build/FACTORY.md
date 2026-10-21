# Github factory distribution

Run **Build Rosco Radio Github Factory** from GitHub Actions to produce
`RoscoRadio-Github-Factory.zip` and its SHA-256 checksum. This workflow builds
an artifact; it does not publish or replace existing GitHub release assets.

Extract the ZIP into a writable folder and launch `run.bat` on Windows.
The source distribution requires Python 3.12+; the launcher installs its
dependencies as with the existing RR packages.

The factory uses a pinned, checksum-verified v0.1.6 source base and identifies
itself as `0.0.0` for update comparisons. This lets the normal Updates tab
offer the current NexusUpdater build even when it is the same version as
the source base. The factory is a starting distribution, not a new numbered
Stable or Beta release.

Home checks the selected NexusUpdater channel asynchronously and displays:

> This is the factory Github install. Please update to [version-grabbed-from-NU] under the Updates tab to unlock the latest features.

The version comes from the same manifest check that enables the install
button. Open Updates navigates to that tab; the user still chooses to
download and install. Offline failures leave the app usable and can be
retried there. The factory performs its startup check even if an existing
user previously disabled automatic checks.

Updates retain the existing HTTPS download, SHA-256 validation, backup,
replacement and restart flow. The complete NU package replaces the factory
source, removing the landing notice without changing per-user settings.
The update server's `/health` version is the NexusUpdater server version;
the landing announcement uses the `rosco-radio` manifest version instead.

This intentionally stays a source ZIP: the current helper launches via
`sys.executable`, which requires a Python interpreter and is not compatible
with simply freezing `main.py` into a one-file EXE.
