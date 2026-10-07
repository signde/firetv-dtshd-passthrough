# Fire TV DTS-HD MA & DTS:X Passthrough

Experimental Magisk module that preserves full DTS-HD/DTS:X audio through the
verified Fire TV Cube 3 vendor audio path, where the stock packer emits DTS core.

**Version 0.1.3 experimental. Gazelle, Android 9 only.**
Installation, startup and the injected agent require one complete four-library
profile from [firmware/](firmware/). The supplied PS7688 through PS7717 builds
share the tested PS7702 audio code; newer HAL hashes differ only in build-ID
and debug metadata. This is static compatibility evidence, not playback
validation of every firmware. Karat and unknown library combinations are rejected.

| Exact library profile | Supplied matching builds |
| --- | --- |
| ps7688 | PS7688.4591, PS7690.4714/.4716, PS7696.5226/.5229, PS7699.4894/.4896, PS7702.4965, PS7704.5024, PS7706.5106, PS7707.5376, PS7710.6003, PS7711.5272, PS7712.5371 |
| ps7713 | PS7713.5443, PS7714.5503/.5506/.5507 |
| ps7715 | PS7715.5585, PS7716.5665, PS7717.5741 |

Profile names identify library families, not an unrestricted firmware-version
range. All four hashes must match the same profile. The packer, hook addresses
and firmware structure offsets are unchanged from v0.1.2.

## Requirements and installation

