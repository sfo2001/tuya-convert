# Compatible Devices (HTTP Firmware)

**Last Updated:** 2025-11-06
**Status:** 🔄 Community Updated

## Overview

This page lists devices produced by Tuya that use HTTP-based firmware and can be flashed with third-party firmware using tuya-convert. The devices are organized by category (Sockets, Lights, Switches, etc.) and include detailed GPIO pin configurations, model information, and compatibility notes.

**Important:** It is recommended that you make a backup of the factory firmware in the event that you need to revert to it should the third-party firmware not function properly with your device.

### About Tasmota Templates

Since [Tasmota](https://github.com/arendst/Tasmota) version 6.4.1.16, the firmware supports [templates](https://tasmota.github.io/docs/Templates/) for configuring unsupported devices. Templates are easily configurable in the web UI. It is recommended to use templates instead of changing `Generic Module (18)` GPIO assignments.

The [Tasmota Device Templates Repository](https://templates.blakadder.com/) maintains a list of templates for Tasmota as well as a list of unsupported devices (ones without an ESP82xx chip). There are numerous devices based on Tuya Wi-Fi modules. It may not be possible for all of them to work as expected with Tasmota. If you have a new device that does not have an existing template, you may refer to the [Configure Unknown Device guide](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/) to configure the device.

## How to Contribute

To add a device to this list:
1. Successfully flash the device using tuya-convert
2. Test the device thoroughly with your chosen firmware (e.g., Tasmota)
3. Document all GPIO pin assignments and device-specific configurations
4. [Edit this page](https://github.com/sfo2001/tuya-convert/edit/master/docs/Compatible-devices-(HTTP-firmware).md) or [open an issue](https://github.com/sfo2001/tuya-convert/issues) with the device details

## Device Tables

## Sockets/Multi-sockets

|Area|Vendor|Vendors device ID|Device Name|GPIOs|Notes|2nd MCU|Flash size/mode
|:--------------:|---------|:---------:|:-----------:|:------------:|:-------------------:|:-----------:|:------------:
|AU|Arlec|PC189HA|Smart Plug In Socket With Grid Connect|GPIO4: Blue LED (inverted), GPIO12: Relay, GPIO13: Red LED (inverted), GPIO14: Button (inverted)|||
|AU|Brilliant|20676/05|Smart Wifi Plug and USB Charger|GPIO05: Relay1, GPIO14: Button1|Tasmota Generic.  New devices have the patched firmware and will not convert OTA |?|1M DOUT
|AU|Brilliant|20925|Smart Wifi Power Monitoring Plug|GPIO03: Button1, GPIO04:HLW8012 CF, GPIO05: HLWBL CF1, GPIO12: HLWBL SELi, GPIO13: LedLinki, GPIO14: Relay1|Tasmota Generic.  New devices have the patched firmware and will not convert OTA |?|1M DOUT
|AU|DETA|6930HA|Rewireable Smart Plug|GPIO1: Button (inverted), GPIO13: LED (inverted), GPIO14: Relay|||
|AU|Kogan|-|Wifi Smart Plug and power meter|GPIO0 (inverted) ( in some versions normal) Switch button, GPIO14 Relay, GPIO13 (inverted) Status led, hlw8012 power meter: GPIO12 sel pin (inverted), GPIO4 CF pin, GPIO5 CF1 pin|Used Tasmota Generic to flash Esphome|?|1M QIO @ 40MHz
|AU|Mirabella|I002341|WiFi Power Plug with USB Port|GPIO2=LED1i(56), GPIO12=Relay1(21), GPIO13=Button1(17)|?|https://mirabellagenio.net.au/|?
|CA|Globe|50000|Smart Plug|GPIO4: LED1i(56), GPIO12: Relay1(21), GPIO14: Button1(17)|Tasmota Generic||
|CA|micmi|sm-pw702|WiFi Plug|GPIO12=Relay1, GPIO13=Button1, GPIO4 Blue LED|Orange LED follows relay|?|1M
|CA|TECKIN|SP20 |Smart Plug with Power Monitoring|?|Tasmota 59 (Teckin US)|?|1M DOUT @ 40MHz
|CA,US|Merkury|MI-WW105|Indoor Wifi Smart Plug|GPIO4=LED2, GPIO5=LED1i, GPIO12=Relay1, GPIO13=Button1|-|?|1M DOUT @ 40MHz
|CA/US|[Costco/CE](https://www.costco.ca/CE-Smart-Home-Wi-Fi-Smart-Plug%2c-2-pack.product.100417575.html)|Wi-Fi Smart Plug|CE smart Home LA-WF3|GPIO4: Led1i (56), GPI05: Led2i (57), GPI12: Relay1 (21), GPI13: Button1 (17)|||
|CA/US|[Oittm](https://www.amazon.ca/gp/product/B074W8GYY6/ref=oh_aui_search_asin_title?ie=UTF8&psc=1)|Smart-Plug-Outdoor|Outdoor Smart Socket with power monitoring|USE SK03 outdoor module|||
|CA/US|PRIME Cable|Sold by Costco in canada|CCRCWFIO2PK|GPIO4: LED2i (57)(Blue), GPIO5: Led1i (56)(Red), GPIO12: Relay1 (12), GPIO13: Button1i (122)|This item was sold in Costco Warehouse in canada only, did not find any online reference|-|-
|CA/US|[PRIME Cable](https://primewirecable.com/collections/smart-home-devices/products/1-outlet-white-mini-wi-fi-control)|Sold by Costco in Canada|CCRCWFII3PK|GPIO4: LED1i (56), GPIO12: Relay1 (21), GPIO14: Button1 (17)|This item was sold in Costco Warehouse in Canada as a 3 pack.|-|1M
|EU|[ANCCY](https://www.amazon.de/gp/product/B07CSL6ZT9/)|SP1|Smart Socket with power monitoring|GPIO1: Led1i, GPIO3: Button1, GPIO4: HLW8012 CF, GPIO5: HLWBL CF1, GPIO12: HLWBL SELi, GPIO13: Led2i, GPIO14: Relay1|Sonoff-sensors||1M
|EU|[cDream](https://www.amazon.de/gp/product/B07HJCHXX6)|NX-SM200|Smart WLAN Socket|GPIO4: Led1, GPIO5: BL0937 CF, GPIO12: HLWBL SELi, GPIO13: Button1, GPIO14: HLWBL CF1, GPIO15: Relay1|[Template](https://blakadder.github.io/templates/nanxin_NX-SM200.html)|?|1M DOUT @ 40MHz
|EU|[Hauppauge](https://www.amazon.de/dp/B07JLMCMMZ)|SL-1642|mySmarthome Voice Plug|GPIO4: Led1, GPIO12: Relay1, GPIO12: Button 1|Red LED is controlled by Relay1||1M QIO @ 40MHz
|EU|[Neo Coolcam 10A](https://www.aliexpress.com/item/32854589733.html)|NAS-WR01W|Smart Plug 2000W/10A|GPIO13: Button1, GPIO04: Led1, GPIO12: Relay1|Sonoff Classic 6.4.1.15 / Generic Module.|?|?
|EU|[Neo Coolcam 16A](https://www.aliexpress.com/i/32966183521.html)|NAS-WR01W|Smart Plug 3680W/16A with power monitoring|GPIO0: Button1 (17), GPIO04: HWL8012 CF (133), GPIO05: HWLBL CF1 (132), GPIO12: HWLBL SELi(132), GPIO13: Led1i (56), GPIO14: Relay1 (21) |Sonoff Classic 6.4.1.15 / Generic Module. Works also on KMC70011, only w/o power monitoring. |?|499kB
|EU|[OxaOxe](https://www.amazon.fr/gp/product/B07MQ4734T/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1)|NX-SM200|Wi-Fi Smart Plug with Energy Monitor|Module 18; gpio0 57; gpio12 21; gpio13 17; gpio15 52; gpio4 131; gpio5 134; gpio14 132|||
|EU|[Panamalar](https://www.amazon.de/gp/product/B07JBRRW1M/)|NX-SM200|Smart WLAN Socket|GPIO4: Led1, GPIO5: BL0937 CF, GPIO12: HLWBL SELi, GPIO13: Button1, GPIO14: NLWBL CF1, GPIO15: Relay1|-|?|1M DOUT @ 40MHz
|EU|[Pearl](https://www.pearl.de/a-NX4458-3103.shtml)|SF-550.avs|Luminea Home Control WLAN Steckdose aussen|?|Luminea ZX2820 - Developer Branch 6.4.1.14 including power monitoring; also KMC 70011 template but without correct power monitoring|?|1M QIO @ 40MHz
|EU|[Slitinto](https://www.amazon.de//dp/B07JGTGGXC)|NX-SP202|WiFi Smart Plug|GPIO12: Relay1, GPIO15: Relay2, The rest: ? |Generic Config|?|?
|EU|Smart Socket |TP22|WiFi Smart Plug|GPIO3: Button1, GPIO13: Led1, GPIO14: Relay1 |Generic Config|?|?
|EU|[Swisstone SH 100](https://www.amazon.de/Swisstone-100-WiFi-Steckdose-Sprachsteuerbar-Kindersicherung-weiß/dp/B07GD3WKVL/ref=sr_1_5?__mk_de_DE=ÅMÅŽÕÑ&keywords=Swisstone+SH+100&qid=1573832717&sr=8-5)|?| WiFi Smart Plug|GPIO12: Relay1 (21); GPIO13: Button1 (17)|Based on Generic(18) module; Use the following template: {"NAME":"SH 100","GPIO":[255,255,255,255,255,255,255,255,21,17,255,255,255],"FLAG":15,"BASE":18}|?|?
|EU|[Vansware Smart Plug 16A](http://www.amazon.de/dp/B07MYCTHJS)|-|Wi-Fi Smart Plug with Energy Monitor|GPIO0: Button1 (17), GPIO04: HWL8012 CF (133), GPIO05: HWLBL CF1 (132), GPIO12: HWLBL SELi(132), GPIO13: Led1i (56), GPIO14: Relay1 (21) |Sonoff Classic 6.4.1.15 / Generic Module|-|-
|EU|ablue|SP1|Smart Plug|?|?|?|?
|EU|AISIRER|AWP07L|Smart Plug|?|works with Tasmota profile #45 (Blitzwolf)||1M DOUT @ 40MHz
|EU|Aplic / CSL|WDP 303075|Wifi Smart Socket|?|Tasmota Profile 53|1M DOUT @ 40 MHz|
|EU|Avatar Controls|AWP07L|Mini Smart Wifi Plug|?|Tasmota Template: {"NAME": "Avatar AWP07L", "GPIO": [56,255,255,255,0,134,0,0,131,17,132,21,0], "FLAG": 0, "BASE": 45}|?|1M DOUT @ 40MHz
|EU|Avatar Controls|AWP08L|Mini Smart Wifi Plug|GPIO03: Led1i, GPIO13: Button1, GPIO15: Relay1|?|?|1M DOUT @ 40MHz
|EU|BlitzWolf|BW-SHP2|Smart Socket|?|Device profile already included in Tasmota|N|1M DOUT
|EU|BlitzWolf|BW-SHP6|Smart Socket|?|Identical to BlitzWolf BW-SHP2|N|?
|EU|Coosa|?|WiFi Smart Socket|GPIO4: LED2, GPIO5: LED1i, GPIO12:Relais 1, GPIO13:Button 1|Tasmota Generic|?|1M DOUT
|EU|Etlephe|?|Powerstrip|GPIO3=LED1i, GPIO4=Relay 4i, GPIO5=Button1, GPIO12=Relay2i, GPIO13=Relay3i, GPIO14=Relay1i, GPIO16=Relay5|?|?|?
|EU|Gosund|SP111|Smart Plug|?|works with Tasmota profile `#45 (BlitzWolf SHP2)`|?|1M DOUT
|EU|Gosund|SP1 (2200W/10A)|Smart Plug|GPIO02: BLUE, GPIO05: CF PIN, GPIO12: SEL PIN, GPIO13: Button1, GPIO14: CF1 PIN, GPIO15: Relay|?|?|?
|EU|Gosund|SP1|Smart Plug|GPIO1: Blue LED, GPIO13: Red LED, GPIO14: Relay, GPIO3: Button, GPIO4&5: hlw8012|-|?|1M DOUT @ 40mhz (ESP8285)
|EU|GREFIC|Gd003100|Mini Smart Plug|GPIO4 = Relay1, GPIO5 = Button1, GPIO12 = Led1i|All is working|Tasmota generic (18)|1M QIO @40MHz
|EU|Hama|176533|WLAN-/Smart Home Steckdose|GPIO12 = Relay1, GPIO13 = Button1|-|?|?
|EU|Hyleton 314|HLT-314|wifi smart plug|GPIO0 = LED2i, GPIO2 = LED1i,GPIO13 = Button1,GPIO15 = Relay1|LEDs do not show state of relais|?|1M QIO
|EU|Joinrun|W-DEXI|Smart Socket|GPIO1: Button1n GPIO13: Led1 GPIO14: Relay1|?|?|?
|EU|JOMARTO|?|Mini Smart WiFi Plug|GPIO2=LED1, GPIO13=Button1, GPIO15=Relay1|-|?|?
|EU|Joywell|?|4-Plug-Multi-Socket (Type F)|--|clearly Tuya, but c't-sample was destroyed when tested, so no GPIOs yet. Hard to flash via serial due to GPIO 0 being on the back of the module (blocked by relay)|N|1M DOUT
|EU|Koogeek|KLOE4|KLOE4 Smart Power Strip|GPIO01 = LED1, GPIO3 = Button1, GPIO4 = Relay2, GPIO5 = Relay1, GPIO12 = Relay3, GPIO13 = Relay4, GPIO14 = Relay5|works with the latest Espurna 1.13.3, build flag ZHILDE_EU44_W, or the precompiled binary espurna-1.13.3-zhilde-eu44-w.bin|?|?
|EU|Lingan|--|SWA1|GPIO 4 = LED, GPIO 5 = Relay, GPIO 13 = Button|--|N|1M QIO
|EU|Lingan|--|SWA11|?|--|?|?
|EU|Maxcio|W-DE004|Wifi Smart Socket|GPIO1 = Button1 GPIO13 = Led1i GPIO14 = Relay1|Tasmota Generic|N|1M QIO @40MHz
|EU|Maxcio|YX-DE02|Wi-Fi Smart Socket|GPIO1=Button1, GPIO3=Relay1, GPIO4=Led1i, GPIO5=PWM4, GPIO12=PWM1, GPIO13=PWM2, GPIO14=PWM3||?|1M
|EU|Mengonee|JHG01E|Wifi smart plug mini|GPIO4=LED1i, GPIO12=Relay1, GPIO13=Button1|-|?|1MB DOUT
|EU|MoesHouse|?|Wifi Plug|GPIO5 = Led1i, GPIO12 = Relay|-|?|?
|EU|Nedis|WIFIP110FWT|Wifi Plug|GPIO0=Pushbutton, GPIO14=Relay, GPIO13=LED, GPIO12=BL0937_Sel_Pin, GPIO5=BL0937_CF1_Pin, GPIO4=BL0937_CF_Pin|Same Config as at the "HYKKER Smart Plug", instead using a HLV8012 i/f Converter, it uses the compatible BL0937. Works fine with espurna (HYKKER-Config); not tested with Tasmota.|?|?
|EU|Nedis|WIFIPO120FWT|Wi-Fi Smart Outdoor Plug|GPIO0=Button1, GPIO4=HLW8012 CF, GPIO5=HLWBL CF1, GPIO12=HLWBL SELi, GPIO13=Led1i, GPIO14=Relay1|[Template](https://templates.blakadder.com/nedis_WIFIPO120FWT.html)|?|?
|EU|Novostella|B07KVWQJCP|9W 810LM E27 RGBCW 2700K-6500K|GPIO00 None, GPIO01 None, GPIO02 None, GPIO03 None,GPIO04 PWM1, GPIO05 PWM4, GPIO09 None, GPIO10 None, GPIO12 PWM2, GPIO13 PWM5, GPIO14 PWM3, GPIO15 None, GPIO16 None, FLAG None|easy flash with tuya-convert, others templates tried with issues, impossibility to manage it well|?|?
|EU|Pearl|LHC-101.on|Luminea Home Control Touch-Lichtschalter|0: Led2; 3: Button1; 4: Relay1; 14: Led1|{"NAME": "LHC-101.on", "GPIO": [53,0,0,17,21,0,0,0,0,0,52,0,0], "FLAG": 0, "BASE": 1}|?|?
|EU|Pearl|SF-450.avs SF-500.avs|Luminea Home Control WLAN Steckdose|Blitzwolf Profile works|Luminea 450 without powermonitor|?|?
|EU|TECKIN|SP21|Smart Plug|?|works with Tasmota profile `#45 (BlitzWolf SHP2)`|?|1M DOUT
|EU|TECKIN|SP23 (UK)|Smart Plug with Energy Monitoring|GPIO15 = Relay, GPIO02 = Blue LED, GPIO05 = CF / Power, GPIO14 = CF1 / Current/Voltage, GPIO12 = Sel, GPIO13 = Button|Works with Tasmota profile `#45 (BlitzWolf SHP2)`, [ESPHome Example](https://gist.github.com/timmo001/7b0cf9958b80f6356a3f47d2f29aa1a6)|?|?
|EU|TECKIN|SP22|WLAN Smart Steckdose|GPIO1: Button1, GPIO3: Led2i (red), GPIO13: Led1i (blue), GPIO14: Relay1|Tasmota Teckin preset works|?|1M DOUT @ 40MHz
|EU|TedGem|SP111|Smart Plug|?|works with Tasmota profile `#45 (BlitzWolf SHP)`. Attention: Gosund EP2 looks much like the SP111 but it uses different chip. In december 2020 amazon.de is selling EP2 not SP111|?|?
|EU|Tellur|TLL331031|Powerstrip|GPIO13 = Relay1, GPIO4 = Relay2, GPIO5 = Relay3, GPIO14 = USB Power|works with Tasmota profile `#60 (Manzoku strip)`<br><br>Used Espurna Generic to flash Esphome v1.14.2 (`board: esp8285`) |?|1M DOUT @ 40MHz
|EU|Tflag|NX-SM100|Smart Plug with Power Monitoring|GPIO0=56, GPIO5=134, GPIO12=21,GPIO13=17,GPIO14=132, GPIO15=57, GPIO16=131|Works with Tasmota template (Nanxin NX-SM200)|?|?
|CA|Topgreener|TGWF115PQM|Smart Plug (10A) with Energy Monitoring|GPIO3=button, GPIO4=CF(hlw8012), GPIO5=CF1(hlw8012), GPIO12=SEL(hlw8012), GPIO13=LED(green), GPIO14=relay/blue LED|Flashed espurna from raspberry pi zero w. Purchased on amazon early 2020. uses ESP8285. Current sensor has markings removed but it is very clearly an HLW8012 based on the way it is connected.||1M
|EU|Unknown|XS-A25|Smart Wifi Power Strip (UK)|GPIO0 = Led1, GPIO2 = Led2, GPIO4 = Relay5, GPIO5 = Relay2, GPIO12 = Relay4, GPIO13 = Button1, GPIO14 = Relay3, GPIO15 = Relay1|[Tasmota template](https://blakadder.github.io/templates/XS-A25.html)|?|1M QIO
|EU|Unknown|BSD23|Wifi Smart Plug|GPIO4 = Led1, GPIO12 = Relay1, GPIO13 = Button1|-|?|1M QIO
|EU|Unknown|BSD29 (UK)|Wifi Smart Plug|GPIO3 = HLWBL SELi,GPIO4 = BL0937 CF,GPIO5 = HLWBL CF1,GPIO12 = Relay1, GPIO13 = Button1,GPIO14 = LED1i|[Tasmota Template](https://blakadder.github.io/templates/bsd29.html)|?|1M DOUT
|EU|Unknown|BSD34 (EU)|Wifi Smart Plug|TX = Blue Led, GPIO12 = Relay1, GPIO13 = Button1, GPIO14 = Red Led|[Tasmota Template](https://blakadder.github.io/templates/bsd34.html)|?|1M DOUT
|EU|WAZA|JH-G01E|Wi-Fi Smart Plug|GPIO4=Relay1, GPIO5=Button1, GPIO12=LED1i|-|?|?
|EU|Woox|R5024|Smart Plug| GPIO15: Relay, GPIO2: Led1i, GPIO13: Button| | | 
|EU|Woox|R4028|Smart Power Strip EU Type 16A 3 Ports|GPIO1 = LED, GPIO3 = Button2, GPIO4 = Relay3 GPIO5 = Relay2, GPIO13 = Relay4, GPIO14 = Relay1|--|?|1M DOUT
|EU|ZEOOTA|Tasmota Generic (18)|Smart Power Strip|GPIO1: Led1i, GPIO3: Button 1 (17), GPIO4: Relay2 (22), GPIO5: Relay1 (21) GPIO12: Relay3 (23) GPIO13: Relay4 (24) GPIO14: Relay5 (25)|Can be bought on [AliExpress](https://www.aliexpress.com/item/Wifi-Smart-Power-Strip-4-EU-Outlets-Plug-Socket-with-USB-4-Charging-Port-App-Voice/32864686078.html?spm=a2g0z.10010108.1000001.12.4f10788cZ6weOS), works well with default Tasmota included in the package.|?|?
|EU|Zhilde|ZLD-44EU-W|Smart-Power-Strip|GPIO01 = LED1, GPIO3 = Button1, GPIO4 = Relay2, GPIO5 = Relay1, GPIO12 = Relay3, GPIO13 = Relay4, GPIO14 = Relay5|works with the latest Espurna 1.13.3, build flag ZHILDE_EU44_W, or the precompiled binary espurna-1.13.3-zhilde-eu44-w.bin|?|?
|EU|ZOOZEE|SE131|Smart Plug||Tasmota Generic|[Template](https://blakadder.github.io/templates/zoozee_SE131.html)|1M DOUT
|UK|[VIGICA 2.1A USB Charger 13A WiFi Wall Socket Smart Switch](https://www.amazon.co.uk/gp/product/B07GBQJSHK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)|Wall outlet|Wall outlet with 2 sockets and 2 USB chargers|GPIO0: Button 1; GPIO5: Relay 2; GPIO9: Button 2; GPIO12: Relay 1|||
|UK|Hyleton 313|HLT-313|wifi smart plug|GPIO0 = LED2i, GPIO2 = LED1i,GPIO13 = Button1,GPIO15 = Relay1|-|?|?
|UK|Hyleton 336|HLT-336|wifi smart power strip|GPIO0 = LED1, GPIO3 = LED2i, GPIO4 = Relay1i, GPIO5 = Button1, GPIO12 = Relay3i, GPIO13 = Relay2i, GPIO16 = Relay4i |[Template](https://blakadder.github.io/templates/hyleton_336.html)|?|1M QIO
|UK|Koogeek|KLUP1|KLUP1 Wifi Smart Plug with energy monitoring|GPIO1: Blue LED, GPIO3: Button1, GPIO4: HLW8012 CF, GPIO5: HLWBL CF1, GPIO12: HLWBL SELi, GPIO13: Red LED, GPIO14: Relay1|<A href="https://blakadder.github.io/templates/kogeek_KLUP1.html">Template</A>|?|
|UK|Maxcio|W-UK007|Wifi Smart Plug w/ Energy Monitoring|GPIO0=Led1i, GPIO13=Button1, GPIO15=Relay1|Relay & power monitoring works with BlitzWolf SHP profile, but not LED (as GPIO0=Led2i)|?|?
|UK|Unknown|SWA9|Power Work Google Plug|GPIO4 = LED1,GPIO5 = Relay1,GPIO13 = Button1|[Tasmota Template](https://blakadder.github.io/templates/SWA9.html)|?|1M DOUT
|US|[AUKEY](https://smile.amazon.com/gp/product/B07CC9S4MS)|SH-PA1|Wi-Fi Smart Plug|GPIO0: Led1i (red), GPIO2: Led2i (blue), GPIO13: Button1, GPIO15: Relay1|[Tasmota Template](https://blakadder.github.io/templates/aukey_SH-PA1.html)|?|?
|US|[BN-LINK](https://www.amazon.com/gp/product/B07HPG58FP/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)|Smart-Plug|Smart WiFi Outlet, Hubless with Energy Monitoring and Timer Function|GPIO2: Led1i, GPIO3: Button1, GPIO13: Led2i, GPIO14: Relay1|||
|US|[Epicka](https://github.com/ct-Open-Source/tuya-convert/wiki/Epicka-Smart-Plug)|WP1000|Smart Plug|GPIO4=LED1i(Blue), GPIO5=LED2i(Red), GPIO12=Relay1, GPIO13=Button1|Tasmota Generic||
|US|[EVA LOGIK](https://www.amazon.com/Socket-Outlet-Compatible-Google-Control/dp/B06XZ3J66L)|NWF001|Mini Smart Plug|GPIO1: Button1, GPIO13: Led1, GPIO14:Relay1|||
|US|[Heygo 02](https://www.amazon.com/gp/product/B075DJL39W)|-|Wi-Fi Smart Plug with Energy Monitor|?|Espurna 1.13.5 HY02 |-| 1M DOUT
|US|[KING-LINK](https://www.amazon.com/gp/product/B0776T26Q3)|C128|OutDoor Smart Plug|GPIO04: Relay2, GPIO12: Relay1, GPIO14: Button1, GPIO15: Relay3, GPIO16: Led1i|Generic Config|?|1M QIO
|US|[OxaOxe](https://www.amazon.com/dp/B07G2NQMGX/ref=cm_sw_em_r_mt_dp_U_LeyzCbPB7YAXE)|NX-SM800/NX-SP201|Wi-Fi Smart Plug with Energy Monitor & Overload Protection|Module 18; gpio0 57; gpio12 21; gpio13 17; gpio15 52; gpio4 131; gpio5 134; gpio14 132|||
|US|[Slitinto](https://www.amazon.com/gp/product/B07F6X4KX3)|NX-SP201|WiFi Dual Smart Plug with Power Monitoring|GPIO0: Led1i, GPIO4: Button1, GPIO5: HLW8012 CF, GPIO12: Relay1, GPIO13: Button2, GPIO14: HLWBL CF1, GPIO15: Relay2, GPIO16 HLWBL SEL |Generic Module - Developer Branch Tasmota 02052019|?|
|US|[Yeron](https://www.amazon.com/gp/product/B07DP12DQP)|US101|Wifi Smart Plug with Power Monitoring|GPIO03: Button1, GPI04: HLW812 CF, GPIO5: HLWBL CF1, GPIO12: HLWBL SELi, GPIO13: LED1i, GPIO14: Relay1|Generic Module - Developer Branch Tasmota 02052019<br><br>*1 of 2 units purchased March 4, 2018 never even tried to connect to the VTRUST network (that unit works with Smart Life, so not defective)|?|
|US|3stone|XS-SSA01|Smart Plug Mini|pin 1: button (low=pressed)<br>pin 13: LED (low=on)<br>pin 14: relay (high=closed)|flash chip seems pretty fast<br>is ETL listed, despite no ETL logo on the device|?|1M QIO
|US|Aicliv|AS2100|Outdoor Smart Socket|GPIO3: Relay3, GPIO4: Led2, GPIO12: Relay1, GPIO13: Button2, GPIO14: Relay2|Tasmota Generic||1M DOUT @ 40MHz
|US|Aicliv|AS2100|Outdoor Smart Socket|GPIO3: Relay3, GPIO4: Led2, GPIO12: Relay1, GPIO13: Button2, GPIO14: Relay2|Tasmota Generic||1M DOUT @ 40MHz
|US/EU|[Albohes](https://www.amazon.de/dp/B07JNQ2FXN/ref=cm_sw_em_r_mt_dp_U_LpKxEbK4GRCNW)|PS-1602/PS-1606|Outdoor Smart Socket Dual|GPIO0: Button1, GPIO5: Relay2, GPIO9: Button2, GPIO12: Relay1|Tasmota Generic|?|?
|US|Aneken|SWA5|Smart Socket|GPIO15: Relay1, GPIO13: Button1, GPIO2: LED1i|Tasmota Generic||1M DOUT
|US|ANIKUV|YM-WS-1|Mini Smart Outlet|GPIO12: LED1i GPIO13: Button1 GPIO15: Relay1|[Wifi-Smart-Plug-ANIKUV-Outlet](https://www.amazon.com/Wifi-Smart-Plug-ANIKUV-Outlet/dp/B075FVRSW6) Works with Tasmota Generic Module|?|1M DOUT
|US|Bestek|MJR1011|Smart Plug|GPIO4 = led1i(56) GPIO12 = Relay1(21) GPIO13 = Button1(17)|Tasmota Generic||1M DOUT @ 40MHz
|US|BlitzWolf|BW-SHP3|Smart Socket|?|[Tasmota Template](https://blakadder.github.io/templates/blitzwolf_SHP3.html)|N|1M DOUT
|US|Blue Shark|W-US003, MPV2RQ-US|Blue Shark Wifi Mini Plug|pin 0 = blue LED (low=on), pin 13 = button (low = pressed), pin 15 = relay (high = on)|cheapest US outlet on amazon march 2019, WARNING: not UL/ETL listed! one of mine registers as "hot ground" and "open neutral" with my outlet tester! DO NOT BUY, UNSAFE|?|1M DOUT
|US|GDTech|MPV2RO-US|WiFi Mini Plug|GPIO1: Button1, GPIO13: LED1 (Inverted), GPIO14: Relay1|?|?|1M DOUT
|US|Geekbes|YM-WS-1|Mini Smart Socket|GPIO1: Button1, GPIO13: LED1, GPIO14: Relay1|Works with Tasmota Generic Module|?|1M ???
|US|Gosund|WP3|Smart Plug| [Template](https://blakadder.github.io/templates/gosund_wp3.html) |-|?|?
|US|Gosund|WP5|Smart Plug|GPIO4: Switch1, GPIO12: LED2i, GPIO13: LED1i, GPIO14: Relay1<BR><BR>If this configuration doesn't work, try the Tecking SP10 Configuration below.|Switch1 / Button1 are interchangeable.  In an arduino sketch, use pins 4, 12, 13, and 14.|?|1M DOUT @ 40mhz (ESP8285)
|US|HoveBeaty|SM-PW701U|WiFi Smart Outlet|GPIO2=LED1i(bright blue), GPIO4=LED2i(dim blue), GPIO12=Relay1, GPIO13=Button1, Red LED tied to relay (no GPIO control)|Tasmota Generic||
|US|HugoAI|AWP02L-N|Mini Smart Socket|GPIO0 = LED2i, GPIO2 = LED1i, GPIO13 = Button1, GPIO15 = Relay1|Tasmota Generic Module|?|1M DOUT
|US|KMC|KT-KMC|4 Outlet WiFi|GPIO 13 Relay 2, GPIO 14 Relay 3, GPIO 15 Relay 1, GPIO 16 Button|?|?|?
|US|Luntak|--|Wifi Smart Plug|GPIO02 = LED GPIO13 = Button GPIO15 = Relay|Tasmota Generic|?|?
|US|MartinJerry|--|mini Smart Plug|GPIO04 = Led1i GPIO12 = Relay1 GPIO13 = Button1|Tasmota Generic|?|?
|US|Merkury|MI-OW101-101W|Outdoor Wifi Smart Plug|GPIO0 = Button1, GPIO5=LED1i, GPIO13=LED2, GPIO14=Relay1|Same As Geeni GN-OW101-101|?|1M QIO
|US|Omoton|W-US002|Wifi Smart Socket|GPIO1 = Button1, GPIO13 = Led1, GPIO14 = Relay1|-|?|?
|US|Rockbirds|?|Wifi Smart Plug|GPIO2 = Led1, GPIO12 = Relay1, GPIO13 = Button1||?|1M QIO
|US|Shenzhen Jiuheng|JH-G01U|Smart Plug|GPIO4 = Relay1, GPIO12 = LED1i, GPIO5 = Button1i|?|?|
|US|TECKIN|SP25 |Smart Plug|GPIO0 = Led1i, GPIO12 = Relay2, GPIO13 = Button1, GPIO15 = Relay1| USB Power is Relay2||1M
|US|TECKIN|SP10 |Smart Plug with Power Monitoring|GPIO0 = Led2i, GPIO2 = Led1i, GPIO13 = Button1, GPIO15 = Relay1|?|?|
|US|Unknown|YX-WS01|Smart-Plug|GPIO1 = Switch1, GPIO13 = Led1i, Gpio14 = Relay1|?|?|
|US|Unknown|X6|Wi-Fi Smart Plug|GPIO0 = LED2i, GPIO2 = LED1i, GPIO13 = Button1, GPIO15 = Relay1|No Manufacturer Information on Plug.  Used Tasmota Generic Module|?|1M QIO
|US|ZOOZEE|SA101|Smart Plug|GPIO0: LED2i-Red, GPIO2: Led1i-Blue, GPIO13: Button1, GPIO15: Relay1|Tasmota Generic|?|1M DOUT
|US|ZOOZEE (Wide Plug)|SA102|Smart Plug with monitoring|?|Teckin US preset works<br><br>May need to configure in Smart Life, then use factory reset option before it can be flashed.|?|1M DOUT


## Lights

|Vendor|Socket-Type|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:
|ASZKJ|E27|Smart Bulb LED Wifi|SB001|Red: GPIO14, Green: GPIO12, Blue:GPIO13, White: GPIO4|Firmware updated already out the box||1M QIO
|Blitzwolf|LED strip|Smart LED Light Strip|BW-LT11|GPIO0: Button1,GPIO4: PWM1, GPIO5: PWM4, GPIO12: PWM2, GPIO14: PWM3|US plug is also available. https://blakadder.github.io/templates/blitzwolf-bw-lt11.html||?
|Boaz|E27|Smart LED Downlight|X00287N3QR|GPIO4: PWM1,GPIO12: PWM2, GPIO14: PWM3, GPIO5: PWM4, GPIO13: PWM5|RGBWW|?|?
|Deltaco|E27|Smart RGB Bulb|SH-LE27RGB|GPIO4: PWM2, GPIO5: PWM1, GPIO12: PWM5, GPIO13: PWM3, GPIO14: PWM4|[Tasmota Template](https://templates.blakadder.com/deltaco_SH-LE27RGB.html)||?
|FCMILA|B22|Generic Dimmable RGBW 7W LED (Cold White)|TYWE3S|GPIO5:PWM1=White, GPIO4:PWM2=Red, GPIO12:PWM3=Green, GPIO14:PWM4=Blue|Used `git clone -b enhance-api https://github.com/kueblc/tuya-convert.git` @20190811|?|1M QIO @40MHz
|Globe|RGB Lamp|Smart Floor Lamp #67589|??|GPIO4: PWM1, GPIO5: PWM4, GPIO12: PWM2, GPIO13: PWM5, GPIO14: PWM3|?|?|1M QIO
|Geeni|E26|Prisma 1050|GN-BW944-999| GPIO04: SM16716 CLK; GPIO05: PMW1;  GPIO13: SM16716 PWR; GPIO14:SM16716 DAT| | |1M QIO
|Feit|E26/E27|Smart Wifi Bulb Color|OM60/RGBW BPA800/RGBW|GPIO5=PWM1, GPIO12=PWM2, GPIO4=CLK, GPIO13=ENABLE, GPIO14=DATA(SM16716)|[Tasmota Template](https://blakadder.github.io/templates/feit_electric-OM60RGBWCAAG.html)<br>If the bulb is not in the blinking state,<br>turn bulb On-Off-On-Off-On.||1M QIO
|Lohas|E14|Smart Bulb LED Wifi|LH-ZN123-2-2700|MY9291: Data pin: GPIO13, Clock Pin: GPIO15|Firmware updated on one, but not on the other. Uses an MY9291 driver||1M QIO
|Luminea|E27|Home Control|[ZX-2831-675](https://www.pearl.de/a-ZX2831-3103.shtml)|GPIO5: PWM1, GPIO12: PWM2|Produced for PEARL GmbH| | 1M QIO
|Luminea|E27|Home Control|[ZX-2832-675](https://www.pearl.de/a-ZX2832-3103.shtml) LAV-100.rgbw|GPIO5: PWM4 (White)|Although this bulb is a true RGBW Bulb, no suiteable configuration for controlling RGB was found yet. | | 1M QIO
|Luminea|E14|RGBW Bulb 4,5Watt|[NX-4462-675](https://www.pearl.de/a-NX4462-3103.shtml)|GPIO5: PWM4, GPIO12: PWM2, GPIO14: PWM3, GPIO4: PWM1|Produced for PEARL GmbH| | 1M QIO
|Lyasi|E27|Wifi Smart Birne|PT-BW09|DI=GPIO4,DCKI=GPIO5|?|?|1M QIO
|Mirabella|B22|Genio Wifi Dimmable 9W LED (Warm White)|I002333|GPIO13:PWM1|KMart, clamshell blister pack|?|1M QIO
|Mirabella|E27|Genio Wifi Dimmable Cool White|I002334|?|?|https://mirabellagenio.net.au/|?|1M QIO
|Mirabella|B22|Genio Wifi Dimmable 9W LED (Warm Cool Day)|I002337|GPIO5:PWM1=Cold6500K, GPIO13:PWM2=Warm2700K|KMart, clamshell blister pack|?|1M QIO @40MHz
|Mirabella|B22|Genio Wifi Dimmable 9W LED (Warm White)|I002605|GPIO13:PWM1|Woolworths, cardboard packaging|?|1M QIO
|Mirabella|E27/B22|Genio Wifi RGBW|?|GPIO4: PWM1, GPIO12: PWM2, GPIO14: PWM3, GPIO5: PWM4|?|https://mirabellagenio.net.au/|1MB
|Mirabella|Downlight|Genio Wifi RGBW|?|GPIO5: PWM1, GPIO4: PWM2, GPIO13: PWM3, GPIO14: PWM4, GPIO12: PWM5|?|https://mirabellagenio.net.au/|1MB
|Merkury|E27|A21 Smart Light Bulb 75W Color|MI-BW904-999W|GPIO4=CLK, GPIO5=PWM1 (warm White), GPIO13=ENABLE (color leds), GPIO14=DATA||-|?|1M QIO
|Merkury|E27|BR30 Smart Light Bulb  65W Tunable White LED|?|GPIO4 PWM1 GPIO5 PWM1 GPIO12 PWM2|-|?|?|
|Merkury|E26|A19 Smart Light Bulb 9W White Dimmable|MIC-BW902-999W|GPIO5=PWM1|US model number maybe MI-BW902-999WS|?|?
|Queo|E27|Fcmila Bulb|??|GPIO 4 PWM 5 = white GPIO 12 PWM 2 = green GPIO 13 PWM 3= blue GPIO 14 PWM 1  = red GPIO 2  PWM 4  to get slider (PWM 4 or 5 can be swapped seems same result)|Tasmota Generic 18|?|1M DOUT @ 40MHz
|Syska|B22|Smartlight Wi-fi Enabled Bulb|SSK-SMW-7W|Generic GPIO4=PWM1, GPIO5=PWM4, GPIO12=PWM2, GPIO14=PWM3 & GPIO15=PWM5(temperature)| Use Tasmota RGBWW config and [`SetOption17 1`](https://github.com/arendst/Sonoff-Tasmota/wiki/Commands#setoption17) & [`SetOption59 1`](https://github.com/arendst/Sonoff-Tasmota/wiki/Commands#setoption19) |N|1M QIO
|[Teckin SB50](https://www.amazon.ca/dp/B07KYJZ523/ref=twister_B07KD3W53F?_encoding=UTF8&psc=1)|E27|Smart LED Bulb|?|GPIO4: PWM4 (40), GPI12: PWM2 (38), GPI13: PWM3 (39), GPI14: PWM1 (37)|[Template](https://blakadder.github.io/templates/teckin-sb50.html)|?|1M DOUT @ 40MHz
|Torkase|E27|[Alexa WiFi Smart Light Bulbs Torkase 9W](https://www.amazon.co.uk/Torkase-Equivalent-2700K-6500K-Multi-Color-Compatible/dp/B07Q5SCW6W/)|?|GPIO5: Cold White, GPIO13: Warm White, GPIO4: Red, GPIO12: Green, GPIO14: Blue| |?|1M QIO @ 40MHz
|[EXTSUD](https://www.amazon.it/gp/product/B07FKQ7N9Q/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|E27|10W RGB Dimmerabile WiFi|?|?|AiLight 27 Profile|?|?
|Arilux|E14|WiFi Smart Bulb|YX-L01C-E4|GPIO4=Data, GPIO5=DCKI|Uses a MY9291 LED Driver. ch0=w, ch1=b, ch2=g, ch3=r, ESP8266EX|?|1M QIO
|Bomcosy/AOJA|E27|7W E27 RGB CW|?|GPIO4: PWM1, GPIO5: PWM4, GPIO12: PWM2, GPIO13: PWM5, GPIO14: PWM3|[Amazon.de](https://www.amazon.de/dp/B07DRGDP2T) [Amazon.co.uk](https://www.amazon.co.uk/dp/B07DRGDP2T) Template:{"NAME":"Generic", "GPIO":[0,0,0,0,37,40,0,0,38,41,39,0,0], "FLAG":1, "BASE":18}|?|1M QIO @ 40MHz
|[Swisstone SH 340](https://www.amazon.de/LED-Leuchtmittel-Multicolor-sprachsteuerbar-kompatibel-340/dp/B07G5X4F7F/ref=sr_1_1?__mk_de_DE=ÅMÅŽÕÑ&keywords=Swisstone+SH+340&qid=1573831830&sr=8-1)|E27|9 W E27 RGBW - 806 Lumen|?|GPIO4: SM16716 CLK (140); GPIO5: PWM1 (37); GPIO13: SM16716 PWR (142); GPIO14: SM16716 DAT (114); ADC0: Analog (1)|Based on SYF05 (69); Use the following template: {"NAME":"SH 340","GPIO":[0,0,0,0,140,37,0,0,0,142,141,0,0],"FLAG":1,"BASE":69}; some SH 340 bulbs does not use ESP8266 |?|? 
|Woox|E27|Smart LED Light Bulb RGBW|R4553|GPIO4: PWM Red, GPIO12: PWM Green, GPIO14: PWM Blue, GPIO5: PWM White|??|??|??

## Switches/Dimmers

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:|
|Costco/CE|CA|Smart Dimmer Switch|CE smart Home WF500D|GPIO13=Tuya RX, GPIO15=Tuya TX|use Tasmota Tuya Dimmer (54) |?|?
|Costco/CE|US|Smart Dimmer Switch|1248524|?|-|?|?
|Costco/Feit|US|Wi-Fi Smart Dimmer|ITM./ART. 1358969|GPIO3=Tuya RX, GPIO1=Tuya TX|use Tasmota Tuya Dimmer (54) |dimmer fnId=21 is set for dpId=2|?
|Martin Jerry|US|Smart Dimmer|?|?|-|?|?
|Gosund|US|120 Wi-Fi Smart Light Switch|KS-602S|GPIO0=Button1, GPIO1=Led1i(green), GPIO12=Relay1, GPIO14=Led2i(red)|Works with Tasmota Generic Module| |1M|
|[Kuled](https://www.amazon.com/gp/product/B079FDTG7T/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)|US|Smart Wifi Light Switch|KS-602S|GPIO0=Button1, GPIO12=Relay1, GPIO13=Led1|Use Tasmota Generic Module  NOTE: If you do not want LED on when switch is off, use Led1i for GPIO13  |?|1M QIO
|[Meamor](https://www.amazon.de/gp/product/B07F9YYB49)|EU|Smart Wall Switch 3 Gang|CD302|see Smart Life CD302 below|Works with Tasmota Generic Module|?|1M QIO
|Moes House|US|Smart Wall Switch 1-Gang|WF-WS01|GPIO3 = Button1, GPIO4 = Relay1, GPIO14 = Led1|Works with Tasmota Generic Module|?|1M|
|Moes House|US|Smart Light Switch 1-Gang|?|GPIO12 = Button1, GPIO13 = Relay1|Works with ESPhome|?|1M|
|Moes House|US|Smart Wall Switch 2-Gang|WF-WS02|GPIO2 = Led2, GPIO5 = Button2, GPIO12 = Button1, GPIO13 = Relay1, GPIO15 = Relay2, GPIO16 = Led1|Works with Tasmota Generic Module|?|1M|
|Moes House|US|Smart Wall Switch 3-Gang|WF-WS03|GPIO2 = Led3, GPIO3 = Button2, GPIO4 = Relay2, GPIO5 = Button3, GPIO12 = Button1, GPIO13 = Relay1, GPIO14 = Led2, GPIO15 = Relay3, GPIO16 = Led1|Works with Tasmota Generic Module|?|1M|
|Nova Digital|BR|Novadigital Interruptor Basic 1|MS101|GPIO4 = Led1i, GPIO12 = Relay1, GPIO13 = Button1 |?|?|?|
|SRL|AU|Smart Light Switch - 1 Gang|SRL 1WW|GPIO12: Button1, GPIO13: Relay1, GPIO14: Led1,|Works with Tasmota Generic Module|?|1M
|SRL|AU|Smart Light Switch - 2 Gang|SRL 2WW|GPIO12: Button1, GPIO13: Relay1, GPIO14: Led1, GPIO5: Button2, GPIO15: Relay2, GPIO16: Led2|Works with Tasmota Generic Module|?|1M
|SRL|AU|Smart Light Switch - 3 Gang|SRL 3WW|GPIO12: Button1, GPIO13: Relay1, GPIO14: Led1, GPIO5: Button2, GPIO15: Relay2, GPIO16: Led2, GPIO3: button3, GPIO4: relay3, GPIO??: Led3|Works with Tasmota Generic Module|?|1M
|SRL|AU|Smart Light Switch - 4 Gang|SRL 4WW|GPIO16: Button1, GPIO14: Relay1, GPIO??: Led1, GPIO3: Button2, GPIO4: Relay2, GPIO??: Led2, GPIO5: button3, GPIO5: relay3, GPIO??: Led3, GPIO12: button4, GPIO13: relay4, GPIO??: Led4|Works with Tasmota Generic Module|?|1M
|[Smart Life](https://www.aliexpress.com/item/All-compatible-Smart-WiFi-wall-switch-for-home-light-remote-control-Alexa-compatible-switch-for-intelligent/32947679016.html?spm=a2g0s.9042311.0.0.f6f24c4d2ei9cP)|EU|Smart Wall Switch 3 Gang|CD302|GPIO13=Relay1, GPIO3(RX)=Button1, GPIO14=Led1i, GPIO15=Relay2, GPIO12=Button2, GPIO16=Led2i, GPIO4=Relay3, GPIO5=Button3, GPIO1=Led3i, GPIO0=Led4 (Red)|Works with Tasmota Generic Module|?|1M QIO
|[TONBUX](https://www.amazon.com/gp/product/B07FFVG67H/)|US|Smart Light Switch|AMZ180648|?|Works with Tasmota Generic Module|?|1M QIO
|[GIRIER](https://www.aliexpress.com/item/4000242679288.html)|EU|Smart Light Switch - 2 Classic Gang|JR-EAK|GPIO0: LedLink(157), GPIO5: Button1(17), GPIO12: Button2(18), GPIO13: Relay1(21), GPIO14: Relay2(22), |Works with Tasmota Generic Module|?|2M
|[GIRIER](https://www.aliexpress.com/item/4000191335997.html)|EU|Smart Light Switch No Neutral- 2 Touch Gang|JRSWR-SEU01|GPIO4: Relay2(22), GPIO12: Button1(17), GPIO13: Relay1(21), GPIO14: Button2(18), GPIO16: LedLink(157), |Works with Tasmota Generic Module|?|2M


## Miscellaneous

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:|
|[Oittm](https://www.aliexpress.com/item/Oittm-USB-Smart-WiFi-LED-Mosquito-Killer-Light-Trap-Zapper-Works-with-Alexa-Google-Assistant/32879811540.html)|CN|Smart Mosquito Killer|MK-01|GPIO2=Button1, GPIO15=Led1i (Blue LED), GPIO5=Fan, GPIO12=UV LEDs, GPIO16=White LEDs|Tasmota Generic Module|no|1M QIO
|Auvisio|EU|Infrared Transceiver|[NX-4519-675](https://www.pearl.de/a-NX4519-3103.shtml?vid=675)|GPIO4=Led1,GPIO5=IRrecv,GPIO14=IRSend|Tasmota Generic Module|?|1M
|[SZMDLX IR Hub](https://www.amazon.com/SZMDLX-Universal-Compatible-Automation-Controlled/dp/B082R44LJM)|Global|Infrared Transceiver|?|GPIO4=Led1(green),GPIO5=IRrecv,GPIO13=Button,GPIO14=IRSend|Used Tasmota Generic to flash Esphome|no|?
|[Technical Pro](https://smile.amazon.com/Technical-Pro-Standing-Oscillating-Compatible/dp/B07RM6XQ4L)|US|WIFI Enabled 16 Inch Standing Fan|FXA16(W)|GPIO1=TuyaMCU TX, GPIO3=TuyaMCU RX||Yes|1M

## Battery-powered Sensors (**Note** Tasmota is not designed to run on battery powered devices. There is NO deep sleep)

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:
|Luminea|EU|WLAN-PIR-Bewegungsmelder|XMD-101.app|--|STM32 as 2nd MCU; Due to the 2nd MCU, this device is currently not supported by tasmota (06 March 2019) Update: the device has successfully been flashed - see [here](https://community.home-assistant.io/t/hkwl-ms03w-motion-sensor-with-tasmota/152421/20)for more details.|Y|1M QIO @ 40MHz|
|Luminea|EU|WLAN-Door/Window Sensor|NX-4470-675|--|?|?|?|

## Wifi Cameras

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:
|Akaso|EU|CS300|?|?|?|?|?|
## Related Pages

- [Compatible Devices Overview](Compatible-devices) - Main device compatibility page
- [Compatible Devices (HTTPS Firmware)](Compatible-devices-(HTTPS-firmware)) - Devices using HTTPS-based firmware
- [Troubleshooting](Troubleshooting) - Common issues and solutions
- [Installation Guide](Installation) - Get started with tuya-convert
- [Quick Start Guide](Quick-Start-Guide) - Quick reference for flashing devices

## External Resources

- [Tasmota Device Templates Repository](https://templates.blakadder.com/) - Community-maintained device templates
- [Tasmota Configuration Guide](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/) - Configure unknown devices
- [Tasmota Documentation](https://tasmota.github.io/docs/) - Complete Tasmota documentation

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
