# Compatible Devices

**Last Updated:** 2025-11-06
**Status:** 🔄 Community Updated

## Overview

This page provides a curated list of devices that have been successfully flashed with third-party firmware using tuya-convert. These devices are produced by Tuya and include various smart plugs, switches, and bulbs that have been tested by the community.

For comprehensive device lists organized by firmware type, see:
- [Compatible Devices (HTTP Firmware)](Compatible-devices-(HTTP-firmware)) - Extensive table of devices with HTTP-based firmware
- [Compatible Devices (HTTPS Firmware)](Compatible-devices-(HTTPS-firmware)) - Devices using HTTPS-based firmware

**Important:** It is recommended that you make a backup of the factory firmware before flashing, in case you need to revert to it if the third-party firmware does not function properly with your device.

## How to Contribute

To add a device to this list:
1. Successfully flash the device using tuya-convert
2. Document the device details including model, purchase date, and any special notes
3. [Edit this page](https://github.com/sfo2001/tuya-convert/edit/master/docs/Compatible-devices.md) or [open an issue](https://github.com/sfo2001/tuya-convert/issues)

## Device List

### eMylo WIFI Smart Switch

Works ootb. PCB type: E331298, bought in 2019, not used since.

### Gosund SP111 V1.1

Works [as described](https://blog.koehntopp.info/2020/05/20/gosund-and-tasmota.html) by @isotopp

### Gosund SP1

Works without issues. [More details about the device over at Tasmota.](https://templates.blakadder.com/gosund_SP1.html)

### Gosund P1 (3x Smart Plug /w USB)

Works without issues.

Template: `{"NAME":"Gosund_P1","GPIO":[0,145,157,146,0,32,0,0,22,23,21,0,17],"FLAG":1,"BASE":18}`

Console rules:

`Rule1 ON Button1#State DO Power4 2 ENDON`

`Rule2 ON Analog#A0div10<30 DO Power3 2 BREAK ON Analog#A0div10<60 DO Power2 2 BREAK ON Analog#A0div10<80 DO Power1 2 ENDON`

`Backlog Rule1 1; Rule2 1; Rule2 5`


### Gosund Smart Plug SP112

https://smile.amazon.de/gp/product/B07PMW88L7

{"NAME":"Smart Plug","GPIO":[57,145,56,146,0,22,0,0,0,0,21,0,17],"FLAG":0,"BASE":18}

### Gosund Smart LED Strip, 2.8M / 5M [RGB]

https://www.officehuman.com/products/gosund-nitebird-sl2-led-smart-light-strips-5m-voice-control-google-alexa-rgb-timer-app-control-music-sync (5M, Controller "SL2", 12V, External Power Supply [included])

https://us.gosund.com/blog/gosund-smart-light-strip-sl1 (2,8M, Controller "SL1", 5V, USB Power Supply)

{"NAME":"LED Strip","GPIO":[0,0,0,0,17,38,0,0,37,39,0,0,0],"FLAG":15,"BASE":18}

### Hama Wifi LED-Bulp E14 Socket

Works  by Tasmota   Gpio5  pwm1  Gpio 13  pwm2. Thanks

### InTempo Smart-Home-Steckdose

https://www.nkd.com/de_de/steckdose-nkd-15032022.html

### MoKo Smart LED Bulb, E14, 9W [RGBW]

https://smile.amazon.de/gp/product/B07SYJC3C9

{"NAME":"MOKO","GPIO":[17,0,0,0,143,144,0,0,0,0,0,0,0],"FLAG":0,"BASE":27}

### Nous A1 Smart Plug

Works without issues. [More details about the device over at Tasmota.](https://templates.blakadder.com/nous_A1.html)

### WOOX WiFi Smart Plug

Works as "SK03 Outdoor Modul", the relay is switching, the sensors for energy consumption are not working.

### Avidsen Home Plug (127006)

Works, but:
* had to switch to development branch to get the psk server up and running
* flashing was performed via RPi3 ... I had to install the necessary python modules by hand adding the `--break-system-packages` option

After that, applied config you can find [here](https://templates.blakadder.com/avidsen_127006.html) and the plug started to work. Updating to latest tasmota firmware also didn't cause any problems.

### Teckin SP25 Smart Plug

* Flash succeeds with latest `tasmota-lite.bin` (http://ota.tasmota.com/tasmota/release/) as of Dec 5 2024 (Release timestamp: 20241015)
* Wifi Configure succeeds as well, showing up as wifi client: tasmota-####X#-####
* HTTP interface (http://device-ip) Loads. Power on/off toggle functions. Assuming rest functions.

## Related Pages

- [Compatible Devices (HTTP Firmware)](Compatible-devices-(HTTP-firmware))
- [Compatible Devices (HTTPS Firmware)](Compatible-devices-(HTTPS-firmware))
- [Troubleshooting](Troubleshooting)
- [Installation Guide](Installation)
- [Quick Start Guide](Quick-Start-Guide)

## External Resources

- [Tasmota Device Templates Repository](https://templates.blakadder.com/)
- [Tasmota Configuration Guide](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/)

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*