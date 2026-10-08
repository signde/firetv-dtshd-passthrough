# Changelog

## 0.2.0 (experimental)

- Add Stick 4K Max 2 / Karat support for 14 reviewed builds from RS8145 to RS8182.
- Select the correct audio patch automatically for Gazelle or Karat.
- Playback-tested on Karat RS8182.3811N, including boot, sleep/wake and audio-HAL
  recovery. Existing Gazelle audio behavior is unchanged.

## 0.1.3 (experimental)

- Expand Cube 3 support to 21 reviewed builds from PS7688 to PS7717.
- Playback-tested on PS7702.4965, PS7714.5506 and PS7717.5741.

## 0.1.2 (experimental)

- Fix boot-time verification after Magisk removes installer-only files.

## 0.1.1 (experimental)

- Fix the native-code lifetime issue that caused first-playback failures.
- Add a startup self-test before activating the patch.

## 0.1.0 (superseded, do not install)

- Initial DTS-HD MA/DTS:X module for Cube 3, with boot activation and restart
  handling. Playback failures were corrected in subsequent releases.
