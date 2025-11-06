# Using Docker for tuya-convert

**Last Updated:** 2025-11-05
**Status:** ✅ Complete

## Overview

This guide covers how to use tuya-convert with Docker instead of installing dependencies directly on your host system. The Docker approach provides a clean, isolated environment for flashing Tuya devices without modifying your host system.

**Advantages of Docker:**
- No host system modifications (except Docker installation)
- All dependencies contained in the Docker image
- Clean separation between host and flashing environment
- Easy cleanup - just remove the container
- Reproducible environment across different Linux distributions

**Time Required:** 20-40 minutes (including Docker image build)
**Difficulty:** Intermediate (requires Docker knowledge)

---

## Prerequisites

### Hardware Requirements

- [ ] **Linux computer** with WiFi adapter capable of AP mode
- [ ] **Secondary WiFi device** (smartphone or tablet) for pairing
- [ ] **USB WiFi adapter** recommended (for better compatibility)

### Software Requirements

- [ ] **Docker** installed and running
- [ ] **docker-compose** installed (v1.27.0+ recommended)
- [ ] **Git** for cloning the repository
- [ ] **Root/sudo access** (Docker requires privileged mode for network operations)

### Knowledge Prerequisites

- [ ] Basic Docker concepts (images, containers, volumes)
- [ ] Basic Linux command line usage
- [ ] Understanding of docker-compose

---

## Installation and Setup

### Step 1: Install Docker and Docker Compose

If you don't have Docker installed:

**Ubuntu/Debian:**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Add your user to docker group (optional - avoids needing sudo)
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

**Arch Linux:**
```bash
sudo pacman -S docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

---

### Step 2: Clone the Repository

```bash
git clone https://github.com/sfo2001/tuya-convert
cd tuya-convert
```

Or if you already have it cloned:
```bash
cd tuya-convert
git pull origin main
```

---

### Step 3: Configure Environment Variables

**3.1 Create .env File**

Copy the template:
```bash
cp .env-template .env
```

**3.2 Edit Configuration**

Open `.env` in your favorite editor:
```bash
nano .env
```

**Configuration Options:**

```bash
# Network interface name on your HOST machine
WLAN=wlan0

# Access Point name (can be anything you want)
AP=vtrust-flash

# Gateway address (leave as-is unless you have conflicts)
GATEWAY=10.42.42.1

# Backup directory on HOST for firmware backups and logs
LOCALBACKUPDIR=./data/backups
```

**3.3 Find Your WiFi Interface Name**

To find your WiFi interface name on the host:

```bash
ifconfig
# or
ip link show
```

Look for interfaces like:
- `wlan0` - Common default
- `wlp3s0` - PCI WiFi adapter
- `wlx...` - USB WiFi adapter (typically starts with wlx)

**Example:**
```
wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether aa:bb:cc:dd:ee:ff  txqueuelen 1000  (Ethernet)
```

Update `WLAN=wlan0` in `.env` to match your interface name.

**3.4 Configure Backup Directory**

The `LOCALBACKUPDIR` setting determines where firmware backups and logs are stored on your **host machine**.

Options:
- **Relative path:** `./data/backups` (inside tuya-convert directory)
- **Absolute path:** `/home/user/tuya-backups` (anywhere on your system)

Example:
```bash
# Create backup directory
mkdir -p ./data/backups

# Or use absolute path
LOCALBACKUPDIR=/home/$USER/tuya-backups
mkdir -p /home/$USER/tuya-backups
```

---

### Step 4: Build the Docker Image

Build the tuya-convert Docker image:

```bash
docker-compose build
```

**What's happening:**
- Downloads Alpine Linux 3.19 base image
- Installs system dependencies (hostapd, dnsmasq, mosquitto, etc.)
- Installs Python dependencies from requirements.txt (paho-mqtt, tornado, sslpsk3, pycryptodomex)
- Copies tuya-convert scripts into the image
- Sets up entrypoint

**Expected output:**
```
Building tuya
Step 1/7 : FROM alpine:3.19
 ---> ...
