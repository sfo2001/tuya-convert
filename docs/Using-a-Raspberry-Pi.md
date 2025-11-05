## Generic Install Instructions
Before running Tuya-Convert, **you need to disconnect the Pi from its Wi-Fi network**, enabling the required `vtrust-flash` WiFi network to broadcast correctly. There are multiple ways of doing this: 

**_Warning_** ***You will need to be connected via Ethernet or "USB Gadget mode" to continue use after disabling wifi.***

Option 1. _Via GUI_: connect via VNC viewer, click the Wifi Icon, select your network and disconnect.

Option 2. _Via SSH/Terminal_: paste the command `sudo killall wpa_supplicant`

Option 3. _Via SSH/Terminal_: 

                       - type sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

                       - Delete the wifi network block including network={}

                       - Close the file (ctrl x, y, enter)

                       - sudo reboot

You can now follow the instructions on the main page.

## Pi Zero W
Setup [USB Serial Gadget mode](https://github.com/ct-Open-Source/tuya-convert/wiki/Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable) (unless you have keyboard/monitor)

### Pi Zero W using only wifi

1. Connect to the Raspberry Pi Zero W using wifi and ssh
2. Follow the normal Raspberry Pi instructions but stop before running start_flash.sh
3. Run the command `screen` (this will prevent your session being terminated when it disconnects)
4. Run `start_flash.sh`
5. Your ssh session will be disconnected when the Pi disassociates from your wifi network and creates its own vtrust-flash AP
6. Connect to the vtrust-flash AP and SSH to 10.42.42.1
7. Run `screen -r` to identify the session id your original screen session
8. Resume that screen session by running `screen -r -d [screen id]`
9. Continue with normal Raspberry Pi instructions