# Helping with New PSK Format Research

**Last Updated:** 2025-11-04
**Status:** ✅ Complete

## Overview

This guide explains how you can help with research into the new PSK (Pre-Shared Key) format used by newer Tuya devices. Your contributions could help restore OTA flashing capabilities for devices with PSK Identity 02 firmware.

## What is the New PSK Format?

Starting in late 2019, Tuya began shipping devices with a new security implementation called **PSK Identity 02**. This uses TLS-PSK (Transport Layer Security with Pre-Shared Keys) to authenticate devices with Tuya's cloud servers.

### Key Characteristics

- **Cipher Suite:** `TLS_PSK_WITH_AES_128_CBC_SHA256`
- **PSK ID Format:** `\x02` + `BAohbmd6aG91IFR1` + SHA256(gwId)
- **PSK Key:** 37-character alphanumeric string (a-zA-Z0-9)
- **Storage Location:** Flash address 0xFB000 (in JSON blob)

### Why It Matters

The new PSK format prevents tuya-convert from flashing custom firmware because:

1. Each device has a unique PSK key
2. The PSK is only known to the device and Tuya's servers
3. Without the PSK, we cannot complete the TLS handshake
4. Without the handshake, we cannot flash new firmware

**The Challenge:** Derive the PSK from publicly available information (like device MAC address and product ID).

## How to Recognize PSK Identity 02

If your `smarthack-psk.log` file shows output like this, you have a PSK Identity 02 device:

```
new client on port 443 from 10.42.42.25:3694
ID: 0242416f68626d6436614739314946523126e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
PSK: 2a9cf84b7a1b6bf1ede712edb7ee53c04b065f673e600f43627a67fea9a9d05d
could not establish sslpsk socket: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC] decryption failed or bad record mac
```

Note the `ID: 02` at the beginning (the `02` is in hex format).

## How You Can Help

### Option 1: Capture Network Traffic

If you have a device with **old firmware** (pre-Sept 2019) that still works with tuya-convert:

1. **Capture a packet trace** during device registration with the official Tuya/SmartLife app
2. Use `tcpdump` or Wireshark to capture the TLS handshake
3. Submit the pcap file to help researchers analyze the PSK exchange

**Why this helps:** Old firmware might reveal patterns in how PSKs are generated.

### Option 2: Extract Firmware

If you can access your device's serial programming pins:

1. **Read out the ESP firmware** using esptool.py or similar
2. **Extract the PSK key** from flash address 0xFB000
3. **Document the device info**: MAC address, product ID, firmware version
4. Submit your findings

**Why this helps:** More PSK samples help researchers look for patterns or derivation methods.

### Option 3: Share Device Information

If tuya-convert fails with PSK ID 02 error:

1. **Save all log files** from the flashing attempt:
   - smarthack-psk.log (most important!)
   - smarthack-mqtt.log
   - smarthack-udp.log
   - smarthack-web.log
   - smarthack-wifi.log
   - device-info.txt (from backup folder)

2. **Note your device details**:
   - Brand and model
   - Purchase date and location
   - Firmware version (if visible in app)

3. **Submit via GitHub issue** on the tuya-convert repository

**Why this helps:** Collecting device data helps identify patterns across manufacturers and firmware versions.

## Reference Files

The following files are examples from community contributions showing what kind of data is helpful:

- [device-info.txt](https://github.com/ct-Open-Source/tuya-convert/files/10252870/device-info.txt) - Device information example
- [Gosund SP111 Firmware.zip](https://github.com/ct-Open-Source/tuya-convert/files/10252871/Gosund.SP111.Firmare.zip) - Old Version 1.0.5 firmware (for comparison)
- [smarthack-mqtt.log](https://github.com/ct-Open-Source/tuya-convert/files/10252872/smarthack-mqtt.log) - MQTT log example
- [smarthack-psk.log](https://github.com/ct-Open-Source/tuya-convert/files/10252873/smarthack-psk.log) - **PSK log example** (most important!)
- [smarthack-udp.log](https://github.com/ct-Open-Source/tuya-convert/files/10252874/smarthack-udp.log) - UDP discovery log
- [smarthack-web.log](https://github.com/ct-Open-Source/tuya-convert/files/10252875/smarthack-web.log) - Web server log
- [smarthack-wifi.log](https://github.com/ct-Open-Source/tuya-convert/files/10252876/smarthack-wifi.log) - WiFi access point log

## Understanding Log Files

### smarthack-psk.log

This log shows TLS-PSK connection attempts. Look for:
- **ID:** The PSK Identity (should start with `02`)
- **PSK:** The derived pre-shared key
- **Errors:** SSL connection failures

### device-info.txt

Created during firmware backup, contains:
- `mac_addr`: Device MAC address
- `prod_idx`: 8-digit product identifier
- `gwId`: Gateway ID (prod_idx + mac_addr)
- `pskKey`: The 37-character PSK (if present at 0xFB000)
- `auz_key`: Authorization key (older devices)

## Important Notes

### Devices That Cannot Be Helped

Some newer Tuya devices have switched from ESP8266/ESP8285 chips to other microcontrollers entirely. These devices:
- Cannot run ESP-based firmware (like Tasmota or ESPHome)
- Will show warnings in logs about non-ESP chips
- Cannot be converted even if we solve the PSK challenge

### Firmware Version Timeline

- **Before Sept 30, 2019:** Old PSK format (MD5 of auzKey) - tuya-convert works
- **Sept 30, 2019 onward:** New PSK format (SHA256 of gwId) - tuya-convert fails
- **Mid-2020 onward:** Many devices switching to non-ESP chips

## Current Research Status

**The Challenge:** Derive the 37-character PSK from publicly available information.

**What We Know:**
- PSK is 37 characters (a-zA-Z0-9 only, no + or / like base64)
- Possibly base62 encoding of 28 bytes (224 bits)
- Might be SHA-224 hash of some combination of device info
- Stored at flash address 0xFB000 in JSON format
- Never transmitted over the network after initial factory programming

**What We Don't Know:**
- The derivation algorithm (if one exists)
- Whether PSKs are truly random or algorithmically generated
- The server-side key generation process

**Current Hypothesis:** The PSK may be totally random and only stored on Tuya servers and the device itself. If true, there is no solution and OTA flashing is no longer viable for these devices.

## Where to Submit Findings

1. **GitHub Issues:** https://github.com/sfo2001/tuya-convert/issues (this fork)
2. **Original Project:** https://github.com/ct-Open-Source/tuya-convert/issues/483
3. **Discussion:** Check for pinned issues or discussions about PSK research

## Next Steps

If you want to dive deeper into the technical details:

- **[PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md)** - Complete technical documentation
- **[PSK Key Extraction Example](PSK-Key-from-Gosund-Wifi-Bulb.md)** - Hardware extraction walkthrough
- **[Troubleshooting](Troubleshooting.md)** - Common issues with newer devices

---

## Related Pages

- [PSK Identity 02 Protocol Documentation](Collaboration-document-for-PSK-Identity-02.md)
- [PSK Key Extraction from Gosund Bulb](PSK-Key-from-Gosund-Wifi-Bulb.md)
- [Troubleshooting Guide](Troubleshooting.md)
- [Compatible Devices](Compatible-devices.md)

---

**Thank you for contributing to this research! Every piece of data helps us understand the PSK system better.**
