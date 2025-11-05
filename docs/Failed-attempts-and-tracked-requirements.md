# System Requirements and Troubleshooting

**Last Updated:** 2025-11-05
**Status:** ✅ Complete

## Overview

This page documents system requirements, known compatibility issues, and failed attempts to run tuya-convert on older or unsupported systems. It serves as a reference for troubleshooting SSL/TLS issues and platform compatibility problems.

---

## Current System Requirements

### Minimum Requirements (2024+)

**Recommended Operating Systems:**
- Ubuntu 20.04 LTS or newer
- Debian 10 (Buster) or newer
- Raspberry Pi OS (based on Debian 10+)
- Other modern Linux distributions with equivalent package versions

**Critical Package Requirements:**
- **OpenSSL:** Version 1.1.1 or newer (for TLS-PSK cipher support)
- **Python:** Version 3.6 or newer
- **SSL/TLS Support:** TLS-PSK ciphers must be available

**Why OpenSSL 1.1.1+ is Required:**
- Proper support for TLS-PSK (Pre-Shared Key) cipher suites
- Required cipher: `TLS_PSK_WITH_AES_128_CBC_SHA256`
- Older versions (1.0.2) may have PSK support disabled or incomplete
- Python's `ssl` module depends on system OpenSSL version

### Package Dependencies

See `install_prereq.sh` for the complete list of required packages:
- `git`, `iw`, `dnsmasq`, `rfkill`, `hostapd`
- `screen`, `curl`, `build-essential`
- `python3-pip`, `python3-setuptools`, `python3-wheel`, `python3-dev`
- `mosquitto`, `haveged`, `net-tools`
- `libssl-dev` (OpenSSL development headers)

**Python Dependencies (via pip):**
- `paho-mqtt` (MQTT client)
- `tornado` (web server)
- `pycryptodomex` (cryptography)
- `sslpsk` (TLS-PSK support - depends on OpenSSL 1.1.1+)

---

## Common Issues and Solutions

### Issue: "No cipher can be selected" Error

**Symptom:**
```
could not establish sslpsk socket: ('No cipher can be selected.',)
```

**Cause:**
- OpenSSL version is too old (< 1.1.1)
- TLS-PSK cipher support not available or disabled
- Python ssl module compiled against old OpenSSL

**Solution:**
Upgrade to a modern distribution with OpenSSL 1.1.1+:
- **Best:** Fresh install of Ubuntu 20.04+ or Debian 10+
- **Alternative:** Upgrade OpenSSL (see workarounds below)

### Issue: Missing smarthack-*.log Files

**Symptom:**
- No log files created in `smarthack-*.log`
- Device connection times out
- Cannot diagnose what's happening

