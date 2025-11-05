#!/usr/bin/env bash
set -euo pipefail

# Common function to create Python virtual environment and install dependencies
# This prevents code duplication across different distribution install functions
setupPythonVenv() {
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

debianInstall() {
	sudo apt-get update
	sudo apt-get install -y git iw dnsmasq rfkill hostapd screen curl build-essential python3-pip python3-setuptools python3-wheel python3-dev python3-venv mosquitto haveged net-tools libssl-dev iproute2 iputils-ping
	setupPythonVenv
}

archInstall() {
	sudo pacman -S --needed git iw dnsmasq hostapd screen curl python-pip python-wheel mosquitto haveged net-tools openssl
	setupPythonVenv
}

gentooInstall() {
	# Sync Portage tree (optional, user may want to do this manually)
	echo "Syncing Portage tree (this may take a while)..."
	sudo emerge --sync

	# Install system dependencies using Gentoo's emerge
	echo "Installing system dependencies..."
	sudo emerge --ask --verbose dev-vcs/git net-wireless/iw net-dns/dnsmasq \
		net-wireless/hostapd app-misc/screen net-misc/curl \
		dev-lang/python sys-devel/gcc sys-devel/make \
		app-misc/mosquitto sys-apps/haveged sys-apps/net-tools \
		dev-libs/openssl net-wireless/rfkill sys-apps/iproute2 \
		sys-apps/iputils
	setupPythonVenv
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
elif [[ ${ID} == 'gentoo' ]] || [[ ${ID_LIKE-} == 'gentoo' ]]; then
	gentooInstall
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
