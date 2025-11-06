# Using Only a Stock Raspberry Pi Zero W and USB Cable

**Last Updated:** 2025-11-06
**Status:** ✅ Complete

## Overview

This guide explains how to set up a [Raspberry Pi Serial Gadget](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/serial-gadget#set-up-logging-in-on-pi-zero-via-serial-gadget-2-13) that allows you to connect your Raspberry Pi Zero W to any computer via USB cable. When configured, the Pi Zero will appear as a serial port, making it easy to use tuya-convert without requiring a keyboard, monitor, or network connection.

The Serial Gadget setup only needs to be done once. After setup, the tuya-convert software can be updated independently (requires WiFi for Internet access).

## Prerequisites

- Raspberry Pi Zero W
- MicroSD card (8GB or larger recommended)
- USB data cable (not just a power cable)
- Computer with microSD card reader
- Text editor
- Serial terminal emulator (e.g., [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/))
- WiFi network credentials for initial setup

**Important:** Ensure your USB cable is a data cable, not just a power cable. Many USB cables are power-only.

## Serial Interface Setup

### Step 1: Prepare the SD Card

1. Download and flash the latest Raspbian Lite on a microSD card
2. After burning, the SD card may be auto-ejected - remove and reinsert it to mount again
3. Open the `boot` partition

### Step 2: Enable USB Serial Gadget

Edit the boot configuration files:

**Edit `config.txt`:**
```bash
# Open config.txt in a text editor
# Go to the bottom and add this line:
dtoverlay=dwc2
```

**Edit `cmdline.txt`:**
```bash
# Open cmdline.txt in a text editor
# After "rootwait", add a space and then:
modules-load=dwc2,g_serial
```

**Important:** Save both files as plain text (not rich text format).

### Step 3: Configure WiFi

Create a new text file on the SD card named `wpa_supplicant.conf`:

```bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    id_str="HOTSPOT NAME"
    ssid="SSID"
    psk="PASSWORD"
    key_mgmt=WPA-PSK
}
```

**Note:** If your WiFi SSID is hidden, add `scan_ssid=1` to the `network` section.

**Code Reference:** WiFi configuration managed by `wpa_supplicant` service

### Step 4: Enable SSH

Create a new empty file on the SD card named `ssh` (no extension).

The Raspberry Pi looks for this file on first boot. If found, it enables SSH and deletes the file.

**Windows:**
```cmd
C:\> <d>:
<d>:\> copy nul ssh
```

**Linux/MacOS:**
```bash
$ cd /Volumes/boot
$ touch ssh
```

### Step 5: Initial Boot and SSH Connection

1. Safely eject the SD card from your computer
2. Insert the SD card into the Raspberry Pi Zero W
3. Power up the Pi using the microUSB connector labeled `PWR`
4. Wait for it to boot and connect to your WiFi network
5. Find its IP address in your router's device list
6. Connect via SSH:
   ```bash
   ssh pi@<IP_ADDRESS>
   ```
7. Default credentials: username `pi`, password `raspberry`

### Step 6: Secure the WiFi Password

Encode the WiFi password (removes plain text from config):

```bash
wpa_passphrase "SSID" "PASSWORD" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null
```

Then edit the configuration to remove the plain text password:

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
# Remove the line with psk="PASSWORD" (plain text)
# Keep the line with psk=<encrypted hash>
```

### Step 7: Configure Serial Gadget for Login

Enable the serial gadget driver and tty service:

```bash
# Verify g_serial driver is bound
sudo dmesg | grep g_serial

# Enable the tty service
sudo systemctl enable getty@ttyGS0.service

# Reboot to apply
sudo reboot
```

After reboot, verify the service is active:

```bash
sudo systemctl is-active getty@ttyGS0.service
# Should output: active
```

**Code Reference:** Serial gadget uses kernel module `g_serial`

### Step 8: Shutdown

Once setup is complete, shut down the Pi:

```bash
sudo shutdown now
```

## Connect to the Raspberry Pi using the Serial Gadget

### Step 1: Physical Connection

Connect the USB cable from your computer to the Raspberry Pi microUSB connector labeled **`USB`**, not the `PWR` connector.

On your computer, a new serial port will be created:

**Windows:**
```
COMN (where N can be any number)
```

**Linux/MacOS:**
```
/dev/tty.usbmodemNNNN
```

**Note:** The `NNNN` number after `usbmodem` will vary. Check your `/dev` folder for the actual device name.

### Step 2: Connect via Serial Terminal

Use a serial terminal emulator application (e.g., [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/)):

1. Select the appropriate port (COM port on Windows, `/dev/tty.usbmodem*` on Mac/Linux)
2. Configure for **115200 baud, 8N1** (8-bit No-parity 1-stop)
3. Connect to the Raspberry Pi

**Note:** You may need to hit return a few times to get the login prompt.

**MacOS shortcut:**
```bash
screen -L /dev/cu.usbmodemXXXX 115200
```

The `-L` option enables output logging for the session.

## Tuya-Convert Installation

⚠️ **Installing software packages requires Internet connection (WiFi)** ⚠️

### Step 1: Update System Packages

```bash
sudo apt-get update && sudo apt-get -y upgrade
```

### Step 2: Install Git

```bash
sudo apt-get install git
```

### Step 3: Install tuya-convert

```bash
git clone https://github.com/ct-Open-Source/tuya-convert
cd tuya-convert
./install_prereq.sh
```

**Code Reference:** See `install_prereq.sh` for dependency installation

### Step 4: Disable WiFi Auto-Connect

After installation, the WiFi interface (`wlan0`) needs to be freed up for tuya-convert to use. Since you'll connect via USB Serial Gadget, disable automatic WiFi connection:

```bash
sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf-saved
```

**Note:** This renames the config file so WiFi won't auto-connect, but preserves it for later use.

## Using Tuya-Convert

### Running the Flash Script

Connect to the Pi via Serial Gadget and run:

```bash
cd tuya-convert
./start_flash.sh
```

Follow the on-screen instructions to flash your Tuya devices.

**Code Reference:** See `start_flash.sh` for the main flashing workflow

### Proper Shutdown

After flashing devices, always shut down the Pi properly:

```bash
sudo shutdown now
```

## Updating the Tuya-Convert Scripts

To update tuya-convert, you need Internet access:

### Step 1: Re-enable WiFi

```bash
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf-saved /etc/wpa_supplicant/wpa_supplicant.conf
```

### Step 2: Reboot

```bash
sudo reboot
```

### Step 3: Update tuya-convert

After the Pi reconnects to WiFi, pull the latest changes:

```bash
cd tuya-convert
git pull
./install_prereq.sh
```

### Step 4: Disable WiFi Again

```bash
sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf-saved
sudo reboot
```

## Optional Housekeeping

### Disable SSH (Security Enhancement)

Since you're using Serial Gadget, you may want to disable SSH:

**For Raspbian Buster:**
```bash
sudo service ssh stop
sudo systemctl disable sshd.service
```

**For Raspbian Stretch:**
```bash
sudo service ssh stop
sudo systemctl disable ssh.service
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No serial port appears | Using power-only USB cable | Use a data-capable USB cable |
| Serial port appears but no login prompt | ttyGS0 service not running | Run `sudo systemctl enable getty@ttyGS0.service` and reboot |
| Cannot connect to WiFi during setup | Incorrect credentials in wpa_supplicant.conf | Verify SSID and password, check for typos |
| g_serial driver not loading | Incorrect config.txt or cmdline.txt | Verify `dtoverlay=dwc2` in config.txt and `modules-load=dwc2,g_serial` in cmdline.txt |
| vtrust-flash AP not broadcasting | WiFi still auto-connecting | Ensure wpa_supplicant.conf is renamed/disabled |
| Login prompt not appearing | Need to press Enter | Hit Return/Enter key several times to trigger prompt |

## Related Pages

- [Using a Raspberry Pi](Using-a-Raspberry-Pi) - General Raspberry Pi setup for tuya-convert
- [Installation Guide](Installation) - Complete installation instructions
- [Quick Start Guide](Quick-Start-Guide) - Quick reference for flashing
- [Troubleshooting](Troubleshooting) - Common issues and solutions

## References

- [Adafruit Serial Gadget Guide](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/serial-gadget)
- [Raspberry Pi Zero USB Configuration](https://www.raspberrypi.org/documentation/hardware/computemodule/cm-designguide.md)
- [WPA Supplicant Documentation](https://w1.fi/wpa_supplicant/)
- Internal code: `install_prereq.sh` - Dependency installation
- Internal code: `start_flash.sh` - Flashing workflow
- Internal code: `scripts/setup_ap.sh` - Access point configuration

## Credits

Thank you to `@SourPickel` (Discord) for bringing this method to the community's attention.

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
