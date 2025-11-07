# Additional Resources

**Last Updated:** 2025-11-07
**Status:** ✅ Complete

> **Note:** This page contains external links to resources from the original tuya-convert project and third-party tools.

## Related Projects

For a comprehensive overview of alternative flashing tools, firmware projects, and chipset-specific solutions, see:

**👉 [Related Projects and Ecosystem](Related-Projects.md)**

This includes:
- **tuya-cloudcutter** - OTA flashing for BK7231 and other non-ESP chips
- **OpenBeken** - Alternative firmware for BK7231T/N, ECR6600, RTL8xxx, W800, and more
- **TuyAPI** - Local control with stock firmware (no flashing required)
- **Zigbee and BLE projects** - For Telink and Phyplus based devices
- PSK v2 status across all projects
- Hardware coverage comparison

## Video Tutorials

**Video walkthrough** (from original tuya-convert project):
https://github.com/ct-Open-Source/tuya-convert/issues/42

## Third-Party Tools

### OTA Flashing Alternatives

**tuya-cloudcutter** - Successor to tuya-convert supporting BK7231 and other non-ESP chips
- Repository: https://github.com/tuya-cloudcutter/tuya-cloudcutter
- Device database: https://tuya-cloudcutter.github.io/
- Supports: BK7231T/N, BL2028N, ESP8266/ESP8285
- **Note:** Partially affected by PSK v2, but some workarounds exist

### Alternative Firmware

**OpenBeken** - Firmware for non-ESP chips (BK7231, ECR6600, RTL8xxx, W800)
- Repository: https://github.com/openshwprojects/OpenBK7231T_App
- Flash tools: https://github.com/openshwprojects/FlashTools
- Device database: https://openbekeniot.github.io/webapp/devicesList.html
- **Use when:** Device has non-ESP chip (see [Alternative Chips Guide](Alternative-Chips-And-Flashing.md))

**Tasmota** - Popular ESP firmware (included in tuya-convert)
- Repository: https://github.com/arendst/Tasmota
- Device templates: https://templates.blakadder.com/
- Documentation: https://tasmota.github.io/docs/

**ESPurna** - Lightweight ESP firmware (included in tuya-convert)
- Repository: https://github.com/xoseperez/espurna
- Documentation: https://github.com/xoseperez/espurna/wiki

### Local Control Without Flashing

**TuyAPI** - Node.js library for LAN control with stock firmware
- Repository: https://github.com/codetheweb/tuyapi
- No firmware flash required
- Requires device key extraction

**tinytuya** - Python module for Tuya device control
- Repository: https://github.com/jasonacox/tinytuya
- Local and cloud API support
- Device discovery and monitoring

### Virtualization

**Proxmox - Tuya-Convert LXC environment**: https://github.com/whiskerz007/proxmox_tuya-convert_container

### Setup Proxmox Community Version

For the above Proxmox script to work, you may need to setup the community version. Copy and paste the entire section below and run once:
```
# Disable Commercial Repo
sed -i "s/^deb/\#deb/" /etc/apt/sources.list.d/pve-enterprise.list
apt-get update

# Add PVE Community Repo
echo "deb http://download.proxmox.com/debian/pve $(grep "VERSION=" /etc/os-release | sed -n 's/.*(\(.*\)).*/\1/p') pve-no-subscription" > /etc/apt/sources.list.d/pve-no-enterprise.list
apt-get update

# Remove nag
echo "DPkg::Post-Invoke { \"dpkg -V proxmox-widget-toolkit | grep -q '/proxmoxlib\.js$'; if [ \$? -eq 1 ]; then { echo 'Removing subscription nag from UI...'; sed -i '/data.status/{s/\!//;s/Active/NoMoreNagging/}' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js; }; fi\"; };" > /etc/apt/apt.conf.d/no-nag-script
apt --reinstall install proxmox-widget-toolkit
```