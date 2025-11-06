# Issue #1162: Flash process doesn't connect on smart device - repeating: SmartConfig complete. Resending SmartConfig Packets

**Reporter**: Edu-ST
**Date Posted**: 2025-05-26
**Status**: Open
**Upstream**: https://github.com/ct-Open-Source/tuya-convert/issues/1162
**Related Issues**: #1153 (sslpsk3 migration)

---

## Executive Summary

User reports that when attempting to flash a Tuya device on Kali Linux 2025.1.c (via Windows bootable USB), the SmartConfig process enters a repeating loop displaying "SmartConfig complete. Resending SmartConfig Packets" without ever successfully connecting to the device. This is a common issue that typically indicates either SSL/TLS handshake failure, device incompatibility, or environmental configuration problems. The maintainer (RoSk0) linked this to issue #1153, suggesting it's related to Python 3.12+ SSL compatibility requiring sslpsk3.

---

## Problem Description

### Context

The user is running tuya-convert from a Windows bootable USB stick with Kali Linux 2025.1.c to flash a Tuya IoT device. They followed the standard procedure:
1. Connected a mobile device to the vtrust WiFi network
2. Put the IoT device in pairing mode (LED blinking rapidly)
3. Pressed Enter to start the flash process

### The Core Issue

After the device LED turns solid (indicating it received the SmartConfig broadcast), the terminal displays:

```
SmartConfig complete.
Resending SmartConfig Packets
```

This message repeats continuously, and the device never connects to install the intermediate firmware.

### User's Environment

- **OS**: Kali Linux 2025.1.c (bootable USB on Windows host)
- **Python Version**: Likely Python 3.12+ (Kali 2025.1.c default)
- **Access Point**: vtrust WiFi network
- **Device Status**: LED turns solid (indicating SmartConfig received)
- **Connection Result**: Device fails to connect to IP 10.42.42.42

---

## Technical Analysis

### Understanding SmartConfig Behavior

The "Resending SmartConfig Packets" message is **normal behavior**, not a bug. Let me explain:

**Code Reference**: `scripts/smartconfig/main.py:24-36`

```python
for i in range(10): # Make 10 attempts
    smartconfig( passwd, ssid, region, token, secret )
    print()
    print('SmartConfig complete.')

    for t in range(3, 0, -1):
        print('Auto retry in %ds. ' % t, end='', flush=True)
        sleep(1)
        print(end='\r')

    print('Resending SmartConfig Packets')
```

**What's happening**:
1. SmartConfig broadcasts WiFi credentials using UDP multicast/broadcast packets
2. The device receives these packets (LED turns solid)
3. The script completes one iteration and waits 3 seconds
4. Then it prints "Resending SmartConfig Packets" and repeats (up to 10 times)
5. This loop runs while `start_flash.sh` waits for the device to connect

### The Real Problem: Device Not Connecting

**Code Reference**: `start_flash.sh:194-230`

After SmartConfig is launched in the background, the main script waits for the device:

```bash
# Wait for device to install intermediate firmware and connect with IP 10.42.42.42
i=120  # 120 second timeout
while ! ping -c 1 -W 1 -n 10.42.42.42 -I 10.42.42.1 &> /dev/null; do
    printf .
    if (( --i == 0 )); then
        echo "Timed out while waiting for the device to (re)connect"
        # ... run diagnostics ...
    fi
done
```

**The issue is**: The device receives SmartConfig but fails to:
1. Connect to the vtrust-flash AP
2. Establish SSL/TLS connection with the PSK frontend
3. Download and install intermediate firmware
4. Reconnect with IP 10.42.42.42

### Root Causes (Multiple Possibilities)

#### 1. SSL/TLS Compatibility Issue (Most Likely - Issue #1153)

**Maintainer's Assessment**: RoSk0 linked this to issue #1153

**Background**:
- Kali Linux 2025.1.c likely uses Python 3.12 or 3.13
- Python 3.12+ removed the deprecated `ssl.wrap_socket()` function
- Old `sslpsk` package doesn't work with Python 3.12+
- Must use `sslpsk3` package instead

