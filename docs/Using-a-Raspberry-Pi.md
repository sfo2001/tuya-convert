# Using a Raspberry Pi

**Last Updated:** 2025-11-06
**Status:** ✅ Complete

## Overview

This guide covers the essential steps for using a Raspberry Pi to run tuya-convert. Before running the flashing process, you need to disconnect the Pi from its Wi-Fi network to enable the required `vtrust-flash` WiFi access point to broadcast correctly.

## Prerequisites

- Raspberry Pi (any model with WiFi)
- Raspbian OS installed and configured
- tuya-convert installed (see [Installation Guide](Installation))
- Access to the Pi via Ethernet, USB Gadget mode, or VNC
- Root/sudo access

**Important:** You will need to be connected via Ethernet or "USB Gadget mode" to continue using the Pi after disabling WiFi.

## Disconnecting from Wi-Fi

Before running tuya-convert, you must disconnect the Pi from its Wi-Fi network. There are three ways to do this:

### Option 1: Via GUI

1. Connect via VNC viewer
2. Click the WiFi Icon
3. Select your network
4. Click "Disconnect"

### Option 2: Via Command (Temporary)

This method temporarily kills the WiFi connection:

```bash
sudo killall wpa_supplicant
```

**Note:** WiFi will reconnect on reboot.

### Option 3: Via Configuration File (Permanent)

This method permanently removes the WiFi configuration:

```bash
# Edit the wpa_supplicant configuration
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# Delete the wifi network block including network={}
# Close the file (ctrl+x, y, enter)

# Reboot to apply changes
sudo reboot
```

**Code Reference:** Configuration managed by `wpa_supplicant` service

## Running tuya-convert

After disconnecting from WiFi, you can follow the standard flashing instructions:

1. Navigate to the tuya-convert directory:
   ```bash
   cd ~/tuya-convert
   ```

2. Run the flashing script:
   ```bash
   ./start_flash.sh
   ```

3. Follow the on-screen instructions

**Code Reference:** See `scripts/setup_ap.sh` for access point configuration

## Pi Zero W Specific Instructions

For Raspberry Pi Zero W users, there are additional setup options:

### Using USB Serial Gadget Mode

If you don't have a keyboard/monitor, set up [USB Serial Gadget mode](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable) for easier access.

### Using Only WiFi

If you need to connect using only WiFi:

1. Connect to the Raspberry Pi Zero W using WiFi and SSH
2. Follow the normal Raspberry Pi instructions but stop before running `start_flash.sh`
3. Run the `screen` command to prevent session termination:
   ```bash
   screen
   ```
4. Run the flashing script:
   ```bash
   ./start_flash.sh
   ```
5. Your SSH session will be disconnected when the Pi creates the `vtrust-flash` AP
6. Connect to the `vtrust-flash` AP and SSH to `10.42.42.1`
7. Run `screen -r` to identify the screen session ID
8. Resume the screen session:
   ```bash
   screen -r -d [screen id]
   ```
9. Continue with normal flashing instructions

**Code Reference:** See `scripts/setup_ap.sh:45` for AP network configuration

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cannot connect after disconnecting WiFi | No alternative connection method | Connect via Ethernet cable or USB Gadget mode before disconnecting WiFi |
| vtrust-flash network not visible | WiFi still connected to home network | Verify WiFi disconnection using `iwconfig` command |
| Lost connection during flashing | Used temporary disconnect method | Use `screen` command before running `start_flash.sh` |
| Cannot SSH to 10.42.42.1 | Not connected to vtrust-flash AP | Verify connection to the `vtrust-flash` network on your device |

## Related Pages

- [Installation Guide](Installation) - Initial setup of tuya-convert
- [Using Raspberry Pi Zero W with USB Cable](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable) - Detailed USB Serial Gadget setup
- [Quick Start Guide](Quick-Start-Guide) - Quick reference for the flashing process
- [Troubleshooting](Troubleshooting) - Common issues and solutions

## References

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [WPA Supplicant Configuration](https://www.freecodecamp.org/news/how-to-setup-wpa-supplicant/)
- Internal code: `scripts/setup_ap.sh` - Access point setup
- Internal code: `scripts/start_flash.sh` - Main flashing script

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
