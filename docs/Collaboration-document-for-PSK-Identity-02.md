Here we will share and organize our findings and data from [#483](https://github.com/ct-Open-Source/tuya-convert/issues/483)

### Please help edit this document!
Much of this was bulk copy-pasted and needs to be transformed into a useful form

# Does output in your smarthack-psk.log look like this?:
```
new client on port 443 from 10.42.42.25:3694
ID: 0242416f68626d6436614739314946523126e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
PSK: 2a9cf84b7a1b6bf1ede712edb7ee53c04b065f673e600f43627a67fea9a9d05d
could not establish sslpsk socket: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC] decryption failed or bad record mac (_ssl.c:1056)
```
If so, you are in the right place. This is where we aim to fix the issue with `ID: 02` and we need your help!

# The Goal
- Derive the PSK from the PSK identity or other known information, if that is even possible with the information we can obtain before a TLS connection is established.

## How can you help?
 1. Grab a pcap (see below)
 1. Compare to other pcap signatures in this wiki
 1. Flag if different

## Why this is hard?
The challenge of this issue is mapping known information (ie `gwId`) to the PSK (`pskKey`), which as mentioned before is indeed unique to every device. This is not possible to extract from the firmware, because to obtain the firmware would require we already know the PSK (or open the device at which point OTA becomes moot).

The previous implementation leaked information through the PSK ID (the MD5 of the `auzKey`), but this latest implementation uses already public information (the SHA256 of the `gwId`) as the PSK ID.

It may be that the `pskKey` is totally random and only stored on Tuya servers and the smart device. If this turns out to be the case, there is no solution to our challenge and this strategy of flashing firmware OTA is no longer viable.
§
> The `prod_idx` is used to compute the PSK identity. This is handed to the server by the client during the handshake, so it is not secret information.

> `prod_idx` is not secret information, it is the first part of the `gwId`. The `gwId` is what is being hashed here, which is `prod_idx` + `mac`.

> The point is that the previous implementation *did* leak secret information through the PSK identity, which we could use to compute the PSK. Now that it does not, our job is harder.

# Open questions
- How is pskKey used to decrypt identity 02 TLS sessions
- Where does pskKey get stored on devices that have been updated from pre-pskKey versions?
- What is with pskKey being 37 characters long? And why does it consist of a-zA-Z0-9 (like base64 but without '+' and '/')
  - If it's base62, then this would be a (16+12) 28-byte value, which are 224 bits. Maybe it's a SHA-224 hash?
- How can we encourage people to check back in this section for things to help with?
  - I would 1) suggest creating a discussion thread than is pinned, much like #483 was and posting any useful information that comes out of it here. 2) rather than pin issue #483, it would be better to pin a link directly to this wiki.  Maybe create a new issue that is closed/locked that only contains a link to this wiki if pinning the wiki itself isn't possible. 

# Findings (and comments that need to be edited into findings)
- firmware ESP8266 RTOS SDK version did not change, but the hash and build time did
  - versions before PSK change are:
    - `OS SDK ver: 2.0.0(898b733) compiled @ May 27 2019 18:49:04`
    - `OS SDK ver: 2.0.0(e8c5810) compiled @ Jan 25 2019 14:26:04`
  - versions after PSK change are:
    - `OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12`
      - interesting that this build date corresponds with the release of tuya-convert 2.0, coincidence?
    - `OS SDK ver: 2.1.1(317e50f) compiled @ Dec 10 2019 11:05:04`
    - `OS SDK ver: 2.1.1(8d30f72) compiled @ Jul 28 2020 12:33:05`
- Tuya version also is changed.
  - versions before PSK change are:
  - versions after PSK change are:
    - `tuya sdk compiled at Jan  4 2020 18:50:11` (oem_esp_plug)
    - `tuya sdk compiled at Mar  6 2020 20:27:48`
    - `tuya sdk compiled at Apr  8 2020 11:36:25` (oem_esp_switch)
    - `tuya sdk compiled at Apr  9 2020 02:33:43` (oem_esp_light_tuya)
    - `tuya sdk compiled at Apr  9 2020 04:37:24` (oem_esp_light)
    - `tuya sdk compiled at Apr 10 2020 14:44:10` (oem_esp_dltj)
    - `tuya sdk compiled at Apr 12 2020 09:45:06` (oem_esp_plug)
    - `tuya sdk compiled at Apr 13 2020 20:17:41` (oem_esp_light1_pwm_e2l_jbt_onoff)
    - `tuya sdk compiled at Mar 19 2020 17:08:43` (smart_lamp_test2)
- PSK ID begins with:
  - `01` tuya-convert handles these nicely
  - `02` This is the problem at hand
    - derivation:
      - '\x02' + 'BAohbmd6aG91IFR1' + sha256(gwId)
        - where gwId = prod_idx + mac_addr
          - where prod_idx is an 8 digit ASCII numeric identifier for that device model
          - where mac_addr is the lowercase hex representation of the device MAC address
        - where 'BAohbmd6aG91IFR1' is base64 of a chunk of "Hangzhou Tuya Information Technology Co." (base64(0x04,0x0a,"!ngzhou Tu"))
      - Example: 0242416f68626d6436614739314946523126e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
        - '\x02' + 'BAohbmd6aG91IFR1' is hex 0242416f68626d64366147393149465231
          - many smarthack-psk.log files have repeating f3 in this section; firmware bug?
        - sha256('81550705c82b9615a3f2') is hex 26e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
          - prod_idx = '81550705'
          - mac_addr = 'c82b9615a3f2'
  - `03` On OHLUX bulbs
    - is this device using certificate pinning?
- disabled most of the serial debugging output
  - unfortunate as this was a useful reverse engineering resource
  - system_uart_swap() is called, switching uart over to GPIO2 (at least for LSC devices). There, the debug output is still shown.
- did not respond to our `smartconfig` procedure
  - it may use a new mechanism or additional restrictions have been imposed
- MAC address in flash appears to be compared with actual device MAC
  - likely to foil reverse engineering attempts by running firmware on a dev board
  - this means that a given firmware backup will only run on the original device
  - MAC address is stored at several places in flash:
    - shuffled at 0x79060: the MAC address 11:22:33:44:55:66 is seen here as 55 44 00 B2 33 22 11 66
    - 0xFB000 in the json string
    - 0xFE484, this is a part of the boot- and network settings (0xFE000)
     - 0xFD484,which contains a copy of the boot- and network settings
       - the sector at 0xFE000 is identical to 0xFD000, except when settings are changed during the last session
