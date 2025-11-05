# Protocol Overview

This section provides an overview of the various protocols used by tuya-convert to intercept and manipulate Tuya device activation and firmware flashing.

## Quick Navigation

### Security Protocols
- [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) - TLS-PSK encryption protocol used by newer devices
- [PSK Research Procedures](PSK-Research-Procedures.md) - How to capture and analyze PSK protocol data
- [PSK Research Tools](PSK-Research-Tools.md) - Tools for PSK protocol research (Phase 5)

### Pairing & Discovery Protocols
- **Smartconfig Protocol** - WiFi configuration via packet length encoding (implementation: `scripts/smartconfig/`)
- **Tuya Discovery Protocol** - UDP broadcast device discovery (implementation: `scripts/tuya-discovery.py`)

### Cloud Communication Protocols
- **Device Registration Protocol** - HTTP/HTTPS device activation and registration (implementation: `scripts/fake-registration-server.py`)
- **MQTT Protocol** - Device command and control messaging (implementation: `scripts/mq*.py`)

---

## Overview

tuya-convert intercepts multiple protocols used during the Tuya device lifecycle to perform OTA firmware flashing:

### 1. PSK Identity 02 Protocol

**Status:** 🔴 **Blocking Issue** - Prevents OTA flashing on newer devices

**Purpose:** TLS-PSK (Pre-Shared Key) encryption for secure device-cloud communication

**Implementation:** `scripts/psk-frontend.py`

**Key Characteristics:**
- Uses TLS_PSK_WITH_AES_128_CBC_SHA256 cipher suite
- PSK Identity format: `0x02` + prefix + SHA256(gwId)
- Each device has unique PSK stored in firmware
- Prevents OTA firmware updates without knowing device-specific PSK

**Affected Devices:** Devices with firmware SDK version 2.0.0(29f7e05) or later (Sept 2019+)

**Known Limitations:**
- PSK cannot be derived from publicly available information
- Requires firmware extraction (physical access) to obtain PSK
- Makes OTA flashing strategy non-viable for affected devices

**Documentation:**
- [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) - Full technical details and research
- [PSK Affected Devices](PSK-Identity-02-Affected-Devices.md) - List of ~220 known incompatible devices
- [PSK Research Procedures](PSK-Research-Procedures.md) - How to contribute to research

---

### 2. Smartconfig Protocol

**Status:** ✅ **Working** - Successfully configures device WiFi credentials

**Purpose:** Wireless WiFi configuration without physical device access

**Implementation:** `scripts/smartconfig/smartconfig.py`

**Key Characteristics:**
- Encodes SSID, password, and tokens in UDP packet lengths
- Uses broadcast (port 30011) and multicast (port 30012) strategies
- Device listens in promiscuous mode and decodes packet lengths
- No prior network connection required

**How It Works:**
1. Device enters pairing mode (listens promiscuously)
2. Smartphone/computer broadcasts encoded WiFi credentials
3. Device decodes credentials from packet length patterns
4. Device connects to specified WiFi network
5. Device proceeds to cloud registration

