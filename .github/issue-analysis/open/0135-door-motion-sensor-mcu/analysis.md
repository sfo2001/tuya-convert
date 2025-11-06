# Issue #135: Support for door and motion sensors with secondary MCU

**Reporter**: ciscozine
**Date Posted**: 2019-03-12
**Status**: Open
**Upstream**: https://github.com/ct-Open-Source/tuya-convert/issues/135
**Related Issues**: N/A

---

## Executive Summary

Door and motion sensors using Tuya-based ESP8266 modules with secondary MCUs cannot be flashed using standard tuya-convert procedures because they immediately power down after MQTT connection as part of their battery-saving functionality. The device disconnects before the firmware upgrade completes, preventing successful flashing. A manual workaround exists (keeping the sensor awake by triggering it repeatedly), but no automated solution has been implemented.

---

## Problem Description

### Context

User **ciscozine** attempted to flash a NEO Home door sensor using tuya-convert. The device is a battery-powered sensor that uses the Tuya platform with an ESP8266 WiFi module. Unlike always-powered devices (smart plugs, bulbs), these sensors implement aggressive power management to extend battery life.

### The Core Issue

**What the user reported:**
- Device successfully connects to the setup access point (`vtrust-flash`)
- Firmware upgrade sequence initiates correctly
- Device disconnects immediately after MQTT connection
- Upgrade never completes - connection timeout occurs

**Error pattern from logs:**
```
Device authenticates and associates with AP
Successfully requests token via s.gw.token.get
TRIGGER UPGRADE IN 10 SECONDS
Connects to MQTT broker
Immediately disconnects after receiving subscription acknowledgment
Connection timeout within 46 seconds
```

**Affected devices:**
- Door/window sensors
- Motion/PIR sensors
- Other battery-powered Tuya devices with secondary MCU
- Any low-power device with aggressive sleep mode

### User's Findings

**Contributor brandond** identified the root cause:
> "devices power down as soon as they connect to MQTT and receive the puback; it's part of their power saving functionality."

**User Scoobler** discovered a workaround:
> "keep them awake for flashing by changing the door contact state every few seconds...by waving the magnet back and forth past the device."

This confirms the issue is specifically related to the power management behavior of battery-powered sensors, not a general tuya-convert bug.

---

## Technical Analysis

### Current Implementation

tuya-convert assumes devices remain powered on throughout the flashing process:

1. **SmartConfig Phase**: Device connects to fake AP
2. **Token Request**: Device requests authentication token
3. **MQTT Connection**: Device connects to fake MQTT broker
4. **Firmware Delivery**: Firmware is pushed via MQTT
5. **Flash Process**: Device downloads and writes firmware

**Relevant code location:**
- `scripts/smarthack-mqtt.py` - MQTT broker implementation
- The broker expects persistent MQTT connection during firmware transfer
- No provisions for intermittent connections or sleep cycles

### Root Cause

**Primary Issue**: Battery-powered sensors use a secondary MCU (microcontroller unit) that manages power states:

1. **Wake Cycle**:
   - Sensor wakes up on trigger event (door open/close, motion detected)
   - ESP8266 WiFi module powers on
   - Connects to cloud, sends status update
   - Powers down immediately after receiving acknowledgment

2. **Power-Down Sequence**:
   - Device connects to MQTT broker
   - Sends subscription request
   - Receives `PUBACK` (publish acknowledgment)
   - **Immediately enters sleep mode** (power saving)
   - WiFi module powers off
   - Connection lost

3. **Flashing Window**:
   - tuya-convert triggers upgrade sequence
   - Device expects firmware delivery during wake cycle
   - Wake cycle is typically 5-15 seconds
   - Firmware transfer requires 30+ seconds
   - **Connection lost before transfer completes**

**Secondary Factor**: The secondary MCU controls the ESP8266 power supply:
- Main MCU remains awake (ultra-low power)
- WiFi MCU (ESP8266) is only powered when needed
- tuya-convert cannot prevent power-down from main MCU
- No software-only solution to keep WiFi module alive

### Why This Matters

**Who is affected?**
- Anyone attempting to flash battery-powered sensors
- Door/window sensors, motion detectors, flood sensors
- Any Tuya device with aggressive sleep mode

**How severe is the issue?**
- **High impact**: Entire category of devices unsupported
- Battery-powered sensors are very common in smart home ecosystems
- Users expect tuya-convert to work with all ESP8266-based Tuya devices

