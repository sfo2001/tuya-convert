#!/usr/bin/env bash
set -euo pipefail

debianInstall() {
	sudo apt-get update
	sudo apt-get install -y git iw dnsmasq rfkill hostapd screen curl build-essential python3-pip python3-setuptools python3-wheel python3-dev python3-venv mosquitto haveged net-tools libssl-dev iproute2 iputils-ping

	# Create Python virtual environment to comply with PEP 668
	# This prevents "externally managed environment" errors on modern distributions
	echo "Creating Python virtual environment..."
	python3 -m venv venv

	# Install Python packages into the virtual environment
	echo "Installing Python packages into virtual environment..."
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
	deactivate
}

archInstall() {
	sudo pacman -S --needed git iw dnsmasq hostapd screen curl python-pip python-wheel mosquitto haveged net-tools openssl

	# Create Python virtual environment to comply with PEP 668
	# This prevents "externally managed environment" errors on modern distributions
	echo "Creating Python virtual environment..."
	python -m venv venv

	# Install Python packages into the virtual environment
	echo "Installing Python packages into virtual environment..."
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
	deactivate
}

if [[ -e /etc/os-release ]]; then
	source /etc/os-release
else
	echo "/etc/os-release not found! Assuming debian-based system, but this will likely fail!"
	ID=debian
fi

if [[ ${ID} == 'debian' ]] || [[ ${ID_LIKE-} == 'debian' ]]; then
	debianInstall
elif [[ ${ID} == 'arch' ]] || [[ ${ID_LIKE-} == 'arch' ]]; then
	archInstall
else
	if [[ -n ${ID_LIKE-} ]]; then
		printID="${ID}/${ID_LIKE}"
	else
		printID="${ID}"
	fi
	echo "/etc/os-release found but distribution ${printID} is not explicitly supported. Assuming debian-based system, but this will likely fail!"
	debianInstall
fi

echo "Ready to start upgrade"
echo
echo "Python packages have been installed in a virtual environment (venv/)"
echo "The virtual environment will be automatically activated when you run ./start_flash.sh"
