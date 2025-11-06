# Issue #1145 Summary: Teckin SP25 "Dead" Device (User Error)

## Quick Facts

- **Issue**: #1145 - "Teckin/Tuya SP25 Plug: dead after post-wifi-reboot"
- **Reporter**: STR4NG3RdotSH
- **Date**: 2024-12-05
- **Status**: 📦 **ARCHIVED** (User Error - Self-Resolved)
- **Device**: Teckin/Tuya SP25 smart plug

## Problem

User reported device appeared "dead" after successful firmware flash:
- No power response
- Not visible on network
- USB and outlet outputs non-functional

## Resolution

**User Error**: Device was working correctly all along. User was searching for the wrong MAC address in their router's connected devices list.

## How It Was Resolved

1. User applied fast power cycle recovery (6x power reinsertion)
2. Device entered configuration mode
3. User reconfigured WiFi settings
4. User checked router again and found device connected
5. Realized they had been looking for incorrect MAC address

## Key Points

- **Not a Bug**: tuya-convert and Tasmota worked perfectly
- **Device Status**: ✅ Fully functional throughout
- **Root Cause**: User verification error (wrong MAC address)
- **Learning**: Demonstrates effective use of fast power cycle recovery

## Educational Value

### Fast Power Cycle Recovery

**How to use**:
- Unplug/replug device 6 times rapidly
- Device enters configuration mode
- Creates WiFi AP for reconfiguration
- Feature of Tasmota/ESPHome firmware, not tuya-convert

**When to use**:
- Device appears unresponsive after flash
- Changed WiFi network
- Troubleshooting connectivity
- Forgot device IP

### Post-Flash Verification Best Practices

1. ✅ Note MAC address from tuya-convert logs (not device label)
2. ✅ Wait 2-3 minutes for device to boot and connect
3. ✅ Check router for new devices (may appear as "ESP_XXXX")
4. ✅ Scan network with nmap or similar tools
5. ✅ Look for devices with Espressif vendor ID

### Common MAC Address Confusion

**Why users get wrong MAC**:
- Pre-flash firmware MAC vs post-flash ESP MAC differ
- Multiple interfaces on device
- Different MAC formats (uppercase/lowercase, separators)
- Physical label MAC vs actual WiFi MAC

## Device Compatibility

**Teckin SP25**: ✅ Confirmed working
- Successfully flashes with tasmota-lite.bin
- Fast power cycle recovery works
- Standard ESP8266 behavior

## Potential Documentation Improvements

While not required (this is user error), docs could be enhanced:

1. **Post-flash verification guide** - How to confirm successful flash
2. **Fast power cycle recovery** - Document this useful feature
3. **Troubleshooting "dead" devices** - Common causes and solutions
4. **MAC address guidance** - Where to find correct MAC

## Related Issues

None - this is an isolated user error case.

## Impact

**Before**: User confused, thought device was bricked
**After**: User found device working correctly, learned recovery technique

**For Community**:
- Validates tuya-convert works on Teckin SP25
- Documents fast power cycle recovery usage
- Shows common post-flash confusion pattern

## References

- Full analysis: `analysis.md`
- Tasmota recovery: https://tasmota.github.io/docs/Device-Recovery/
- Upstream: https://github.com/ct-Open-Source/tuya-convert/issues/1145

---

**Status**: 📦 Archived - User error, no action needed
**Documentation**: 2025-11-06
**Priority**: Low (optional doc improvements only)