- new factory written key found in flash, `"pskKey"`
  - the app never has access to the PSK, it is only used between the IoT device and the cloud
  - once written to flash it is never transmitted, period.
  - stored in JSON blob at 0xFB000
    - from factory only; updated devices do not have pskKey at 0xFB000
      - so where is pskKey stored on field updated devices?
  - this is indeed the PSK key, unencrypted
    - this means if you have a firmware backup you can use this to decrypt captures from the same device
    - since obtaining the firmware requires a working hack or physically opening the device, this doesn't help us for OTA purposes
  - the PSK key does not change with each new session
    - previously the PSK key changed each session, computed using the PSK ID (fixed) and PSK hint from the server (variable)
    - the previous implementation leaked information via the PSK ID while 02 does not
  - this may mean the encryption key will no longer be derived deterministically, big bummer
  - only found in @rsbob's backup, looks like @Farfar's was updated to this firmware and thus lacks this factory written key
    - this may mean there is still hope for devices that came with a lower firmware, since updating to this firmware would require fetching the key
    - this is a very interesting new endpoint: `tuya.device.uuid.pskkey.get`
      - if we can figure out the format of this call, we could try faking it and seeing what it returns after multiple calls
      - to do this, we'll need to capture network traffic from a device upgrading to this firmware from an older one without PSK 02
- The device can request the server downgrade to the old authentication, but the server cannot ask the device to downgrade
  - Since we emulate the server, the downgrade path doesn't help us.
- outside of updating a vulnerable device to the new firmware, the PSK never leaves Tuya's servers
  - Since this communication is encrypted by the highest version of the encryption scheme that the device supports, this isn't too helpful. Currently we can only decrypt that communication if the device is on the old firmware or we have a firmware dumps from that particular device.
- the PSK is unique to each device, not shared among an entire model
- there is currently unused code for what I think is certificate pinning in the Tuya SDK (the one on the device)
  - why do they use PSK, why not do the certificate pinning to the cloud?
    - likely answer is that the public key cryptography necessary to validate a certificate or chain is too slow on the ESP8266
- the server cannot tell Tuya devices to turn off encryption
  - The devices will reject any connection not secured with the TLS_PSK_WITH_AES_128_CBC_SHA256 cipher suite.
- The alphabet for both auz_key and pskKey seem to be (a-z, A-Z, 0-9)
  - We know that is it likely not base64, as we have plenty of samples and no instances of the `+/` characters
  - It is possible that it is base62, but it seems more likely that this is a random string generated at the factory and stored only on the device and the cloud.
    - That would lead me to the guess, that they are not the result of any computation (like hashing the mac_addr or the like), because converting the binary result of such a computation into the above format is not straight forward.
    - If it's base62, then this would be a (2*8) 24-byte value, which are 192 bits. Maybe it's an AES key?
  - Does anybody have an idea, why the length of the pskKey is 37? That sounds rather random.

## Procedures

### Decrypting network captures with known PSK

```
tshark -o "ssl.psk:3ce2b65bc30c7d91bf2e50884a49f6ddc77a8c44b991a1120b298ab846e97704" -z follow,ssl,ascii,9 -r gosund-upgrade.pcap -Y null
```
This assumes you:
- want to look at stream number 9
- are reading gosund-upgrade.pcap, found below as #34
- will replace 3ce2b65bc30c7d91bf2e50884a49f6ddc77a8c44b991a1120b298ab846e97704 with the actual psk if you want to look at a different pcap or stream using a different hint
  - see psk-frontend.py for how to calculate psk when looking at streams using identity 01

### Creating network captures and firmware backups

1. Install `create_ap`
```
git clone https://github.com/oblique/create_ap
cd create_ap
sudo make install
cd ..
```
2. Setup a pass-through AP (assuming your interface is `wlan0`)
```
sudo create_ap wlan0 wlan0 MyAccessPoint MyPassPhrase
```
3. Start recording
```
tcpdump -i wlan0 -w capture.pcap
```
4. Connect your phone to `MyAccessPoint` (or whatever you decide to call it)
5. Use the app (SmartLife or vendor branded app) to pair the device
6. Wait for registration to complete
7. Disconnect the device
8. Go back to `tcpdump` and press `Ctrl` + `C`
9. Disassemble the device and connect to the serial port of the ESP
10. Download the firmware using [`esptool`](https://github.com/espressif/esptool)
```
esptool.py read_flash 0 0x100000 firmware.bin
```
11. Upload both `capture.pcap` and `firmware.bin`

#### Experiment:

The question here is how are devices with old firmware being integrated into Tuya's newer security scheme, which can help us understand how these new PSKs are created.

- It may be when a device is first updated through the app, that the new randomly generated PSK is linked to the device MAC (or other device identifier), and that same PSK is issued again after downgrading and updating
  - we could potentially obtain the PSK by faking the API call to the cloud, however this strategy would likely be patched against quickly
- Or a random PSK is generated each time
  - this would be bad

##### Requirements:

- Tuya device with
  - old firmware that works with TuyaConvert, or
  - a converted device with the original backup for that device (MAC address **must** match)
- firmware upgrade available for that device model in the Tuya app
  - Confirmed that it is possible to get the new PSK firmware through the app, but not guaranteed to be there for all devices
  - Teckin SB50 firmware was upgraded through Tuya app to new PSK firmware
  - Powertech SL225X sold with new PSK firmware, but no firmware update available in Tuya app for SL225x devices with old firmware
- ability to open the device and serial flash it

##### Steps:

1) take a device with pre-patched Tuya firmware and back it up
2) step up network capture via WireShark or tcpdump
3) register the device to the app and get the updated patched firmware
4) backup the new firmware to determine the new PSK
5) flash the device back to the pre-patched firmware
6) register the device again to the Tuya app to get the patched firmware
7) backup the new firmware, extract the PSK and determine if it matches the PSK from step 3)
8) share your findings here!

##### Issues:
Several attempts have been made to follow the steps above (see files 10 and 34 in the Firmware table above). It seems that devices which ship with PSK ID 01 firmware and then are updated to firmware which uses PSK ID 02, do not store the pskKey at 0xfb000 as expected. So this experiment is stalled until we can find where pskKey is being stored on these devices, if at all. It is not found in the same 37 character base64-ish format.

# Data

