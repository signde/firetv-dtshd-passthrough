# Third-party notices and provenance

The MIT license applies to original project source and documentation. It does
not replace the licenses of Frida or any firmware components.

## Frida 17.22.2

The build packages the official `frida-inject-17.22.2-android-arm` executable.
It is not committed to this repository. The module ZIP includes component notices
under licenses/. A pinned source companion is published on the same release:
`frida-17.22.2-source-and-notices.tar.gz`.

See [the dependency inventory](third_party/frida/README.md),
[source manifest](third_party/frida/source-manifest.json), and
[rebuild/relink instructions](third_party/frida/BUILDING.md).
Those materials cover the additional LGPL and permissively licensed components;
Frida's top-level wxWindows exception does not override their individual terms.

Upstream: https://github.com/frida/frida/tree/17.22.2

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