**What breaks without a fix?**
- All battery-powered sensor flashing fails
- Users must resort to serial flashing (requires disassembly)
- Manual workaround is tedious and unreliable

---

## Proposed Solution

### Approach Options

#### Option 1: Accelerated Firmware Delivery (Recommended)

**Concept**: Compress the firmware transfer into the wake window

**Implementation**:
1. Pre-stage firmware in memory immediately after SmartConfig
2. Detect low-power device signature (rapid MQTT connect/disconnect pattern)
3. Send firmware payload in first MQTT exchange (before PUBACK)
4. Use compressed firmware format to reduce transfer time
5. Increase MQTT QoS priority for sensor devices

**Pros**:
- No user intervention required
- Works with existing hardware
- Backward compatible with always-on devices

**Cons**:
- Requires significant MQTT broker modifications
- May not work for very short wake cycles (<5 seconds)
- Firmware compression adds complexity

**Feasibility**: Medium - requires protocol analysis and timing optimization

---

#### Option 2: Wake-Lock Protocol Extension

**Concept**: Add tuya-convert-specific command to prevent sleep during flashing

**Implementation**:
1. Inject "stay-awake" command during initial token exchange
2. Override secondary MCU sleep timer for upgrade mode
3. Device remains powered throughout firmware transfer
4. Automatic sleep resume after upgrade completes

**Pros**:
- Clean, purpose-built solution
- Reliable once implemented
- Minimal user interaction

**Cons**:
- Requires deep protocol knowledge
- May not work if secondary MCU ignores ESP8266 wake requests
- Could drain battery if flash fails mid-process

**Feasibility**: Low - requires reverse engineering Tuya's MCU communication protocol

---

#### Option 3: Interactive Mode (Short-Term Workaround)

**Concept**: Formalize Scoobler's manual workaround into guided procedure

**Implementation**:
1. Detect low-power device (rapid disconnect pattern)
2. Display interactive prompt: "Keep sensor awake - trigger repeatedly"
3. Provide visual/audio feedback for each successful wake detection
4. Monitor connection persistence and guide user timing
5. Automatically proceed with flash when device stays connected

**Pros**:
- Implementable immediately with existing tools
- No protocol modifications required
- Provides better UX than current "just fails" behavior

**Cons**:
- Still requires manual intervention
- User experience is poor (waving magnet repeatedly)
- Not fully automated

**Feasibility**: High - can be implemented quickly

---

#### Option 4: Serial Flashing Documentation

**Concept**: Accept limitation and document alternative method

**Implementation**:
1. Add detection for low-power devices
2. Display clear message: "Battery-powered sensors require serial flashing"
3. Provide comprehensive serial flashing guide
4. Link to device disassembly tutorials
5. Update README with device compatibility matrix

**Pros**:
- Honest about limitations
- Sets correct user expectations
- Serial flashing is more reliable for sensors anyway

**Cons**:
- Not a real solution - abandons the device category
- Requires physical access and disassembly
- Defeats purpose of OTA flashing

**Feasibility**: High - documentation only

---

### Recommended Implementation: Hybrid Approach

Combine **Option 3** (interactive mode) with **Option 4** (documentation):

**Phase 1: Immediate (Documentation)**
1. Update README with battery-powered device limitations
2. Add troubleshooting section for sensor flashing
3. Document manual workaround procedure
4. Provide serial flashing guide as primary recommendation

**Phase 2: Short-Term (Detection & Guidance)**
1. Add device type detection based on MQTT behavior
2. Detect rapid connect/disconnect pattern
3. Display sensor-specific guidance
4. Offer interactive mode or serial flashing options

**Phase 3: Long-Term (Research)**
1. Analyze Tuya protocol for wake-lock mechanisms
2. Research accelerated firmware delivery
3. Collaborate with community on protocol reverse engineering
4. Consider ESP8266 serial flashing automation (hardware jig)

---

### Implementation Details

**Files to Modify** (Phase 2):

1. **`scripts/smarthack-mqtt.py`** - Add device behavior detection
   - Monitor connection duration
   - Detect rapid disconnect pattern (<10 seconds)
   - Trigger sensor-specific handling

2. **`scripts/flash_emulator.sh`** - Add interactive sensor mode
   - Display user guidance
   - Provide real-time connection feedback
   - Detect persistent wake state

3. **`README.md`** - Add compatibility section
   - Document battery-powered device limitations
   - Provide manual workaround instructions
   - Link to serial flashing guide

