The following devices are produced by Tuya and can be flashed with third-party firmware. It is recommended that you make a backup of the factory firmware in the event that you need to revert to it should the third-party firmware not function properly with your device.

Since [Tasmota](https://github.com/arendst/Tasmota) version 6.4.1.16, the firmware supports [templates](https://tasmota.github.io/docs/Templates/) for configuring unsupported devices. Templates are easily configurable using the web UI. It is recommended to use templates instead of changing `Generic Module (18)` GPIO assignments. [Tasmota Device Templates Repository](https://templates.blakadder.com/) maintains a list of templates for Tasmota as well as a list of unsupported devices (ones without an ESP82xx chip). There are numerous devices based on Tuya Wi-Fi modules. It may not be possible for all of them to work as expected with Tasmota. If you have a new device that does not have an existing template, you may refer to [Configure Unknown Device guide](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/) to configure the device.

## Sockets/Multi-sockets

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|Yes|Anoopsyche|EU|[AWP08L](https://blakadder.github.io/templates/anoopsyche_AWP08L.html)|GPIO 04: Button1. GPIO 05: LED1 inverted. GPIO 12: Relay1.|![AWP08L](https://images-na.ssl-images-amazon.com/images/I/61WY7viI5eL._AC_SL1500_.jpg)|16A 3680W. Ordered in July 2019 from Amazon. Attention: different GPIO-Layout than AWP08L plug sold in france.|
|Yes|AOFO|UK|[ZLD-44UK-W](https://templates.blakadder.com/aofo_power_strip.html)|0,56,0,17,23,24,0,0,22,21,33,0,0|![ZLD-44UK-W](https://i.imgur.com/Z1xgaQE.jpg)|Ordered in January 2020 from [Amazon](https://www.amazon.co.uk/gp/product/B07MZSH3CF).|
|Yes|Yagala|UK|[SWB3](https://templates.blakadder.com/yagala_SWB3.html)|0,0,53,0,0,23,0,0,21,0,22,24,0|![Yagala SWB3](https://images-na.ssl-images-amazon.com/images/I/511KSaQSxWL._AC_SL1001_.jpg)|Sep. 2020 [Amazon](https://www.amazon.co.uk/gp/product/B07R7H6RT5).|
|Yes|Aoycocr|US|[X5P](https://templates.blakadder.com/aoycocr_X5P.html)|56,0,57,0,0,0,0,0,0,17,0,21,0 / GPIO00:Led1i, GPIO02:Led2i, GPIO13:Button1, GPIO15:Relay1|![AoycocrX5P](https://images-na.ssl-images-amazon.com/images/I/5166t5gp8PL._AC_SL1100_.jpg)|Ordered Dec. 2019 from [Amazon](https://www.amazon.com/gp/product/B07N1JPPXK). There are several reports of incompatibility with devices ordered since Fall 2020.|
|Yes|AVATTO|EU|[JH-G01E](https://blakadder.github.io/templates/avatto_JH-G01E.html)|1:CSE7766Tx, 3:CSE7766Rx, 12:Button1, 13:Led1i, 14:Relay1|||
|No|AVATTO|EU|[Mini, NAS-WR01W](https://templates.blakadder.com/avatto_NAS-WR01W-10A.html)||![NAS-WR01W](https://ae01.alicdn.com/kf/Ha1109aad67eb4f01b5d9c49a0a59c5b8n.jpeg)|2020 Nov, First phase of autoconfig restarts socket, but intermediate firmware not loaded|
|Yes|Bakibo|EU|TP2201|||Use "Teckin" module|
|Yes|BlitzWolf|CN|[BW-SHP5](https://blakadder.github.io/templates/blitzwolf_SHP5.html)||![Blitzwolf - BW-SHP5](https://user-images.githubusercontent.com/10838968/66516356-202ef400-eae1-11e9-9e78-317727135a4b.jpg)||
|Yes|BlitzWolf|CN|[BW-SHP6](https://blakadder.github.io/templates/blitzwolf_SHP6.html)||![Blitzwolf - BW-SHP6](https://user-images.githubusercontent.com/10838968/66516357-20c78a80-eae1-11e9-944d-5f7c5f738189.jpg)||
|Yes|BlitzWolf|DE|[BW-SHP7](https://blakadder.github.io/templates/blitzwolf_SHP7.html)||![Blitzwolf - BW-SHP7](https://www.blitzwolf.com/bg_os/other/upload_temp/products/original/201908/1566443922_26.jpg)||
|Yes|BlitzWolf|DE|[BW-SHP10](https://templates.blakadder.com/blitzwolf_SHP10.html)||![Blitzwolf - BW-SHP10](https://templates.blakadder.com/assets/images/blitzwolf_SHP10.jpg)|D/C 4620 & 0521|
|No|BN-Link|US|[BNC-60](https://templates.blakadder.com/bn-link_bnc-60.html)||![BN-Link - BNC-60](https://images-na.ssl-images-amazon.com/images/I/31CZNuAeZaL._SY90_.jpg)|Units shipping from Amazon as of October 2020 are not flashable.  Manually flashing requires fullly desoldering the ESP8285 daughterboard. |
|Yes|Brilliant|AU|[Smart Wifi Plug and USB Charger 20676/05](https://templates.blakadder.com/brilliantsmart_20676.html)|5: Relay1, 13: Led1i, 14: Button1|![Brilliant Smart Wifi Plug with USB photo](https://i.ebayimg.com/images/g/HpQAAOSwf9Rc0haw/s-l640.jpg)||
|Yes|CE (Costco)|CA|[Wifi power bar LTS-6A-W5](https://blakadder.github.io/templates/ce_smart_home_LTS-6A-W5.html)|0: LED1i, 14: Relay1 (Left), 12: Relay2, 13: Relay3, 4: Relay4, 5: Relay5, 16: Button1i|||
|No|Dwfeng|US|[Amazon Wifi smart plug 2 packs](https://www.amazon.com/Switch-Compatible-Google-Control-DWFeng/dp/B07J4QK88D)|[GPIOs](https://github.com/superm1/esphome-devices/blob/master/images/tasmota.png)||Previously reported as working, but units purchased in December 2019 were based on Realtek chips, not ESPs|
|Yes|Gosund|EU|[SP1](https://blakadder.github.io/templates/gosund_SP1.html)||||
|Yes|Gosund|EU|[SP111](https://templates.blakadder.com/gosund_SP111.html)|56,0,57,0,0,134,0,0,131,17,132,21,0|![Gosund SP111](https://templates.blakadder.com/assets/images/gosund_SP111.jpg)|Original version with 2300W max|
|Yes|Gosund|EU|[SP111 v1.1](https://templates.blakadder.com/gosund_SP111_v1_1.html)|56,0,158,0,132,134,0,0,131,17,0,21,0|![Gosund SP111](https://templates.blakadder.com/assets/images/gosund_SP111.jpg)|"New" version of the SP111, 3450W max|
|?|Gosund|EU|[SP111 v1.4](https://templates.blakadder.com/gosund_SP111_v1_4.html)|57,255,56,255,0,134,0,0,131,17,132,21,0|![Gosund SP111](https://templates.blakadder.com/assets/images/gosund_SP111.jpg)|One more "new" version of the SP111, 3450W max|
|Yes|Gosund|UK|[UP111](https://templates.blakadder.com/gosund_UP111.html)|||Purchased from Amazon in November 2020, 2990W|
|No|Gosund|EU|[SP112](https://blakadder.github.io/templates/gosund_SP112.html)|||Previously reported as working but a July 2020 Amazon order came with a new firmware that prevents flashing via tuya-convert|
|Yes|Gosund|EU|[SP112](https://blakadder.github.io/templates/gosund_SP112.html)|||Date code 12/2020|
|**No**|Gosund|EU|SP112|||2022-11-13: Uses now another CPU (W701) which is not compatible with Tasmota|
|Yes|Generic|EU|[ebay Mini Smart Socket - RGBW, USB](https://blakadder.github.io/templates/mini-smart-socket.html)||![Mini Smart Socket](https://user-images.githubusercontent.com/13064701/69457976-996f6700-0d6e-11ea-82fa-60e97bd85634.png)|LED night-light with USB charging socket and 10A relay|
|No|Generic|UK|[Smart Plug with Energy Monitoring - G type plug](https://www.amazon.ae/gp/product/B07Y3YVWK3)||![Bad Type G Smart Plug](https://user-images.githubusercontent.com/35885181/69918118-62164f80-142b-11ea-8880-936cc6494536.jpg)|Purchased in UAE, Tuya-Convert failed with logs saying it isn't ESP82xx-based.|
|No|Kunova|CA|SWA5|Unknown||I opened one up to replace the fuse, it contains an ESP8266 LM2 module| 
|Yes*|LSC|EU|[Power Plug](https://blakadder.github.io/templates/lsc_smart_connect.html)|0,255,0,255,56,0,0,0,21,0,17,0,0|![LSC Smart Connect - Power Plug](https://user-images.githubusercontent.com/10838968/66515902-35efe980-eae0-11e9-9326-88b857db0b53.jpg)|The new versions do not have an ESP chip and are NOT supported!|
|Yes|Luminea|EU|[NX-4491](https://www.luminea.info/WLAN-Steckdose-fuer-Amazon-Alexa-und-Google-Home-1-NX-4491-919.shtml)|Configure by Template; 2: LED1i, 13: Button1, 15: Relay1||Sold by Pearl as "SF-450.avs"|
|Yes|Medion|AU|[Smart Plug S85225](https://blakadder.github.io/templates/medion_life_S85225.html)|3:Button1, 4:BL0937CF, 5:HLWBLCF1, 12:HLWBL SELi, 13: Led1i, 14: Relay1||
|Yes|Neo|EU|[Coolcam 16A](https://blakadder.github.io/templates/neocoolcam_16a_v2.html)|||
|No|Nooie|US|PA10|||UNSUPPORTED: Non-ESP chip (RTL8710BN)|
|No|Nous A1|EU|[Nous A1](https://templates.blakadder.com/nous_A1.html)||![](https://templates.blakadder.com/assets/images/nous_A1.jpg)|New version with non-ESP chip on the market. Ordered in May 2022 from [Amazon](https://www.amazon.de/-/en/gp/product/B0054PSES6/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1).|
|No*|Teckin|EU|[SP21](https://templates.blakadder.com/teckin_SP21.html)|||*New version with non-ESP chip on the market|
|Yes*|Teckin|EU|[SP22](https://blakadder.github.io/templates/teckin_SP22.html)|||*New version with non-ESP chip on the market|
|Yes|Teckin|UK|[SP23-2-D](https://blakadder.github.io/templates/teckin_SP23.html)||||
|Yes|Teckin|US|SS31|4:Led1i, 5:Led2i, 12:Relay1, 13:Button1, 14:Relay2,|![SS31 Outdoor Dual Plug](https://images-na.ssl-images-amazon.com/images/I/51GU2F3O1ZL._SL1001_.jpg)|[SS31 Template](https://templates.blakadder.com/teckin_SS42.html)|
|Yes|Teckin|EU|[SS42](https://templates.blakadder.com/teckin_SS42.html)||||
|No|Teckin|CA|SP10|||Not using ESP82XX, FW 1.0.3, Previous version has been seen with ESP|
|No*|Teckin|UK|SP27||![SP27](https://i.imgur.com/n0zLMU7.png)|Rapid flashes for a long time without Tuya-Convert. Rapid flashing stops, no progress, with Tuya-Convert. *Have not done a tear down to determine module.|
|Yes|Vivitar|US|HA-7001|0: LED1i, 4: Relay2i, 5: Button1, 12: Relay4i, 13: Relay3i, 14: Relay5i, 16: Relay1|![Vivitar HA-1007](http://www.vivitar.com/files_products/88/5a28a50356721aea258e15619a92fc47._1535476025.441.jpg)|
|No|ZooZee|EU|[SE131](https://blakadder.github.io/templates/zoozee_SE131.html)||Not using ESP82XX|
|No|Generic|CN|AWP08L-like|-|![AWP08L-like not ESP](https://images-na.ssl-images-amazon.com/images/I/5188D2hboyL._SX679_.jpg)|Similar as AWP08L from AliExpress (shop smartgorilla dropshipping Store). Failed as not using ESP chip. May be newer version.|
|Yes|Espressi|UK|TP24||![TP24](http://www.sowye.com/wp-content/uploads/2018/11/TP24.png)||
|No|rdxone|EU|LSPA9||![LSPA9](https://ae01.alicdn.com/kf/Ha58f94da37144de3b8c2533f4bdf3611f.jpg)|Not an ESP chip|

## Lights

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|Yes|Iotton|US|Iotton Smart Light Bulb|0,0,0,0,37,38,0,0,0,0,0,0,0|![](https://images-na.ssl-images-amazon.com/images/I/414vmIyC0eL._AC_SX679_.jpg)|Tasmota template: ``{"NAME":"Iotton Light","GPIO":[0,0,0,0,37,38,0,0,0,0,0,0,0],"FLAG":0,"BASE":18}``|
|No|Teckin|UK|SB50|255,255,255,255,37,255,255,255,38,40,39,255,255||Firmware sold after September 2020 not vulnerable, earlier firmware did work.|
|Yes|Bneta|ZA|A60/IO-WIFI-GU10|255,255,255,255,140,37,0,0,38,142,141,255,255|||
|Yes|Bneta|ZA|IO-WIFI60-E27P|255,255,255,255,37,41,255,255,38,40,39,255,255|||
|Yes|Feit|US|BPA800/RGBW/AG/2(P)|255,255,255,255,37,38,255,255,141,142,140,255,255||Used tuya-convert development branch from commit 69ea7d3d2604e00c195c615223085bba3dd605f4 [#6534](https://github.com/arendst/Sonoff-Tasmota/issues/6534#issuecomment-538788860)[Tasmota Template](https://blakadder.github.io/templates/feit_electric-BPA800RGBWAG2.html)|
|Yes|Generic|EU|darty Onearz Connect OECO_LB9WCCT|0,0,0,0,140,37,0,0,38,142,141,0,0|| [darty link](https://www.darty.com/nav/achat/telephonie/eclairage_domotique/ampoules_connectees/onearz_connect_oeco_lb9wcct.html)|
|Yes|Generic (also Avatar)|EU|RGBCW GU10|0,255,0,255,40,0,0,0,38,39,37,0,0|![Generic GU10 WiFi](https://user-images.githubusercontent.com/10838968/66516493-6ab07080-eae1-11e9-8c79-1109199fa56b.jpg)|Works before firmware 1.0.2, LEDs turn on full brightness when no PWM signal is given (power on), see [ebay link](https://www.ebay.com/itm/GU10-Wifi-Smart-LED-Light-Bulb-For-Amazon-Alexa-Google-Home-Remote-Control-F3d/254298981417) [amazon link](https://www.amazon.fr/gp/product/B082F7NWWB/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)|
|No|LOHAS|EU|Filament GU 10||![LOHAS Smart LED - Filament GU10](https://images-na.ssl-images-amazon.com/images/I/51WrHVi-f4L._AC_SL1200_.jpg)|X0013YZ1OP|
|Yes|LSC|EU|Filament E14|0,255,0,255,0,0,0,0,38,0,37,0,0|![LSC Smart Connect - Filament E14](https://user-images.githubusercontent.com/10838968/66515570-a1858700-eadf-11e9-884b-e085a64f6dd7.jpg)||
|Yes|LSC|EU|Filament M E27|0,255,0,255,0,0,0,0,38,0,37,0,0|![LSC Smart Connect - Filament E27 Normal](https://user-images.githubusercontent.com/10838968/66515403-608d7280-eadf-11e9-9e35-7c2b4ca85a6b.jpg)||
|Yes|LSC|EU|Filament L E27|0,255,0,255,0,0,0,0,38,0,37,0,0|![LSC Smart Connect - Filament E27 L](https://user-images.githubusercontent.com/10838968/66515571-a1858700-eadf-11e9-8fe6-533f4d320059.jpg)||
|Yes|LSC|EU|Filament XL E27|0,255,0,255,0,0,0,0,38,0,37,0,0|![LSC Smart Connect - Filament E27 XL](https://user-images.githubusercontent.com/10838968/66515572-a1858700-eadf-11e9-8543-ac65c5a57c30.jpg)||
|Yes|LSC|EU|Filament XXL E27|0,255,0,255,0,0,0,0,38,0,37,0,0|![LSC Smart Connect - Filament E27 XXL](https://user-images.githubusercontent.com/10838968/66515569-a1858700-eadf-11e9-8115-d173242a4927.jpg)||
|Yes|LSC|EU|RGBW E14|0,255,0,255,0,0,0,0,181,0,180,0,0|![LSC Smart Connect - RGBW E14](https://user-images.githubusercontent.com/10838968/66515904-35efe980-eae0-11e9-85ce-58d5f0744619.jpg)|See [#6495](https://github.com/arendst/Sonoff-Tasmota/issues/6495)|
|Yes|LSC|EU|RGBW GU10|0,255,0,255,0,0,0,0,181,0,180,0,0|![LSC Smart Connect - RGBW GU10](https://user-images.githubusercontent.com/10838968/66515897-35575300-eae0-11e9-8fa8-b19300a4548d.jpg)|See [#6495](https://github.com/arendst/Sonoff-Tasmota/issues/6495)|
|No|LSC|EU|W GU10|n/a|![LSC Smart Connect - W GU10](https://user-images.githubusercontent.com/10838968/88850828-303ccf00-d1ec-11ea-80c3-34f33a05adee.jpg)|Unknown|
|No|LSC|EU|RGBW E27|n/a|![LSC Smart Connect - RGBW E27](https://user-images.githubusercontent.com/10838968/66515905-35efe980-eae0-11e9-8e7e-231bb01dbcdd.jpg)|Contains RTL8710BN|
|No|LSC|EU|Ceiling Fixture W|n/a|![LSC Smart Connect - Ceiling Fixture W](https://user-images.githubusercontent.com/10838968/66515898-35575300-eae0-11e9-98d7-20472b266c99.jpg)|Contains RTL8710BN, but easily replaceable with ESP-12|
|No|LSC|EU|Ceiling Fixture RGBCCT|0,255,0,255,0,0,0,0,181,0,180,0,0|![LSC Smart Connect - Ceiling Fixture RGBCCT](https://user-images.githubusercontent.com/10838968/88850348-86f5d900-d1eb-11ea-94e6-d3ed715c4295.jpg)|Contains TYCL5 & SM2135|
|Yes|Teckin|EU|SP50 Smart RGB Bulb E27|||uses Protocol 2.2|
|Yes|Brilliant|EU|RGBW E14 HK17653S72|255,255,255,255,37,40,255,255,38,255,39,255,255|
|No|Twoon|US| XZ-190 |says not ESP chip in logs||[Amazon](https://www.amazon.com/dp/B07R9TWL38?ref=ppx_pop_mob_ap_share)|
|Yes|Novostella|US|HM-FL36-RGBCW-US-2/RGBCW|0,0,0,0,37,40,0,0,38,41,39,0,0|![Novostella 20W Flood Light](https://images-na.ssl-images-amazon.com/images/I/71JV5A3kSkL._AC_SL1500_.jpg)|[Tasmota Template](https://templates.blakadder.com/novostella_20W_flood.html) To enter pairing mode turn the device on, off, on, off, on|
|No|LUMIMAN|US|LM530||![LM530-4p-us](https://images-na.ssl-images-amazon.com/images/I/41U7q7dB1GL._SL500_AC_SS350_.jpg)|Flashing hangs after initial firmware uploads. Other folks mentioned progress [using this method](https://github.com/ct-Open-Source/tuya-convert/issues/343#issuecomment-546507831) on other devices, but I was not successful.|
|No|NiteBird|US|[TT-WB4](https://templates.blakadder.com/nitebird_TT-WB4.html)|0,0,0,0,40,0,0,0,37,38,39,0,0|![TT-WB4](https://m.media-amazon.com/images/S/aplus-media/sc/b70090ee-c12e-4454-9a59-02721cb27415.__CR0,0,600,600_PT0_SX300_V1___.jpg)|Ordered from [Amazon](https://www.amazon.com/gp/product/B07MTYVSSV).  Firmware sold after September 2020 not vulnerable, earlier firmware did work|
|NO!|Miboxer|Aliexpress|WL5|||Unsupported, based on WR3 RTL8710BN|
|Yes|Elari|RU|[SmartLED Filament E27](https://elari.net/en/catalog/smart-home/smartled-filament-e27/)|[0,0,0,0,0,0,0,0,56,0,46,0,0,0]|![SmartLED Filament E27](https://elari.net/upload/iblock/a8a/a8a1a26479b4edf0fccbe5b599658e72.png)|To enter pairing mode switch on and off 5 times|
|No|LVWIT|EU|GU10 RGB+CCT 5W 350lm|||firmware sold after Jun 2020 not vulnerable|
|No|LVWIT|EU|E14 RGB+CCT 5W 470lm|||firmware sold after Jun 2020 not vulnerable, earlier firmware did work|
|No|LVWIT|EU|E27 A60 RGB+CCT 8.5W 806lm|||firmware sold after Jun 2020 not vulnerable, earlier firmware did work|
|No|Brizlabs|EU|E14 RGB+WW 5W 350lm|||firmware sold after Jun 2020 not vulnerable, earlier firmware did work|
|No|LedLite|UK|GU10 RGB+WW 4W 300lm|||Issue logged: https://github.com/ct-Open-Source/tuya-convert/issues/817|
|No|AISIRER|EU|E27 RGB 10W 1000lm||![AISIRER](https://i.ibb.co/6v00mBb/aisirer.jpg)|Bought in Dec 2020, has WB3L chip, cannot disassemble without destroying|
|No|Anten|EU|LED Ceiling Floodlight RGB||![https://ibb.co/tQfGhbF](https://i.ibb.co/vV5FBJR/71-in2-Zxn-L-AC-SL1500.jpg)|Bought April 2021, firmware not vulnerable|


## LED Strips

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|Yes|LSC|EU|970750|51,255,255,255,37,255,255,255,38,40,39,255,255|![LSC Smart Connect - LED Strip](https://user-images.githubusercontent.com/10838968/66515900-35575300-eae0-11e9-8ca2-c74981e4994b.jpg)|[IR Rules](https://www.mikrocontroller.net/attachment/430330/rules.text)

## Switches/Dimmers

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|Yes|MoesHouse|CN|MS-105 (rev.2?)| GPIO01 = TuyaTX (107), GPIO03 = TuyaRX (108) |<img src="https://user-images.githubusercontent.com/13876030/70728594-ffae3080-1d01-11ea-8a5b-c7d5f25ae9ff.jpg" width="100px"/><img src="https://user-images.githubusercontent.com/13876030/70728853-6e8b8980-1d02-11ea-9a84-ad81d7b21922.jpg" width="100px"/><img src="https://user-images.githubusercontent.com/13876030/70728857-70554d00-1d02-11ea-81c3-2bece9bbf85c.jpg" width="100px"/>|This 1 Gang Dimmer looks different from most sources I could find.|
|Yes|Generic|UK|4 gang WiFi Switch (No Neutral)|TuyaMCU|![](https://ae01.alicdn.com/kf/Hb9612f2df6b74b63b1087256d8c46155Q/No-need-neutral-line-WIFI-Touch-Light-Wall-Switch-White-Glass-Panel-Blue-LED-EU.jpg)|Flash completed successfully, set up Tasmota in TuyaMCU mode
|Yes|Jinvoo|EU|Curtain WiFi Switch|52,0,0,10,22,11,0,0,9,21,0,23,0|| Issue this in console: SwitchMode 3 - Interlock 1 - LedPower 0 - SetOption31 1 - PulseTime1 130 (amount of seconds for curtain movement + 100 i.e. 30sec + 100 = 130) - PulseTime2 1 - Pulsetime3 130 (amount of seconds for curtain movement + 100 i.e. 30sec + 100 = 130) - SaveOption 1
|Yes|Jinvoo|EU|1 gang WiFi Switch|52,0,0,0,0,0,0,0,9,21,0,0,0|
|Yes|Jinvoo|EU|2 gang WiFi Switch|52,0,0,10,22,0,0,0,9,21,0,0,0|
|Yes|Jinvoo|EU|3 gang WiFi Switch|52,0,0,10,22,11,0,0,9,21,0,23,0|
|Yes|Whpuliao|EU|Bulb Socket|17,255,0,255,0,0,0,0,21,56,0,0,0|![](https://images-eu.ssl-images-amazon.com/images/I/41nLMwL3o5L._SY180_.jpg)|Module type: Slampher (9) tested successfully with tasmota 7.0.0.3
## Fans

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|No|Arlec|AU|Grid Connect 40cm SMART Pedestal Fan |||Does not use ESP82XX|
|Yes|Geek Aire|US|[Geek Aire Fan, Air Circulator](https://smile.amazon.com/Geek-Aire-Circulator-Oscillating-Compatible/dp/B082WBPWBF)||![](https://m.media-amazon.com/images/I/61lTSwYUTFL._AC_UL320_.jpg)|TuyaMCU
## Miscellaneous

|Success?|Vendor|Area|Device Name|GPIOs|Picture|Notes|
|--------|------|----|-----------|-----|-----|-----|
|No|LSC|EU|Siren|n/a|![LSC Smart Connect - Siren](https://user-images.githubusercontent.com/10838968/66516935-781a2a80-eae2-11e9-9643-b2357c816b70.jpg)|Contains RTL8710BN, but easily replaceable with ESP-12|
|Yes|LSC|EU|[Smart Movement Sensor (5 meters)](https://www.action.com/nl-nl/p/lsc-smart-connect-bewegingsmelder2/) V1.0|unknown||Flashing OTA works, but decouple the battery and power the board with 3.3V & GND to prevent deep sleep.
|Yes|Generic|EU|[Wi-Fi Smart IR Controller SRW-001 (I bought it from AliExpress)](http://google.com/#q=SRW-001)|The YTF IR Bridge Tasmota module works perfectly|![](https://ae01.alicdn.com/kf/H4bc997073d5c49c5a809706df9ebcf46n/TV-Universal-Remote-Control-14m-Smart-Life-IR-Wireless-Remote-Control-Voice-Alexa-Need-Write-Use.jpg_960x960.jpg)|Please make sure you upgrade the Tasmota firmware to [Tasmota-IR](https://github.com/arendst/Tasmota/wiki/Tasmota-IR)
|Yes|Moes/Beca|EU|MOES WiFi Smart Thermostat (BHT-002-GCLW) My variant was: 5A for boiler heating white|N/A|![](https://images-eu.ssl-images-amazon.com/images/I/41CYufQVMgL._SL500_AC_SS350_.jpg)|Use tuya-convert to flash this firmware: https://github.com/klausahrenberg/WThermostatBeca Tasmota will NOT work.
|No|Tuya|EU|TY01|n/a||TY01 Door Window Contact Sensor, offline after intermediate reboot|