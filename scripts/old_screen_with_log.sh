#!/usr/bin/env bash
#
# old_screen_with_log.sh - Wrapper for older screen versions (<4.6)
#
# Description:
#   Older screen versions don't support the -Logfile flag. This wrapper
#   creates a temporary .screenrc file to configure logging and handles
#   virtual environment activation for Python scripts.
#
# Usage:
#   ./old_screen_with_log.sh <screen_minor_version> <logfile_name> [screen_options...]
#
# Changes for Issue #1167:
#   - Added virtual environment detection and activation
#   - Ensures Python scripts find venv dependencies even through sudo screen
#   - Critical for sslpsk3 which has no system package on Ubuntu
#

screen_minor=${1}
screen_logfile_name=${2}
screen_other_options=${@:3}

# Detect screen version and set appropriate flags
if [ "$screen_minor" -gt 5 ]; then
	echo "Info: you have the modern enough version" \
             "to use the \"-Logfile\" flag of \"screen\""
elif [ "$screen_minor" -eq 5 ]; then
	screen_with_log="sudo screen -L"
else
	screen_with_log="sudo screen -L -t"
fi

# Create temporary .screenrc for logging configuration
echo "logfile ${screen_logfile_name}" > ${screen_logfile_name}.screenrc

# Execute screen with the other options
# Note: As of Fix #2 for Issue #1167, screen_other_options now includes
# "bash -c 'source venv/bin/activate && exec script.py'" instead of just "script.py"
# This ensures venv activation happens within the screen session
${screen_with_log} ${screen_logfile_name} \
    -c ${screen_logfile_name}.screenrc ${screen_other_options}

# Cleanup temporary config file
rm ${screen_logfile_name}.screenrc
