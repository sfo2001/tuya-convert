# System Architecture

**Last Updated:** 2025-11-07
**Status:** ✅ Complete
**Implementation:** Multiple components (see Code References)

## Overview

tuya-convert uses a sophisticated multi-component architecture to intercept and manipulate the device activation process of Tuya-based IoT devices. The system creates a fake Tuya cloud environment that tricks devices into installing custom firmware instead of connecting to the official Tuya cloud.

**Architecture Strategy:**
- **Rogue Access Point** - Fake WiFi network that devices connect to
- **Fake Cloud Services** - Intercept and respond to device registration/upgrade requests
- **Protocol Handlers** - Handle PSK encryption, smartconfig pairing, discovery
- **Firmware Delivery** - Serve intermediate and final custom firmware

**Attack Surface:** Device activation and OTA firmware upgrade process

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         HOST COMPUTER (Linux)                          │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     tuya-convert System                       │   │
│  │                                                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌─────────────┐             │   │
│  │  │  Access    │  │   DHCP/    │  │  Smartconfig│             │   │
│  │  │   Point    │  │    DNS     │  │  Broadcast  │             │   │
│  │  │ (hostapd)  │  │ (dnsmasq)  │  │  (UDP)      │             │   │
│  │  └────┬───────┘  └──────┬─────┘  └──────┬──────┘             │   │
│  │       │                 │                │                     │   │
│  │       └─────────────────┴────────────────┘                     │   │
│  │                         │                                       │   │
│  │           ┌─────────────┴───────────────────┐                  │   │
│  │           │    WiFi Interface (wlan0)      │                  │   │
│  │           │       10.42.42.1/24            │                  │   │
│  │           └─────────────┬───────────────────┘                  │   │
│  │                         │                                       │   │
│  │  ┌──────────────────────┴────────────────────────────┐         │   │
│  │  │         Application Layer Services                │         │   │
│  │  │                                                    │         │   │
│  │  │  ┌──────────┐ ┌───────────┐ ┌────────────────┐  │         │   │
│  │  │  │   Web    │ │   MQTT    │ │  PSK Frontend  │  │         │   │
│  │  │  │  Server  │ │  Broker   │ │  (TLS-PSK)     │  │         │   │
│  │  │  │ (HTTP)   │ │(Mosquitto)│ │  Proxy         │  │         │   │
│  │  │  │  :80     │ │  :1883    │ │  :443 → :8886  │  │         │   │
│  │  │  └────┬─────┘ └─────┬─────┘ └────────┬───────┘  │         │   │
│  │  │       │             │                 │           │         │   │
│  │  │  ┌────┴─────────────┴─────────────────┴─────┐    │         │   │
│  │  │  │         Tuya Discovery Service           │    │         │   │
│  │  │  │         (UDP :6666, :6667)               │    │         │   │
│  │  │  └──────────────────────────────────────────┘    │         │   │
│  │  └──────────────────────────────────────────────────┘         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                      ┌─────────┴─────────┐
                      │   vtrust-flash    │
                      │   WiFi Network    │
                      │   10.42.42.0/24   │
                      └─────────┬─────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
  ┌─────┴──────┐       ┌────────┴────────┐      ┌──────┴────────┐
  │ Smartphone │       │  Tuya IoT Device│      │   (Other)     │
  │  (Helper)  │       │   (Target)      │      │   Devices     │
  │            │       │   10.42.42.42   │      │               │
  └────────────┘       └─────────────────┘      └───────────────┘