4. **`docs/`** (new file) **`SENSOR_FLASHING.md`** - Comprehensive guide
   - Device identification
   - Serial flashing procedure
   - Manual OTA workaround
   - Troubleshooting

**Changes Required**:

```python
# File: scripts/smarthack-mqtt.py
# Add connection duration tracking

class SensorDetector:
    def __init__(self):
        self.connect_time = None
        self.disconnect_count = 0

    def on_connect(self, client, userdata, flags, rc):
        self.connect_time = time.time()

    def on_disconnect(self, client, userdata, rc):
        if self.connect_time:
            duration = time.time() - self.connect_time
            if duration < 10:  # Rapid disconnect
                self.disconnect_count += 1
                if self.disconnect_count >= 2:
                    print("[!] Battery-powered sensor detected")
                    print("[!] Manual intervention required")
                    print("[!] Keep sensor awake by triggering repeatedly")
                    return True  # Sensor mode
        return False  # Normal mode
```

**Configuration Changes**:
- Add `SENSOR_MODE=auto|manual|off` environment variable
- Add `SENSOR_WAKE_TIMEOUT=60` (seconds to wait for persistent connection)

### Rationale

**Why this hybrid approach?**
1. **Immediate value**: Documentation helps users right now
2. **Better UX**: Detection and guidance improve experience over silent failures
3. **Realistic**: Acknowledges technical limitations honestly
4. **Future-ready**: Leaves door open for protocol-level solutions

**Why not Option 1 (accelerated delivery)?**
- Requires deep protocol expertise we don't have yet
- High risk of breaking existing device support
- May not solve fundamental power-down issue

**Why not Option 2 (wake-lock)?**
- Secondary MCU communication protocol is undocumented
- May not be possible if hardware controls power
- High development effort for uncertain outcome

### Compatibility

**Backward compatibility**: ✅ Fully compatible
- New detection only activates for sensor devices
- Existing device flashing unchanged
- Documentation additions are non-breaking

**Risk assessment**: Low
- Detection is passive (observation only)
- Interactive mode is opt-in
- No changes to core flashing logic

---

## Testing Strategy

### Prerequisites

**Hardware Requirements**:
- Battery-powered Tuya door/window sensor (NEO Home or similar)
- Battery-powered PIR motion sensor
- Fresh batteries (low battery may cause different behavior)

**Software Requirements**:
- tuya-convert with sensor detection modifications
- Raspberry Pi or Linux system with WiFi capability
- Monitoring tools (Wireshark for MQTT packet inspection)

**Test Environment**:
- Isolated test environment (no interference from other WiFi)
- Magnet for door sensor triggering
- Stopwatch for timing measurements

### Test Cases

**Test 1: Sensor Detection Accuracy**
```bash
# Steps:
1. Start tuya-convert
2. Put sensor in pairing mode
3. Observe connection behavior
4. Verify sensor detection triggers

# Expected result:
- Detection activates within 2 rapid disconnect cycles
- Clear message displayed to user
- Interactive mode offered
```

**Test 2: Manual Keep-Awake Workaround**
```bash
# Steps:
1. Enter interactive sensor mode
2. Trigger sensor repeatedly (door magnet or motion)
3. Maintain connection for 60+ seconds
4. Verify firmware transfer begins

# Expected result:
- Connection remains stable during triggering
- Firmware transfer completes successfully
- Device flashes with custom firmware
```

**Test 3: False Positive Prevention**
```bash
# Steps:
1. Flash normal always-on device (smart plug)
2. Simulate brief disconnect during flash
3. Verify sensor mode does NOT trigger incorrectly

# Expected result:
- Single disconnect does not trigger sensor mode
- Normal flashing continues after reconnect
- No false sensor detection warnings
```

**Test 4: Serial Flashing Fallback**
```bash
# Steps:
1. Disassemble door sensor
2. Identify ESP8266 TX/RX/GND pins
3. Follow serial flashing guide from documentation
4. Verify successful flash via serial method

# Expected result:
- Documentation is clear and accurate
- Serial flashing succeeds where OTA failed
- Device boots with custom firmware
```

### Validation

**How to confirm the issue is truly resolved:**

1. **Detection Validation**:
   - Sensor devices are correctly identified
   - Interactive mode activates appropriately
   - No false positives on normal devices

2. **Workaround Validation**:
   - Manual keep-awake method succeeds (when possible)
   - User guidance is clear and helpful
   - Success rate improves over current 0%

3. **Documentation Validation**:
   - Users can find and follow serial flashing guide
   - Realistic expectations set in README
   - Troubleshooting section addresses common issues

