# Issue #1145: Teckin/Tuya SP25 Plug: dead after post-wifi-reboot

**Reporter**: STR4NG3RdotSH
**Date Posted**: 2024-12-05
**Status**: 📦 Archived (User Error - Self-Resolved)
**Upstream**: https://github.com/ct-Open-Source/tuya-convert/issues/1145
**Related Issues**: None

---

## Executive Summary

User reported a Teckin SP25 smart plug appearing "dead" after successful firmware flash and WiFi configuration. After troubleshooting with the fast power cycle recovery method, the user discovered the device was actually working correctly - they had been searching for the wrong MAC address on their network. This is a user error case, not a tuya-convert bug or issue, but provides valuable documentation of the recovery process and common troubleshooting mistakes.

---

## Problem Description

### Context

User STR4NG3RdotSH successfully flashed a Teckin/Tuya SP25 smart plug using tuya-convert with `tasmota-lite.bin` firmware. The flash process completed successfully, and WiFi configuration was entered. However, after the post-setup reboot, the device appeared to be completely unresponsive.

### The Core Issue

**Initial symptoms reported**:
- Device would not power back on after reboot
- No response to power cycling
- Device not appearing on WiFi network
- Both USB and standard outlet power outputs non-functional
- No LED indicators or signs of life

**User's troubleshooting attempts**:
1. Power cycled the device multiple times
2. Held power button while unplugged to discharge capacitors
3. Verified device wasn't appearing on WiFi network scans
4. Tested both USB and outlet power functionality
5. Applied "fast power cycle device recovery" method (6x power reinsertion)

### Resolution

After using the fast power cycle recovery method, the device returned to configuration mode. Upon reconfiguring WiFi and allowing another reboot, the user checked their gateway's connected devices list and discovered:

**The device had successfully connected to the network all along** - the user had been searching for the wrong MAC address.

---

## Technical Analysis

### Current Implementation

tuya-convert works as designed. The flashing process completed successfully. The device booted correctly with new firmware and connected to WiFi as expected.

### Root Cause

**User Error**: The user was looking for an incorrect MAC address in their router's connected devices list.

**Common Sources of MAC Address Confusion**:

1. **Pre-flash vs Post-flash MAC**:
   - Original Tuya firmware may have used one MAC address
   - After flashing with Tasmota/custom firmware, the device uses the ESP chip's actual MAC
   - Users may note down the wrong MAC during the process

2. **Multiple interfaces**:
   - Some devices may display different MACs for different purposes
   - WiFi MAC vs physical label MAC may differ

3. **DHCP lease timing**:
   - Device may take time to appear in router's active devices list
   - Old lease from original firmware may still be showing

4. **Network scanning tools**:
   - Different tools may show MACs in different formats (uppercase/lowercase, colon vs dash separators)

### Why This Appeared to Be a Hardware Failure

The symptoms mimicked complete device failure:
- No immediate network visibility
- User performed extensive power cycling (which is normal troubleshooting)
- Fast power cycle recovery put device back into config mode

However, the fast power cycle recovery is a **feature, not a fix** - it's designed to reset devices to config mode for troubleshooting, which is exactly what happened.

### Why This Matters

**Documentation Value**:
- Demonstrates effective use of fast power cycle recovery
- Shows common post-flash troubleshooting confusion
- Validates that tuya-convert works correctly on Teckin SP25 devices
- Provides template for similar user confusion issues

**Not a Software Issue**:
- No bug in tuya-convert
- No bug in Tasmota firmware
- Device functioned correctly throughout
- User verification process was incomplete

---

## Proposed Solution

### For This Specific Issue

**Status**: Already resolved - user error, device working correctly.

No code changes needed.

### For Future Users

**Documentation improvements** that could prevent similar confusion:

#### 1. Add Post-Flash Verification Guide

Update documentation to include clear steps for verifying successful flash:

