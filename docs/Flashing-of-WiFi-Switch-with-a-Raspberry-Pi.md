# Background information

There are many similar devices made by the same big company (Tuya) and redistributed by 3rd parties companies (like Sonoff, AVATTO, ...). These devices are natively integrated with the Tuya cloud which can operate the device remotely.
For example, from the cloud it's possible to upload a new firmware via OTA.

If you consider this to be unsecure and a kind of leakage in your home network, you can flash the device with a open source firmware (Tasmota) which can be operated locally on your network, does not require a cloud, and can be integrated locally with other system like Domoticz, Home Assistant, Alexa, Google.

Devices produced up to early 2020, could be flashed with a Tuya cloud simulator, e.g. tuya-convert.
The vulnerability has been fixed and tuya-convert cannot work anymore (see [#483](https://github.com/ct-Open-Source/tuya-convert/issues/483)).

If you want to flash the Tasmota firmware, you need to open the device and connect a serial device (like a Raspberry PI) to the test points.
A bit of reverse engineering needs to be done to map the testing point to the ESP chip pins.

For the ESP pinout, you need to check the Espressif datasheet.
See for example:
* ESP8266 https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf
* ESP8255 https://www.espressif.com/sites/default/files/documentation/0a-esp8285_datasheet_en.pdf

This page applies to a specific device: ![DEVICE](https://user-images.githubusercontent.com/4344157/93678312-5294ef80-faad-11ea-891a-99ed5893b5c9.png)

# Precondition

## Configure Raspberry PI switching ttyAMA and ttyS0 serials 
Follow one of these procedures to edit /boot/config.ini and /boot/cmdline.txt
https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3-4/
https://hallard.me/enable-serial-port-on-raspberry-pi/

In alternative, you can use any USB Serial devices or an Arduino serial

## Install the esptool

Follow this procedure https://tasmota.github.io/docs/Esptool/#download-esptool

## Connection

For this device the connection scheme is:
- connect RPI GPIO 5V to pin 3 of 5V/3V converted
- connect RPI GPIO TX to ESP serial RX
- connect RPI GPIO RX to ESP serial TX
- connect RPI GPIO GND to ESP GND

In order to make the reverse engineering of the connection, you need to identify the test points and to follow the path up to the ESP pins.
The test points are typically always present in any device as they are used by the manufacturer to flash the firmware after the HW assembly.
The test points shall allows therefore to power the chip (ESP 0 GND, +3.3 V), to connect to its serial (ESP GPIO TX, RX), to force the flash mode (ESP GPIO0) and to test that the button works properly. Indeed we need *six* test points.
In this example...

### Device board
![1](https://user-images.githubusercontent.com/4344157/93675811-55dbab80-faac-11ea-8a5e-5cf27d72f4ed.jpg)
First observation: you recognize the black square chip; in this example it's ESP8285.

### Zoom on the test points
![2](https://user-images.githubusercontent.com/4344157/93675825-570cd880-faac-11ea-86db-cab972c76687.jpg)
The test points (6 in this example) are the circles plate in the bottom right part. Let's call the A, B, C, D, E, F.

To follow the path up the ESP chip, you need to follow some solders on the back plate.
See the attached photo. Note that this photo is left-right flip so that it's easy to correlate the points in which the connection moves from the front to the back plate. These points are _holes_ which are visible in the same position on both plates.
![3](https://user-images.githubusercontent.com/4344157/93675832-57a56f00-faac-11ea-8e5b-db9c40ab4bd1.jpg)

### Follow the test points

![scheme](https://user-images.githubusercontent.com/4344157/93706962-70089e80-fb2b-11ea-91fe-259753d1a660.png)

The pin A is clearly soldered with the button; there is no further need to solder this pin.

The pin F is clearly connected to the main ground (the light red present almost everywhere in the board)

The other pins need a bit of attention and checks.

The result is:
* A: one of the ESP GPIO
* B: U0RXD Serial receive
* C: U0TXD Serial transmit
* D: GPIO0 needed to force the flash mode
* E: VDDA +3.3V
* F: GROUND 0V

### Connection to the Raspberry Pi serial

Here a connection scheme
![4](https://user-images.githubusercontent.com/4344157/93675839-583e0580-faac-11ea-99dc-b309b40f227c.jpg)

A small caveat.
It is not possible to connect the Raspberry +3.3V to the ESP VDDA. It will not work. You need to find another power source.
Instead of powering directly the ESP chip, I chose to connect the Raspberry +5V to the device internal power converter. In the photo it's the black chip AMS1117, pin Vin http://www.advanced-monolithic.com/pdf/ds1117.pdf

# Validate the setup: esp _hello world_

If everything was fine, you should be able to establish a connection with the chip

`esptool.py --port /dev/ttyS0 chip_id`

# Flash procedure

Reference: https://nodemcu.readthedocs.io/en/master/flash/

1. switch on the device with ESP GPIO0 shortcut on GND; this can be done by pressing the device button
1. run esptool and flash the firmware

`esptool.py --port /dev/ttyS0 erase_flash`

`esptool.py --port /dev/ttyS0 write_flash -fm dout 0x0 tasmota.bin`

# Post firmware flashing

There a couple of additional step to configure your new tasmota devices.
For example you need to explain to the firmware what is the expected action to execute when the button is pressed (i.e. seitch the relee).
There is a procedure in the Tasmota wiki which explains how to reverse engineering the internal device GPIO connections.
Once you have done, you can create a template to be uploaded to any equivalent device.
For this specific device the template is:
`{"NAME":"Switch","GPIO":[0,0,0,0,0,17,0,0,21,0,0,0,0],"FLAG":0,"BASE":18}`
