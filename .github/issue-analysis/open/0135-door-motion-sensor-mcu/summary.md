# Issue #135 Summary: Door/Motion Sensor Secondary MCU

**Status**: 🔍 Open - Enhancement Needed
**Severity**: High (entire device category unsupported)
**Date**: 2019-03-12 (6+ years old, still active)
**Type**: Hardware Architecture Limitation

---

## Quick Summary

Battery-powered Tuya sensors (door/window sensors, motion detectors) cannot be flashed via tuya-convert because they immediately power down after connecting to MQTT as part of their battery-saving functionality. The firmware transfer requires 30+ seconds, but the device's wake cycle is typically only 5-15 seconds.

---

## Root Cause

**Secondary MCU Power Management**:
- Main MCU controls ESP8266 WiFi module power supply
- Device wakes only on trigger events (door open, motion detected)
- Connects to MQTT, sends status, receives acknowledgment
- **Powers down immediately** to save battery
- Connection lost before firmware transfer completes

**Technical Flow**:
```
Device triggers → ESP8266 powers on → Connects to MQTT →
Receives PUBACK → Powers down (5-15 sec total) →
Firmware transfer fails (needs 30+ sec)
```

---

## Current Workarounds

### Manual Keep-Awake (Community Method)
- **What**: Wave magnet past door sensor repeatedly during flash
- **Success Rate**: ~30% (timing-dependent)
- **User Experience**: Poor (very manual, unreliable)

### Serial Flashing (Recommended)
- **What**: Disassemble device, flash ESP8266 via serial connection
- **Success Rate**: ~95% (standard ESP8266 procedure)
- **User Experience**: Moderate (requires tools and disassembly)

---

## Affected Devices

- Door/window contact sensors
- PIR motion detectors
- Flood/water leak sensors
- Any battery-powered Tuya device with aggressive sleep mode
- Devices with secondary MCU controlling ESP8266 power

---

## Recommended Solution Path

### Phase 1: Documentation (Immediate)
✅ Update README with battery-powered device limitations
✅ Add troubleshooting section for sensors
✅ Document manual workaround and serial flashing
✅ Set realistic user expectations

### Phase 2: Detection & Guidance (Short-Term)
🔄 Add sensor device detection (rapid MQTT disconnect pattern)
🔄 Display sensor-specific guidance and options
🔄 Provide interactive mode with real-time feedback
🔄 Offer serial flashing as primary recommendation

### Phase 3: Research (Long-Term)
🔬 Reverse engineer Tuya wake-lock protocol
🔬 Investigate accelerated firmware delivery
🔬 Research secondary MCU communication
🔬 Collaborate with community on solutions

---

## Technical Challenges

| Challenge | Difficulty | Feasibility |
|-----------|-----------|-------------|
| Protocol wake-lock command | High | Low (requires deep RE) |
| Accelerated firmware delivery | Medium | Medium (compression/optimization) |
| Interactive keep-awake mode | Low | High (can implement now) |
| Documentation improvements | Low | High (immediate value) |

---

## Impact Assessment

**Who's Affected**: Anyone attempting to flash battery-powered sensors
**Severity**: High - entire device category unsupported
**Workaround Availability**: Yes (serial flashing or manual keep-awake)
**Fix Complexity**: High (may require hardware/protocol changes)

---

## Key Decisions

### ✅ Recommend Serial Flashing
- Most reliable solution (95% success rate)
- Well-documented ESP8266 procedure
- Works for all ESP-based sensors
- Sets correct user expectations

### ✅ Document Limitations Prominently
- Update README with compatibility matrix
- Add "Battery-Powered Devices" section
- Link to serial flashing guide
- Prevent user frustration from failed attempts

### ✅ Add Sensor Detection
- Detect rapid MQTT disconnect pattern
- Provide helpful error message
- Offer alternative methods
- Improve user experience over silent failure

### ⚠️ Don't Promise Automated OTA (Yet)
- No proven solution exists
- Hardware limitations may be insurmountable
- Better to be honest about limitations
- Keep door open for future research

---

## Related Resources

**Community Findings**:
- brandond's root cause analysis (power-down behavior)
- Scoobler's manual workaround (magnet waving)
- Multiple user confirmations across device types

**Potential Solutions**:
- Tasmota community (sensor flashing experience)
- ESPHome battery device handling
- Tuya-local project research
- Custom hardware flashing jigs

**Labels**: `enhancement`, `help wanted`, `new device`

---

## Next Actions

1. **Create Documentation** (High Priority):
   - `docs/SENSOR_FLASHING.md` - Comprehensive guide
   - Update `README.md` - Compatibility section
   - Add troubleshooting entries

2. **Implement Detection** (Medium Priority):
   - Modify `scripts/smarthack-mqtt.py`
   - Add connection duration tracking
   - Display sensor-specific messages

3. **Community Engagement** (Low Priority):
   - Request testing volunteers
   - Gather device-specific wake duration data
   - Collaborate on protocol research

---

**Analysis Date**: 2025-11-06
**Analyst**: Claude
**Recommendation**: Document limitations, implement detection, recommend serial flashing
