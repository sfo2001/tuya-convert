# Installation Guide

**Last Updated:** 2025-11-05
**Status:** ✅ Complete

## Overview

This guide covers the complete installation process for tuya-convert. The installation script (`install_prereq.sh`) automatically installs all required dependencies on supported Linux distributions. This guide is for users who want to set up tuya-convert on their system for the first time.

## Prerequisites

### Hardware Requirements

- **Linux computer with WiFi adapter** capable of acting as an Access Point
- **Secondary WiFi device** (smartphone, tablet, or another computer) for monitoring
- **Sufficient disk space** (~500MB for dependencies and tools)

### Software Requirements

- **Supported Operating Systems:**
  - Debian-based: Ubuntu 18.04+, Debian 10+, Raspberry Pi OS
  - Arch Linux and Arch-based distributions
  - Other Linux distributions (may work with manual adjustments)

- **Git** (for cloning the repository)
- **Root/sudo access** (for installing system packages)

### Tested Platforms

tuya-convert has been successfully tested on:
- Kali Linux 2018.4 (VMware)
- Raspberry Pi Zero W with Raspbian
- Raspberry Pi 3B/3B+/4B with Raspbian Stretch and Raspberry Pi OS Buster
- Ubuntu 18.04+ (64-bit) in VirtualBox with USB WiFi adapter
- Ubuntu MATE 18.04+ (32-bit) in VirtualBox with WiFi adapter

**Note:** For Raspberry Pi users, we recommend a clean installation. If you use your Pi for other purposes, use a dedicated SD card for tuya-convert.

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/sfo2001/tuya-convert
cd tuya-convert
```

**Note:** Replace `sfo2001/tuya-convert` with `ct-Open-Source/tuya-convert` if you want the original repository.

### Step 2: Run the Installation Script

The installation script automatically detects your distribution and installs the appropriate packages.

```bash
./install_prereq.sh
```

The script will:
1. Detect your Linux distribution from `/etc/os-release`
2. Install required system packages
3. Install Python dependencies
4. Set up the environment

**What gets installed:**

#### For Debian/Ubuntu/Raspberry Pi OS:
- **System packages:** git, iw, dnsmasq, rfkill, hostapd, screen, curl, build-essential, net-tools, libssl-dev, iproute2, iputils-ping, mosquitto, haveged
- **Python packages:** python3-pip, python3-setuptools, python3-wheel, python3-dev
- **Python modules:** paho-mqtt, tornado, sslpsk3, pycryptodomex

#### For Arch Linux:
- **System packages:** git, iw, dnsmasq, hostapd, screen, curl, python-pip, python-wheel, net-tools, openssl, mosquitto, haveged
- **Python modules:** python-pycryptodomex, python-paho-mqtt, python-tornado, sslpsk3

### Step 3: Wait for Installation to Complete

The installation process may take several minutes depending on your internet connection and system speed. You will see:

```
Ready to start upgrade
```

When the installation is complete.

### Step 4: Verify Installation

After installation completes, verify that key components are installed:

```bash
# Check Python dependencies
python3 -c "import paho.mqtt; import tornado; import Cryptodome; print('Python dependencies OK')"

# Check system tools
which hostapd dnsmasq mosquitto
```

If these commands run without errors, your installation is successful.

---

## Platform-Specific Notes

### Debian/Ubuntu

On Debian-based systems, the script uses `apt-get` to install packages:

```bash
sudo apt-get update
sudo apt-get install -y [packages...]
sudo python3 -m pip install --user --upgrade [python-packages...]
```

**Known Issues:**
- Ubuntu 16.04 and earlier have outdated OpenSSL (< 1.1.1) - see [System Requirements](Failed-attempts-and-tracked-requirements.md)
- Use Ubuntu 18.04+ for best compatibility

### Arch Linux

On Arch-based systems, the script uses `pacman`:

```bash
sudo pacman -S --needed [packages...]
sudo python -m pip install --user --upgrade [python-packages...]
```

### Raspberry Pi

**Recommendations:**
- Use Raspberry Pi OS (formerly Raspbian) Buster or newer
- Use a clean SD card installation if possible
- Raspberry Pi 3B/3B+/4B recommended (Pi Zero W works but is slower)
- Built-in WiFi works well on Pi 3/4

**Setup Tips:**
1. Flash fresh Raspberry Pi OS to SD card
2. Enable SSH before first boot (create empty `ssh` file in boot partition)
3. Connect via Ethernet for initial setup
4. Run installation after first boot

See dedicated guides:
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md)
- [Using Pi Zero W](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md)

### VirtualBox / Virtual Machines

**Important:** When running in a VM:
1. **USB WiFi adapter required** - VM must pass through a USB WiFi adapter
2. **USB passthrough** - Configure VM to pass USB device to guest OS
3. **Test adapter** - Ensure WiFi adapter works in VM before proceeding

**Tested Adapters:**
- RTL8188CU chipset (cheap USB adapters)
- Ralink RT5370 chipset
- Most USB WiFi adapters with Linux support

---

## Troubleshooting

### Installation Fails: "Distribution not supported"

**Symptom:**
```
/etc/os-release found but distribution X is not explicitly supported
```

**Solution:**
The script will attempt to use Debian-based installation commands. This may work on Ubuntu derivatives, Linux Mint, or other Debian-based systems. If it fails, you may need to manually install packages.

### Installation Fails: Package not found

**Symptom:**
```
E: Unable to locate package [package-name]
```

**Solution:**
1. Update package lists: `sudo apt-get update`
2. Check your repository configuration
3. Ensure your distribution is supported
4. For old distributions (Ubuntu < 18.04), upgrade to a modern version

### Python SSL/TLS Errors After Installation

**Symptom:**
```
could not establish sslpsk socket: ('No cipher can be selected.',)
```

**Cause:** OpenSSL version is too old (< 1.1.1)

**Solution:**
- Upgrade to Ubuntu 18.04+ or Debian 10+
- See [System Requirements](Failed-attempts-and-tracked-requirements.md) for detailed information

### Permission Denied Errors

**Symptom:**
```
Permission denied when running install_prereq.sh
```

**Solution:**
```bash
chmod +x install_prereq.sh
./install_prereq.sh
```

### WiFi Adapter Not Detected

**Symptom:** WiFi adapter doesn't work after installation

**Solution:**
1. Check adapter is recognized: `lsusb` or `ip link show`
2. Check driver is loaded: `lsmod | grep -i wifi`
3. Test AP mode capability: `iw list | grep -A 10 "Supported interface modes"`
4. Some adapters require additional firmware packages

---

## Post-Installation

### Next Steps

After successful installation:

1. **[Quick Start Guide](Quick-Start-Guide.md)** - Flash your first device
2. **[Compatible Devices](Compatible-devices.md)** - Check if your device is supported
3. **[Troubleshooting](Troubleshooting.md)** - Common issues and solutions

### Keeping Updated

To update tuya-convert:

```bash
cd tuya-convert
git pull origin main
./install_prereq.sh  # Re-run to update dependencies if needed
```

---

## Related Pages

- [Quick Start Guide](Quick-Start-Guide.md) - First device flash walkthrough
- [Using Docker](Using-Docker.md) - Alternative Docker-based installation
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md) - Raspberry Pi specific setup
- [System Requirements](Failed-attempts-and-tracked-requirements.md) - Detailed compatibility info
- [Troubleshooting](Troubleshooting.md) - Common issues

## Code References

- **Installation Script:** `install_prereq.sh` - Main installation script
  - `debianInstall()` function (line 4-8) - Debian/Ubuntu installation
  - `archInstall()` function (line 10-13) - Arch Linux installation

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
