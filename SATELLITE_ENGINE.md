# Rosco Radio Satellite Engine — v0.1.3 Beta

The Satellite workspace is a native Rosco Radio UI backed by the SatDump processing engine bundled in packaged Beta builds under `runtime/satdump/`.

Users do not select a SatDump executable and RR does not launch the SatDump UI.

Runtime flow:

1. User chooses a recording and pipeline in Rosco Radio.
2. RR invokes the embedded SatDump processing backend internally.
3. SatDump loads its bundled pipelines/plugins/resources from the runtime folder.
4. RR streams processing status into the Satellite activity panel.
5. Products are written to the RR Satellite output directory.

The engine can also run SDR probing from the RR Satellite interface to enumerate supported SDR hardware.