```

---

## Component Architecture

### 1. Network Layer

#### 1.1 Access Point (hostapd)

**Purpose:** Create fake WiFi network for devices to connect to

**Implementation:** `scripts/setup_ap.sh` (line 55-59)

**Configuration:**
- SSID: `vtrust-flash` (configurable via `config.txt`)
- Network: 10.42.42.0/24
- Gateway: 10.42.42.1
- No encryption (open network)

**Process:**
```bash
# Interface configuration
sudo ip link set $WLAN down
sudo ip addr add $GATEWAY/24 dev $WLAN
sudo ip link set $WLAN up
sudo ip route add 10.42.42.0/24 dev $WLAN src $GATEWAY
```

**Dependencies:**
- Stops NetworkManager/wpa_supplicant to prevent conflicts
- Unblocks WiFi with rfkill
- Requires interface supporting AP mode

#### 1.2 DHCP Server (dnsmasq)

**Purpose:** Assign IP addresses and redirect all DNS queries to gateway

**Implementation:** `scripts/setup_ap.sh` (line 45-53)

**Configuration:**
```bash
sudo dnsmasq \
    --no-resolv \
    --interface=$WLAN \
    --bind-interfaces \
    --listen-address=$GATEWAY \
    --except-interface=lo \
    --dhcp-range=10.42.42.10,10.42.42.40,12h \
    --address=/#/$GATEWAY