**Code Reference**: `start_flash.sh:123-127`
```bash
# PSK (Pre-Shared Key) frontend manages encryption keys
# Explicitly activate venv in screen session to ensure sslpsk3 is available
$screen_with_log smarthack-psk.log -S smarthack-psk -m -d bash -c "source $PWD/venv/bin/activate && exec ./psk-frontend.py -v"
```

**What happens**:
1. Device receives SmartConfig and tries to connect
2. Device attempts SSL/TLS-PSK handshake with `psk-frontend.py`
3. If `sslpsk3` is not installed (or old `sslpsk` is used), handshake fails
4. Device gives up and never progresses to intermediate firmware installation

**Evidence**: This would show in `smarthack-psk.log` as SSL/TLS errors

#### 2. Device Incompatibility

**Possibility**: Device uses non-ESP chip (e.g., Eswin ECR6600, Beken BK7231, Realtek chips)

**Similar to**: Issue #1157 (archived - ECR6600 chip incompatibility)

**Why SmartConfig "works"**: SmartConfig is a generic protocol supported by many chips, so the device can receive the WiFi credentials even if it's not an ESP8266/ESP32. However, tuya-convert's firmware payload is ESP-specific, so the device won't accept it.

**Evidence**: Check device chip type (if accessible via serial/UART)

#### 3. Newer Security Protocol

**Possibility**: Device uses PSK Identity 02 (newer Tuya firmware)

**Reference**: Documented in `docs/Failed-attempts-and-tracked-requirements.md:98`

```
**Cause:**
- Device uses PSK Identity 02 (newer devices - see below)
```

**What this means**: Tuya updated their security protocol on newer devices. These devices may accept SmartConfig but reject the fake registration server because they use different PSK identities.

**Evidence**: Check `smarthack-psk.log` for PSK Identity errors

#### 4. Kali Live USB Environment Issues

**Possibility**: Network adapter configuration issues on live USB system

**Specific concerns**:
- USB boot environment may have limited persistence
- Network adapter drivers might not be optimal
- WiFi regulatory domain settings
- Insufficient system resources

**Common issue**: Hostapd (access point daemon) may not configure properly on live systems

**Evidence**: Check `smarthack-wifi.log` for AP errors

#### 5. Python Virtual Environment Not Activated

**Possibility**: Virtual environment not set up or not activated properly

**Why this matters**: If `install_prereq.sh` wasn't run with virtual environment support, or if the venv wasn't created, then `sslpsk3` won't be available even if the script tries to import it.

**Code Reference**: `start_flash.sh:69-83`
```bash
if [ -d "venv" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
    export VENV_PATH="$PWD/venv/bin:$PATH"
else
    echo "WARNING: Virtual environment not found!"
    echo "Attempting to continue with system Python packages..."
fi
```

---

## Proposed Solution

### Immediate Diagnostic Steps

**Step 1: Check the logs**

The issue cannot be definitively diagnosed without examining the log files:

```bash
cd scripts/
cat smarthack-psk.log    # SSL/TLS errors
cat smarthack-wifi.log   # AP configuration
cat smarthack-web.log    # Device registration attempts
cat screen0.log          # General errors
```

**Step 2: Verify Python environment**

```bash
python3 --version                    # Should be 3.12+
pip list | grep sslpsk               # Should show sslpsk3, not sslpsk
source venv/bin/activate             # Activate venv if it exists
python3 -c "import sslpsk3; print(sslpsk3.__version__)"  # Test import
```

**Step 3: Run diagnostics**

The script includes a diagnostic tool:
```bash
./scripts/dr_tuya.sh
```

### Solution Path A: Fix SSL/TLS Compatibility (Most Likely)

If the issue is related to #1153 (Python 3.12+ compatibility):

**1. Ensure sslpsk3 is installed**

```bash
cd /path/to/tuya-convert
./install_prereq.sh
# This should set up virtual environment and install sslpsk3
```

**Verify**:
```bash
source venv/bin/activate
pip show sslpsk3
```

**2. Remove old sslpsk if present**

```bash
pip uninstall sslpsk
pip install sslpsk3
```

