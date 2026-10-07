#!/system/bin/sh
# Accept a complete verified library set, never a mixture of profiles.
verify_firmware() {
    for profile in "$1"/firmware/*.sha256; do
        [ -f "$profile" ] || continue
        sha256sum -c "$profile" >/dev/null 2>&1 && return 0
    done
    return 1
}
