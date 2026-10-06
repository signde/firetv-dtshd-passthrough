# Fire TV DTS-HD MA & DTS:X Passthrough

Experimental Magisk module that preserves full DTS-HD/DTS:X audio through the
verified Fire TV Cube 3 vendor audio path, where the stock packer emits DTS core.

**Version 0.1.1. Supported: Gazelle, Fire OS PS7702.4965N, Android 9.**
Installation and startup require exact matches for all four libraries listed in
[firmware.sha256](firmware.sha256). Karat and other firmware are not supported.

## Requirements and installation

- Root and Magisk (tested with Magisk 30.2).
- The separate [Dolby passthrough module](https://github.com/signde/firetv-dolby-passthrough)
  installed and enabled. It maintains `hdmi_format=6` at boot and after sleep/wake.
- A receiver advertising eight-channel DTS-HD at 192 kHz.
- Best Available in Fire OS; system passthrough in Emby/Nova.

Install the built ZIP in Magisk and reboot. Allow roughly 65 seconds after Android
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

The boot-loaded v0.1.1 package passed user playback checks for DD, DD+, DTS-HD MA
and DTS:X in Emby, Nova and Kodi. Four patched HD sessions and thirteen
discontinuity resets had clean teardown and no errors. Scope: tested 48 kHz,
512-sample core frames. See [VALIDATION.txt](VALIDATION.txt). Receiver hotplug,
arbitrary source profiles and other firmware remain unvalidated. Already-working
Kodi passthrough continues to work; app/server transcoding cannot be undone here.

The Dolby dependency is explicit and remains unchanged in this source import.
Making DTS standalone requires its own tested boot/resume handling.

## Runtime behavior and troubleshooting

Version 0.1.1 retains its native code for the entire script lifetime and forces
garbage collection before exercising native functions at startup. Only a passed
self-test allows `ACTIVE`. Version 0.1.0 had a native-code lifetime regression;
do not install it.

The installer, startup service and injected agent verify firmware compatibility.
Receiver capabilities and the supported first-buffer profile are checked before
each new DTS-HD stream is activated. Unsupported initial streams stay on the stock
path, as do streams already open when the module attaches.

There is no idle polling. Only startup and audio-service restarts trigger bounded
HDMI-mode checks; the Dolby module handles sleep/resume. Duplicate attachment to
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
Prototype results do not substitute for packaged playback checks; the successful
persistent v0.1.1 checks are recorded separately in [VALIDATION.txt](VALIDATION.txt).

## Build and checks

Requires Python 3.9+, Node.js and a POSIX shell. No pip/npm packages are needed.

```sh
python3 build.py --fetch-runtime
# Or use an existing official, uncompressed ARM32 runtime:
python3 build.py --runtime /path/to/frida-inject
python3 tests/run.py  # additionally requires clang with ASan/UBSan
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
runtime equivalence to the tested v0.1.1 package is checked separately.

## License and releases

Original project code is MIT licensed. Frida retains its own licenses, included
under licenses/; see [NOTICE.md](NOTICE.md) for source, dependency notices and
rebuild instructions. Each release also provides the pinned Frida source companion
archive and its checksum. That archive is for source access, not Magisk installation.
[CHANGELOG.md](CHANGELOG.md) records versions. No update feed or automated
publishing is configured. Keep the module ID `firetv_dtshd_passthrough` stable.
