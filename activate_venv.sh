#!/usr/bin/env bash
#
# activate_venv.sh - Helper script to activate the Python virtual environment
#
# Usage:
#   source ./activate_venv.sh
#
# Note: This script must be sourced, not executed directly, to activate
#       the virtual environment in your current shell session.
#

if [ ! -d "venv" ]; then
	echo "ERROR: Virtual environment not found!"
	echo "Please run ./install_prereq.sh first to create the virtual environment."
	return 1 2>/dev/null || exit 1
fi

echo "Activating Python virtual environment..."
source venv/bin/activate

echo "Virtual environment activated!"
echo "Python: $(which python3)"
echo "Pip: $(which pip)"
echo
echo "To deactivate the virtual environment, run: deactivate"