**3. Restart tuya-convert**

```bash
./start_flash.sh
```

### Solution Path B: Device Incompatibility (If not ESP chip)

If the device uses a non-ESP chip:

**1. Identify chip type**
- Open device (if possible)
- Look for chip markings
- Common non-ESP chips: Eswin ECR6600, Beken BK7231T, Realtek RTL8710B

**2. If non-ESP chip**:
- tuya-convert **will not work** (it's ESP-specific)
- See archived issue #1157 for alternative flashing methods
- Consider hardware serial flashing tools

**3. Alternative tools**:
- `ltchiptool` for BK7231 and RTL8710 chips
- Serial UART flashing with appropriate firmware

### Solution Path C: Newer Security Protocol

If the device uses PSK Identity 02:

**Currently no fix available** - these devices are designed to resist tuya-convert

**Indicators**:
- `smarthack-psk.log` shows PSK Identity 02 errors
- Device is relatively new (2023+)
- Device has recently updated firmware

**Options**:
1. Try firmware downgrade via Tuya app (if possible)
2. Serial flashing as alternative
3. Accept device as incompatible with tuya-convert

### Solution Path D: Environment Configuration

If running on Kali Live USB:

**1. Consider persistent installation**
- Full Linux installation (dual boot or dedicated hardware)
- Linux VM on Windows host
- Raspberry Pi dedicated device

**2. Check network adapter**
```bash
iw list | grep -A 10 "Supported interface modes"
# Should show "AP" mode support
```

**3. Verify regulatory domain**
```bash
iw reg get
# Some channels may be restricted
```

---

## Testing Strategy

### Prerequisites

- Tuya device in pairing mode
- Smartphone connected to vtrust-flash AP
- Fresh installation of tuya-convert with venv support
- Access to log files

### Test Case 1: Verify SSL/TLS Functionality

**Setup**:
```bash
cd tuya-convert
source venv/bin/activate
python3 -c "import sslpsk3; print('sslpsk3 OK')"
```

**Expected Result**: Should print "sslpsk3 OK" without errors

**If fails**: Install/fix sslpsk3 per Solution Path A

### Test Case 2: Monitor PSK Frontend During Flash

**Setup**:
```bash
# In one terminal
tail -f scripts/smarthack-psk.log

# In another terminal
./start_flash.sh
```

**Expected Result**: Should see device attempting SSL/TLS connection when SmartConfig completes

**If no connection attempts**: Device not receiving SmartConfig or not connecting to AP

**If SSL errors**: Confirm sslpsk3 issue or cipher negotiation failure

### Test Case 3: Full Flash Process

**Setup**:
1. Install latest tuya-convert from this fork (with sslpsk3 support)
2. Run `./install_prereq.sh` to set up venv
3. Verify venv activation in `start_flash.sh`
4. Put device in pairing mode
5. Run `./start_flash.sh`

**Expected Result**:
```
SmartConfig complete.
Resending SmartConfig Packets
.....
IoT-device is online with ip 10.42.42.42
Stopping smart config
```

**Success Criteria**: Device connects within 120 seconds and proceeds to firmware backup

---

## Implementation

**Status**: Awaiting user feedback and log files for definitive diagnosis

### Changes Required (If SSL/TLS Issue)

If the issue is confirmed as sslpsk3-related:

**Good News**: Already fixed in this fork!

**Commits**:
- `59549b1` - Migrated to sslpsk3 for Python 3.12+ compatibility (#1153)
- `1663d29` - Added virtual environment support (#1143)
- `d071bdc`, `83db9d2` - Fixed venv activation in screen sessions (#1167)

**User Action Required**:
1. Pull latest changes from this fork
2. Run `./install_prereq.sh` to set up venv
3. Verify sslpsk3 is installed
4. Retry flashing

### Changes Required (If New Issue Found)

If log analysis reveals a different issue:
- Update this analysis with findings
- Implement appropriate fix
- Test thoroughly
- Update documentation

---

## Related Work

### Related Issues

- **#1153** - AttributeError: module 'ssl' has no attribute 'wrap_socket'
  - **Status**: ✅ Resolved
  - **Solution**: Migrated to sslpsk3
  - **Relevance**: Directly related per maintainer RoSk0
  - **Commit**: 59549b1

- **#1157** - new tuya smart plug 20A convert failed attempt
  - **Status**: 📦 Archived (Hardware incompatibility)
  - **Relevance**: Similar symptom (device doesn't connect after SmartConfig)
  - **Resolution**: ECR6600 chip - not ESP, requires different tools

- **#1167** - Ubuntu non-docker deps issue (Venv PATH)
  - **Status**: ✅ Resolved
  - **Relevance**: Virtual environment activation in screen sessions
  - **Commits**: d071bdc, 83db9d2

- **#1143** - install_prereq.sh needs --break-system-packages
  - **Status**: ✅ Resolved
  - **Solution**: Virtual environment support
  - **Commit**: 1663d29

### Related Documentation

- `docs/Failed-attempts-and-tracked-requirements.md:84-105` - SmartConfig timeout troubleshooting
- `scripts/smartconfig/main.py` - SmartConfig implementation
- `start_flash.sh:194-230` - Device connection waiting logic

---

## Timeline

- **2025-05-26**: Issue reported by Edu-ST
- **2025-07-27**: RoSk0 (maintainer) links to #1153, requests logs
- **2025-11-06**: Analysis started by Claude
- **Next**: Awaiting user response with diagnostic information

---

## Notes

### Open Questions

1. **What does `smarthack-psk.log` show?**
   - SSL/TLS errors would confirm #1153 relationship
   - PSK Identity errors would indicate newer security protocol
   - No connection attempts would suggest AP or network issue

2. **Is sslpsk3 installed?**
   - Kali 2025.1.c would have Python 3.12+
   - Without sslpsk3, SSL handshake will definitely fail

3. **What chip is in the device?**
   - ESP8266/ESP32: tuya-convert should work (if SSL fixed)
   - ECR6600/BK7231/RTL8710: tuya-convert won't work

4. **Did `install_prereq.sh` complete successfully?**
   - Was virtual environment created?
   - Are all dependencies installed?

5. **Is this a live USB or persistent installation?**
   - Live USB may have additional challenges
   - Persistent installation recommended for reliability

### User Action Required

To move forward with diagnosis, the user should provide:

1. **Complete log files**:
   ```bash
   cd tuya-convert/scripts/
   cat smarthack-psk.log
   cat smarthack-wifi.log
   cat smarthack-web.log
   cat screen0.log
   ```

2. **Python environment info**:
   ```bash
   python3 --version
   pip list | grep sslpsk
   ls -la venv/
   ```

3. **Device information** (if available):
   - Brand and model
   - Chip type (if accessible)
   - Firmware version (from Tuya app)

4. **Installation method**:
   - Output from `./install_prereq.sh`
   - Any errors during setup

### Most Likely Resolution

**Hypothesis**: This is almost certainly related to #1153 (sslpsk3 compatibility)

**Reasoning**:
1. Kali 2025.1.c uses Python 3.12+
2. Maintainer explicitly linked to #1153
3. SmartConfig works (device LED responds)
4. Device doesn't connect (SSL handshake likely failing)

**Recommended Action**:
1. Update to latest tuya-convert from this fork
2. Ensure virtual environment and sslpsk3 are properly installed
3. Retry flash process
4. If still fails, provide logs for deeper analysis

### Future Improvements

If this issue reveals gaps in error reporting:

1. **Better diagnostics**: Enhance `dr_tuya.sh` to check:
   - sslpsk3 installation
   - Virtual environment status
   - Python version compatibility

2. **User-friendly error messages**: Detect Python 3.12+ without sslpsk3 and show clear error

3. **Pre-flight checks**: Add validation before starting flash:
   - Check sslpsk3 availability
   - Verify venv activation
   - Test SSL cipher availability

4. **Documentation**: Add troubleshooting section for "SmartConfig loops but device doesn't connect"

---

**Analysis By**: Claude
**Analysis Date**: 2025-11-06
**Last Updated**: 2025-11-06