- Root and Magisk (tested with Magisk 30.2 and 30.7).
- The separate [Dolby passthrough module](https://github.com/signde/firetv-dolby-passthrough)
  installed and enabled. Version 0.3.2 is recommended: it maintains `hdmi_format=6`
  at boot, after sleep/wake, and following watched framework/audio restart events.
- A receiver advertising eight-channel DTS-HD at 192 kHz.
- Best Available in Fire OS; system passthrough in Emby/Nova.

Download the [v0.1.3 module ZIP](https://github.com/signde/firetv-dtshd-passthrough/releases/download/v0.1.3/firetv-dtshd-passthrough-v0.1.3.zip),
install it in Magisk and reboot. Allow roughly 65 seconds after Android
boot completes. GitHub's automatic source ZIP is not an installable module.
From a root shell:

```sh
cat /data/adb/modules/firetv_dtshd_passthrough/status.txt
tail -40 /data/adb/modules/firetv_dtshd_passthrough/service.log
```

Expected status: `ACTIVE` with the audio-service PID. Start a new playback after
activation. Disable/remove this module and reboot to undo it. Do not run the
earlier diagnostic hooks concurrently or force-kill module processes mid-playback.

## Implementation and validation

The native packer preserves DTS-HD access units and emits IEC61937 type-17 bursts.
The hooks correct transport timing to eight channels at 192 kHz and bound
calls to the vendor IEC decoder to 128 KiB.
Changes are in memory; vendor files and app APKs are not replaced. A bundled
standalone Frida injector needs no ADB connection, Mac or listening server during
operation. The installed module captures no audio bytes. Runtime supervision
waits for process exit and reattaches after an audio-service restart. Frida may
install injection-related SELinux allowances; SELinux remains enforcing.

Version 0.1.3 passed hardware checks on FC3b with PS7702.4965N, PS7714.5506N
and PS7717.5741N. The user confirmed in-person audio/video testing passed on all
three, covering one representative of each accepted library profile.
Instrumented Nova checks identified DTS-HD MA, DTS:X, DD+, DD+ Atmos and TrueHD
at the receiver. Pause/resume and post-wake DTS-HD playback were checked too.
On PS7717, Dolby v0.3.2 also recovered after a controlled framework restart;
DTS reattached and subsequent DD+ Atmos and DTS:X playback passed without manual
mode restoration. The runtime payloads are unchanged from those tested candidates.

Earlier PS7702/PS7714 runs with Dolby v0.3.1 needed manual restoration after late
bypass resets. The PS7714 reset followed a framework watchdog whose underlying
cause remains unproven. Dolby v0.3.2 handles watched restart events; it does not
prevent watchdogs or guarantee recovery from every possible mode reset.
Other accepted builds have static compatibility evidence, not individual playback
tests.

The corrected v0.1.2 package previously passed actual Magisk installation, reboot
activation and a user playback smoke test on FC3b alongside Dolby v0.3.1.

The earlier boot-loaded local v0.1.1 package passed user playback checks for DD, DD+, DTS-HD MA
and DTS:X in Emby, Nova and Kodi. Four patched HD sessions and thirteen
discontinuity resets had clean teardown and no errors. Scope: tested 48 kHz,
512-sample core frames. Receiver hotplug,
arbitrary source profiles and other firmware remain unvalidated. Already-working
Kodi passthrough continues to work; app/server transcoding cannot be undone here.

The Dolby dependency is explicit and remains unchanged in this source import.
Making DTS standalone requires its own tested boot/resume handling.

## Runtime behavior and troubleshooting

Version 0.1.2 also fixes the persistent manifest: Magisk removes the root README.md
and installer script after installation, so neither is required by boot-time checks.
Use v0.1.2 or later instead of the GitHub v0.1.1 ZIP, which failed this check.

Version 0.1.2 retains its native code for the entire script lifetime and forces
garbage collection before exercising native functions at startup. Only a passed
self-test allows `ACTIVE`. Version 0.1.0 had a native-code lifetime regression;
do not install it.

The installer, startup service and injected agent verify firmware compatibility.
Receiver capabilities and the supported first-buffer profile are checked before
each new DTS-HD stream is activated. Unsupported initial streams stay on the stock
path, as do streams already open when the module attaches.

There is no idle polling. Only startup and audio-service restarts trigger bounded
HDMI-mode checks; the Dolby module handles sleep/resume and, from v0.3.2, watched service restarts. Duplicate attachment to
the same audio process is refused. Three rapid audio-process exits latch a
`blocked` file in the module directory to prevent a restart loop. Inspect the logs
before clearing it. Never disable SELinux globally to work around a failure.
Runtime logs rotate at approximately 64 KiB.

Seek handling resets partial data at tested aligned resume/flush boundaries.
Stream cleanup restores decoder timing and forgets reused decoder addresses.
Active modified streams keep their script loaded until transport/decoder cleanup
finishes, preventing an unload from freeing active output buffers. A failure after
activation stops that stream's patched output; stop and reopen playback.
Unsupported or malformed first buffers fall back before any HD transport is emitted.
Full arbitrary-byte resynchronization is not implemented.

### Earlier prototype tests

Before persistent packaging, eight HD sessions and twelve seek/resume resets
passed in Emby and Nova system passthrough, with matching captured source HD units
and driver transport. Tested samples were:

- DTS-HD MA 7.1 Speaker Phase.mkv
- DTS-X 'Gravity' Demo.mkv
- DTS-X sound unbound callout 11.1.mkv
- DTS-X 'Movement' Demo.mts (Nova)

Emby encountered `DirectPlayError` on Movement and server-transcoded it to AC3
5.1 at 384 kbps, which this packer cannot reverse. Other sample rates, core frame
periods, receiver hotplug during playback and unrelated firmware are unvalidated.
Prototype results do not substitute for the packaged playback checks described above.

## Player limitations

The module needs the original DTS-HD stream to reach the system packing path.
It cannot recover HD extensions discarded by an app or undo server transcoding.
On PS7702, Plex 2026.19.1 blocked DTS passthrough and requested AAC transcoding
for the tested DTS samples. Jellyfin Android TV 0.19.10 output DTS core for the
Speaker Phase sample despite server DirectPlay, and requested AAC transcoding
for Gravity. Neither activated the HD transport fix. These player versions are
not verified working DTS-HD/DTS:X paths; they were not retested on PS7714/PS7717.
Earlier Emby/Nova/Kodi results do not establish support for every app or firmware.

## Build and checks

Requires Python 3.9+, Node.js and a POSIX shell. No pip/npm packages are needed.

```sh
python3 build.py --fetch-runtime
# Or use an existing official, uncompressed ARM32 runtime:
python3 build.py --runtime /path/to/frida-inject
python3 tests/run.py  # additionally requires clang with ASan/UBSan
python3 tests/package.py dist/firetv-dtshd-passthrough-v0.1.3.zip
# Optional external corpus check; vendor binaries are not included:
python3 tests/firmware.py /path/to/fireos_audio_libs dist/firetv-dtshd-passthrough-v0.1.3.zip
```

The download is pinned to Frida 17.22.2 and both compressed and uncompressed
SHA256 values are verified. Later offline builds can reuse `.cache/frida-inject`.
The builder generates runtime.js from src/, verifies syntax, creates the payload
manifest and writes an installable ZIP plus checksum to dist/. Generated files,
runtime binaries, captures and vendor libraries are not committed.
`src/native.c` contains the packer and `src/agent.js` handles integration and stream
lifetimes. Nothing is downloaded during installation or boot.

The native tests use synthetic framing for boundary, fragmentation, discontinuity,
capacity, error/reset and mute checks. They do not demonstrate audible decoding
or replace hardware testing. Build/archive hashes change when documentation changes;
release runtime payloads are compared with the installed, hardware-tested candidate.

## License and releases

Original project code is MIT licensed. Frida retains its own licenses, included
under licenses/; see [NOTICE.md](NOTICE.md) for source, dependency notices and
rebuild instructions. Each release also provides the pinned Frida source companion
archive and its checksum. That archive is for source access, not Magisk installation.
[CHANGELOG.md](CHANGELOG.md) records versions. No update feed or automated
publishing is configured. Keep the module ID `firetv_dtshd_passthrough` stable.
