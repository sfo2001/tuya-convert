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

## Installation Methods

tuya-convert offers three installation methods:

1. **[Native Installation](#option-1-native-installation-recommended)** (Recommended) - Use your distribution's package manager
2. **[Docker Installation](Using-Docker.md)** - Fully containerized environment
3. **[Nix Flake](#option-3-nix-flake-reproducible-environment)** - Reproducible, isolated development environment

### Comparison

| Feature | Native Install | Docker | Nix Flake |
|---------|----------------|--------|-----------|
| Setup Speed | ⚡ Fast | 🐢 Slow (image build) | ⚡ Fast (after first time) |
| System Impact | ⚠️ Modifies system | ✅ None | ✅ None |
| Reproducibility | ⚠️ Version drift | ✅ Good | ✅ Perfect |
| Disk Usage | 📊 ~100MB | 📊 ~1GB+ | 📊 ~500MB |
| Best For | Single device flashing | CI/CD, isolation | Development, NixOS users |

---

## Option 1: Native Installation (Recommended)

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
3. **Create a Python virtual environment** (`venv/`)
4. Install Python dependencies into the virtual environment
5. Set up the environment

> **Note on Virtual Environments:** Modern Linux distributions (Ubuntu 24.04+, Debian 12+) enforce PEP 668, which prevents system-wide pip installations. The installation script creates a virtual environment to comply with this requirement. The virtual environment is automatically activated when you run `start_flash.sh`, and special handling ensures Python scripts launched in sudo screen sessions can access the virtual environment dependencies (see issue #1167).

**What gets installed:**

#### For Debian/Ubuntu/Raspberry Pi OS:
- **System packages:** git, iw, dnsmasq, rfkill, hostapd, screen, curl, build-essential, net-tools, libssl-dev, iproute2, iputils-ping, mosquitto, haveged
- **Python packages:** python3-pip, python3-setuptools, python3-wheel, python3-dev, python3-venv
- **Python modules (in venv):** paho-mqtt, tornado, sslpsk3, pycryptodomex

> **Note:** `sslpsk3` is NOT available as a system package on Ubuntu/Debian, which is why the virtual environment is mandatory for non-Docker installations.

#### For Arch Linux:
- **System packages:** git, iw, dnsmasq, hostapd, screen, curl, python-pip, python-wheel, net-tools, openssl, mosquitto, haveged
- **Python modules (in venv):** paho-mqtt, tornado, sslpsk3, pycryptodomex

### Step 3: Wait for Installation to Complete

The installation process may take several minutes depending on your internet connection and system speed. You will see:

```
Ready to start upgrade

Python packages have been installed in a virtual environment (venv/)
The virtual environment will be automatically activated when you run ./start_flash.sh
```

When the installation is complete.

### Step 4: Verify Installation

After installation completes, verify that key components are installed:

```bash
# Check that virtual environment was created
ls -la venv/

# Activate virtual environment
source venv/bin/activate

# Check Python dependencies (inside venv)
python3 -c "import paho.mqtt; import tornado; import sslpsk3; import Cryptodome; print('✓ Python dependencies OK')"

# Deactivate virtual environment
deactivate

# Check system tools
which hostapd dnsmasq mosquitto
```

If these commands run without errors, your installation is successful.

> **Note:** You don't need to manually activate the virtual environment when running tuya-convert - `start_flash.sh` does this automatically.

---

## Option 3: Nix Flake (Reproducible Environment)

Nix provides a reproducible, isolated development environment without modifying your system packages. This is ideal for developers, NixOS users, and anyone who values reproducibility.

### Benefits

✅ **Reproducible**: Exact same dependencies on every machine
✅ **Isolated**: No system package modifications
✅ **Cross-distribution**: Works on any Linux (and macOS)
✅ **One Command**: `nix develop` installs everything
✅ **Version Locked**: No "works on my machine" issues

### Quick Start

```bash
# 1. Install Nix (if not already installed)
sh <(curl -L https://nixos.org/nix/install) --daemon

# 2. Enable flakes
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf

# 3. Clone repository
git clone https://github.com/sfo2001/tuya-convert
cd tuya-convert

# 4. Enter development environment (installs all dependencies)
nix develop

# 5. Flash your device
./start_flash.sh
```

### First Time Setup

The first `nix develop` will download and install dependencies (~500MB). This takes 5-10 minutes. Subsequent runs are instant because packages are cached.

**You'll see:**
```
╔════════════════════════════════════════════════════════════════╗
║                    🔧 tuya-convert (Nix)                       ║
╚════════════════════════════════════════════════════════════════╝

✅ Development environment loaded successfully
📦 Installed dependencies:
   • Python 3.11.x with packages: paho-mqtt, tornado, pycryptodomex, sslpsk3
   • System tools: git, iw, dnsmasq, hostapd, mosquitto, screen
   ...
```

### Verify Installation

```bash
# Check Python and packages
python3 --version
python3 -c "import sslpsk3; print(f'sslpsk3 {sslpsk3.__version__}')"

# Check system tools
which dnsmasq hostapd mosquitto
```

### Exit Environment

```bash
exit  # Or press Ctrl+D
```

Your system remains unaffected - all packages are stored in `/nix/store/` and only available within the Nix shell.

### Full Documentation

See **[Using Nix](Using-Nix.md)** for:
- Detailed setup instructions
- Troubleshooting
- Advanced usage (direnv, offline mode, version pinning)
- How Nix works under the hood

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

### Python Module Import Errors (ModuleNotFoundError)

**Symptom:**
```
ModuleNotFoundError: No module named 'sslpsk3'
ModuleNotFoundError: No module named 'tornado'
```

**Cause:** Virtual environment not activated or Python scripts can't find venv packages

**Solution:**
1. **If running manually:** Activate venv first with `source venv/bin/activate`
2. **If running start_flash.sh:** This should not happen - the fix for issue #1167 ensures venv is activated in sudo screen sessions
3. **If problem persists:** Re-run `./install_prereq.sh` to recreate virtual environment
4. **Verify venv:** Run `source venv/bin/activate && python3 -c "import sslpsk3; print('OK')"`

> **Technical Note:** As of issue #1167 fix, `start_flash.sh` explicitly activates the virtual environment within each sudo screen session to ensure Python scripts can access dependencies. This is critical for `sslpsk3` which has no system package equivalent.

### Python SSL/TLS Errors After Installation

**Symptom:**
```
could not establish sslpsk socket: ('No cipher can be selected.',)
```

**Cause:** OpenSSL version is too old (< 1.1.1)

**Solution:**
- Upgrade to Ubuntu 18.04+ or Debian 10+
- See [System Requirements](Failed-attempts-and-tracked-requirements.md) for detailed information

### "This environment is externally managed" Error (PEP 668)

**Symptom:**
```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install python3-xyz
```

**Cause:** Modern Linux distributions (Ubuntu 24.04+, Debian 12+) prevent system-wide pip installations

**Solution:**
✅ **No action needed** - `install_prereq.sh` automatically creates a virtual environment to comply with PEP 668. The virtual environment is activated automatically when you run `start_flash.sh`.

**If you see this error:** You're likely trying to manually install packages. Let the installation script handle it instead.

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
- [Using Nix](Using-Nix.md) - Nix flake installation and usage
- [Using Raspberry Pi](Using-a-Raspberry-Pi.md) - Raspberry Pi specific setup
- [System Requirements](Failed-attempts-and-tracked-requirements.md) - Detailed compatibility info
- [Troubleshooting](Troubleshooting.md) - Common issues

## Code References

- **Installation Script:** `install_prereq.sh` - Main installation script
  - `debianInstall()` function (line 4-8) - Debian/Ubuntu installation
  - `archInstall()` function (line 10-13) - Arch Linux installation

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