```markdown
## Verifying Your Device After Flashing

After flashing and WiFi configuration, your device should reboot and connect to your network. To verify:

1. **Find the correct MAC address:**
   - Check tuya-convert output logs for the device MAC (shown during flash)
   - The MAC is the ESP chip's actual address, not the manufacturer's label
   - Format: XX:XX:XX:XX:XX:XX (may appear in different formats on different tools)

2. **Check your router:**
   - Wait 1-2 minutes for device to appear
   - Look in DHCP leases or connected devices
   - Search for devices connected in the last 5 minutes
   - May appear as "ESP_XXXXXX" or similar hostname

3. **Scan your network:**
   - Use tools like: nmap, arp-scan, Fing, or your router's admin interface
   - Look for new devices with ESP vendor ID (Espressif Inc.)

4. **Access the device:**
   - For Tasmota: Check for new access point "tasmota-XXXX" or scan for device IP
   - For ESPHome: Device should appear in ESPHome dashboard
   - For custom firmware: Follow firmware-specific instructions
```

#### 2. Document Fast Power Cycle Recovery

Add clear explanation of this recovery feature:

```markdown
## Fast Power Cycle Recovery

Many ESP-based smart plugs include a recovery feature that detects rapid power cycling:

**How to use:**
1. Unplug the device
2. Plug it back in
3. Immediately unplug again
4. Repeat 5-6 times within 10 seconds

**What happens:**
- Device enters configuration mode (safe mode)
- WiFi AP is created (usually "tasmota-XXXX" for Tasmota)
- Allows you to reconfigure WiFi settings
- Does NOT erase your firmware

**When to use:**
- Device appears unresponsive after flashing
- Changed WiFi network and device can't connect
- Forgot device IP address
- Troubleshooting connectivity issues

**Important:** This is a FEATURE of the firmware (Tasmota, ESPHome, etc.), not a tuya-convert recovery method. Only works AFTER successfully flashing custom firmware.
```

#### 3. Create Troubleshooting Flowchart

Add to FAQ or troubleshooting docs:

```markdown
## Device Appears Dead After Flashing - Troubleshooting

1. **Wait 2-3 minutes** - Device may be booting slowly
2. **Check for new WiFi AP** - Many firmwares create AP if can't connect
3. **Verify MAC address** - Check tuya-convert logs for actual MAC
4. **Scan network** - Use nmap or router admin panel
5. **Try fast power cycle recovery** - See above
6. **Check power** - Ensure plug is receiving power (test with another device)
7. **Serial connection** - Advanced: Connect via serial for debugging

Most "dead" devices are actually working but not where you're looking for them.
```

### Rationale

These documentation improvements would:
- ✅ Reduce false reports of "dead" devices
- ✅ Help users verify successful flashes
- ✅ Teach proper post-flash troubleshooting
- ✅ Reduce maintainer support burden
- ✅ Document the fast power cycle recovery feature

### Compatibility

Documentation changes only - no code impact.

---

## Testing Strategy

Not applicable - this was user error, not a software issue.

### Validation

✅ User confirmed device was working correctly
✅ Fast power cycle recovery worked as designed
✅ tuya-convert successfully flashed Teckin SP25
✅ Tasmota firmware booted and connected to WiFi

---

## Implementation

N/A - No code changes required.

### Potential Documentation Updates

**Files that could be updated** (optional):

1. **docs/Troubleshooting.md** or similar:
   - Add post-flash verification guide
   - Document fast power cycle recovery
   - Add "device appears dead" troubleshooting section

2. **docs/FAQ.md**:
   - Q: "My device appears dead after flashing, is it bricked?"
   - A: Probably not - see troubleshooting guide

3. **README.md**:
   - Link to post-flash verification guide in "What's Next" section

### Testing Results

User successfully resolved their own issue by:
1. Using fast power cycle recovery feature
2. Reconfiguring WiFi
3. Finding device on network using correct MAC address

---

## Related Work

### Related Issues

No directly related tuya-convert issues - this is user error.

**Similar patterns** (hypothetical):
- Users confusing device states
- Post-flash verification confusion
- MAC address identification issues

### Related Documentation

**Tasmota Recovery Documentation**:
- https://tasmota.github.io/docs/Device-Recovery/
- Documents the fast power cycle recovery feature

**ESPHome Recovery**:
- https://esphome.io/guides/faq.html#device-not-responding

### Related Commits

