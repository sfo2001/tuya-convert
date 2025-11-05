#!/usr/bin/env bash
#
# start_flash.sh - Main entry point for tuya-convert
#
# Description:
#   This script orchestrates the complete tuya-convert process for flashing
#   Tuya-based IoT devices with custom firmware (e.g., Tasmota, ESPurna).
#   It sets up a rogue access point, intercepts device communication, and
#   installs intermediate firmware before flashing the final custom firmware.
#
# Usage:
#   ./start_flash.sh
#
# Requirements:
#   - All prerequisites installed via install_prereq.sh
#   - config.txt properly configured
#   - Root/sudo access for network operations
#   - Compatible wireless adapter supporting AP mode
#
# Process Overview:
#   1. Sets up a fake AP with the name configured in config.txt
#   2. Starts web server to intercept device registration
#   3. Starts MQTT broker for device communication
#   4. Initiates smartconfig pairing to trick device
#   5. Installs intermediate firmware on device
#   6. Backs up original firmware
#   7. Flashes user-selected custom firmware
#
# Exit Codes:
#   0 - Success
#   1 - Setup failure or user cancellation
#

# Terminal formatting variables
bold=$(tput bold)
normal=$(tput sgr0)

# Load configuration settings (AP name, gateway, etc.)
. ./config.txt

#
# setup() - Initialize the tuya-convert environment
#
# This function:
#   - Displays the current tuya-convert version
#   - Runs prerequisite checks
#   - Configures screen logging based on version
#   - Starts all required services in separate screen sessions:
#     * Access Point (AP)
#     * Web server (fake registration)
#     * MQTT broker
#     * PSK frontend
#     * Tuya discovery service
#
# Global Variables Used:
#   $GATEWAY - Gateway IP from config.txt
#   $PWD - Present working directory
#
# Screen Sessions Created:
#   - smarthack-wifi: Access point
#   - smarthack-web: Fake registration server
#   - smarthack-mqtt: MQTT broker
#   - smarthack-psk: PSK frontend
#   - smarthack-udp: Device discovery
#
setup () {
	echo "tuya-convert $(git describe --tags)"

	# Activate Python virtual environment if it exists
	# This ensures all Python scripts can find their dependencies
	if [ -d "venv" ]; then
		echo "Activating Python virtual environment..."
		source venv/bin/activate
	else
		echo "WARNING: Virtual environment not found!"
		echo "Please run ./install_prereq.sh to set up the environment properly."
		echo "Attempting to continue with system Python packages..."
	fi

	pushd scripts >/dev/null || exit

	# Run environment checks (network adapter, dependencies, etc.)
	. ./setup_checks.sh

	# Detect screen version and configure logging appropriately
	# Screen 4.6+ uses -Logfile, older versions need a wrapper script
	screen_minor=$(screen --version | cut -d . -f 2)
	if [ "$screen_minor" -gt 5 ]; then
		screen_with_log="sudo screen -L -Logfile"
	else
		screen_with_log="./old_screen_with_log.sh ${screen_minor}"
	fi

	echo "======================================================"
	echo -n "  Starting AP in a screen"
	# Start the access point in a detached screen session
	$screen_with_log smarthack-wifi.log -S smarthack-wifi -m -d ./setup_ap.sh

	# Wait for the AP to be fully operational by pinging the gateway
	while ! ping -c 1 -W 1 -n "$GATEWAY" &> /dev/null; do
		printf .
	done
	echo

	# Give the AP additional time to stabilize
	sleep 5

	echo "  Starting web server in a screen"
	# Fake registration server intercepts device cloud registration
	$screen_with_log smarthack-web.log -S smarthack-web -m -d ./fake-registration-server.py

	echo "  Starting Mosquitto in a screen"
	# MQTT broker handles device communication protocol
	$screen_with_log smarthack-mqtt.log -S smarthack-mqtt -m -d mosquitto -v -c $PWD/mosquitto.conf

	echo "  Starting PSK frontend in a screen"
	# PSK (Pre-Shared Key) frontend manages encryption keys
	$screen_with_log smarthack-psk.log -S smarthack-psk -m -d ./psk-frontend.py -v

	echo "  Starting Tuya Discovery in a screen"
	# Discovery service finds and communicates with Tuya devices
	$screen_with_log smarthack-udp.log -S smarthack-udp -m -d ./tuya-discovery.py
	echo
}

#
# cleanup() - Terminate all services and restore system state
#
# This function:
#   - Sends SIGINT (Ctrl+C) to all screen sessions
#   - Terminates the hostapd access point
#   - Restores the working directory
#
# Called automatically on script exit via trap
#
cleanup () {
	echo "======================================================"
	echo "Cleaning up..."

	# Send Ctrl+C to all screen sessions to gracefully stop services
	sudo screen -S smarthack-web          -X stuff '^C'
	sudo screen -S smarthack-mqtt         -X stuff '^C'
	sudo screen -S smarthack-psk          -X stuff '^C'
	sudo screen -S smarthack-udp          -X stuff '^C'

	echo "Closing AP"
	# Kill the hostapd process to stop the access point
	sudo pkill hostapd

	# Deactivate virtual environment if it was activated
	if [ -n "${VIRTUAL_ENV:-}" ]; then
		deactivate
	fi

	echo "Exiting..."
	popd >/dev/null || exit
}