Step 2/7 : RUN apk add --update bash git iw dnsmasq ...
 ---> Running in ...
...
Successfully built abc123def456
Successfully tagged tuya-convert_tuya:latest
```

**Build time:** 5-15 minutes (depending on internet speed)

**Rebuild (if needed):**
```bash
# Force rebuild without cache
docker-compose build --no-cache
```

---

## Using Docker to Flash Devices

### Step 5: Run tuya-convert in Docker

**Standard Usage:**

```bash
docker-compose run --rm tuya
```

**What this does:**
- Creates a new container from the tuya-convert image
- Runs in **privileged mode** (required for network operations)
- Uses **host network mode** (required for AP creation)
- Mounts backup directory as volume
- Automatically starts `start_flash.sh`
- Removes container after exit (`--rm` flag)

**Expected Output:**
```
tuya-convert v2.4.5
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
2. Put your IoT device in autoconfig/smartconfig/pairing mode
3. Press ENTER to continue
```

---

### Step 6: Add Custom Firmware (Optional)

The `files/` directory is automatically mounted in the Docker container, making it easy to use custom firmware.

**To add custom firmware:**

```bash
# Copy your firmware to the files directory
cp /path/to/custom-firmware.bin files/

# Or download directly
cd files/
wget https://example.com/custom-firmware.bin
cd ..
```

**Supported firmware files:**
- Tasmota (included: `tasmota-lite.bin`)
- ESPurna (included: `espurna-base.bin`)
- Custom builds (ESPHome, etc.)

**Requirements:**
- Maximum 512KB for first flash
- Must include first-stage bootloader

The firmware will automatically appear in the flash menu when you run tuya-convert.

---

### Step 7: Flash Your Device

Follow the same procedure as the [Quick Start Guide](Quick-Start-Guide.md):

1. **Connect smartphone** to the `vtrust-flash` AP (or your custom AP name from `.env`)
2. **Put device in pairing mode** (fast blinking LED)
3. **Press ENTER** in the Docker container terminal
4. **Wait for device connection** (shows `IoT-device is online with ip 10.42.42.42`)
5. **Backup completes automatically**
6. **Select firmware** to flash (includes any custom firmware you added)
7. **Complete!**

---

### Step 8: Access Backups and Logs

After flashing, find your backups in the directory specified by `LOCALBACKUPDIR`:

```bash
ls -la ./data/backups/
# or
ls -la /home/$USER/tuya-backups/
```

**Backup Contents:**
```
20251105_143022/
├── user1.bin              # Original firmware backup
├── device-info.txt        # Device information
├── smarthack-psk.log      # PSK identity log
├── smarthack-web.log      # Web server log
├── smarthack-mqtt.log     # MQTT broker log
├── smarthack-wifi.log     # AP log
└── smarthack-udp.log      # Discovery log
```

---

## Docker Command Reference

### Common Docker Operations

**Start container with immediate tuya-convert:**
```bash
docker-compose run --rm tuya
```

**Start container and get bash shell (for debugging):**
```bash
docker-compose run --entrypoint bash tuya
```

Then manually run tuya-convert inside:
```bash
./start_flash.sh
```

**Keep container after exit (for troubleshooting):**
```bash
docker-compose run tuya
# Container persists after exit - remove manually later
```

**List running containers:**
```bash
docker ps
```

**List all containers (including stopped):**
```bash
docker ps -a
```

**Remove stopped containers:**
```bash
docker container prune
```

**View container logs:**
```bash
docker logs [container-id]
```

**Stop running container:**
```bash
docker stop [container-id]
```

---

## Advanced Configuration

### Custom Firmware

The `files/` directory is automatically mounted as a Docker volume, so you can simply add firmware files and they'll be immediately available:

```bash
# Add your custom firmware
cp /path/to/custom-firmware.bin files/