None - no code changes needed.

---

## Timeline

- **2024-12-05**: Issue reported by STR4NG3RdotSH
- **2024-12-05**: User performed troubleshooting
- **2024-12-05**: User discovered device was actually working (wrong MAC address)
- **2024-12-05**: Issue self-resolved
- **2025-11-06**: Issue analyzed and archived as user error

---

## Notes

### Why Archive Instead of Close?

This issue is archived in our tracking system because:
1. ✅ **Not a bug** - tuya-convert and firmware worked correctly
2. ✅ **User error** - Wrong MAC address verification
3. ✅ **Self-resolved** - User found their own answer
4. ✅ **Documentation value** - Shows common confusion pattern
5. ✅ **Educational** - Demonstrates fast power cycle recovery usage

### Key Learnings

**For users**:
- Always verify the correct MAC address from tuya-convert logs
- "Dead" devices are often just connected with unexpected MAC/hostname
- Fast power cycle recovery is a firmware feature, not a fix
- Wait adequate time (2-3 minutes) for device to boot and connect

**For maintainers**:
- Post-flash verification documentation could reduce support burden
- Fast power cycle recovery should be prominently documented
- Common troubleshooting flowcharts would help users self-resolve

**For documentation**:
- Need clear post-flash verification guide
- Should document fast power cycle recovery feature
- Troubleshooting section for "appears dead" scenarios would help

### Open Questions

None - issue fully understood and resolved.

### Future Improvements

**Optional documentation enhancements** (not required, but helpful):

1. Add video or screenshots showing:
   - Where to find MAC in tuya-convert logs
   - How to locate device in router admin panel
   - Fast power cycle recovery demonstration

2. Create post-flash checklist:
   - [ ] Note MAC address from logs
   - [ ] Wait 2-3 minutes
   - [ ] Check router for new device
   - [ ] Scan network if needed
   - [ ] Try fast power cycle if still not found

3. Add common device hostnames after flashing:
   - Tasmota: "tasmota-XXXX" or "ESP_XXXX"
   - ESPHome: User-configured name
   - Generic ESP: "ESP_XXXX"

### Device Compatibility Note

**Teckin SP25**: ✅ Confirmed working with tuya-convert
- Successfully flashes with tasmota-lite.bin
- Fast power cycle recovery works correctly
- Standard ESP8266-based device behavior

---

## Recommendation

### For Upstream Repository

**Action**: Close issue #1145 as "User Error - Working as Designed"

**Suggested Comment**:
```
This issue was self-resolved. The device was functioning correctly - the user
was searching for the wrong MAC address. We recommend:

1. Check tuya-convert logs for the actual device MAC address
2. Wait 2-3 minutes after reboot for device to connect
3. Use fast power cycle recovery (6x power reinsertion) to enter config mode if needed

See [Troubleshooting Guide](link) for more information.
```

**Optional**: Add documentation enhancements described above.

### For This Fork

**Status**: 📦 **ARCHIVED** (User Error)

**Action**: Document as example of common user confusion, but no code changes needed.

**Next Steps**:
1. ✅ Document the issue (this file)
2. ✅ Update TRACKING.md
3. ⏳ Consider adding post-flash verification guide to docs (optional)
4. ⏳ Consider documenting fast power cycle recovery feature (optional)

---

## References

- [Upstream Issue #1145](https://github.com/ct-Open-Source/tuya-convert/issues/1145)
- [Tasmota Device Recovery](https://tasmota.github.io/docs/Device-Recovery/)
- [Tasmota Configuration](https://tasmota.github.io/docs/Getting-Started/)
- [ESP8266 WiFi Documentation](https://arduino-esp8266.readthedocs.io/en/latest/esp8266wifi/readme.html)

---

## Priority

**LOW**: User error, not a software issue. Documentation improvements are optional QoL enhancements.

---

**Analysis By**: Claude (AI Assistant)
**Analysis Date**: 2025-11-06
**Last Updated**: 2025-11-06
**Branch**: claude/next-open-issue-011CUs8zYwfVmXXkDYJ2YhCq
**Status**: 📦 Archived - User error, device working correctly, self-resolved
