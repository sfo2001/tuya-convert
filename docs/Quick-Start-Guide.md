# Quick Start Guide

**Last Updated:** 2025-11-05
**Status:** ✅ Complete

## Overview

This guide walks you through flashing your first Tuya-based IoT device with custom firmware (Tasmota or ESPurna) using tuya-convert. This is a complete walkthrough from installation to successful device flash, designed for first-time users.

**Time Required:** 30-60 minutes for your first device
**Difficulty:** Intermediate (requires basic command line knowledge)

> **⚠️ CRITICAL WARNING:** Do NOT connect your device to the official Tuya/Smart Life app before flashing. The app may automatically update the device firmware, making it impossible to flash with tuya-convert.

---

## Prerequisites

Before you begin, ensure you have:

### Hardware
- [ ] **Linux computer** with WiFi adapter capable of AP mode
- [ ] **Tuya-based IoT device** (check [Compatible Devices](Compatible-devices.md))
- [ ] **Secondary WiFi device** (smartphone or tablet) for the pairing process
- [ ] Device is **unplugged** and ready to flash

### Software
- [ ] **tuya-convert installed** - See [Installation Guide](Installation.md)
  - **Option 1:** Native install (`./install_prereq.sh`)
  - **Option 2:** Docker (`./start_flash.sh -d`)
  - **Option 3:** Nix flake (`nix develop`) - See [Using Nix](Using-Nix.md)
- [ ] **Root/sudo access** on your Linux machine
- [ ] **Custom firmware binary** (optional - Tasmota included)

### Knowledge
- [ ] How to put your device in **pairing mode** (usually hold button until LED blinks rapidly)
- [ ] Basic Linux command line usage

---

## Step-by-Step Flashing Process

### Step 1: Prepare Your Device

**1.1 Verify Device Compatibility**

Before starting, check if your device has been successfully flashed by others:
- [Compatible Devices (HTTP firmware)](Compatible-devices-(HTTP-firmware).md)
- [Compatible Devices (HTTPS firmware)](Compatible-devices-(HTTPS-firmware).md)

> **Note:** Devices with PSK Identity beginning with `02` may not be flashable. See [System Requirements](Failed-attempts-and-tracked-requirements.md).

**1.2 Prepare Your Workspace**

```bash
cd tuya-convert
ls -la
```

Verify you see these key files:
- `start_flash.sh` - Main flashing script
- `install_prereq.sh` - Installation script
- `config.txt` - Configuration file
- `files/` - Directory for custom firmware

**1.3 (Optional) Add Custom Firmware**

If you want to use your own firmware instead of the included Tasmota:

```bash
cp /path/to/your-firmware.bin files/
```

**Requirements:**
- Maximum size: **512KB**
- Must include first-stage bootloader
- Compatible with ESP8266

---

### Step 2: Start the Flashing Process

**2.1 Launch tuya-convert**

Open a terminal and run:

```bash
cd tuya-convert

# If using Nix, enter the dev shell first:
# nix develop

sudo ./start_flash.sh
```

> **Note for Nix users:** If you installed using `nix develop`, make sure you're inside the Nix shell before running `start_flash.sh`. The virtual environment will be automatically activated.

**Expected Output:**
```
tuya-convert v2.4.5
Activating Python virtual environment...
======================================================
  Starting AP in a screen.....
  Starting web server in a screen
  Starting Mosquitto in a screen
  Starting PSK frontend in a screen
  Starting Tuya Discovery in a screen

======================================================

IMPORTANT
1. Connect any other device (a smartphone or something) to the WIFI vtrust-flash
   This step is IMPORTANT otherwise the smartconfig may not work!
2. Put your IoT device in autoconfig/smartconfig/pairing mode (LED will blink fast)
   Make sure nothing else is plugged into your IoT device while attempting to flash.
3. Press ENTER to continue
```

> **What's happening:** tuya-convert is setting up a fake WiFi access point called `vtrust-flash` and starting several background services (web server, MQTT broker, discovery service). The Python virtual environment is automatically activated to ensure all dependencies are available.

---

### Step 3: Connect Your Smartphone

**3.1 Connect to the Fake AP**

On your **smartphone or tablet**:

1. Open WiFi settings
2. Look for network: **vtrust-flash**
3. Connect to it (no password required)
4. **Stay connected** - don't close WiFi settings

> **Why this is important:** The smartconfig protocol requires another device to be connected to the AP for the pairing signal to work properly. Your phone acts as a "witness" to make the device trust the fake AP.