# Start flashing (no rebuild needed!)
docker-compose run --rm tuya
```

**No image rebuild required!** The files directory is mounted from your host system, so any changes are immediately reflected in the container.

**Included firmware:**
- `tasmota-lite.bin` - Tasmota minimal build
- `espurna-base.bin` - ESPurna base build

Your custom firmware will appear in the selection menu alongside these included options

### Network Configuration

The Docker container uses:
- **privileged: true** - Required for network interface control
- **network_mode: "host"** - Required for creating the access point

These settings are necessary and cannot be changed without breaking functionality.

### Environment Variables

All environment variables from `.env` are passed to the container:

```yaml
environment:
    WLAN: ${WLAN}          # WiFi interface
    AP: ${AP}              # AP name
    GATEWAY: ${GATEWAY}    # Gateway IP
```

These are used by `config-tuya.sh` to generate `config.txt` inside the container.

---

## Troubleshooting

### Build Fails

**Symptom:**
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solutions:**
1. Check internet connection
2. Try rebuild without cache: `docker-compose build --no-cache`
3. Check Docker has enough disk space: `docker system df`
4. Clean up old images: `docker system prune`

### Can't Connect to WiFi Adapter

**Symptom:**
- AP doesn't start
- Smartphone can't find AP
- Error about network interface

**Solutions:**

1. **Verify interface name in .env:**
   ```bash
   ifconfig
   # Update WLAN= in .env to match your interface
   ```

2. **Check interface is available:**
   ```bash
   ip link show wlan0
   ```

3. **Try different USB port** (for USB adapters)

4. **Check interface supports AP mode:**
   ```bash
   iw list | grep -A 10 "Supported interface modes"
   # Should show "AP" in the list
   ```

### Backups Not Appearing on Host

**Symptom:**
Flash successful but can't find backups on host

**Solutions:**

1. **Check LOCALBACKUPDIR path in .env:**
   ```bash
   cat .env | grep LOCALBACKUPDIR
   ```

2. **Verify directory exists:**
   ```bash
   ls -la ./data/backups/
   ```

3. **Check volume mount:**
   ```bash
   docker-compose config
   # Verify volumes section shows correct path
   ```

4. **Create directory if missing:**
   ```bash
   mkdir -p ./data/backups
   ```

### Custom Firmware Not Appearing in Menu

**Symptom:**
Added firmware to `files/` but it doesn't appear in the flash menu

**Solutions:**

1. **Verify file is in the correct location:**
   ```bash
   ls -la files/
   # Should show your custom firmware file
   ```

2. **Check file permissions:**
   ```bash
   chmod 644 files/your-firmware.bin
   ```

3. **Verify file size (must be ≤512KB):**
   ```bash
   ls -lh files/your-firmware.bin
   # First flash must be 512KB or smaller
   ```

4. **Check file extension:**
   - Must be `.bin` file
   - Ensure no extra extensions (e.g., `.bin.txt`)

5. **Restart the container:**
   ```bash
   # Exit current container and restart
   docker-compose run --rm tuya
   ```

### Phone Can't Connect to AP

**Symptom:**
Smartphone finds vtrust-flash but can't connect

**Possible Causes:**

1. **Host firewall blocking:**
   ```bash
   # Temporarily disable firewall (if safe to do so)
   sudo ufw disable
   # Or add rules for the gateway network
   ```

2. **Wrong network interface:**
   Check `smarthack-wifi.log` in backups directory

3. **Interface already in use:**
   Make sure no other process is using the WiFi adapter

### Container Can't Be Deleted

**Symptom:**
```
Error response from daemon: cannot remove container
```

**Solution:**
```bash
# Force stop container
docker stop [container-id]

# Force remove container
docker rm -f [container-id]