**Cause:**
Logging bug in older versions (fixed in PR #943)

**Solution:**
- Update to latest version of tuya-convert
- Check `screen0.log` for error messages
- See [original PR #943](https://github.com/ct-Open-Source/tuya-convert/pull/943)

### Issue: SmartConfig Timeout

**Symptom:**
```
SmartConfig complete.
Resending SmartConfig Packets
..................
Timed out while waiting for the device to (re)connect
```

**Cause:**
- Device not entering pairing mode properly
- Network configuration issues
- SSL/TLS handshake failing (check logs)
- Device uses PSK Identity 02 (newer devices - see below)

**Solution:**
1. Verify device is in pairing mode (blinking rapidly)
2. Check `smarthack-psk.log` for SSL errors
3. If PSK Identity 02 error, device uses new security (may not be flashable)
4. Try different device reset procedures

---

## Historical: End-of-Life Ubuntu Versions

> **Note:** The following sections document historical compatibility issues with EOL Ubuntu versions. **These systems are no longer supported and should not be used.**

### Ubuntu 12.04 LTS (EOL: April 2017)

**Architecture:** i386

**Problems:**
- Missing critical packages: `python3-pip`, `python3-wheel`
- Python 3 ecosystem too old
- Many security vulnerabilities

**Solution:** Use modern distribution (Ubuntu 20.04+)

---

### Ubuntu 14.04 LTS (EOL: April 2019)

**Architecture:** i386

**Problems:**
- Missing `python3-wheel` package
- Python 3 version too old
- OpenSSL too old for TLS-PSK

**Solution:** Use modern distribution (Ubuntu 20.04+)

---

### Ubuntu 16.04 LTS (EOL: April 2021)

**Architecture:** i386

#### System Specification (Historical)
```
Ubuntu 16.04 LTS (i386)
OpenSSL: 1.0.2g-1ubuntu4.14
libssl-dev: 1.0.2g-1ubuntu4.19
Python: 3.5.1-3
```

#### Problem
- **OpenSSL 1.0.2:** Insufficient TLS-PSK cipher support
- **Error:** `could not establish sslpsk socket: ('No cipher can be selected.',)`
- **Root Cause:** OpenSSL 1.0.2 series has incomplete PSK implementation
- No `smarthack-*.log` files created (logging bug)

#### Attempted Workarounds (Not Recommended)

**Workaround 1: Add Ubuntu 18.04 Repositories**

Add bionic security repositories to `/etc/apt/sources.list`:
```bash
deb http://security.ubuntu.com/ubuntu bionic-security main restricted
deb http://security.ubuntu.com/ubuntu bionic-security universe
deb http://security.ubuntu.com/ubuntu bionic-security multiverse
```

Then upgrade OpenSSL:
```bash
sudo apt update
sudo apt install openssl libssl-dev
```

This upgrades to:
- `openssl=1.1.1-1ubuntu2.1~18.04.9`
- `libssl-dev=1.1.1-1ubuntu2.1~18.04.9`

**However:** This is insufficient. Additional packages that need updating:
- `libssl1.1` - OpenSSL 1.1.1 runtime library (required)
- `python3` - Must be rebuilt against new OpenSSL
- `python3-dev` - Development headers
- Possibly other Python packages depending on ssl module

**Why This Approach Fails:**
- Mixing Ubuntu 16.04 packages with 18.04 packages creates dependency conflicts
- Python 3.5 in Ubuntu 16.04 is compiled against OpenSSL 1.0.2
- Upgrading OpenSSL alone doesn't help if Python still uses old version
- Risk of breaking system stability

**Recommended Solution:**
Upgrade to Ubuntu 18.04 LTS (or newer). Fresh installation is safer than mixing repositories.

#### References
- [Issue #942](https://github.com/ct-Open-Source/tuya-convert/issues/942) - Ubuntu 16.04 SSL cipher problem
- [PR #943](https://github.com/ct-Open-Source/tuya-convert/pull/943) - Fix for missing log files

---

## Modern Distribution Support (2020+)

### Ubuntu 18.04 LTS (Bionic) ✅

**Status:** Fully Supported (EOL: April 2028 with ESM)

**Why It Works:**
- OpenSSL 1.1.1 with full TLS-PSK support
- Python 3.6+ with proper ssl module
- All required packages available

### Ubuntu 20.04 LTS (Focal) ✅

**Status:** Recommended

**Why It's Better:**
- OpenSSL 1.1.1f or newer
- Python 3.8+
- Long-term support until 2030 (with ESM)
- Best tested platform

### Ubuntu 22.04 LTS (Jammy) ✅

**Status:** Fully Supported

**Features:**
- OpenSSL 3.0 (fully compatible)
- Python 3.10+
- Latest security updates

### Raspberry Pi OS ✅

**Status:** Fully Supported (Debian-based)

**Requirements:**
- Based on Debian 10 (Buster) or newer
- Raspberry Pi 3 or newer recommended
- Pi Zero W works but is slower

See dedicated setup guides:
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md)
- [Using Pi Zero W](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md)

---

## Troubleshooting Checklist

If tuya-convert fails, check:

1. **Operating System Version**
   - [ ] Using Ubuntu 18.04+ or Debian 10+
   - [ ] Not using EOL distribution

2. **OpenSSL Version**
   - [ ] Check: `openssl version`
   - [ ] Should be: 1.1.1 or newer
   - [ ] If older: Upgrade OS

3. **Python Version**
   - [ ] Check: `python3 --version`
   - [ ] Should be: 3.6 or newer

4. **Required Packages**
   - [ ] Run: `./install_prereq.sh`
   - [ ] No errors during installation

5. **Log Files**
   - [ ] Check `smarthack-psk.log` for SSL errors
   - [ ] Check `screen0.log` for startup errors
   - [ ] Check other `smarthack-*.log` files for issues

6. **Device Compatibility**
   - [ ] Check [Compatible Devices](Compatible-devices.md)
   - [ ] Verify device uses old firmware (pre-Sept 2019)
   - [ ] PSK Identity 02 devices may not be flashable

---

## Related Pages

- [Troubleshooting Guide](Troubleshooting.md) - Common issues and solutions
- [Installation Guide](Installation.md) - Complete installation instructions
- [Compatible Devices](Compatible-devices.md) - Device compatibility list
- [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) - New security protocol
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md) - Raspberry Pi setup
- [Quick Start Guide](Quick-Start-Guide.md) - First time setup

---

## References

### External Issues
- [ct-Open-Source/tuya-convert#942](https://github.com/ct-Open-Source/tuya-convert/issues/942) - Ubuntu 16.04 SSL cipher issue
- [ct-Open-Source/tuya-convert#943](https://github.com/ct-Open-Source/tuya-convert/pull/943) - Fix for missing log files

### Code References
- **Installation Script:** `install_prereq.sh` - Package requirements
- **SSL/PSK Implementation:** `scripts/psk-frontend.py` - TLS-PSK server

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