**Implementation Details:**
- Broadcast strategy ported from [tuyapi/link](https://github.com/tuyapi/link)
- Multicast strategy reverse engineered by kueblc
- Uses CRC validation for data integrity
- Packet gap: 5ms between transmissions

**Code References:**
- `scripts/smartconfig/smartconfig.py` - Main protocol implementation
- `scripts/smartconfig/broadcast.py` - Broadcast encoding strategy
- `scripts/smartconfig/multicast.py` - Multicast encoding strategy
- `scripts/smartconfig/crc.py` - CRC calculation utilities

**When Used:** During initial device pairing to configure WiFi network

---

### 3. Tuya Discovery Protocol

**Status:** ✅ **Working** - Device discovery functional

**Purpose:** Discover Tuya devices on the local network and retrieve device information

**Implementation:** `scripts/tuya-discovery.py`

**Key Characteristics:**
- Uses UDP broadcast on ports 6666 and 6667
- Discovers device IP address, gwId, and product ID
- Works on local network without cloud access
- Devices respond with JSON-encoded device information

**How It Works:**
1. Broadcast discovery request on UDP ports 6666/6667
2. Devices respond with identity information (gwId, productKey, IP)
3. System collects device information for registration process

**Code Reference:** `scripts/tuya-discovery.py`

**When Used:** After device connects to WiFi, before cloud registration

---

### 4. Device Registration & Activation Protocol

**Status:** ✅ **Working** - Successfully intercepts device registration

**Purpose:** Intercept device activation and redirect to custom firmware download

**Implementation:** `scripts/fake-registration-server.py`

**Key Characteristics:**
- HTTP/HTTPS server mimicking Tuya cloud endpoints
- Intercepts device registration and token exchange
- Provides fake firmware upgrade URLs
- Serves custom firmware (stage 1 & stage 2)

**Key Endpoints:**
- `/gw.json` - Gateway configuration
- `/d.json` - Device activation and token exchange
- `/upgrade.json` - Firmware upgrade information
- Various cloud API endpoints (`tuya.device.timer.count`, etc.)

**How It Works:**
1. Device sends activation request to "Tuya cloud" (our fake server)
2. Server responds with fake tokens and device configuration
3. Device requests firmware upgrade information
4. Server provides URL to custom firmware
5. Device downloads and flashes custom firmware

**Code Reference:** `scripts/fake-registration-server.py` (lines 216-432)

**When Used:** During device activation and firmware upgrade process

---

### 5. MQTT Protocol

**Status:** ✅ **Working** - MQTT communication supported

**Purpose:** Device command and control messaging

**Implementation:** Mosquitto broker + Python scripts (`scripts/mq*.py`)

**Key Characteristics:**
- Standard MQTT protocol on port 1883
- Topics include device status, commands, and responses
- Used for device control and monitoring
- Part of the Tuya IoT ecosystem

**Code References:**
- `scripts/mq_pub_15.py` - MQTT message publishing
- Mosquitto broker (configured in `start_flash.sh`)

**When Used:** Post-activation device communication

---

## Protocol Lifecycle During Flashing

The protocols are used in sequence during a typical flashing operation:

```
1. Device Reset → Pairing Mode
   └─> Smartconfig Protocol

2. Device Receives WiFi Credentials
   └─> Connects to "vtrust-flash" network

3. Device Discovery
   └─> Tuya Discovery Protocol (UDP 6666/6667)

4. Device Activation
   └─> Registration Protocol (HTTP/HTTPS)
   └─> PSK Protocol (if supported by device)

5. Firmware Upgrade Request
   └─> Registration Protocol provides firmware URL

6. Firmware Download & Flash
   └─> HTTP download of custom firmware

7. Post-Flash Communication
   └─> MQTT Protocol (optional)
```

---

## Implementation Status Summary

| Protocol | Status | Implementation File(s) | Blocking Issue |
|----------|--------|------------------------|----------------|
| PSK Identity 02 | 🔴 Research | `scripts/psk-frontend.py` | Yes - prevents OTA on new devices |
| Smartconfig | ✅ Working | `scripts/smartconfig/*.py` | No |
| Tuya Discovery | ✅ Working | `scripts/tuya-discovery.py` | No |
| Registration | ✅ Working | `scripts/fake-registration-server.py` | No |
| MQTT | ✅ Working | `scripts/mq*.py` | No |

---

## Known Limitations

### PSK Identity 02 Issue
- **Impact:** Prevents OTA flashing on devices manufactured after ~September 2019
- **Root Cause:** Device-specific PSK stored only on device and Tuya servers
- **Workaround:** None for OTA; requires physical access (serial flashing)
- **Research Status:** Active community research, no breakthrough yet

### Smartconfig Restrictions
- **Newer Devices:** Some newer devices use modified smartconfig with additional restrictions
- **Encrypted Variants:** Some devices use encrypted smartconfig (implementation pending)

### Network Requirements
- **Open Network Required:** vtrust-flash network must be open (no WPA/WPA2)
- **No Internet Needed:** Device flashing works offline
- **DNS Spoofing:** All Tuya domains redirected to local server

---

## Related Documentation

### System Architecture
- [System Architecture](System-Architecture.md) - Complete system component overview
- [Quick Start Guide](Quick-Start-Guide.md) - Step-by-step flashing walkthrough

### Setup Guides
- [Installation](Installation.md) - Install prerequisites and dependencies
- [Using Docker](Using-Docker.md) - Docker setup for protocol services

### Troubleshooting
- [Troubleshooting](Troubleshooting.md) - Common protocol issues
- [Failed Attempts and Requirements](Failed-attempts-and-tracked-requirements.md) - Known device limitations

### Research & Contribution
- [PSK Research Procedures](PSK-Research-Procedures.md) - How to help with PSK protocol research
- [How to Contribute](How-to-Contribute.md) - Contributing guide (Phase 4.7)

---

## External References

- **TuyAPI Project:** https://github.com/codetheweb/tuyapi - Tuya device control library
- **Tuya IoT Platform:** https://iot.tuya.com/ - Official Tuya developer platform
- **Original PSK Issue Discussion:** [Issue #483](https://github.com/ct-Open-Source/tuya-convert/issues/483)
- **Smartconfig Reference:** https://github.com/tuyapi/link - Original smartconfig implementation

---

*Back to [Home](Home)*