# Or remove all stopped containers
docker container prune -f
```

### Permission Denied Errors

**Symptom:**
```
permission denied while trying to connect to Docker daemon
```

**Solutions:**

1. **Run with sudo:**
   ```bash
   sudo docker-compose run --rm tuya
   ```

2. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

3. **Check Docker daemon is running:**
   ```bash
   sudo systemctl status docker
   sudo systemctl start docker
   ```

### "No cipher can be selected" in Logs

**Symptom:**
In `smarthack-psk.log`: `could not establish sslpsk socket`

**Note:** This is expected for newer devices with PSK Identity 02. The Docker environment has correct OpenSSL version - this is a device limitation, not a Docker issue.

See [System Requirements](Failed-attempts-and-tracked-requirements.md) for more information.

---

## Docker vs Native Installation

### When to Use Docker

✅ **Use Docker if:**
- You don't want to modify your host system
- You use tuya-convert occasionally
- You want easy cleanup
- You want reproducible environment
- You're comfortable with Docker

### When to Use Native Installation

✅ **Use Native Installation if:**
- You use tuya-convert frequently
- You want faster startup (no container overhead)
- You want to modify/debug scripts easily
- You prefer direct access to logs
- Docker adds complexity you don't need

### Performance Comparison

| Aspect | Docker | Native |
|--------|--------|--------|
| **Setup Time** | Longer (image build) | Shorter (direct install) |
| **Startup Time** | ~5-10 seconds slower | Faster |
| **Runtime Performance** | Nearly identical | Slightly faster |
| **Disk Space** | ~500MB (image) | ~200MB (packages) |
| **Ease of Cleanup** | Easy (remove image) | Manual (remove packages) |

---

## Maintenance

### Updating tuya-convert

```bash
cd tuya-convert
git pull origin main
docker-compose build
```

### Cleaning Up

**Remove old images:**
```bash
docker image prune -a
```

**Remove all tuya-convert data:**
```bash
docker-compose down
docker rmi tuya-convert_tuya
rm -rf ./data/backups/
```

---

## Related Pages

- [Quick Start Guide](Quick-Start-Guide.md) - Step-by-step flashing guide
- [Installation Guide](Installation.md) - Native installation method
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions
- [System Requirements](Failed-attempts-and-tracked-requirements.md) - Compatibility information
- [Compatible Devices](Compatible-devices.md) - Device compatibility list

## Code References

- **Docker Configuration:**
  - `Dockerfile` - Image build instructions
    - Line 1: Base image (Alpine 3.19)
    - Line 3: System package installation
    - Lines 6-10: Python package installation from requirements.txt
    - Line 18: Entrypoint configuration
  - `docker-compose.yml` - Service orchestration
    - Line 5: Privileged mode (required for network control)
    - Line 6: Host network mode (required for AP)
    - Lines 8-10: Environment variable mapping
    - Line 12: Volume mount for backups
    - Line 13: Volume mount for custom firmware files

- **Docker Scripts:**
  - `docker/bin/tuya-start` - Container entrypoint
  - `docker/bin/config-tuya.sh` - Generates config.txt from environment variables

- **Environment Configuration:**
  - `.env-template` - Configuration template with comments

---

## Frequently Asked Questions

**Q: Where are my logs after flashing?**
A: Logs are stored in the `LOCALBACKUPDIR` specified in your `.env` file, inside timestamped folders.

**Q: Can I use Docker on macOS or Windows?**
A: No. tuya-convert requires direct hardware access to WiFi adapters and Linux networking features. Docker Desktop on macOS/Windows uses a Linux VM which doesn't provide the required hardware access.

**Q: Why does Docker need privileged mode?**
A: tuya-convert needs to create a WiFi access point and manipulate network interfaces, which requires privileged access.

**Q: Can I run multiple containers simultaneously?**
A: No. Each container needs exclusive access to the WiFi adapter. Only run one container at a time.

**Q: How do I update the firmware files in the container?**
A: Simply add your firmware files to the `files/` directory - they're automatically available in the container via volume mount. No rebuild required!

**Q: Can I use this with Podman instead of Docker?**
A: Possibly, but it's untested. Podman's handling of privileged containers and host networking may differ.

---

## Summary

Docker provides a clean, isolated environment for tuya-convert:

1. **Setup:** Install Docker, clone repo, configure `.env`
2. **Build:** `docker-compose build`
3. **Run:** `docker-compose run --rm tuya`
4. **Flash:** Follow standard procedure
5. **Cleanup:** Container auto-removes, backups persist on host

The Docker approach is ideal if you want to keep your host system clean and don't need frequent access to tuya-convert.

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting.md) page.*
