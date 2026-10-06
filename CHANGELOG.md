# Changelog

## 0.1.1 (experimental)

- Retain native code for the lifetime of the injected script, fixing the packaged
  v0.1.0 first-playback failure caused by garbage collection.
- Force collection and exercise native functions before declaring the module ready.
- Validated after reboot with Emby, Nova and Kodi, including DD/DD+ regressions
  and DTS-HD MA/DTS:X playback. Logs confirm seek handling and clean stream teardown.

## 0.1.0 (superseded, do not install)

- Initial separate persistent DTS module with firmware checks, full-HD packing,
  transport/timing corrections, stream cleanup and audio-service restart handling.
- Boot supervision worked, but packaged DTS playback failed. Fixed in 0.1.1.

## Source repository preparation

- Add an explicit build file list, pinned runtime retrieval and synthetic native tests.
- Preserve the verified v0.1.1 runtime and the existing Dolby companion dependency.
- No new device deployment or runtime behavior change.