**3.2 Verify Connection**

Your phone should show "Connected" to vtrust-flash, even though it may warn about "No Internet". This is expected and correct.

---

### Step 4: Put Device in Pairing Mode

**4.1 Enter Pairing Mode**

This varies by device, but common methods:

- **Smart Plugs:** Press and hold button for 5-10 seconds
- **Light Bulbs:** Turn on/off 3 times, leave on
- **Switches:** Press and hold button for 5-10 seconds

**What to look for:**
- **Fast blinking LED** (usually 2-3 blinks per second)
- Some devices may blink in a pattern or change color

> **Tip:** If your device goes into slow blink mode (AP mode), that's wrong. Try again to get fast blinking (smartconfig mode).

**4.2 Ensure Device is Isolated**

Make sure:
- [ ] Device is **not plugged into other devices** (lamps, appliances)
- [ ] Device has **power** (plugged in or battery)
- [ ] Device is **close to your computer** (within a few feet)

---

### Step 5: Begin Pairing

**5.1 Press ENTER**

Back in your terminal, press **ENTER** to start the pairing process.

**Expected Output:**
```
======================================================
Starting smart config pairing procedure
Waiting for the device to install the intermediate firmware
........................................................
```

**5.2 What's Happening (Behind the Scenes)**

1. **Smartconfig broadcasts** fake WiFi credentials to the device
2. **Device connects** to the vtrust-flash AP
3. **Device contacts** the fake Tuya registration server
4. **Intermediate firmware** is pushed to the device
5. **Device reboots** with intermediate firmware
6. **Device reconnects** with IP address 10.42.42.42

This process takes **30-90 seconds**. Be patient!

**5.3 Expected Timeline**

- **0-10 seconds:** Smartconfig broadcasting
- **10-30 seconds:** Device receives credentials and connects
- **30-60 seconds:** Intermediate firmware installing
- **60-90 seconds:** Device reboots and reconnects

---

### Step 6: Wait for Connection

**6.1 Successful Connection**

**Expected Output:**
```
.................................
IoT-device is online with ip 10.42.42.42
Stopping smart config
Fetching firmware backup
```

✅ **Success!** Your device has accepted the intermediate firmware and is ready for flashing.

**6.2 Connection Timeout**

If you see:
```
Timed out while waiting for the device to (re)connect
Attempting to diagnose the issue...
```

