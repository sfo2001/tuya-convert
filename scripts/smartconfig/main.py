#!/usr/bin/env python3
# encoding: utf-8
"""
main.py
Created by kueblc on 2019-01-25.
Configure Tuya devices via smartconfig for tuya-convert

This script sends smartconfig packets to configure Tuya devices with the
vtrust-flash AP credentials, allowing them to be flashed with custom firmware.
"""

from time import sleep

from smartconfig import smartconfig

# Configuration for vtrust-flash AP used by tuya-convert
ssid: str = "vtrust-flash"
passwd: str = ""  # Open network (no password)
region: str = "US"  # Region code
token: str = "00000000"  # Default token
secret: str = "0101"  # Default secret

# Number of smartconfig attempts to make
MAX_ATTEMPTS: int = 10
RETRY_DELAY_SECONDS: int = 3

print("Put device in EZ config mode (blinking fast)")
print("Sending SSID                  " + ssid)
print("Sending wifiPassword          " + passwd)
print("Sending token                 " + token)
print("Sending secret                " + secret)

for i in range(MAX_ATTEMPTS):  # Make 10 attempts

    smartconfig(passwd, ssid, region, token, secret)

    print()
    print("SmartConfig complete.")

    # Countdown to next attempt
    for t in range(RETRY_DELAY_SECONDS, 0, -1):
        print("Auto retry in %ds. " % t, end="", flush=True)
        sleep(1)
        print(end="\r")

    print("Resending SmartConfig Packets")
