# Fire TV DTS-HD MA & DTS:X Passthrough

Experimental Magisk module that enables full DTS-HD MA and DTS:X passthrough
where Fire OS normally outputs DTS core.

Supports **Fire TV Cube 3 (Gazelle, Fire OS 7)** and **Fire TV Stick 4K Max 2
(Karat, Fire OS 8)**. Requires the separate
[Dolby passthrough module](https://github.com/signde/firetv-dolby-passthrough).

**Version 0.2.0 (experimental).**

## Supported firmware

**User-tested** builds have passed device playback tests. **Static review** means
the relevant libraries match the working patch, but that build has not been
playback-tested. Installation checks library hashes and rejects unknown combinations.

### Cube 3 / Gazelle

| User-tested builds | Static review only |
| --- | --- |
| PS7702.4965 | PS7688.4591, PS7690.4714/.4716, PS7696.5226/.5229, PS7699.4894/.4896, PS7704.5024, PS7706.5106, PS7707.5376, PS7710.6003, PS7711.5272, PS7712.5371 |
| PS7714.5506 | PS7713.5443, PS7714.5503/.5507 |
| PS7717.5741 | PS7715.5585, PS7716.5665 |

### Stick 4K Max 2 / Karat

| Fire OS | Build(s) | Status |
| --- | --- | --- |
| 8.1.4.5 | RS8145.3070N | Static review |
| 8.1.4.9 | RS8149.3133N | Static review |
| 8.1.5.3 | RS8153.3202N | Static review |
| 8.1.5.5 | RS8155.3474N | Static review |
| 8.1.5.8 | RS8158.4105N | Static review |
| 8.1.6.0 | RS8160.3372N, RS8160.3380N | Static review |
| 8.1.6.6 | RS8166.3482N | Static review |
| 8.1.6.9 | RS8169.3556N | Static review |
| 8.1.7.4 | RS8174.3641N, RS8174.3648N | Static review |
| 8.1.8.0 | RS8180.3729N, RS8180.3739N | Static review |
| 8.1.8.2 | RS8182.3811N | User-tested |

RS8185.3879N has not been reviewed. Karat support starts with module v0.2.0.

## App results

Observed output with the tested samples:

| App | Cube 3 / Gazelle | Stick 4K Max 2 / Karat |
| --- | --- | --- |
| Nova, system passthrough | DTS-HD MA, DTS:X | DTS-HD MA, DTS:X |
| Emby | DTS-HD MA, DTS:X | DTS-HD MA, DTS:X |
| Kodi 21 | DTS-HD MA, DTS:X | DTS-HD MA, DTS:X |
| Plex 2026.19.1 | AAC transcode | DTS-HD MA, DTS:X |
| Jellyfin Android TV 0.19.10 | DTS core or AAC transcode | DTS core |

Karat results use RS8182.3811N, Nova 6.4.3, Emby 3.5.63 (`com.mb.android`)
and Kodi 21.3. Installation, reboot, sleep/wake and audio-HAL recovery were tested.
Gazelle's Plex/Jellyfin results are from PS7702. Kodi uses its own packer and does
not need this module. App/server transcoding cannot be reversed by the module.

## Installation

You need root, Magisk, a supported firmware, and a receiver or TV/eARC chain
advertising eight-channel DTS-HD at 192 kHz.

1. Install and enable the **Dolby passthrough module**, preferably v0.3.2 or newer.
   It maintains the required HDMI bypass mode.
2. Set Fire OS audio to **Best Available** and enable passthrough in your player.
   In Nova, choose **system passthrough**.
3. Install the DTS module ZIP in Magisk and reboot. Allow about a minute after
   boot before starting playback.

Use the module ZIP from [Releases](https://github.com/signde/firetv-dtshd-passthrough/releases),
not GitHub's automatic source ZIP. To uninstall, disable/remove the module in
Magisk and reboot.

## Troubleshooting

From a root shell:

```sh
cat /data/adb/modules/firetv_dtshd_passthrough/status.txt
tail -40 /data/adb/modules/firetv_dtshd_passthrough/service.log
```

Look for `ACTIVE`, then start a new playback. If a stream fails, stop and reopen
it. Do not run older trial hooks alongside the module. Repeated audio-service
failures stop further attachment; inspect the logs before retrying.

The tested audio profile is 48 kHz DTS-HD with 512-sample core frames. Other source
profiles and receiver hotplug during playback remain untested.

## How it works

The module replaces the system DTS packing path in memory, preserving HD audio
in IEC61937 bursts. Vendor libraries and app APKs are not replaced. A bundled
Frida runtime operates on-device without ADB or a computer. It captures no audio
and does not poll the audio service while idle.

## License

Project code is MIT licensed. Frida retains its own licenses; see
[NOTICE.md](NOTICE.md) for dependency licenses and notices.
Releases include a Frida source companion archive, which is not a Magisk module.
See [CHANGELOG.md](CHANGELOG.md) for version history.
