A [Raspberry Pi Serial Gadget](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/serial-gadget#set-up-logging-in-on-pi-zero-via-serial-gadget-2-13) makes it so when you plug in the Raspberry Pi Zero to your computer, it will pop up as a Serial Port. You can use the Raspberry Pi with any computer and operating system and it doesn't require special drivers or configuration.

The setup process for the Serial Gadget only has to be done once. The `Tuya-Convert` software can be updated independently of this setup (requires setting up Wi-Fi for accessing the Internet).

## Serial Interface Setup
* Download and flash the latest Raspbian Lite on a microSD card
  After burning the SD card, the SD flasher may automatically eject it from your computer. If so, remove the SD card and reinsert it to mount it again.
* Edit config.txt & cmdline.txt
  * Find the partition labeled boot and open that folder
  * Use a text editor to open config.txt
  * Go to the bottom and add `dtoverlay=dwc2` (no quotation marks) as the last line in the file
  * Save the file as plain text
  * Use a text editor to open cmdline.txt
  * After `rootwait`, add a space and then `modules-load=dwc2,g_serial` (no quotation marks)
  * Save the file as plain text
* Create a new text file on the SD card named `wpa_supplicant.conf`  
  * Add the following lines:
    ```
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
    * If your Wi-Fi SSID is hidden, add `scan_ssid=1` to the `network` section  
* Enable SSH
  * Create a new file on the SD card named `ssh`  
    The contents of the ssh file don’t matter. When the Raspberry Pi first boots, it looks for this file. If it finds it, it will enable SSH and then delete the file.  

    **Windows**:  
    `C:\> <d>:` (where 'd' is the drive letter of the SD card)  
    `<d>:\> copy nul ssh`  

    **Linux/MacOS**:  
    `$ cd /Volumes/boot`  
    `$ touch ssh`  
* Remove the SD card from the computer by using the proper eject procedure  
* Connect to your Raspberry Pi using SSH over Wi-Fi  
  * Insert the SD card in the Raspberry Pi
  * Power up the Raspberry Pi using the microUSB connector labeled `PWR`. Once it boots, it should be connected to your Wi-Fi network
  * Find its IP address in the router and connect to the Raspberry Pi via SSH
  * Log in with user ID `pi`; password `raspberry`
  * Encode the Wi-Fi free text password  
    `wpa_passphrase "SSID" "PASSWORD" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null`  
    where `SSID` and `PASSWORD` are your network's Wi-Fi credentials
  * Edit `wpa_supplicant.conf` to remove the free text password  
* Set up the Raspberry Pi ZeroW Serial Gadget to accept logins  
  * Run `sudo dmesg` to verify that it bound the `g_serial` driver
  * Enable the tty service  
    `$ sudo systemctl enable getty@ttyGS0.service`  
    > Created symlink /etc/systemd/system/getty.target.wants/getty@ttyGS0.service → /lib/systemd/system/getty@.service.  

    `$ sudo reboot`  
  * After the Raspberry Pi reboots, connect to it via SSH again and verify that the service is running:  
    `$ sudo systemctl is-active getty@ttyGS0.service`  
    > active
* Shut down the Raspberry Pi  
  `$ sudo shutdown now`
## Connect to the Raspberry Pi using the Serial Gadget
* Ensure that your USB cable is data cable and not just a USB power cable. Plug in the USB cable from your computer to the Raspberry Pi microUSB connector labeled `USB`, **not** the `PWR` connector.  
  * On your computer you'll see a new Serial port is created  

    **Windows**:  
    `COMN` (where N can be any number)  

    **Linux/MacOS**:  
    `/dev/tty.usbmodemNNNN`  
      The `NNNN` number after `usbmodem` will vary. Check your `/dev` folder for the actual device name  

* Use a serial terminal emulator application (e.g., [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/))  
  * Select the port and configure it for `115200` baud, `8N1` (8-bit No-parity 1-stop) (e.g., using [PuTTY](https://tartarus.org/~simon/putty-snapshots/htmldoc/Chapter3.html#using-serial))  
  * Connect to the Raspberry Pi and log in
    _**You may have to hit return a few times to get it to come up with the login prompt.**_  

    * On MacOS, the following command may help establish a successful session window:  
       `screen -L /dev/cu.usbmodemXXXX 115200`  

      * The `XXXX` number after `usbmodem` will vary. Check your `/dev` folder for the actual device name  
      * The `-L` option turns output logging on for this window  

  You are now connected to your Raspberry Pi ZeroW via the USB cable.  

## Tuya-Convert Installation
:warning: :warning: _**Installing software packages requires a connection to the Internet (i.e., Wi-Fi)**_ :warning: :warning:  

* Update Raspbian packages  
  `$ sudo apt-get update && sudo apt-get -y upgrade`  
* Install git to clone the GitHub repository  
  `$ sudo apt-get install git`  
* Install and configure `Tuya-Convert`  
  ```
  $ git clone https://github.com/ct-Open-Source/tuya-convert
  $ cd tuya-convert
  $ ./install_prereq.sh
  ```
* **The Wi-Fi interface (`wlan0`) is now freed up for `Tuya-Convert` to use to flash your Tuya smart devices.**  
  You will connect to the Raspberry Pi with the wired USB Serial Gadget and will no longer want it to connect to your Wi-Fi network automatically. Disable your Wi-Fi network configuration by renaming the Wi-Fi configuration file:  
  `sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf-saved`  

## Optional Housekeeping
* Disable SSH  
  ```
  $ sudo service ssh stop
  $ sudo systemctl disable sshd.service (Buster)
  $ sudo systemctl disable ssh.service (Stretch)
  ```

## Using Tuya-Convert
* [Invoke the `Tuya-Convert` flashing script as usual](https://github.com/ct-Open-Source/tuya-convert/blob/master/README.md#flash-third-party-firmware) to flash your Tuya smart devices:  
  ```
  $ cd tuya-convert
  $ ./start_flash.sh
  ```
* After flashing your Tuya devices, be sure to shut down the Raspberry Pi properly:  
  `$ sudo shutdown now`

## Updating the Tuya-Convert Scripts
* The Raspberry Pi will need to connect to the Internet. Connect to the Raspberry Pi via the Serial Gadget and enable the connection to your Wi-Fi network:  
  `cp /etc/wpa_supplicant/wpa_supplicant.conf-saved /etc/wpa_supplicant/wpa_supplicant.conf`  
* Reboot the Raspberry Pi:  
  `$ sudo reboot`  
* Repeat the [`Tuya-Convert` installation procedure](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable#tuya-convert-installation)  

Thank you to `@SourPickel` (Discord) for bringing this to the community's attention.