❌ **Failed** - The device did not connect. See [Troubleshooting](#troubleshooting) below.

---

### Step 7: Firmware Backup

**Expected Output:**
```
Fetching firmware backup
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  512k  100  512k    0     0  12.3M      0 --:--:-- --:--:-- --:--:-- 12.5M
======================================================
Getting Info from IoT-device
```

> **What's happening:** tuya-convert is automatically backing up your device's original firmware to `backups/YYYYMMDD_HHMMSS/`. This backup can be used to restore your device to stock firmware if needed.

**Backup includes:**
- Original firmware binary (user1.bin or user2.bin)
- Device information (chip ID, flash size, MAC address)
- All log files from the flashing process

---

### Step 8: Flash Custom Firmware

**8.1 Select Firmware**

**Expected Output:**
```
======================================================
Ready to flash third party firmware!

For your convenience, the following firmware images are already included:
  Tasmota v9.2.0 (wifiman)
  ESPurna 1.5 (base)

You can also provide your own image by placing it in the /files directory
Please ensure the firmware fits the device and includes the bootloader
MAXIMUM SIZE IS 512KB

Select the file to flash:
1) tasmota-lite.bin
2) espurna-base.bin
3) custom-firmware.bin
```

**8.2 Choose Your Firmware**

For most users, we recommend **Tasmota**:

```
Enter selection: 1
```

**8.3 Flashing Progress**

**Expected Output:**
```
Flashing tasmota-lite.bin to device...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  512k  100  512k    0     0  8.2M      0 --:--:-- --:--:-- --:--:-- 8.3M

Flash successful!
```

✅ **Congratulations!** Your device is now flashed with custom firmware!

---

### Step 9: Initial Device Configuration

After successful flash, your device will reboot with the new firmware.

#### If You Flashed Tasmota:

**9.1 Find the Tasmota AP**

Your device will broadcast a WiFi network:
- **SSID:** `tasmota-xxxx` (where xxxx is random)
- **Password:** None (open network)

**9.2 Connect and Configure**

1. **Connect** your smartphone to the `tasmota-xxxx` AP
2. **Open browser** to `http://192.168.4.1`
3. **Enter your WiFi credentials:**
   - SSID: Your home WiFi network name
   - Password: Your WiFi password
   - ✅ **Check the "Show Password" box** to verify!
4. **Triple-check credentials** before clicking Save
5. Click **Save**

**9.3 Device Connects to WiFi**

- Device will reboot and connect to your home WiFi
- Find device IP in your router's DHCP list
- Access device at `http://[device-ip]`

**9.4 Configure Device Hardware**

See [Tasmota documentation](https://tasmota.github.io/docs/) for:
- Device templates
- GPIO configuration
- MQTT setup
- Automation rules

#### If You Flashed ESPurna:

**9.1 Find the ESPurna AP**

- **SSID:** `ESPURNA-XXXXXX`
- **Password:** `fibonacci`

**9.2 Connect and Configure**

1. Connect to `ESPURNA-XXXXXX` using password `fibonacci`
2. Open browser to `http://192.168.4.1`
3. Follow initial configuration wizard
4. Go to WIFI tab to configure your home network
5. Or go to ADMIN tab to upgrade to device-specific firmware

---

### Step 10: Flash Another Device (Optional)

**Expected Output:**
```
======================================================
Do you want to flash another device? [y/N]
```

- Press **y** to flash another device (returns to Step 4)
- Press **n** to exit tuya-convert

---

## What Success Looks Like

### During Flashing
✅ Device LED blinks during smartconfig
✅ Terminal shows "IoT-device is online with ip 10.42.42.42"
✅ Backup completes without errors
✅ Flash shows "Flash successful!"

### After Flashing
✅ Device broadcasts new AP (tasmota-xxxx or ESPURNA-XXXXXX)
✅ You can access device web interface
✅ Device responds to commands
✅ Device connects to your home WiFi

---

## Troubleshooting

### Device Timeout (Most Common Issue)

**Symptom:**
```
Timed out while waiting for the device to (re)connect
```

**Possible Causes & Solutions:**

1. **Device Already Patched**
   - Check `smarthack-psk.log` for PSK Identity
   - If starts with `02`, device cannot be flashed
   - Solution: Try a different device or older firmware version

2. **Wrong Pairing Mode**
   - Device in AP mode (slow blink) instead of smartconfig (fast blink)
   - Solution: Reset device and try again for fast blink

3. **Phone Not Connected to vtrust-flash**
   - Smartconfig requires another device connected
   - Solution: Verify phone is connected and stays connected

4. **WiFi Adapter Issues**
   - Adapter doesn't support AP mode properly
   - Solution: Try a different USB WiFi adapter (RTL8188CU recommended)

5. **Interference**
   - Other WiFi networks or devices interfering
   - Solution: Move away from other WiFi devices, try in different location

### Backup Fails

**Symptom:**
```
Could not fetch a complete backup
Do you want to continue anyway? [y/N]
```

**Possible Causes:**
- Network timeout
- Device connection unstable

**What to do:**
- You can continue (press `y`), but you won't have a backup to restore
- Or abort (press `n`) and try again

**Recommendation:** Only continue if you're OK losing ability to restore original firmware.

### Flash Fails

**Symptom:**
- Flash command returns error
- Device stops responding

**Solutions:**
1. **Firmware too large:** Ensure binary is under 512KB
2. **Wrong firmware:** Verify firmware is for ESP8266
3. **Device disconnected:** Start over from Step 1

### Device Doesn't Broadcast AP After Flash

**Symptom:**
- Flash successful, but no tasmota-xxxx or ESPURNA-XXXXXX AP appears

**Solutions:**
1. **Wait longer:** Can take 2-3 minutes for first boot
2. **Power cycle:** Unplug device, wait 10 seconds, plug back in
3. **Check router:** Device may have connected to your WiFi automatically (some firmwares remember networks)
4. **Wrong firmware:** Firmware may not be compatible with device

### "No cipher can be selected" Error

**Symptom:**
In logs: `could not establish sslpsk socket: ('No cipher can be selected.',)`

**Cause:** OpenSSL version too old (< 1.1.1)

**Solution:** Upgrade to Ubuntu 18.04+ or Debian 10+. See [System Requirements](Failed-attempts-and-tracked-requirements.md).

### "ModuleNotFoundError: No module named 'sslpsk3'" Error

**Symptom:**
In logs: `ModuleNotFoundError: No module named 'sslpsk3'` or similar import errors

**Cause:** Virtual environment not properly activated (pre-#1167 fix) or corrupted venv

**Solution:**
1. Update to latest version with issue #1167 fix
2. Re-run installation: `./install_prereq.sh`
3. Verify venv: `source venv/bin/activate && python3 -c "import sslpsk3; print('OK')"`

> **Note:** As of the #1167 fix, virtual environments are properly activated in sudo screen sessions. If you still see this error, your installation may be outdated or corrupted.

---

## Common First-Time Mistakes

### ❌ Mistake 1: Connecting Device to Official App
**Never** open the Smart Life or Tuya app before flashing. It will update the firmware and make the device unflashable.

### ❌ Mistake 2: Wrong Pairing Mode
Fast blink = smartconfig mode ✅
Slow blink = AP mode ❌

### ❌ Mistake 3: Phone Not Connected
The phone connection to vtrust-flash is **required**, not optional.

### ❌ Mistake 4: Wrong WiFi Credentials in Tasmota
Triple-check your WiFi password! Tasmota has no easy way to fix wrong credentials without serial access.

### ❌ Mistake 5: Firmware Too Large
Custom firmware **must** be ≤ 512KB for first flash. You can OTA update to larger firmware after.

### ❌ Mistake 6: Device Plugged Into Appliance
Always flash the device standalone, not while plugged into a lamp or appliance.

---

## Post-Flash Next Steps

After successfully flashing your device:

### For Tasmota Users
1. **Update firmware:** OTA update to latest Tasmota release
2. **Configure template:** Apply device-specific template from [Tasmota Device Templates](https://templates.blakadder.com/)
3. **Set up MQTT:** Configure MQTT broker for home automation
4. **Create rules:** Set up automation rules
5. **Integration:** Connect to Home Assistant, OpenHAB, etc.

### For ESPurna Users
1. **Update to device-specific firmware:** Use OTA or web interface
2. **Configure device:** Set up device type and GPIOs
3. **MQTT setup:** Configure MQTT broker
4. **Integration:** Connect to home automation platform

### Add Device to Compatibility List
Help the community by reporting your success:
1. Note device model, firmware type, flash result
2. Add to [Compatible Devices](Compatible-devices.md) wiki page
3. Or [open an issue](https://github.com/sfo2001/tuya-convert/issues) with device info

---

## Related Pages

- [Installation Guide](Installation.md) - Install tuya-convert
- [Compatible Devices](Compatible-devices.md) - Check device compatibility
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md) - Flash using Raspberry Pi
- [Using Docker](Using-Docker.md) - Docker-based setup
- [System Requirements](Failed-attempts-and-tracked-requirements.md) - Compatibility info
- [Troubleshooting](Troubleshooting.md) - Detailed troubleshooting guide

## Code References

- **Main Script:** `start_flash.sh` - Orchestrates entire flashing process
  - `setup()` function (line 66-112) - Initializes environment and starts services
  - Main loop (line 154-265) - Device pairing and flashing loop
  - Device connection check (line 183) - Critical IP check for 10.42.42.42
  - Backup phase (line 214-238) - Firmware backup process
  - Flash phase (line 240-255) - Custom firmware selection and upload

- **Configuration:** `config.txt` - AP name, gateway, and settings
- **Smartconfig:** `scripts/smartconfig/main.py` - Pairing protocol implementation
- **Discovery:** `scripts/tuya-discovery.py` - Device discovery service
- **Web Server:** `scripts/fake-registration-server.py` - Intercepts device registration

---

## Getting Help

If you're stuck:

1. **Check logs** in `backups/[timestamp]/` directory:
   - `smarthack-psk.log` - Shows PSK identity (check for `02`)
   - `smarthack-web.log` - Web server communication
   - `smarthack-udp.log` - Device discovery
   - `smarthack-wifi.log` - AP status

2. **Run diagnostics:** The script automatically runs `dr_tuya.sh` on timeout

3. **Search existing issues:** [GitHub Issues](https://github.com/sfo2001/tuya-convert/issues)

4. **Ask for help:**
   - [Open a new issue](https://github.com/sfo2001/tuya-convert/issues/new)
   - Include: device model, logs, error messages

---

**Good luck with your first flash!** 🎉

*Most first-time users successfully flash their device on the first or second attempt. Don't give up if it doesn't work immediately - troubleshooting is part of the process.*
