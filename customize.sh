#!/system/bin/sh
SKIPMOUNT=true
[ "$BOOTMODE" = true ] || abort "Install from Magisk in Fire OS."
. "$MODPATH/verify-firmware.sh"
verify_firmware "$MODPATH" || abort "Unsupported audio libraries. No DTS patch installed."
(cd "$MODPATH" && sha256sum -c payload.sha256 >/dev/null 2>&1) || abort "Module payload checksum mismatch."
DOLBY=/data/adb/modules/gazelle_ddplus_bypass
[ -f "$DOLBY/module.prop" ] && [ ! -e "$DOLBY/disable" ] && [ ! -e "$DOLBY/remove" ] || abort "Enable the separate Fire TV Dolby passthrough module first."
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/service.sh" 0 0 0755
set_perm "$MODPATH/bin/frida-inject" 0 0 0700
ui_print "Verified $FIRMWARE_PROFILE audio libraries. Installing separate DTS companion."
ui_print "Existing Dolby module is unchanged. No vendor files are replaced."
ui_print "Experimental: tested 48 kHz DTS-HD MA/DTS:X streams and DTS-HD capable receivers."
ui_print "Reboot to activate. Disable/remove this module and reboot to undo."