# Register cleanup function to run on script exit (success or failure)
trap cleanup EXIT

# Initialize environment and start all services
setup

#
# Main Loop - Device Flashing Process
#
# This loop allows flashing multiple devices without restarting the entire
# environment. Each iteration handles one device from pairing to firmware flash.
#
while true; do
	echo "======================================================"
	echo
	echo "IMPORTANT"
	echo "1. Connect any other device (a smartphone or something) to the WIFI $AP"
	echo "   This step is IMPORTANT otherwise the smartconfig may not work!"
	echo "2. Put your IoT device in autoconfig/smartconfig/pairing mode (LED will blink fast). This is usually done by pressing and holding the primary button of the device"
	echo "   Make sure nothing else is plugged into your IoT device while attempting to flash."
	echo "3. Press ${bold}ENTER${normal} to continue"
	read -r
	echo
	echo "======================================================"

	echo "Starting smart config pairing procedure"
	# Launch smartconfig in background to broadcast fake WiFi credentials
	./smartconfig/main.py &

	echo "Waiting for the device to install the intermediate firmware"

	# Timeout counter: 120 seconds to wait for device
	i=120

	# !!! CRITICAL: DEVICE IP MUST BE 10.42.42.42 !!!
	# The intermediate firmware is configured to request this specific IP.
	# If your device gets a different IP, it means the intermediate firmware
	# failed to install and you should NOT proceed with flashing.
	# Do NOT modify this IP address - it will break the entire process.
	#
	# Wait for device to install intermediate firmware and connect with IP 10.42.42.42
	while ! ping -c 1 -W 1 -n 10.42.42.42 -I 10.42.42.1 &> /dev/null; do
		printf .

		# Decrement counter and check for timeout
		if (( --i == 0 )); then
			echo
			echo "Timed out while waiting for the device to (re)connect"
			pkill -f smartconfig/main.py && echo "Stopping smart config"
			echo "======================================================"
			echo "Attempting to diagnose the issue..."
			# Run diagnostic script to help troubleshoot
			./dr_tuya.sh
			echo "======================================================"
			read -p "Do you want to try flashing another device? [y/N] " -n 1 -r
			echo
			# Exit both loops if user doesn't want to retry
			[[ "$REPLY" =~ ^[Yy]$ ]] || break 2
			# Continue outer loop to retry with same or different device
			continue 2
		fi
	done

	echo
	echo "IoT-device is online with ip 10.42.42.42"

	# Stop smartconfig - no longer needed once device is connected
	pkill -f smartconfig/main.py && echo "Stopping smart config"

	#
	# Firmware Backup Phase
	#
	echo "Fetching firmware backup"
	sleep 2

	# Create timestamped backup directory
	timestamp=$(date +%Y%m%d_%H%M%S)
	backupfolder="../backups/$timestamp"
	mkdir -p "$backupfolder"
	pushd "$backupfolder" >/dev/null || exit

	# Attempt to download original firmware from device (90 second timeout)
	# The intermediate firmware exposes a /backup endpoint for this purpose
	if ! curl -JOm 90 http://10.42.42.42/backup; then
		echo "Could not fetch a complete backup"
		read -p "Do you want to continue anyway? [y/N] " -n 1 -r
		echo
		# Exit if user doesn't want to proceed without backup
		[[ "$REPLY" =~ ^[Yy]$ ]] || break
		sleep 2
	fi

	echo "======================================================"
	echo "Getting Info from IoT-device"
	# Fetch and save device information (chip ID, flash size, etc.)
	curl -s http://10.42.42.42 | tee device-info.txt
	popd >/dev/null || exit

	#
	# Custom Firmware Flashing Phase
	#
	echo "======================================================"
	echo "Ready to flash third party firmware!"
	echo
	echo "For your convenience, the following firmware images are already included in this repository:"
	echo "  Tasmota v9.2.0 (wifiman)"
	echo "  ESPurna 1.5 (base)"
	echo
	echo "You can also provide your own image by placing it in the /files directory"
	echo "Please ensure the firmware fits the device and includes the bootloader"
	echo "MAXIMUM SIZE IS 512KB"

	# Interactive firmware selection and flashing
	./firmware_picker.sh

	# Move all log files to backup folder for later analysis
	sudo mv *.log "$backupfolder/"

	echo "======================================================"
	read -p "Do you want to flash another device? [y/N] " -n 1 -r
	echo
	# Exit loop if user is done flashing devices
	[[ "$REPLY" =~ ^[Yy]$ ]] || break
done
