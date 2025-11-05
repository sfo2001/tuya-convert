# PSK Research Procedures

**Related:** [PSK Identity 02 Protocol](PSK-Identity-02-Protocol.md) | [Firmware Database](PSK-Firmware-Database.md) | [Affected Devices](PSK-Identity-02-Affected-Devices.md)

This document provides step-by-step procedures for capturing and analyzing PSK Identity 02 protocol data to assist in research efforts.

---

## Table of Contents

1. [Decrypting Network Captures](#decrypting-network-captures-with-known-psk)
2. [Creating Network Captures and Firmware Backups](#creating-network-captures-and-firmware-backups)
3. [Experimental Procedure](#experiment)

---

## Decrypting Network Captures with Known PSK

If you have obtained a PSK key from a firmware backup, you can decrypt network captures using `tshark`:

```bash
tshark -o "ssl.psk:3ce2b65bc30c7d91bf2e50884a49f6ddc77a8c44b991a1120b298ab846e97704" \
       -z follow,ssl,ascii,9 \
       -r gosund-upgrade.pcap \
       -Y null
```

**Parameters:**
- `-o "ssl.psk:<PSK>"` - Replace with the actual PSK from firmware
- `-z follow,ssl,ascii,9` - Follow stream number 9 (adjust as needed)
- `-r gosund-upgrade.pcap` - Input capture file
- `-Y null` - Display filter

**Notes:**
- See [PSK Firmware Database](PSK-Firmware-Database.md) for firmware samples with known PSKs
- See `scripts/psk-frontend.py` for how to calculate PSK for identity 01 streams
- PSK keys are 64 hexadecimal characters (256 bits)

**Code Reference:** `scripts/psk-frontend.py` - PSK calculation implementation

---

## Creating Network Captures and Firmware Backups

This procedure helps gather data about how devices with PSK Identity 02 communicate with Tuya servers.

### Prerequisites

- Linux machine with WiFi adapter
- Android phone or device running SmartLife app
- Target Tuya device
- Serial connection equipment (for firmware extraction)
- [`esptool`](https://github.com/espressif/esptool) installed

### Step 1: Install create_ap

```bash
git clone https://github.com/oblique/create_ap
cd create_ap
sudo make install
cd ..
```

### Step 2: Setup Pass-Through Access Point

Replace `wlan0` with your wireless interface name:

```bash
sudo create_ap wlan0 wlan0 MyAccessPoint MyPassPhrase
```

This creates an AP that bridges to your existing network.

### Step 3: Start Recording Network Traffic

```bash
tcpdump -i wlan0 -w capture.pcap
```

### Step 4: Pair the Device

1. Connect your phone to `MyAccessPoint` (or whatever you named it)
2. Use the SmartLife app (or vendor-branded app) to pair the device
3. Wait for registration to complete
4. Disconnect the device from power

### Step 5: Stop Recording

Press `Ctrl+C` in the `tcpdump` terminal

### Step 6: Extract Firmware

1. Disassemble the device
2. Connect to the serial port of the ESP8266/ESP8285
3. Download the firmware using `esptool`:

```bash
esptool.py read_flash 0 0x100000 firmware.bin
```

**Important:** Use `0x100000` (1MB) for most devices. Some may require `0x200000` (2MB) or other sizes.

### Step 7: Share Your Data

Upload both files to help the research effort:
- `capture.pcap` - Network traffic capture
- `firmware.bin` - Full firmware dump

Open an issue on the [tuya-convert repository](https://github.com/ct-Open-Source/tuya-convert/issues) with:
- Device model and manufacturer
- Purchase date and location
- Both files attached
- Any relevant observations

---

## Experiment

### Goal

Understand how devices with old firmware are integrated into Tuya's newer security scheme when updated.

### Research Questions

1. **Is the PSK persistent?**
   - When a device is updated, downgraded, and re-updated, does it receive the same PSK?
   - If YES: We could potentially obtain PSK by faking the API call (though likely patched quickly)
   - If NO: Random PSK each time (bad for OTA flashing)

2. **Where is PSK stored on updated devices?**
   - Factory devices: PSK at `0xfb000` in flash
   - Updated devices: PSK location unknown (not at `0xfb000` in same format)

### Requirements

- **Tuya device with:**
  - Old firmware that works with TuyaConvert, OR
  - Converted device with original backup where MAC address matches
- **Firmware upgrade available** for that device model in Tuya app
  - ✅ Confirmed: Possible to get new PSK firmware through app
  - ⚠️ Not guaranteed: Available for all device models
  - Example: Teckin SB50 was upgraded to PSK firmware via app
  - Example: Powertech SL225X with old firmware has no update available
- **Ability to open device** and serial flash it

### Procedure Steps

1. **Backup original firmware**
   - Take a device with pre-patched Tuya firmware
   - Use `esptool.py read_flash 0 0x100000 firmware_original.bin`

2. **Setup network capture**
   - Configure WireShark or tcpdump as described above
   - Start recording before pairing

3. **Register and update device**
   - Register device to the Tuya app
   - Allow firmware update to patched version
   - Wait for update to complete

4. **Backup updated firmware**
   - Use `esptool.py read_flash 0 0x100000 firmware_updated_1.bin`
   - Extract PSK from `0xfb000` (if present)
   - Record the PSK value

5. **Flash back to original**
   - Use `esptool.py write_flash 0 firmware_original.bin`
   - Erase device pairing from app

6. **Register and update again**
   - Register device to Tuya app again
   - Allow firmware update again
   - Wait for completion

7. **Backup second updated firmware**
   - Use `esptool.py read_flash 0 0x100000 firmware_updated_2.bin`
   - Extract PSK (if present)

8. **Compare PSKs**
   - Compare PSK from step 4 with PSK from step 7
   - Document whether they match or differ

9. **Share findings**
   - Post results to this documentation
   - Include all firmware files and captures
   - Document device model and observations

### Known Issues

**PSK Storage Location Unknown on Updated Devices:**

Several attempts have been made following the steps above (see [Firmware Database](PSK-Firmware-Database.md) files 10 and 34). Devices that:
- Ship with PSK ID 01 firmware, AND
- Are updated to firmware using PSK ID 02

...do **not** store the `pskKey` at `0xfb000` as expected.

**Current Status:** Experiment is stalled until we can find where `pskKey` is stored on these devices, if at all. The key is not found in the same 37-character base64-ish format as factory devices.

**Theories:**
1. PSK may be stored in encrypted form
2. PSK may be in different flash location
3. PSK may be computed on-demand from other stored values
4. PSK may not be stored locally on updated devices

---

## Safety and Ethics

**Important Reminders:**

- Only experiment with devices you own
- Do not attempt to flash devices belonging to others without permission
- Share findings responsibly through official channels
- Respect intellectual property and terms of service
- This research is for educational purposes and improving open-source alternatives

---

## Contributing

Found a better procedure or discovered something new? Please:

1. Open an issue on the [tuya-convert repository](https://github.com/ct-Open-Source/tuya-convert/issues)
2. Reference this documentation page
3. Provide detailed steps to reproduce your findings
4. Include any relevant code, captures, or firmware dumps

---

**See Also:**
- [PSK Identity 02 Protocol](PSK-Identity-02-Protocol.md) - Main research findings
- [PSK Firmware Database](PSK-Firmware-Database.md) - Analyzed firmware samples
- [Affected Devices List](PSK-Identity-02-Affected-Devices.md) - Known incompatible devices
- [Research Tools](PSK-Research-Tools.md) - Tools and resources for PSK research
