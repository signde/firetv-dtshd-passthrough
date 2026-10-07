# Changelog

## 0.1.3 (experimental)

- Accept three exact four-library profiles covering the 21 supplied PS7688
  through PS7717 builds. Two newer HAL hashes differ only in metadata.
- Share profile selection between installation and startup; require the same
  complete profile in the injected agent. Unknown combinations remain rejected.
- Keep audio hooks, structure offsets, native packer and Frida unchanged.
- Add corpus checks for allowed, older, corrupt and mixed library sets.
- Hardware checks and user audio/video confirmation passed on PS7702.4965N,
  PS7714.5506N and PS7717.5741N, one representative of each accepted profile.
  Other listed builds have static compatibility evidence only.

## 0.1.2 (experimental)

- Exclude root README.md from the persistent payload manifest because Magisk
  removes it after installation. This fixes startup rejection of the GitHub
  v0.1.1 ZIP after an actual install.
- Preserve the tested audio hooks, packer and Frida runtime.
- Pass actual Magisk install, reboot activation and user playback smoke testing
  on FC3b with Dolby v0.3.1; add a post-install cleanup regression check.

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

## Release packaging

- Include the pinned dependency inventory, component notices and source companion.
- Document rebuilding/relinking and replacing the integrity-pinned Frida runtime.
- Keep the official Frida binary and tested audio hooks unchanged.

## Source repository preparation

- Add an explicit build file list, pinned runtime retrieval and synthetic native tests.
- Preserve the verified v0.1.1 runtime and the existing Dolby companion dependency.
- No new device deployment or runtime behavior change.
