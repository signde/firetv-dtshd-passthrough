# Third-party notices and provenance

The MIT license applies to original project source and documentation. It does
not replace the licenses of Frida or any firmware components.

## Frida 17.22.2

The build packages the official `frida-inject-17.22.2-android-arm` executable.
It is not committed to this repository. Its core/gum license notices and the
referenced LGPL text are retained under licenses/. Upstream source and build
instructions: https://github.com/frida/frida/tree/17.22.2

Release: https://github.com/frida/frida/releases/tag/17.22.2

- Compressed SHA256: cb9621771f5922272ef64c51259b904027cb026d756864716fc98455f338d356
- Executable SHA256: 6a6d539f09cc2ed2679b8bdea3ce2cb343224adc6887d9fb227b5d1f41bebf07

## Firmware and research

No Amazon vendor libraries or captured media are distributed in this repository.
Firmware paths, hashes and offsets identify the verified integration points.
The native packer and lifecycle hooks are supplied in src/. Playback comparisons
used Kodi's working IEC output as a reference. Related implementation context:

- Kodi: https://github.com/xbmc/xbmc
- Plezy DTS work: https://github.com/edde746/plezy/commit/658469f9545398ab56835315796045716c6bc57f
- Magisk module format: https://topjohnwu.github.io/Magisk/guides.html

Amazon, Dolby, DTS, Kodi, Emby, Nova, Frida and Magisk names identify compatibility
or third-party components. This project is not endorsed by those projects or owners.
