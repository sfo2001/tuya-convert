# Related Projects and Ecosystem

**Last Updated:** 2025-11-07
**Status:** 📚 Complete
**Related:** [Alternative Chips](Alternative-Chips-And-Flashing.md) | [PSK Identity 02](Collaboration-document-for-PSK-Identity-02.md)

---

## Overview

This document catalogs related projects in the Tuya device hacking ecosystem. As Tuya has implemented countermeasures against OTA flashing (PSK v2, chipset switches), the community has developed multiple approaches to regain local control of IoT devices.

**Key Takeaway:** While tuya-convert pioneered ESP8266/ESP8285 OTA flashing, the ecosystem has evolved to address new challenges including PSK v2 firmware and alternative chipsets.

---

## Table of Contents

1. [OTA Flashing Tools](#ota-flashing-tools)
2. [Alternative Firmware Projects](#alternative-firmware-projects)
3. [Chipset-Specific Projects](#chipset-specific-projects)
4. [API and Cloud Control](#api-and-cloud-control)
5. [PSK v2 Status Across Projects](#psk-v2-status-across-projects)
6. [Hardware Coverage Comparison](#hardware-coverage-comparison)
7. [Community Resources](#community-resources)

---

## OTA Flashing Tools

### tuya-convert (This Project)
**Repository:** https://github.com/ct-Open-Source/tuya-convert

**Description:** The original OTA flashing tool exploiting Tuya's SmartConfig pairing process.

**Hardware Support:**
- ✅ ESP8266
- ✅ ESP8285
- ❌ Non-ESP chips (BK7231, ECR6600, etc.)

**PSK v2 Status:** ❌ **Does not support PSK v2** (PSK ID starting with "02")

**Advantages:**
- No hardware modification required
- Automatic firmware backup
- Well-documented and tested
- Active community

**Limitations:**
- Only works with vulnerable firmware (pre-PSK v2)
- Only supports ESP82xx chipsets
- Requires specific timing during device pairing

**When to Use:**
- ESP82xx devices purchased before 2020
- Devices that have never been paired with official app
- When you want non-destructive testing before serial flashing

---

### tuya-cloudcutter
**Repository:** https://github.com/tuya-cloudcutter/tuya-cloudcutter

**Description:** Successor approach exploiting cloud connectivity to flash devices OTA, supporting devices and chipsets that tuya-convert cannot handle.

**Hardware Support:**
- ✅ ESP8266/ESP8285
- ✅ **BK7231T** (Beken)
- ✅ **BK7231N** (Beken)
- ✅ **BL2028N** (Bouffalo Lab)
- ✅ Other non-ESP Tuya chips

**PSK v2 Status:** ⚠️ **Partially affected** - Some devices with PSK v2 fail, but workarounds exist using alternative device profiles

**Approach:**
- Exploits device-cloud handshake vulnerabilities
- Can flash non-ESP devices (major advantage over tuya-convert)
- Does not require SmartConfig timing

**Key Issues:**
- GitHub Issue #88: Treatlife SL10 - PSK ID 02 errors
- GitHub Issue #210: LSC Smart Plug 970766 - "Using PSK v1 - Received PSK ID version 02" error

**Workarounds:**
- Try different device profiles (e.g., `oem-bk7231n-plug-1.1.8-sdk-2.3.1-40.00.json`)
- Check wiki for known patched firmware: https://github.com/tuya-cloudcutter/tuya-cloudcutter/wiki/Known-Patched-Firmware

**Advantages over tuya-convert:**
- Supports BK7231 and other non-ESP chips
- Different exploit vector (may work when tuya-convert fails)
- Can flash LibreTiny compatible firmware

**When to Use:**
- Device has BK7231 or other non-ESP chip
- tuya-convert failed
- Device manufactured 2020-2023 (transition period)

**Website:** https://tuya-cloudcutter.github.io/ (device compatibility list)

---

## Alternative Firmware Projects

### Tasmota
**Repository:** https://github.com/arendst/Tasmota

**Description:** The most popular alternative firmware for ESP82xx/ESP32 devices.

**Hardware Support:**
- ✅ ESP8266/ESP8285
- ✅ ESP32/ESP32-S2/ESP32-C3
- ❌ Non-ESP chips

**Features:**
- Web UI configuration
- MQTT support
- Home Assistant auto-discovery
- Extensive sensor support
- Large community and device templates

**Flashing Methods:**
- tuya-convert (for vulnerable devices)
- Serial flashing (UART)
- OTA updates after initial flash

**When to Use:**
- You have ESP-based device
- Need mature, well-documented firmware
- Want extensive Home Assistant integration

---

### ESPurna
**Repository:** https://github.com/xoseperez/espurna

**Description:** Alternative firmware focused on efficiency and flexibility.

**Hardware Support:**
- ✅ ESP8266/ESP8285
- ❌ Non-ESP chips

**Features:**
- Lower memory footprint than Tasmota
- Web UI
- MQTT, Alexa, Domoticz support
- OTA updates

**When to Use:**
- Limited flash/RAM on device
- Need specific feature set

---

### OpenBeken (OpenBK7231T_App)
**Repository:** https://github.com/openshwprojects/OpenBK7231T_App

**Description:** Open-source firmware for non-ESP Tuya devices. **This is the primary solution for devices with alternative chipsets.**

**Hardware Support:**
- ✅ **Beken BK7231T**
- ✅ **Beken BK7231N**
- ✅ **Eswin ECR6600** (Wi-Fi 6)
- ✅ **Realtek RTL8710/RTL8720**
- ✅ **WinnerMicro W800/W801, W600/W601**
- ✅ **Tuya T34**
- ✅ **BL2028N** (Bouffalo Lab)
- ✅ **XinRui XR809**
- ✅ **BL602** (Bouffalo Lab)
- ✅ **LN882H**

**Features:**
- Home Assistant auto-discovery (MQTT)
- Web interface (similar to Tasmota)
- OTA updates after initial serial flash
- GPIO control for relays, dimmers, LEDs
- Power monitoring support
- Sensor support (temperature, humidity, etc.)
- 100% local control

**Flashing Methods:**
- Serial/UART flashing (required for initial flash)
- tuya-cloudcutter (for compatible devices)
- OTA updates after initial flash

**Why This Matters:**
By 2025, non-ESP chips represent the **majority** of new Tuya devices. OpenBeken provides feature parity with Tasmota for these chips.

**When to Use:**
- Device has non-ESP chip (BK7231, ECR6600, RTL8xxx, W800, etc.)
- tuya-convert/tuya-cloudcutter failed with "does not use ESP82xx" warning
- Willing to do serial flashing (one-time hardware access)

**Device Database:** https://openbekeniot.github.io/webapp/devicesList.html

**See Also:** [Alternative Chips and Flashing Guide](Alternative-Chips-And-Flashing.md) for detailed OpenBeken flashing instructions

---

### LibreTiny
**Repository:** https://github.com/kuba2k2/libretiny

**Description:** Framework providing a unified API for non-ESP chips, enabling ESPHome support for BK7231, RTL8710, and other chipsets.

**Hardware Support:**
- ✅ BK7231T/N/Q/U
- ✅ RTL8710B, RTL8720C
- ✅ BL602

**Integration:**
- ESPHome support for non-ESP chips
- Works with tuya-cloudcutter
- Arduino core compatibility layer

**When to Use:**
- Want to use ESPHome with non-ESP devices
- Need unified codebase across ESP and non-ESP devices

---

## Chipset-Specific Projects

### Zigbee Devices

#### doctor64/tuyaZigbee
**Repository:** https://github.com/doctor64/tuyaZigbee

**Description:** Replacement firmware for Tuya Zigbee devices based on Telink chips.

**Hardware Support:**
- ✅ **Telink TLSR8258**
- ✅ Tuya modules: ZT3L, ZTLC5, ZTU-IPEX, ZTU, ZT5, ZT2S, ZTC

**Flashing Method:** Serial (SWS protocol)

**Key Point:** Completely different from Wi-Fi devices - these are Zigbee coordinators/routers.

**Limitations:**
- Some complex devices (thermostats, roller shutters) use dual MCU architecture
- Telink handles Zigbee, separate MCU controls hardware
- Replacement firmware may not work for dual-MCU devices

---

#### pvvx/ZigbeeTLc
**Repository:** https://github.com/pvvx/ZigbeeTLc

**Description:** Custom firmware for Zigbee 3.0 IoT devices on TLSR825x chips.

**Hardware Support:**
- ✅ TLSR825x chips
- ✅ Temperature/humidity sensors
- ✅ Door sensors
- ✅ Motion sensors

---

### Bluetooth/BLE Devices

#### pvvx/THB2
**Repository:** https://github.com/pvvx/THB2

**Description:** Custom firmware for Tuya devices on the PHY622x2 chipset (Phyplus BLE chips).

**Hardware Support:**
- ✅ PHY622x2 chipset
- ✅ BLE temperature/humidity sensors

**Flashing Method:** Serial or OTA (device-dependent)

---

### Other Wi-Fi Chipsets

#### WDoorSensor
**Repository:** https://github.com/klausahrenberg/WDoorSensor

**Description:** Replacement firmware specifically for Tuya door/window sensors with ESP8266.

**Hardware Support:**
- ✅ ESP8266-based door sensors
- ✅ Battery-powered devices

---

## API and Cloud Control

### TuyAPI (Node.js)
**Repository:** https://github.com/codetheweb/tuyapi

**Description:** NPM library for **LAN control** of Tuya devices **with stock firmware**.

**Approach:**
- No firmware replacement needed
- Reverse-engineered local protocol
- Requires device key extraction

**Advantages:**
- No hardware modification
- Works with stock firmware
- LAN control (no cloud required for operation)

**Disadvantages:**
- Requires initial cloud connection to obtain device keys
- Keys may change with firmware updates
- Limited to devices that support local control

**When to Use:**
- Don't want to flash firmware
- Need quick local control solution
- Device works well but want Home Assistant integration

---

### python-tuya
**Repository:** https://github.com/clach04/python-tuya

**Description:** Python library for local control of Tuya devices with stock firmware.

**Similar to TuyAPI but for Python ecosystem.**

---

### tinytuya
**Repository:** https://github.com/jasonacox/tinytuya

**Description:** Python module for Tuya device control (both local and cloud).

**Features:**
- Device discovery
- Cloud API access
- Local protocol support
- Device monitoring
- Gateway to MQTT bridge

---

### MockTuyaCloud
**Repository:** https://github.com/kueblc/mocktuyacloud

**Description:** Framework replicating Tuya cloud functionality for local control without firmware changes.

**Approach:**
- DNS/routing redirect to local server
- Implements Tuya cloud API locally
- Devices think they're talking to Tuya cloud

**When to Use:**
- Can't or don't want to flash firmware
- Need to intercept cloud traffic
- Research/reverse engineering purposes

---

## PSK v2 Status Across Projects

### What is PSK v2?

PSK Identity version 02 is a security enhancement Tuya deployed starting in late 2019/early 2020. Devices with PSK v2:
- Use Pre-Shared Key (PSK) stored in device flash
- PSK is unique per device
- PSK is only known to device and Tuya cloud
- PSK ID in TLS handshake reveals version: `ID: 02...`

**Detection:** Check `smarthack-psk.log` for lines starting with `ID: 02` followed by `DECRYPTION_FAILED_OR_BAD_RECORD_MAC` error.

### Project Compatibility Matrix

| Project | PSK v2 Support | Notes |
|---------|---------------|-------|
| **tuya-convert** | ❌ No | Cannot decrypt PSK v2 TLS sessions |
| **tuya-cloudcutter** | ⚠️ Partial | Some PSK v2 devices fail; workarounds exist with alternative profiles |
| **Serial Flashing** | ✅ Yes | **PSK v2 does not affect serial flashing** - direct flash chip access bypasses all security |
| **OpenBeken** | ✅ Yes | Flashed via serial, PSK irrelevant |
| **Tasmota** | ✅ Yes | If flashed via serial |
| **TuyAPI** | ⚠️ Maybe | Depends on device local protocol version |

### Current PSK v2 Research Status

**Consensus (as of 2025-11-07):** PSK v2 is **not crackable via OTA methods** without the device-specific PSK key.

**Why It's Hard:**
- PSK is 37-character random string (likely base62 encoding of 224-bit value)
- Stored only on device flash and Tuya servers
- Not derivable from public information (gwId, MAC, etc.)
- Previous PSK v1 leaked secret info via PSK ID; PSK v2 does not

**Only Known PSK v2 Retrieval Methods:**
1. **Serial flash dump** → Extract PSK from flash memory at 0xFB000 (JSON blob)
   - Requires opening device
   - At which point you might as well flash custom firmware
2. **Capture upgrade traffic** → Devices upgrading from PSK v1 to PSK v2 fetch key via `tuya.device.uuid.pskkey.get` API
   - Requires vulnerable device upgrading
   - Communication is encrypted
3. **Tuya developer account** → Some devices allow PSK retrieval via official API
   - Requires device registration
   - Not available for all devices

**See:** [PSK Identity 02 Collaboration Document](Collaboration-document-for-PSK-Identity-02.md) for detailed research.

---

## Hardware Coverage Comparison

### ESP-Based Devices (ESP8266, ESP8285, ESP32)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| tuya-convert | ✅ Yes (PSK v1 only) | N/A | ⭐ Easy |
| Tasmota | N/A | ✅ Yes | ⭐⭐ Medium |
| ESPurna | N/A | ✅ Yes | ⭐⭐ Medium |
| TuyAPI | N/A (no flash) | N/A (no flash) | ⭐ Easy (setup) |

---

### Beken Chips (BK7231T, BK7231N)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| tuya-cloudcutter | ⚠️ Sometimes | N/A | ⭐⭐ Medium |
| OpenBeken | N/A | ✅ Yes | ⭐⭐ Easy (GUI tool) |
| LibreTiny + ESPHome | N/A | ✅ Yes | ⭐⭐⭐ Medium |

**Prevalence:** By 2024-2025, BK7231 chips are found in **~40-50%** of budget Tuya devices (<$10 price range).

**Flashing Tool:** BK7231GUIFlashTool (user-friendly, forgiving timing)

---

### Eswin ECR6600 (Wi-Fi 6 Chip)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| tuya-cloudcutter | ❓ Unknown | N/A | N/A |
| OpenBeken | N/A | ✅ Yes | ⭐⭐⭐ Medium (timing-critical) |

**Prevalence:** Rapidly increasing in 2024-2025, especially in newer/higher-power devices (15A+ plugs, Wi-Fi 6 marketed devices).

**Flashing Tool:** RDTool (requires precise power-on timing)

**Challenge:** Tighter timing window than BK7231; expect 3-5 attempts to get timing right.

---

### Realtek Chips (RTL8710, RTL8720)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| tuya-cloudcutter | ⚠️ Sometimes | N/A | ⭐⭐ Medium |
| OpenBeken | N/A | ✅ Yes | ⭐⭐⭐ Medium |
| LibreTiny | N/A | ✅ Yes | ⭐⭐⭐ Medium |

**Prevalence:** Less common than BK7231/ECR6600 but found in some devices.

---

### WinnerMicro (W800/W801)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| OpenBeken | N/A | ✅ Yes | ⭐⭐⭐ Medium |

**Prevalence:** Increasingly common in 2024-2025 devices.

---

### Telink Zigbee (TLSR8258)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| doctor64/tuyaZigbee | N/A | ✅ Yes (SWS) | ⭐⭐⭐⭐ Hard |

**Note:** Zigbee devices, not Wi-Fi. Requires SWS programming protocol.

---

### Phyplus BLE (PHY622x2)

| Project | OTA Flash | Serial Flash | Difficulty |
|---------|-----------|--------------|------------|
| pvvx/THB2 | ⚠️ Device-dependent | ✅ Yes | ⭐⭐⭐ Medium |

**Note:** Bluetooth Low Energy devices (sensors).

---

## Community Resources

### Forums and Discussion

1. **elektroda.com RTVForum** (Polish, use Google Translate)
   - https://www.elektroda.com/rtvforum/
   - **Best source for teardowns, pinouts, and chipset identification**
   - Active community reverse-engineering Tuya devices
   - Search topics: "tuya", "BK7231", "tuya-cloudcutter"

2. **Home Assistant Community**
   - https://community.home-assistant.io/
   - Search: "tuya", "OpenBeken", "tuya-cloudcutter"
   - Integration guides and support

3. **Tasmota Community**
   - https://github.com/arendst/Tasmota/discussions
   - Device templates and support

4. **OpenBeken Discord**
   - Link in GitHub repo README
   - Real-time help with flashing and configuration

### Device Databases

1. **tuya-convert Compatible Devices**
   - [HTTP firmware devices](Compatible-devices-(HTTP-firmware).md)
   - [HTTPS firmware devices](Compatible-devices-(HTTPS-firmware).md)
   - [PSK Identity 02 Affected Devices](PSK-Identity-02-Affected-Devices.md)

2. **tuya-cloudcutter Devices**
   - https://tuya-cloudcutter.github.io/
   - Device profiles and compatibility

3. **OpenBeken Devices**
   - https://openbekeniot.github.io/webapp/devicesList.html
   - Pin configurations and templates

4. **Tasmota Templates**
   - https://templates.blakadder.com/
   - Searchable database of device configs

### Tools and Utilities

1. **OpenBeken Flash Tools**
   - https://github.com/openshwprojects/FlashTools
   - Contains all chip-specific flashing tools (RDTool, BK7231GUIFlashTool, etc.)

2. **Tuya Developer Platform**
   - https://iot.tuya.com/
   - Device registration and (sometimes) PSK retrieval
   - API documentation

3. **Tuya Reverse Engineering**
   - https://github.com/nalajcie/tuya-sign-hacking
   - Tools for reverse engineering Tuya API signing algorithm
   - https://github.com/xety1337/tuya-reverse

### Video Tutorials

Search YouTube for:
- "tuya-convert flashing"
- "OpenBeken flashing"
- "BK7231 serial flash"
- "ECR6600 tuya flash"
- "tuya-cloudcutter tutorial"

### Hardware Suppliers

**USB-UART Adapters:**
- Amazon: Search "CP2102 USB UART 3.3V" or "CH340G USB TTL"
- AliExpress: Search "USB serial adapter 3.3V"

**Pogo Pin Jigs:**
- AliExpress: Search "BK7231 programming jig" or "spring loaded test pins"

---

## Comparison Table: When to Use Which Project

| Scenario | Recommended Project | Reason |
|----------|---------------------|--------|
| ESP8266 device, never paired | tuya-convert | Non-destructive, easy OTA flash |
| ESP8266 device, PSK v2 | Serial flash + Tasmota | OTA blocked, serial works |
| BK7231 device, new | Serial flash + OpenBeken | No OTA available, serial reliable |
| BK7231 device, want to try OTA first | tuya-cloudcutter | May work, non-destructive to try |
| ECR6600 device | Serial flash + OpenBeken | OTA unlikely, OpenBeken is mature |
| Don't want to flash firmware | TuyAPI or tinytuya | Local control with stock firmware |
| Zigbee device (TLSR8258) | doctor64/tuyaZigbee | Zigbee-specific firmware |
| BLE sensor (PHY622x2) | pvvx/THB2 | BLE-specific firmware |
| ESPHome user with BK7231 | LibreTiny | Enables ESPHome on non-ESP |
| Research/reverse engineering | MockTuyaCloud | Local cloud simulator |

---

## Future Outlook

### Chip Migration Trends

**2019-2020:** ~90% ESP8266/ESP8285
**2021-2022:** ~60% ESP, ~40% BK7231/others
**2023-2024:** ~40% ESP, ~60% BK7231/ECR6600/others
**2025+:** Projected ~30% ESP, ~70% non-ESP

**Drivers:**
- Cost: BK7231 cheaper than ESP8266
- Wi-Fi 6: ECR6600 supports newer standard
- Supply chain: Diversification away from single vendor
- Security: Harder to flash = better for manufacturers (worse for consumers)

### PSK Evolution

**PSK v1** (pre-2019): Exploitable by tuya-convert
**PSK v2** (2019-present): Blocks OTA methods
**PSK v3?** (future): Possible further hardening

**Community Response:**
- Focus shifting from OTA to serial flashing
- OpenBeken maturity increasing
- Tool UX improving (BK7231GUIFlashTool, etc.)

### Serial Flashing Acceptance

**Past:** Seen as "last resort"
**Present:** Increasingly normalized
**Future:** May become standard approach

**Why:**
- One-time effort, then OTA updates forever
- Works regardless of PSK version
- Works for all chipsets
- Learning curve decreasing (better tools, more tutorials)

---

## Contributing

Found a new project? Tested a device? Have updates?

1. **Edit this document** via pull request
2. **Add device entries** to [compatible device lists](Compatible-devices.md)
3. **Share research** in [PSK Identity 02 document](Collaboration-document-for-PSK-Identity-02.md)
4. **Report issues** at https://github.com/ct-Open-Source/tuya-convert/issues

---

## Acknowledgments

This document consolidates research and development from:
- VTRUST and c't magazine (original tuya-convert)
- tuya-cloudcutter community
- OpenBeken/openshwprojects developers
- doctor64 (Zigbee firmware)
- pvvx (BLE firmware)
- elektroda.com community
- Home Assistant community
- Countless individual contributors

**Thank you to everyone working to make IoT devices more open and user-controlled.**

---

*Last Updated: 2025-11-07*
*Maintainer: Community*