## Known Affected Devices
- AIMASON BSD34 Smart WLAN Plug (4 Pack, Amazon - March 2021)
- AISIRER WiFi Smart Bulb 10W RGBCW (4 pack, Amazon - December 2020)
- Aoycocr U2S (4 pack, Amazon - December 03, 2020)
- Aoycocr U3S (4 pack, Amazon - October 13, 2020)
- Aoycocr X5P Ordered from (4 pack Amazon US November 23, 2020, FCC ID 2AKBP-X5)
- Aoycocr X10S Ordered from Amazon April 21, 2020 (FCC ID 2AKBP-X10S)
- Amico Smart LED Recessed Lighting ‎DC08-DR6-12W120-CCT+W5 (August 2023)
- Amzdest C168 Outdoor Plug (Amazon 1 OCT 2020)
- AL Above Lights 810lm
- Anko HEGSM40 Fan (Kmart December 2020)
- AOFO Smart Power Strip (ZLD-44EU-W)
- Arlec GLD060HA lamp
- Arlec GLD064HA E14 Bulb (November 2020)
- Arlec GLD120HA (Bunnings September 2020)
- Arlec GLD112HA (Bunnings May 2021)
- Arlec GLD081HA (Bunnings October 2020)
- Arlec PC190HA
- Arlec PC389HA
- Arlec PC399HA
- AHRise AHR-083 Power Strip
- AHRise AHR-085 Power Strip (Amazon, Oct 24 2020)
- Aubees smart plug 10-240V european plug. wireless version 2.4 GHz
- Avatar Mini Smart Socket AWP14H (4 pack, Amazon - October 16, 2020) - note: board is marked HYS-U1S-SOCKET-V1.3 2018-09-21.
- AWOW EU3S smart socket
- Avatto NAS-WR01W 10 Amps / 2300 Watt smart socket
- Avatto NAS-WR01W 16 Amps / 3680 Watt smart socket
- Bearware WDP 303899 / 20200422WZ001 (/20190809WZ001 is working!) (Amazon, Nov. 17 2020)
- BAC-002ALW (unbranded) fan coil thermostat (H33711B-2) (Aliexpress, Oct 06 2020)
- Bakibo TB95
- Bakibo TP22Y
- BENEXMART Wifi Tuya WiFi Roller Shade Driver 
- BHT-002-GALW (Decdeal, Moes, MoesGo, etc.) room thermostat (ordered Oct 15, 2020 over Amazon - Moes Go)
- BHT-002GBLW room thermostat (ordered Sept 16, 2020)
- BHT-3000GBLW room thermostat (ordered Sept 28, 2020)
- Blitzwolf BW-LT11
- Blitzwolf BW-LT20
- Blitzwolf BW-LT29
- Blitzwolf BW-SHP8
- Blitzwolf BW-SHP11 (ordered via banggood 5th nov, 2020)
- BNETA IoT Smart WiFi LED Bulb+ (IO-WIFI60-E27P)
- BNETA IoT Smart WiFi Plug WITH POWER METER IO-WiFi-PlugSA (ordered via Takealot oct, 2022)
- BN-Link BNC-60 (ordered Amazon Sept 6, 2020)
- BN-Link Smart Wall Socket KS-604S (w/ USB, Amazon purchase April 2021)
- Brennenstuhl Ecolor 3AC (ordered at Amazon NL on Nov 21, 2022)
- BSD33 smart socket (ordered at Aliexpress on Dec 21, 2020)
- BSD34 smart socket
- [Calex Multi Color Floor Lamp](https://www.calex.eu/en/products/product/CALEX-SMARTVLOERLAMP/) 
- [Calex Smart RGB Reflector](https://www.calex.eu/en/product/LEDREFGU10-5W-2200-4000SMD-RGBSMART/)
- Connect SmartHome CCT Downlight
- Deltaco SH-LE27W (Post-ESP8266: ESP8285 TYWE2L)
- Deltaco SH-LE27RGB (More recent units (at least since 2020 summer?) have new PSK. ESP8285 on Tuya TYWE2L)
- Deltaco SH-LFE27G125 G125 golden globe with CCT
- Deltaco SH-OP01
- Deltaco SH-P01
- Deltaco SH-P01E
- Deltaco SH-LGU10W
- [DENVER SHP-100](https://denver-electronics.com/products/smart-home-security/smart-plugs/denver-shp-100/c-1024/c-1292/p-3820) Smart home power plug
- [DENVER PLO-109](https://denver.eu/products/smart-home-security/smart-plugs/denver-plo-109/c-1024/c-1292/p-4135) Smart home power plug
- DETA Quad Smart Switch (6904HA)
- DETA Smart Downlight (DET902HA)
- DETA Triple Smart Switch
- Dogain E12 (packaging says GDT-smart bulb Q5-4) (Amazon Nov 20, 2020)
- Eachen WiFi-IR Universal Remote (SANT-IR-01)
- eLinkSmart BSD29 (packaging says Smart Plug eLinkSmart 16A - Amazon Nov 20, 2020)
- EKAZA EKNX-T005 (same product as NX-SM400) (Mercado Livre / Nova Digital - Jan 2021 2 pack)
- Etersky WF-CS01 Curtain Switch
- Etersky Wifi Smart Bulb (LDS-WF-A60-9W-E27-RGB) (Amazon Dec 2020, 2 pack)
- Esicoo Wifi Smart Plug (US package listes device model is 'YX-WS01', Amazon US May 2021, 4 pack) Suspect RelTek IC Not ESP8266 IC based
- FCMILA Smart Bulb RGBW
- Feit Smart Wifi Bulb
- Feit OM100/RGBW/CA/AG (fccid: SYW-A21RGBWAGT2R - non R versions seem to be unaffected)
- Feit OM100/RGBW/CA/AG(C) (Amazon purchase in Oct 2021, `TYWE3L` module, OS SDK: `2.1.1(317e50f)`, Tuya SDK: `Apr 13 2020 10:28:31`, firmware info name: `oem_esp_light_v1_tuya version:1.1.1`, FCC ID `SYW-A12RGBWAGT2R`)
- Feit Smart Dimmer
- Feit Smart Plug (SYW-PLUGWIFIG2)
- Fitop Smart Bulb E27
- Freecube Smart Bulb E14 5W (amazon.co.uk Dec 2020)
- GD.Home LED Floor Lamp (Anten, Amazon Jan 2021)
- Geeni Prisma 10W 1050lm RGBCCT Bulb 
  - 17 Dec 20 - Latest firmware for GN-BW94-999 is 1.0.3.  Unable to use latest Tuya-Convert from development branch - #54277bcf.  Bulb connects to vtrust AP but that's it.  Nothing in the logs of any use).
- Girier 16A Power Monitoring Plug (JR-PM01)
- Globe Smart Ambient Light (Amazon May 2022)
- Globe Smart Bulb [3.0] (A19, E26 Medium Base, RGB, 2000k - 5000k, 60W, 800 lumens. From Costco Canada)
- GoKlug WIFI Light Switch (Amazon, Jan 2021, GoKlug logo on front), but can be opened & flashed directly
- Gosund 800l bulb
- Gosund EP2 (2500W, sucessor of SP111 Plug - now glued and soldered, ESP8285. Amazon, Oct 2020)
- Gosund SP 1 (new PSK: Amazon, Nov. 2020, 4 Pack)
- Gosund SP 112
- Gosund SW 1 (1-way switch; new PSK: Amazon, Dec. 2020, 4 pack)
- Gosund SW2 1-way Dimmer Smart Switch
- Gosund SW6 3-way Smart Switch (ESP8285-based as of Amazon Dec 2020 purchase)
- Gosund WB4 bulb
- Gosund WB5 bulb
- Gosund WP2 socket (new PSK: Amazon 2021-06-10 (2-pack, ASIN B07F58N32V); ESP8266EX; mfg. date on device: 02/2021; prod_idx 34751287)
- Gosund WP3 socket (old PSK: Amazon 2020-08-26; new PSK: Amazon 2020-10-20)
- Gosund WP5 socket (Amazon, October 8, 2020)
- Gosund WP6 socket (Amazon, December 31, 2020)
- Halonix Prime Prizm 12W RGB Bulb(Amazon.in, October 28, 2020)
- Hama 10W 1050lm RGBW E27 Bulb (Amazon, October 2020)
- Hama Outdoor WiFi socket 176570
- HBN Outdoor Smart WiFi Plug U151T (Amazon, December 2020)
- Hiking DDS238-2 Wifi - Smart Meter with relay
- Hombli Smart Socket power plug - HBPP-0204
- iiglo Wi-Fi Smart Power Strip – IISMART0003 (Komplett, November 2020, SKU:1174244) (Shows up with ESP_xxxxxx in the DHCP lease, returns PSK 02)
- Jasco Enbrighten Smart Plug, model WFD4105E
- Jinvoo SM-AW713 Valve
- Jinvoo SM-PW713
- KHSUIN A19 E26 RGBCW 7w 800lm bulb (Amazon, June 2020)
- Klas Remo SWA11
- Kogan KASMCDSKTLA 1.7L Smart Kettle
- Kogan SmarterHome Smart Plug with Energy Meter [KASPEMHA, KASPEMHUSBA] (Kogan, June 2020, but by Oct 2021, KASPEMHA now WB2S, incompatible with tasmota)
- Kogan KAB22RGBC1A Smart Bulb (B22) 10W 806LM
- LangPlus+ 40W 3500LM Smart Outdoor Floodlight (Amazon, 16 APR 2021)
- Legelight Smart Light Bulb (2pack - 7W 650LM - E26)
- Lenovo SE-241EB Smart Bulb (Mfg Date: 20/9/9)
- [Lexi Lighting APT01](https://www.lexilighting.com.au/products/wifi-tuya-app-control-adaptor)
- LOHAS E14 bulb
- LOHAS Candelabra LED Bulb E12 Base
- LOHAS RGBCW GU10 Bulb
- Lonsonho X801A-L Light Switch (No neutral)
- Loratap sc500w curtain switch
- Loratap SC511WSC Curtain switch module with remote
- [LSC Filament E27 Dimmable Bulb](https://www.action.com/nl-nl/p/lsc-smart-connect-slimme-filament-ledlamp2/)
- [LSC Filament C35/E14 Dimmable Bulb](https://www.action.com/nl-nl/p/lsc-smart-connect-slimme-filament-ledlamp3/)
- [LSC Garden Spots](https://shop.action.com/nl-nl/p/8712879154488/lsc-smart-connect-tuinspots/)
- Lumary Downlights 18W (Amazon ES, 15 Apr 2022) comes with WB2S, incompatible with tasmota)
- Luminea NX-4491-675 (from Pearl)
- Luminea ZX-2820-675 Smartmeter Plug (from Pearl)
- LUMIMAN ‎LM530-4P-US
- ‎LUMIMAN LM650-2P-CA
- LVWIT A70-3 WIFI DIM+CCT+RGB 12W E27 X-Y X0014O0801 LED Bulb 4pack (Amazon, December 2020)
- Maxcio YX-L01C-E14
- Maxcio YX-L01C-E27
- Merkury MI-BW320-999W Light bulb
- Merkury MI-BW944-999W 11W 1050LM Light Bulb
- Merkury MI-EW003-999W LED Light strip
- Merkury MI-EW010-999W LED Light strip
- Merkury MI-OW101 (DR-1703) Outdoor smart plug
- Minoston MP22W Outdoor Plug
- Milfra Smart Module TB41
- Mirabella Genio 5W 450lm Candle RGBCCT Bulb (E14) (Kmart, May 2021)
- Mirabella Genio 9W 800lm RGBW Bulb (B22) - (I002608, Coles 10 Dec 2020; Note: "Sale" (AU) units bought from Coles 20 Sep 2020 and KMart approx Oct 2020 both PSK 01)
- Mirabella Genio 9W LED Wi-Fi Dimmable Downlight - I002741
- Mirabella Genio Christmas Wi-Fi 200 LED Colour Wheel Icicle Lights (Big W, 14 Nov 2020)
- Mirabella Genio 5W LED Wi-Fi Dimmable Downlight - I002943
- Mirabella Genio Smart IR Controller (Kmart, 18 Dec 2020)
- MoesHouse Smart Downlight
- Moes WS-US1-W 1 Gang
- Moes Wi-Fi Smart Wall Socket KS-604S (w/ USB, Amazon purchase April 2021)
- NEO Coolcam NAS-WR01W
- Nedis Wi-Fi Smart Plug WIFIP110FWT
- Nedis Wi-Fi Smart Plug WIFIP130FWT
- Nedis Wi-Fi Smart Outdoor Plug WIFIPO120FWT (November 25 2020)
- Nedis Wi-Fi Smart Bulb WIFILT10GDA60 (December 2020)
- Nedis Wi-Fi Smart Bulb WIFILW13WT (May 2021)
- Nedis Wi-Fi Smart Extension Socket WIFIP311FWT (Dec 2021)
- Nedis Wi-Fi Smoke Detector WIFIDS10WT (Dec 2021)
- Nedis Wi-Fi Remote Control WIFIRC10CBK (Sep 2024)
- Nexxt Home Smart Wi-FI LED NHB-W110 (June 9, 2023)
- NOUS Smart WIFI Socket A1 "NOUS A1" (4 pack, Amazon.de, Feb 2022)
- Novostella 20w Smart LED Floodlight
- Novostella 13W Smart LED Light Bulbs RGBCW (Model: `UT55509`, Amazon purchase in Oct 2021, `TYWE3L` module, OS SDK: `2.1.1(317e50f)`, Tuya SDK: `Apr 9 2020 04:37:24`, firmware info name: `oem_esp_light version:1.6.1`)
- NX-SM112
- NX-SM400
- OHLUX Smart WiFi LED (ASIN B08CL2CKW3, OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12)
- OHLUX 40W 4000LM Smart Outdoor Flood Lights (ASIN B083TZFB29)
- Olafus 10W WiFi LED (2 pack, Amazon.it, Mar 2022, Model: E10WIFI, SKU LA-E10-78FDRGBW-EU02)
- Polux WI-FI SMART LED, 400lm, 5,5W, GU10 (GU10SMDWWCW+RBG) (Model: MK-010011001067, Series: SE2006MK-1)
- Polux WI-FI SMART LED, 400lm, 5,5W, E12 (E12SMDWWCW+RBG) (Model: MK-010052019005, Series: SE2004MK-1)
- Polux WI-FI SMART LED, 1055lm, 13W, E27 (E27SMDWWCW+RBG) (Model: MK-010112048001, Series: SE2006MK-1)
- Polux Wi-Fi SMART LED Strip RGB+NW 4000K 2m, 540lm, 6,5W, (Model: CL-5050RGB2835WWaaaHYbb-Wcc-WiFi, Series: SE20006CL-1)
- Powertech SL225X (firmware V3.3.16 TC compatible, V3.3.30 new PSK)
- Prime WiFi SmartOutlet Outdoor (Date Code: 08/20, from Costco.ca)
- QS-WIFI-S03 Module Switch
- SANA SW02-02 Smart Switch
- SHENZHEN LONG SI PU TECHNOLOGY LIMITED FCCID: 2AV9Z-LSPA6, tuya product: jorlvalcdf5lz6qa, [FCCID](https://fccid.io/2AV9Z-LSPA6)
- Sinotimer TM608 Smart Timer & Meter (from 09-2021)
- SmartPoint Smart WIFI Universal Remote Control SPCNTRL-WM (Walmart)
- SMRTLite (Costco) LED Panel Light DS18901
- Spectrum SMART GLS LED lamp, 5W COG E-27 Wi-Fi CCT DIMM Milky
- Spectrum SMART 2 LED lamp, 5W E-14 Wi-Fi CCT DIMM (WOJ14414, 1322050)
- Stirling Black Premium Fan Tower with Wi-Fi (TF4601TR-S) (Aldi)
- Stitch Wireless Smart Power Strip (Monoprice.com, Oct 26 2020, P/N 34082)
- Sunco G25 RGBW Smart Bulb
- Sunco PAR38 WIFI LED SMART (PAR38_S-13W-27K_5K-2PK)
- SRL Glass Wallplate Touch Switches (all gang combos) https://srltech.com.au/portfolio_page/one-gang-series/
- Swisstone SH 320 (ordered from condrad.cz)
- TCP Smart 13A Plug (WISSINWUK)
- Teckin SB50 (firmware V1.61 new PSK, was previously TC compatible until firmware update through Tuya app).
- Teckin SB53 (some of them, even BNIB never updated)
- Teckin SS31 Outdoor smart outlet
- Teckin SS42 Outdoor smart outlet
- Teckin SR40 Wi-Fi Smart Wall Socket (Amazon Jan 2021)
- Tellur TLL331031 (emag.ro, Jan 2021)
- TopGreener TGWF15RM smart outlet with Energy Monitor  (4 pack, purchased Amazon Nov 2020)
- TopGreener TGWF115PQM [4-Pack, Amazon Nov 2024]
- Treatlife A19 8W 650lm RGBCCT Bulb
- Treatlife Ceiling Fan & Light Dimmer Switch DS03
- TreatLife Smart Dimmer Switch DS01C
- Treatlife Smart Dimmer Switch DS02S
- TreatLife Smart Plug-in Dimmer DP10
- TreatLife SS01S (4 pack, purchased on Amazon Nov 2020)
- Treatlife SS01 3-Way Switch
- Treatlife SS02S Single Pole Switch
- UCOMEN Outdoor Sockets PA-GEBA-01SWP2
- UFO-R1 / SRW-001 Smart Wifi Infrared Controller (tested version is labeled by MOES)
- Ultra Link UL-P01W (Takealot, 26 November 2020)
- Veargree Smart Timer ATMS1601
- WiFi Smart Power Strip 4 AC - SA-P402A (Zeoota)
- Wipro Garnet 9W RGBCCT Bulb
- Wipro Smart Extension DSE2150
- Wipro Smart Plug 16A
- Wofea Smart Garage Controller WG-088
- Woox r5024 (pack of 4 bought on ibood in june 2020)
- Zebronics ZEB-SP116
- Zemismart 4 inch 10W Wifi RGBW
- Zemismart 6 inch 14W WiFi RGBCW
- Zemismart Curtain Motor ZM79E-DT WiFi [here](https://www.zemismart.com/products/smart-curtain-customized-electric-curtain-motor-with-tracket-rf-remote-broadlink-control)
- Zemismart WiFi Roller Shutter [YH002](https://www.zemismart.com/products/zemismart-tuya-wifi-roller-shade-driver-diy-roller-yh002)
- Zeoota ZLD-44EU-W - WiFi Smart Power Strip

## Firmware
🔢 | pcap | SDK_ver_A | SDK_ver_B | mac | mac_addr | prod_idx | auz_key | pskKey
-- | ---- | --------- | --------- | --- | -------- | -------- | ------- | ------
 [1](https://github.com/ct-Open-Source/tuya-convert/files/4021684/BSD34--image1M.zip) |  | 🔴29f7e05 |  |  | c44f33bc1794 | 65046664 | tKzPU69mMe3ns8PmA5M2cAuUUDOtrTeA | yhULg57DUA3Uo1xTP5xhoI0C1kRpWQOwqjMO8
 [2](https://github.com/ct-Open-Source/tuya-convert/files/4052386/Deltaco_SH-P01E_20200110_image1M.zip) |  | 🟢e8c5810 | 🟡29f7e05 | 5e1 |  | 84067851 | iyTIVyDnqiMiMfzWf5KZZsZIcn7gfvMI | 
 [3](https://github.com/ct-Open-Source/tuya-convert/files/4287008/moeshouse_downlight_1m.zip) |  | 🔴29f7e05 |  |  | 98f4abc96ac3 | 06402221 | Yw0VAIvFe3aWlvdKEZfmBPg8xfQ3Jg4Q | kPJ6yZaAbTUqlk5fHrCN6DyWY2Flz9LLI49un
 [4](https://github.com/ct-Open-Source/tuya-convert/files/4303944/BSD29_firmware_1M.zip) |  | 🔴29f7e05 |  |  | d8f15bd5c898 | 83203175 | JQ1YB6PV5AHHLttPZwkKDs9plRFSWpoY | x8rMeGHKE4KVEQiNyUUSyvWxc561vIIN82PMt
 [5](https://github.com/ct-Open-Source/tuya-convert/files/4338606/module1.zip) | ✅ | 🔴29f7e05 |  |  | 2462ab3989fe | 08488420 | diI5mLzLQx5GBNCQQZsZ8J0dQLYMaAeT | Z9ir6z2hsTlRVJKwEZyqpfyIzfLyzkMBkwyGd
 [6b](https://github.com/ct-Open-Source/tuya-convert/files/4360647/tuya_pairing.zip#before4.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [6a](https://github.com/ct-Open-Source/tuya-convert/files/4360647/tuya_pairing.zip#after4.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [7b2](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before2.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ac8 | 06402221 | dhDirFfJylXSWmkpdXUhcVlY5XK97YtW | sLPbe7MDpYMdaQzEYID8gX3flbuUuUHxmQ3Mz
 [7a2](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after2.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ac8 | 06402221 | dhDirFfJylXSWmkpdXUhcVlY5XK97YtW | sLPbe7MDpYMdaQzEYID8gX3flbuUuUHxmQ3Mz
 [7b3](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before3.bin) |  | 🔴29f7e05 |  |  | 98f4abc96bde | 06402221 | lpb6dZ9qFwE4beS6SYepUQtPAUOdBmlI | f0xlg6wbkihLXju2ZVaXmbwJlf2qzsGvxBlqX
 [7a3](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after3.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96bde | 06402221 | lpb6dZ9qFwE4beS6SYepUQtPAUOdBmlI | f0xlg6wbkihLXju2ZVaXmbwJlf2qzsGvxBlqX
 [7b4](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before4.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [7a4](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after4.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [8](https://github.com/ct-Open-Source/tuya-convert/files/4732853/AOFO_ZLD-44EU-W_20200604_image1M.bin.gz) |  | 🔴29f7e05 |  |  | 600194facb50 | 02063503 | oDg2MkXuvbyxqNEp1Uz1myBAyQarmnUf | 6CJRAyEyBuUzueuVBCItKRnQMfOJhdBWm4BvO
 [9](https://github.com/ct-Open-Source/tuya-convert/files/4732914/firmware-backup.zip) |  | 🔴29f7e05 |  |  | 500291e8f141 | 26636676 | wg7xdxUcsi7W0EmnPUlEtuwoyZwcF2W2 | GUKgTWzsxGCn8UR5tIFFluuKD2qA8FYmaZwY2
[10b](https://github.com/ct-Open-Source/tuya-convert/files/4743192/gosund_sp112_capture.zip#gosund_sp112_firmware_orig.bin) |  | 🟢e8c5810 | 🟡29f7e05 | b60 |  | 10801581 | qxm7SD7sgStYPZUBfIjlUgtDVAN6AoGP | 
[10a](https://github.com/ct-Open-Source/tuya-convert/files/4743192/gosund_sp112_capture.zip#fw_after_onboarding_1.bin.bin) | ✅ | 🟢e8c5810 | 🟡29f7e05 | b60 |  | 10801581 | qxm7SD7sgStYPZUBfIjlUgtDVAN6AoGP | 
[11](https://github.com/ct-Open-Source/tuya-convert/files/4755710/Merkaryv3.3.zip) |  | 🟡29f7e05 |  |  | c44f33b5ed3e | 22885450 | fMFu4XqaRa8f1HLzI9QDm7DJXSdGqJzf | 
[12b](https://github.com/ct-Open-Source/tuya-convert/files/4812333/gosund-WB4.zip#gosund_pre_wb4.bin) |  | 🔴29f7e05 |  |  | c82b9615a3f2 | 81550705 | DWH2FCFhYROGKFyFrflC3hNAUc0HlPdX | rgHG2E1ToDyRq1d4rB1fsSaZJQn3fArLFmTGE
[12a](https://github.com/ct-Open-Source/tuya-convert/files/4812333/gosund-WB4.zip#gosund_post_wb4.bin) | ✅ | 🔴29f7e05 |  |  | c82b9615a3f2 | 81550705 | DWH2FCFhYROGKFyFrflC3hNAUc0HlPdX | rgHG2E1ToDyRq1d4rB1fsSaZJQn3fArLFmTGE
[13](https://github.com/ct-Open-Source/tuya-convert/files/4875072/dxpow_WP1_original_fw.zip) |  | 🟢23fbe10 |  | 2c3ae838e6e4 |  | 01200101 | opTcwaOCLL2nhutEvmdqJMgspspjiAA7 | 
[14](https://github.com/ct-Open-Source/tuya-convert/files/4903594/backup_20200709_112518.zip) |  | 🔴29f7e05 |  |  | c82b96580af8 | 54354408 | AA8tiO3d0Mm8L1tXxVrvjxUrC4ecwjg4 | 2ncs17NzxeXXlu0rdSVuWBy1PH9CQvvhtFWPK
[15](https://github.com/ct-Open-Source/tuya-convert/files/4907683/backup_20200711_210602.zip) |  | 🔴? |  |  | a4cf12e5b2ec | 62531570 | DAuwPH9PaBKgFzBg7Zq4CpUhYDzG4rDQ | y5Vsp5b5OTWUqLjp6kOLYxu0Z0PBByRTYuYym
[16d1](https://github.com/ct-Open-Source/tuya-convert/files/4981803/firmware-backup-devices.zip#firmware-backup-device1.bin) |  | 🔴29f7e05 |  |  | c82b964e3b29 | 64785071 | eDOnWtAUy5gJOiKtcXkNplBMqOMjJmM3 | ggD99i71cC7R7MTVnHadCtjaK28H2f6fOJLrG
[16d2](https://github.com/ct-Open-Source/tuya-convert/files/4981803/firmware-backup-devices.zip#firmware-backup-device2.bin) |  | 🔴29f7e05 |  |  | c82b964e3b22 | 64785071 | in18hm8DJch2NzlkjkSVHVuFJ3kpUo6k | hcXNpRfvnob0zqZWQ4zL4oxa0BHHRzC6jns3X
[17](https://github.com/ct-Open-Source/tuya-convert/files/5011017/tuya1way_flash_1M.zip) |  | 🔴317e50f |  |  | f4cfa209f296 | 02017786 | XAQxizdPqgrnvQbOIghkjPVfKfucx57H | jJ0OviSFn83XvHf8mkcqxtDPupbv9ahGcMMOk
[18](https://github.com/ct-Open-Source/tuya-convert/files/5015727/firmware-baf0cc.bin.zip) |  | 🟢e8c5810 |  | 0cc |  | 66058212 | lUYMJPQn6rXCboADiborfnCqTUreKyAT | 
[19b1](https://github.com/ct-Open-Source/tuya-convert/files/5016179/Backup.zip#Backup1_20200803_140803.bin) |  | 🔴317e50f |  |  | 600194fa3ee6 | 62520020 | ra6mACgWjH95YpxmYKGOY8lBJrBOApq0 | 2addWd7o1Qv9duggcFeklHqI3A3oSaKMJMrYx
[19b2](https://github.com/ct-Open-Source/tuya-convert/files/5016179/Backup.zip#Backup2_20200803_142458.bin) |  | 🔴317e50f |  |  | d8f15bb9ce4d | 62520020 | 54SbITkxFzL2bUPjFqijQJH3AxRdaT6e | 92JWevlzWoAHtlYEOHkX4LsCsQPGyqIWW3bEm
[20](https://github.com/ct-Open-Source/tuya-convert/files/5018720/Tuya_Backup_20200803_134931.zip) |  | 🔴29f7e05 | 🔴317e50f |  | 2462ab3d3499 | 80340470 | yXbeuWdxJyD8IVYCvukoSvKrApH4fOaf | Tln7d8Uou2pp8TtJbe5JTfdw3b7SYj2YOkmfY
[21](https://github.com/ct-Open-Source/tuya-convert/files/5037513/old-original-fw.zip) |  | 🟢898b733 |  | b4e |  | 27080852 | mJOBHtZuvzvAK0g8JiRaqyYHn2FOS5Cb | 
[22](https://github.com/ct-Open-Source/tuya-convert/files/5059741/backup_BW-LT29.zip) |  | 🔴29f7e05 |  |  | 50029178b020 | 54436323 | AG1rTspXIeEv0VIciXnD8kAcGu8QUR4c | bPzGF9hhpAOCzTZ1bnyEPcLtFXnQlMJSxF1A0
[23](https://github.com/ct-Open-Source/tuya-convert/files/5067474/backup_20200812_163954.zip) |  | 🟢898b733 |  | 133 |  | 06847238 | iL4ePi4zaV1V7TjAgOWKcyzBkdI34e2r | 
[24](https://github.com/ct-Open-Source/tuya-convert/files/5069154/MoesGarageDoor.zip) |  | 🟢e8c5810 |  | 6ac |  | 03733058 | rlPU5cNvqskvc5TpT6tA2AfupOyLrlYl | 
[25](https://github.com/ct-Open-Source/tuya-convert/files/5071350/firmware-backup.zip) |  | 🔴317e50f |  |  | fcf5c4800682 | 40426764 | UOLjYJbk07gHZO0VBHaZshkxW65HsW0d | WgWAqXlPnX8qAdaD8GU2Ljoa8TYaTcD65r6Ur
[26](https://github.com/ct-Open-Source/tuya-convert/files/5080563/firmware-backup.zip) |  | 🔴317e50f |  |  | c82b96ccd0e2 | 68116280 | 3KEWyyZHNAOzqyZ8gHpu1IqLasrMlOJZ | pfQ9jVNRUArItWV4qaSUuP3ojC5vsXY0L6SIB
[27](https://github.com/Elkropac/esp-firmware-backup/blob/master/aofo_socket/firmware-backup.bin) |  | 🔴29f7e05 |  |  | d8f15bdf7e98 | 20432477 | 5RpboSdogNamQInfsrpMeVbr01fvAd9V | eH3eYWXmNxaAxTJXPLhJSCucK0N8VkPwCxp24
[28](https://github.com/Elkropac/esp-firmware-backup/blob/master/zemismart_downlight/firmware-backup.bin) |  | 🔴317e50f |  |  | fcf5c4800682 | 40426764 | UOLjYJbk07gHZO0VBHaZshkxW65HsW0d | WgWAqXlPnX8qAdaD8GU2Ljoa8TYaTcD65r6Ur
[29](https://drive.google.com/file/d/1VtKJz6VznqlBdR5x_OySgMEKB6OoGbIR/view?usp=sharing) |  | 🔴317e50f |  |  | 50029117b5d0 | 07045557 | CTuF4WV3hKInKYPt6QrJPgX9LaK9M4Bk | gibTC21CwXiuH4S3Wjg2wOOqj0Tx1PTtnCknc
[30](https://github.com/ct-Open-Source/tuya-convert/files/4881063/firmware-9c52d8.bin.gz) |  | 🟢e8c5810 |  | 2d8 |  | 56435352 | ZJO0QadxOoDTlPFbwW8Larh2r7L8AOBW | 
[31](https://github.com/ct-Open-Source/tuya-convert/files/4881064/firmware-52a6fb.bin.gz) |  | 🟢898b733 |  | 6fb |  | 04453323 | yzCEW1vz7Y1ZvoCEeEynhxO36JVdZcKA | 
[32](https://github.com/ct-Open-Source/tuya-convert/files/4881065/firmware-a068f4.bin.gz) |  | 🟢898b733 |  | 8f4 |  | 78677700 | HkXr1p695mO3YpjniaFqhR7PFd3XDHpB | 
[33](https://github.com/ct-Open-Source/tuya-convert/files/4881066/firmware-a0709d.bin.gz) |  | 🟢898b733 |  | 09d |  | 78677700 | DAY0eL57GnmVALIvgqDm7YUVkzsWuAEh | 
[34b](https://drive.google.com/file/d/1hp39MsYcBcs9J3TP-fvSbwExhxE9OTQ0/view?usp=sharing) |  | 🟢e8c5810 |  | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a1](https://drive.google.com/file/d/1qoh6I7l_Pod-Mqlm6ueOxtrMb65UBbuy/view?usp=sharing) | [✅](https://drive.google.com/file/d/1cHvrW2p7CmO9tF1GvJ1RZ2mUXha_Al3y/view?usp=sharing) | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a2](https://drive.google.com/file/d/1vauElr2v8wzsW5nsNx5cC8XmKP_pxqJl/view?usp=sharing) |  | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a3](https://drive.google.com/file/d/1CbihDyMF9bwTVEcM-JBJJPWg54fkCA57/view?usp=sharing) |  | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[35](https://drive.google.com/file/d/1Im1MXfnPsr1JYGHsrD_wbz3NYd8o1ve_/view?usp=sharing) |  | 🔴317e50f | |  | 8caab5e5a280 | 87860851 | fCAAa6f5iNYRj7NzCZGPWpnzMq4cOizF | WSWCRf3nG93ttY4j90V3HGXjB1sDeCXYBoVVa
[36](https://drive.google.com/file/d/1ilAbKvsUMM1mAl-XiT2gJPrUJWhU03xM/view?usp=sharing) |  | 🔴317e50f | | | c82b966b3de4 | 05653062 | IG95zG4NOs4hKNtLHxAGz1Mu9h9UiEj1 | PeB57pbhtNUVANIstnaGUFBGWyWjwLqWf1uBk
[37](https://github.com/ct-Open-Source/tuya-convert/files/6470124/wp5_02.bin.gz) |  | 🔴317e50f | | | 70039f8968a6 | 22057624 | x9cW1Vg3FEr6s7RKoys8FmTj5SgGHGqO | k8WTEIHdy0VBeqovXFdSo2WxwuvlwTLbMZJt1
[38](https://github.com/ct-Open-Source/tuya-convert/files/6470144/wp5_03.bin.gz) |  | 🔴317e50f | | | 24a16016e177 | 00080070 | whhqiFzXBinHg33dheVvwyWhRJBBcFV4 | gIjRhFwGBgSibk8czel34IsYoWmImUi2lnjwQ
[39](https://drive.google.com/file/d/1nlIC8da5J0kvIZijlKlHp2ajeqAtyuEY/view?usp=sharing) | [✅] | 🔴29f7e05| | | e09806009aed | 35558538 | CRiNIby4WavZFUX7enncDcFK0M43WQRM | fJNQuzsUEBT8TIY88fpATIdaSka3dfZ0hp1Bu
[40](https://we.tl/t-TKAB7wSbwM) | [✅] | 🔴29f7e05| | | d8f15bad691d | 40014435 | KLeaREf1DijkQ5uFmPidcE0gv0A4VfQG | YR0fEdw2QVwyhCCqwJDBd4WiU1G8BhQPzd9bC


- There can be two firmware builds in a single 1MB image if the device has been updated; listed as SDK_ver_A and SDK_ver_B
- 🟢 build doesn't know about pskKey (Tuya-Convert probably works)
- 🟡 build knows about pskKey but doesn't appear to have one set
- 🔴 build knows about pskKey and has one set in 0xfb000 JSON blob
- 11 is interesting because it is not upgraded and a build known to use pskKey elsewhere, but doesn't include the string literal pskKey
- 13 is an older SDK ver (1.4.2 compiled @ Sep 22 2016 13:09:03) and has full MAC address as mac rather than mac_addr
- 15 is missing the "OS SDK ver:" string
- 34 are the following firmwares: Original + 3 different upgrades (from the same device) via reflashing original and then upgrading. Hope this helps. I'm available on digiBlur's discord channel @jschwalbe#6176 - hit me up if any questions or something you need that I missed.
- The pcap from 34a1 shows a spurious retransmit of a "change cipher spec" which prevents wireshark/tshark from decoding the response to the `tuya.device.uuid.pskkey.get` call.  Ignoring that packet allows it to be decoded, yielding the following JSON: `{"result":"EqY/PCRBZBAhkpujEEx/X9NrCDCOWuqpmCBIXztwprnMeDhTV4cd9flrbszbTDFlmQ99FJWjDwwrsjr9uDBjKGJ76hlBrDLSxPXMJvFfyMrM6sQezfgCpkIpys5lOBK7","sign":"5dd1747ae9294467","t":1599425271}`
- 35 are images of 2 identical devices, one booted original firmware and tryed wifi flashing, other never booted original fw.
- None of the images captured so far of a Tuya-Convert compatible build that are updated to an incompatible pskKey build include the pskKey in the JSON blob at 0xfb000

## Additional Network Captures
- https://github.com/ct-Open-Source/tuya-convert/files/4142919/bakibo_bulp_pcap.zip
- https://github.com/ct-Open-Source/tuya-convert/files/4205411/bakiboT22Y.pcap.zip

## Strings
```
OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12
[N]%s:%d metedata is without encryption, cover this partition with encrypted data
[N]%s:%d var block [%d] last version is without encryption,now need to encrypt data and cover this partition
[ERR]%s:%d flash_aes128_ecb_encrypt err
[ERR]%s:%d !!!!!!CHIP_MAC:%s FLASH_MAC:%s!!!!!!
aes-internal-dec.c
aes-internal-enc.c
lhttps://a3.tuyacn.com/gw.json
https://a3.tuyaeu.com/gw.json
https://a3-ueaz.tuyaus.com/gw.json
https://a3.tuyaus.com/gw.json
{"mac_addr":"500291e8f141","prod_idx":"26636676","auz_key":"wg7xdxUcsi7W0EmnPUlEtuwoyZwcF2W2","pskKey":"GUKgTWzsxGCn8UR5tIFFluuKD2qA8FYmaZwY2","prod_test":false}
{"ap_ssid":"SmartLife","ap_pwd":null}
{"CC":"CN"}
vtrust-flash
ESP_E8F141
vtrust-flash
```
***

Novostella RBGWC 13W E27
`{"mac_addr":"e098060153ad","prod_idx":"80157022","auz_key":"ksJHynYgCMs7caHDzXtvb8EwtCtFsLxC","pskKey":"eZklnPtc0xuRVn8mf6bj1Hzarr7p7uTBfgKt3","prod_test":false}`
``

## Useful Info/Links
- The [tuyapi library](https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md) has interesting info including developer accounts at https://iot.tuya.com/ and although deprecated, some MITM procedure to get ID and keypairs.
- Tools for reverse engineering of Tuya API signing algo https://github.com/nalajcie/tuya-sign-hacking

## More Investigations in Tuya IoT Platform:
- Cloud tokens are security encryption certificates that Tuya issues to devices. They are credentials for smart devices to connect to Tuya Cloud. Each device shall have a unique token. If you use a Tuya standard module SDK to develop your products, purchase modules and the same number of tokens.
- Also this might be interesting: https://developer.tuya.com/en/docs/iot/device-development/tuya-development-board-kit/tuya-sandwich-evaluation-kits/development-guide/authorization-code-firmware-burning?id=K9br41pefnksv

## Reverse Engineering Tools
maybe this helps someone: https://github.com/xety1337/tuya-reverse

## Using mitmproxy with a rooted Android device and TCP Smart
* It is possible to use mitmproxy to inspect the TLS traffic when pairing one of these devices using the Android TCP Smart application
* The application will note that it is being run on a rooted device, but will permit you to continue
* The mitmproxy certificate must be installed as a system certificate, as pretty much everything on Android will not trust a user certificate and will ignore the cert
* Note that the the smart device will need access to a DHCP server, so this may influence your proxy setup
* The pairing won't complete if the smart device is proxied, as the device won't trust the mitmproxy certificate
* Unless there are alternative methods for configuring pinning, network_security_config.xml suggests that the Android app is not using certificate pinning
* Proxying just the Android device (and not the smart device) allows the pairing process to complete
* When decrypted, the TLS communication between the app and the servers is json encoded and appears to be encrypted and signed (I can understand the latter as an additional authentication step, but not the former)
* Next steps:
  * Find out how the communication between the app and the servers is further encrypted
  * Attempt to build firmware for the smart device that has the mitmproxy embedded?