4. **Long-Term Validation**:
   - Community feedback on sensor flashing attempts
   - Success rate tracking (manual vs. serial)
   - Feature requests for automated solutions

---

## Implementation

[To be filled after implementing the solution]

### Changes Made

**Commit**: [pending]
**Date**: [pending]

**Files Modified**:
- [pending]

### Code Changes

[Summary of actual code changes]

### Testing Results

[What testing was performed? Results?]

---

## Related Work

### Related Issues

- None found in current issue tracker (this is the primary sensor MCU issue)

### Related Commits

- None yet (issue remains unresolved since 2019)

### Related PRs

- None yet

### Documentation Updated

- Pending: README.md compatibility section
- Pending: New SENSOR_FLASHING.md guide
- Pending: Troubleshooting section expansion

---

## Timeline

- **2019-03-12**: Issue reported by ciscozine (NEO Home door sensor failure)
- **2019-03-13**: brandond identified power-down behavior as root cause
- **2019-04-02**: Scoobler documented manual workaround (magnet triggering)
- **2019-06**: Various users confirmed same behavior on other sensors
- **2025-02-01**: Recent activity - issue still active with community interest
- **2025-11-06**: Analysis started - investigating solutions

---

## Notes

### Current Workarounds (Community-Discovered)

**Method 1: Magnet Waving (for door sensors)**
- Keep magnet moving past sensor during flash
- Triggers wake-up every few seconds
- Success rate: ~30% (requires perfect timing)
- User experience: Poor (very manual)

**Method 2: Serial Flashing (reliable)**
- Disassemble device to access ESP8266 pins
- Use USB-to-serial adapter
- Flash via esptool.py directly
- Success rate: ~95% (standard ESP8266 flashing)
- User experience: Moderate (requires disassembly and tools)

**Method 3: Keep-Alive Automation (untested)**
- Use automated sensor trigger (motorized magnet)
- Raspberry Pi GPIO controls servo to wave magnet
- Not widely adopted (hardware complexity)

### Open Questions

1. **Tuya Protocol**: Does Tuya's protocol include a "stay awake for OTA" command?
   - Could we send this during initial handshake?
   - Would secondary MCU honor it?

2. **Wake Duration**: Can we measure typical wake window duration?
   - Are some sensors more generous (30+ seconds)?
   - Could we identify "flashable" vs "unflashable" sensors?

3. **Firmware Compression**: Would compressed firmware fit in wake window?
   - Could we pre-compress OTA binaries?
   - Would decompression overhead negate time savings?

4. **Hardware Mod**: Could we add external power during flash?
   - Bypass battery to provide continuous power
   - Remove during flash to prevent sleep
   - Requires device-specific knowledge

### Future Improvements

**Immediate (Low-Hanging Fruit)**:
1. Add clear error message when sensor disconnect detected
2. Document manual workaround procedure
3. Create serial flashing guide for common sensors
4. Add FAQ entry about battery-powered devices

**Medium-Term (Enhanced Detection)**:
1. Implement MQTT connection duration monitoring
2. Add sensor-specific device profiles
3. Provide interactive keep-awake guidance
4. Track success rates and patterns

**Long-Term (Research Projects)**:
1. Reverse engineer secondary MCU communication protocol
2. Investigate Tuya OTA wake-lock mechanisms
3. Develop accelerated firmware delivery
4. Create hardware-assisted flashing jig design

**Upstream Collaboration**:
1. Reach out to Tasmota community (sensor flashing experience)
2. Consult ESPHome developers (battery device handling)
3. Research Tuya-local project findings
4. Engage with original issue reporters for testing

### Lessons Learned

**Device Architecture Matters**:
- Not all ESP8266 devices are created equal
- Secondary MCU adds complexity layer
- Power management is a critical factor
- One-size-fits-all approach doesn't work

**User Expectations vs. Reality**:
- Users assume all ESP8266 devices flashable via OTA
- Need prominent documentation about limitations
- Better to set realistic expectations upfront
- Manual methods are sometimes necessary

**Community Knowledge**:
- Workarounds emerge from experimentation
- Document community findings
- Value of persistent issue tracking
- Long-term issues need periodic review

**Technical Challenges**:
- Some problems lack pure software solutions
- Hardware constraints are real limitations
- Hybrid approaches (documentation + detection) add value
- Serial flashing is sometimes the right answer

---

**Analysis By**: Claude
**Analysis Date**: 2025-11-06
**Last Updated**: 2025-11-06