```

**Key Features:**
- DHCP range: 10.42.42.10 - 10.42.42.40
- DNS wildcard: All domains resolve to 10.42.42.1
- Critical: Device MUST receive IP 10.42.42.42 from intermediate firmware

---

### 2. Application Services Layer

#### 2.1 Fake Registration Server (HTTP)

**Purpose:** Intercept device activation and upgrade requests

**Implementation:** `scripts/fake-registration-server.py`

**Endpoints:**

| Endpoint | Method | Purpose | Line Ref |
|----------|--------|---------|----------|
| `/d.json` | GET/POST | Device activation | ~128 |
| `/d.json/v2` | GET/POST | Activation v2 | ~142 |
| `/gw.json` | GET/POST | Gateway activation | ~156 |
| `/upgrade.json` | GET/POST | Firmware upgrade info | ~170 |
| `/files/*` | GET | Firmware file delivery | ~210 |

**Encryption:**
- Supports both encrypted (protocol 2.2) and unencrypted (2.1) modes
- AES-ECB encryption with configurable secret key
- Default key: `0000000000000000` (16 bytes)

**Firmware Upgrade Response:**
```python
{
    "success": true,
    "result": {
        "url": "http://10.42.42.1/files/upgrade.bin",
        "md5": "...",
        "version": "9.0.0",
        "size": 524288
    }
}
```

#### 2.2 MQTT Broker (Mosquitto)

**Purpose:** Handle device communication protocol

**Implementation:** mosquitto + `scripts/mosquitto.conf`

**Configuration:**
- Port: 1883 (unencrypted MQTT)
- Anonymous access enabled
- No authentication required

**Usage:**
- Devices publish status updates
- Devices subscribe to command topics
- Used for device state management

**Note:** Minimal role in flashing process; primarily for device communication after intermediate firmware installed.

#### 2.3 PSK Frontend (TLS-PSK Proxy)

**Purpose:** Terminate TLS-PSK connections and proxy to HTTP server

**Implementation:** `scripts/psk-frontend.py`

**Architecture:**
```
Device (TLS-PSK :443) → PSK Frontend → HTTP Server (:8886)
                         ↓
                    Decrypt/Encrypt
```

**PSK Generation Algorithm:**
```python
def gen_psk(identity, hint):
    # Identity format: '\x02' + 'BAohbmd6aG91IFR1' + sha256(gwId)
    key = md5(hint[-16:]).digest()
    iv = md5(identity).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    psk = cipher.encrypt(identity[:32])
    return psk
```

**Line References:**
- PSK generation: line 26-36
- Hint value: line 48-49
- SSL setup: line 61-66

**Security:**
- TLS 1.2 only
- Cipher: `PSK-AES128-CBC-SHA256`
- Identity must start with PSK Identity prefix

#### 2.4 Tuya Discovery Service (UDP)

**Purpose:** Detect Tuya devices announcing themselves on the network

**Implementation:** `scripts/tuya-discovery.py`

**Listening Ports:**
- UDP 6666: Unencrypted broadcasts
- UDP 6667: Encrypted broadcasts

**Message Handling:**
```python
# Decrypt AES-ECB with key derived from "yGAdlopoPVldABfn"
udpkey = md5(b"yGAdlopoPVldABfn").digest()
```

**Device Detection:**
- Devices broadcast presence on connection
- JSON payload contains device info, abilities
- Typo detection: "ablilty" vs "ability" indicates non-ESP device

---

### 3. Pairing and Flashing Layer

#### 3.1 Smartconfig Protocol

**Purpose:** Send fake WiFi credentials to device in pairing mode

**Implementation:** `scripts/smartconfig/main.py`

**Protocol:**
- Broadcasts WiFi SSID and password via UDP multicast/broadcast
- Encodes credentials in packet length sequence
- Device in fast-blink mode receives and connects

**Process:**
1. Device in pairing mode listens for smartconfig packets
2. Smartconfig broadcasts vtrust-flash credentials
3. Device decodes and connects to fake AP

#### 3.2 Intermediate Firmware

**Purpose:** Gain initial control of device

**Delivery:**
- Served via fake registration server `/files/` endpoint
- Device requests upgrade, receives intermediate firmware
- Intermediate firmware:
  - Exposes HTTP endpoints (backup, flash)
  - Connects with IP 10.42.42.42 (hardcoded)
  - Allows firmware flash and backup retrieval

**Critical Requirement:** Device MUST connect with IP 10.42.42.42 after intermediate firmware installed. This IP is hardcoded in flash scripts.

---

## Data Flow and Sequence of Operations

### Phase 1: Environment Setup

```
start_flash.sh
  │
  ├──→ setup_ap.sh
  │      ├──→ Stop NetworkManager
  │      ├──→ Configure interface (10.42.42.1/24)
  │      ├──→ Start dnsmasq (DHCP + DNS)
  │      └──→ Start hostapd (AP)
  │
  ├──→ fake-registration-server.py (HTTP :80, :8886)
  ├──→ mosquitto (MQTT :1883)
  ├──→ psk-frontend.py (TLS-PSK :443 → HTTP :8886)
  └──→ tuya-discovery.py (UDP :6666, :6667)
```

**Line References:**
- Orchestration: `start_flash.sh` line 66-112
- Service startup: `start_flash.sh` line 85-110

### Phase 2: Device Pairing

```
User Action: Put device in pairing mode (fast blink)
User Action: Connect smartphone to vtrust-flash
User Action: Press ENTER
  │
  └──→ smartconfig/main.py starts
         │
         └──→ Broadcasts fake WiFi credentials
                │
                └──→ Device receives and connects to vtrust-flash
                       │
                       └──→ Device gets IP via DHCP (10.42.42.10-40)
```

**Line References:**
- Smartconfig launch: `start_flash.sh` line 167-169
- Wait loop: `start_flash.sh` line 173-203

### Phase 3: Device Activation and Upgrade

```
Device connects to AP
  │
  ├──→ Gets IP via DHCP (dnsmasq)
  ├──→ Broadcasts presence (UDP 6666/6667) → tuya-discovery.py detects
  │
  ├──→ Attempts DNS lookup for Tuya cloud domains
  │      └──→ All DNS queries return 10.42.42.1 (dnsmasq wildcard)
  │
  ├──→ Connects to "cloud" (actually fake-registration-server)
  │      │
  │      ├──→ HTTP or TLS-PSK connection
  │      │      ├──→ HTTP → fake-registration-server.py :80
  │      │      └──→ TLS-PSK → psk-frontend.py :443 → :8886
  │      │
  │      ├──→ POST /d.json (activation request)
  │      │      └──→ Responds with success + device token
  │      │
  │      └──→ POST /upgrade.json (firmware check)
  │             └──→ Responds with intermediate firmware URL
  │
  └──→ Downloads intermediate firmware from /files/upgrade.bin
         │
         └──→ Installs intermediate firmware and reboots
```

### Phase 4: Intermediate Firmware and Backup

```
Device reboots with intermediate firmware
  │
  ├──→ Connects to vtrust-flash with IP 10.42.42.42 (CRITICAL!)
  │      └──→ start_flash.sh detects connection via ping
  │
  ├──→ Exposes HTTP endpoints:
  │      ├──→ GET http://10.42.42.42/ (device info)
  │      └──→ GET http://10.42.42.42/backup (firmware download)
  │
  └──→ start_flash.sh fetches backup
         │
         └──→ Saved to backups/YYYYMMDD_HHMMSS/
```

**Line References:**
- IP check: `start_flash.sh` line 183
- Backup fetch: `start_flash.sh` line 214-238

### Phase 5: Final Firmware Flash

```
User selects firmware (Tasmota/ESPurna/custom)
  │
  └──→ firmware_picker.sh
         │
         └──→ Uploads firmware to http://10.42.42.42/flash
                │
                └──→ Device installs final firmware and reboots
                       │
                       └──→ Device now running custom firmware (Tasmota/ESPurna)
```

**Line References:**
- Firmware selection: `start_flash.sh` line 244-255

---

## Network Topology

### IP Addressing Scheme

| Component | IP Address | Purpose |
|-----------|------------|---------|
| Gateway (Host) | 10.42.42.1 | All services (HTTP, MQTT, PSK, DNS) |
| DHCP Pool | 10.42.42.10 - 10.42.42.40 | Smartphones, devices (initial) |
| Target Device (Intermediate) | 10.42.42.42 | Device after intermediate firmware (REQUIRED) |

### Port Mapping

| Port | Protocol | Service | Purpose |
|------|----------|---------|---------|
| 80 | HTTP | fake-registration-server.py | Device activation (unencrypted) |
| 443 | TLS-PSK | psk-frontend.py | Device activation (encrypted) |
| 1883 | MQTT | mosquitto | Device communication |
| 6666 | UDP | tuya-discovery.py | Device discovery (unencrypted) |
| 6667 | UDP | tuya-discovery.py | Device discovery (encrypted) |
| 8886 | HTTP | fake-registration-server.py | Backend for PSK proxy |
| 53 | DNS | dnsmasq | DNS wildcard |
| 67/68 | DHCP | dnsmasq | IP address assignment |

### DNS Wildcard Strategy

**All domain lookups return 10.42.42.1:**
```
a.gw.tuyaus.com → 10.42.42.1
a.gw.tuyaeu.com → 10.42.42.1
anything.else.com → 10.42.42.1
```

This ensures devices connect to fake cloud regardless of region or hardcoded domains.

---

## Security Model

### Attack Vector Analysis

**tuya-convert exploits:**
1. **Lack of certificate pinning** - Devices don't verify TLS certificate
2. **Pre-shared key predictability** - PSK can be calculated from device identity
3. **Firmware signature bypass** - Older devices don't verify firmware signatures
4. **Open OTA process** - Devices accept firmware from cloud without authentication

### What tuya-convert DOES:

✅ **Man-in-the-Middle Attack**
- Intercepts device-cloud communication
- Impersonates Tuya cloud servers

✅ **DNS Hijacking**
- Redirects all DNS queries to attacker

✅ **Firmware Replacement**
- Delivers malicious/custom firmware
- Bypasses normal OTA security

### What tuya-convert DOES NOT do:

❌ **Does not exploit code vulnerabilities**
- No buffer overflows, RCE, etc.
- Relies on design flaws, not implementation bugs

❌ **Does not crack encryption**
- Uses device's own encryption keys
- Does not break AES or TLS

❌ **Does not work on patched devices**
- Tuya has patched newer firmware
- Devices with PSK Identity 02 may be protected

### Tuya Countermeasures

Tuya has implemented patches:

1. **PSK Identity 02** (January 2019)
   - New PSK generation algorithm
   - May resist tuya-convert attack

2. **Firmware Signature Validation** (Ongoing)
   - Newer devices verify firmware signatures
   - Prevents custom firmware installation

3. **Certificate Pinning** (Some devices)
   - Validates cloud certificate
   - Prevents MITM attacks

4. **Chipset Migration**
   - Moving from ESP82xx to other chipsets
   - Makes ESP-based firmware incompatible

---

## Code References

### Core Scripts

**Orchestration:**
- `start_flash.sh` - Main entry point
  - setup() function: line 66-112
  - Main loop: line 154-265
  - Device connection check: line 183
  - Backup phase: line 214-238
  - Flashing phase: line 244-255

**Network Setup:**
- `scripts/setup_ap.sh` - AP and network configuration
  - Interface setup: line 38-43
  - DHCP/DNS start: line 45-53
  - AP start: line 55-59

**Application Services:**
- `scripts/fake-registration-server.py` - HTTP/HTTPS fake cloud
  - Encryption functions: line 52-101
  - Request handlers: line 105-231
  - Server setup: line 27-31

- `scripts/psk-frontend.py` - TLS-PSK termination
  - PSK generation: line 26-36
  - Hint value: line 48-49
  - SSL wrapper: line 61-66

- `scripts/tuya-discovery.py` - UDP device discovery
  - Protocol class: line 24-47
  - Decryption: line 19-20
  - ESP detection: line 44-45

**Pairing:**
- `scripts/smartconfig/main.py` - WiFi credentials broadcast
- `scripts/smartconfig/broadcast.py` - UDP broadcast implementation
- `scripts/smartconfig/multicast.py` - Multicast implementation

**Configuration:**
- `config.txt` - AP name, gateway, interface settings
- `scripts/hostapd.conf` - hostapd configuration
- `scripts/mosquitto.conf` - MQTT broker configuration

---

## System Requirements

### Hardware

- **WiFi adapter** supporting AP mode (HostAPd)
- **Sufficient CPU** for AES encryption/decryption
- **Network isolation** (optional but recommended)

### Software

- **Linux kernel** with mac80211 wireless stack
- **hostapd** with AP mode support
- **dnsmasq** for DHCP/DNS
- **Python 3** with pycryptodomex, paho-mqtt, tornado, sslpsk3
- **OpenSSL 1.1.1+** for TLS 1.2 PSK ciphers
- **mosquitto** MQTT broker

### Network

- WiFi interface must support:
  - AP mode (check with `iw list`)
  - Channel switching
  - No concurrent station mode

---

## Debugging and Monitoring

### Log Files

All services write to timestamped log files in `backups/YYYYMMDD_HHMMSS/`:

| Log File | Service | Content |
|----------|---------|---------|
| `smarthack-wifi.log` | hostapd | AP events, client connections |
| `smarthack-web.log` | fake-registration-server.py | HTTP requests, responses |
| `smarthack-mqtt.log` | mosquitto | MQTT messages |
| `smarthack-psk.log` | psk-frontend.py | PSK identities, TLS handshakes |
| `smarthack-udp.log` | tuya-discovery.py | Device discoveries |

### Screen Sessions

Services run in detached screen sessions:

```bash
# List sessions
screen -ls

# Attach to session
screen -r smarthack-web    # Web server
screen -r smarthack-psk    # PSK frontend
screen -r smarthack-udp    # Discovery
screen -r smarthack-mqtt   # MQTT
screen -r smarthack-wifi   # AP
```

### Key Debug Points

**Device not connecting:**
1. Check `smarthack-wifi.log` for AP events
2. Check `smarthack-udp.log` for discovery broadcasts
3. Verify smartphone connected to vtrust-flash

**Device times out:**
1. Check `smarthack-psk.log` for PSK identity (starts with 02?)
2. Check `smarthack-web.log` for HTTP requests
3. Verify DNS wildcard working: `nslookup test.com 10.42.42.1`

**Intermediate firmware fails:**
1. Device MUST get IP 10.42.42.42
2. Check DHCP leases: `cat /var/lib/misc/dnsmasq.leases`
3. Ping device: `ping -c 1 10.42.42.42`

---

## Process Architecture and Inter-Service Communication

### Overview: Shell-Orchestrated Microservices

tuya-convert uses a **process-based microservices architecture** where multiple independent services run in separate `screen` sessions, orchestrated by bash scripts rather than a monolithic Python application.

```
start_flash.sh (Bash Orchestrator)
├── screen: hostapd (C binary - WiFi AP)
├── screen: dnsmasq (C binary - DHCP/DNS)
├── screen: fake-registration-server.py (Python - HTTP/HTTPS server)
├── screen: mosquitto (C binary - MQTT broker)
├── screen: psk-frontend.py (Python - TLS-PSK proxy)
├── screen: tuya-discovery.py (Python - UDP discovery)
└── background: smartconfig/main.py (Python - WiFi pairing)
```

### Inter-Process Communication Patterns

**Services communicate via:**
- **Network protocols** (HTTP, MQTT, UDP) - not Python imports
- **File system** (logs, configuration files)
- **Process signals** (SIGTERM, SIGINT, pkill)
- **Subprocess calls** (one Python script calling another)

### The Subprocess Pattern

**Two instances where Python scripts call other Python scripts:**

#### 1. Killing smartconfig Process

```python
# scripts/fake-registration-server.py:307
subprocess.run(["pkill", "-f", "smartconfig/main.py"], check=False)
```

**Context:**
- smartconfig/main.py is launched by start_flash.sh in background
- When device activates, fake-registration-server needs to stop smartconfig
- Uses subprocess + pkill because processes are in different execution contexts

#### 2. Triggering MQTT Upgrade Message

```python
# scripts/fake-registration-server.py:333-342
def trigger_upgrade():
    import time
    time.sleep(10)
    subprocess.run(["./mq_pub_15.py", "-i", gwId, "-p", protocol], check=False)

threading.Thread(target=trigger_upgrade, daemon=True).start()
```

**Context:**
- Device has activated and needs firmware upgrade trigger
- mq_pub_15.py publishes MQTT message to device
- Runs in background thread with 10 second delay
- Uses subprocess instead of function import

**Line References:**
- smartconfig kill: `scripts/fake-registration-server.py` line 307
- mq_pub_15.py call: `scripts/fake-registration-server.py` lines 333-342
- mq_pub_15.py script: `scripts/mq_pub_15.py` (command-line tool)

### Why This Architecture?

#### Historical Context

**Origins (2018):**
- Developed by security researchers (VTRUST)
- Created for **35C3 conference demonstration**
- Goal: Proof-of-concept exploit, not production software
- Timeline: Built quickly for specific use case

**Design Drivers:**
1. **Shell-first approach** - Linux tools (hostapd, dnsmasq, mosquitto) orchestrated by bash
2. **Debugging ease** - Each service in separate screen → view logs independently
3. **Process isolation** - Services can crash without affecting others
4. **Mixed languages** - C binaries + Python scripts + bash glue
5. **Simplicity** - Subprocess was quickest way to integrate services

#### Advantages

✅ **Easy debugging**
- Attach to any screen session to see live output
- Independent log files per service
- Kill/restart individual services without restarting all

✅ **Process isolation**
- One service crash doesn't bring down the system
- Can run different Python versions per script (if needed)
- Clear separation of concerns

✅ **Language flexibility**
- Mix C binaries (hostapd), Python scripts, bash orchestration
- Each tool uses best language for the job

✅ **Monitoring**
- Screen sessions make it easy to see what's happening
- Users can watch attack progress in real-time
- Good for education/demonstration

#### Disadvantages

❌ **Not Pythonic**
- Can't import mq_pub_15 functions into other modules
- Hard to unit test (requires subprocess mocking)
- Tight coupling to file system paths (`./ mq_pub_15.py`)
- No dependency injection or inversion of control

❌ **Fragile inter-process coupling**
- Assumes specific file paths and executable permissions
- Process signals (pkill) can fail silently
- No error handling for subprocess failures

❌ **Testing complexity**
- Integration tests require full process orchestration
- Can't easily mock subprocess calls
- Hard to test individual components in isolation

❌ **Maintenance burden**
- Changes to one script may require changes to orchestrator
- Command-line argument parsing duplicated across scripts
- No shared code structure or interfaces

### Alternative Architectures Considered

#### Option 1: Monolithic Python Application
```python
# Single Python process with asyncio
async def main():
    await asyncio.gather(
        run_fake_server(),
        run_psk_frontend(),
        run_discovery(),
        run_smartconfig()
    )
```

**Pros:** True Python modules, better testability, shared state
**Cons:** Harder to debug, single point of failure, loses screen sessions

#### Option 2: Python with Function Imports
```python
# Make mq_pub_15.py importable
from mq_pub_15 import publish_upgrade_message

def trigger_upgrade():
    time.sleep(10)
    publish_upgrade_message(gwId, options.secKey, protocol)
```

**Pros:** Pythonic, testable, no subprocess overhead
**Cons:** Requires refactoring all scripts, changes orchestration model

#### Option 3: Message Queue (Redis/RabbitMQ)
```
fake-server → [Redis Queue] → mq_pub_15 worker
```

**Pros:** Proper async, decoupled, scalable
**Cons:** Overkill for single-use tool, adds dependencies

### Current Status (2025)

**Decision:** Keep process-based architecture for now

**Rationale:**
1. **Works reliably** - Proven in production use since 2018
2. **Matches use case** - Single-user, single-device, one-time operation
3. **Education value** - Screen sessions aid learning and debugging
4. **Bash integration** - Deep coupling with shell orchestration
5. **Not production software** - Security research tool, not long-running service

### Future Architectural Investigation

⚠️ **Post-Refactoring Investigation Planned**

After current code quality improvements (Phase 1-2) are complete, investigate:

1. **Module-based refactoring**
   - Make Python scripts importable while preserving CLI functionality
   - Extract functions from scripts for reuse (e.g., mq_pub_15.py)
   - Add proper `if __name__ == "__main__":` guards

2. **Improved subprocess handling**
   - Better error handling and timeout management
   - Structured logging of subprocess calls
   - Validation of return codes and output

3. **Testing infrastructure**
   - Integration tests for inter-process communication
   - Mock subprocess calls in unit tests
   - Test script CLI interfaces independently

4. **Architectural decision points**
   - Keep screen-based orchestration vs migrate to Python-native?
   - Preserve bash orchestrator vs rewrite in Python?
   - Maintain process isolation vs shared Python runtime?
   - Balance between "works now" and "pythonic architecture"

5. **Risk assessment**
   - What breaks if we change architecture?
   - Can we maintain backward compatibility?
   - Is the effort justified for a research tool?

**Timeline:** After Phase 2 completion (type hints, constants, cleanup)

**Status:** Investigation only - no implementation commitment

**Goal:** Make informed architectural decisions with full understanding of trade-offs

---

## Related Pages

- [Quick Start Guide](Quick-Start-Guide.md) - Step-by-step flashing walkthrough
- [Installation Guide](Installation.md) - System setup and dependencies
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions
- [PSK Identity 02 Research](Collaboration-document-for-PSK-Identity-02.md) - Protocol details
- [System Requirements](Failed-attempts-and-tracked-requirements.md) - Compatibility info

---

## External References

- [hostapd Documentation](https://w1.fi/hostapd/)
- [dnsmasq Manual](http://www.thekelleys.org.uk/dnsmasq/doc.html)
- [Mosquitto MQTT Broker](https://mosquitto.org/)
- [Tuya IoT Platform](https://en.tuya.com/)

---

*This architecture document provides a comprehensive overview of how tuya-convert works internally. For security research and authorized testing only.*
