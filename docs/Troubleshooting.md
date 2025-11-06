|Symptom|Reason|Recommendation|
|-------|------|--------------|
|Dots never end|Too many possible reasons|Open your logs and try other troubleshooting or seek support by filing a new issue|
|Device button unresponsive|Device is not running stock firmware|Check if the device is running intermediate firmware, or configure custom firmware|
|Device appears bricked|It may be running intermediate firmware or hasn't been configured yet|Check for `sonoff-****` or `vtrust-recovery` and proceed to troubleshooting|
|Device does not take IP `10.42.42.42`|Device is not running intermediate firmware|Do not alter the script, try other troubleshooting or seek support by filing a new issue|
|Port 6668 is open or device does not respond on port 80|Device is still running stock firmware|Try other troubleshooting or seek support by filing a new issue|
|`Smartlife-****` SSID is visible or device is blinking slowly|Device is in AP config mode|Device must be in EZ config mode (blinking quickly). Hold button for 5 seconds or turn on and off 3 times|
|`sonoff-****` SSID is visible|Device is running Tasmota|Connect to the AP and configure your device at `192.168.4.1`|
|`vtrust-recovery` SSID is visible|Device is running intermediate firmware but could not connect to `vtrust-flash`|Make sure `start_flash` is running and `vtrust-flash` is visible, then unplug and plug your device back in, wait a minute for script to continue|
|`KeyboardInterrupt` exception in log|You ran `stop_flash` or otherwise stopped the script|Nothing, this is not an issue|
|`wlan0: Could not connect to kernel driver` in wifi log||Not an issue|
|`Socket error on client P1, disconnecting` in mqtt log|Older versions of `tuya-convert` do not disconnect from the broker properly|Not an issue, will not impact the process whatsoever|
|`WARNING: it appears this device does not use an ESP82xx and therefore cannot install ESP based firmware` in web log|Device uses a different microcontroller|Nothing else we can do, return the device or use it as is. You will not be able to flash Tasmota or other ESP based firmware, even over wire.|
|`vtrust-flash` rejects subsequent connections after the first|`hostapd` is broken on some Raspberry Pi builds ([#241](https://github.com/ct-Open-Source/tuya-convert/issues/241))|See [raspberrypi/firmware#1117](https://github.com/raspberrypi/firmware/issues/1117)|
|Repeated requests for `tuya.device.dynamic.config.get` in the web log|Device may be rejecting the fake `schema`|Try to obtain the real schema using `tuyapi` or by capturing the official registration through `tcpdump` and open an issue with this information|
|`[SSL: NO_SHARED_CIPHER] no shared cipher` in psk log|Your phone is trying to make HTTPS connections to the outside internet, but we are capturing all HTTPS requests|It will not impact flashing, safe to ignore|
|`ModuleNotFoundError: No module named 'sslpsk3'` in logs|Virtual environment not activated in sudo screen sessions (issue #1167)|Update to latest version with issue #1167 fix, or re-run `./install_prereq.sh`|
|`error: externally-managed-environment` during installation|Modern Linux (Ubuntu 24+, Debian 12+) enforces PEP 668|Use `./install_prereq.sh` which creates a virtual environment automatically|
|`start_flash` stalls at `Starting AP...` when running over SSH|You are getting disconnected when the wireless interface is used to create the AP|Connect through some other means, secondary wifi, ethernet, USB or control directly|
|`vtrust-flash` WLAN does not give devices an IP|firewall blocks DHCP reaching dnsmasq|temporarily turn off firewall|
|`vtrust-flash` WLAN does not give devices an IP and logs tell `dnsmasq[2744]: failed to create listening socket for 127.0.0.1: Address already in use`|another service is listening on the device|temporarily disable the other DNS-server, or (if the other service is dnsmasq as well) add `except-interface`|
|Backup Times Out|Unknown|This can happen on some devices, and may leave it in an unresponsive state until power cycled. You may need to stop the backup process from occuring to successfully flash|