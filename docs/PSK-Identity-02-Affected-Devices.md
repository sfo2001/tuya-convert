# PSK Identity 02 - Affected Devices

**Last Updated:** 2025-11-04
**Status:** 🔄 Community Maintained
**Parent Document:** [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md)

## Overview

This page lists devices confirmed to use **PSK Identity 02** firmware, which prevents OTA flashing with tuya-convert. These devices require the new TLS-PSK authentication that cannot currently be bypassed.

### How to Identify PSK ID 02 Devices

If your flashing attempt fails with this error in `smarthack-psk.log`:
```
ID: 02xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
could not establish sslpsk socket: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC]
```

Your device uses PSK Identity 02 and is listed below (or similar).

### What This Means

- ❌ **Cannot flash via OTA** using tuya-convert
- ⚠️ **May require hardware flashing** (serial connection to ESP chip)
- 🔍 **Help with research** - See [Helping with PSK Format](Helping-with-new-psk-format.md)

### Device Purchase Timeline

- **Pre-September 2019:** Most devices work with tuya-convert
- **September 30, 2019 onwards:** New PSK format introduced
- **Mid-2020 onwards:** Many devices switching to non-ESP chips entirely

---

## Known Affected Devices

This list is community-contributed. Devices are listed alphabetically by brand/model.

> **Note:** Some devices may have switched chipsets (away from ESP8266/ESP8285) entirely, making them incompatible with ESP-based firmware even if PSK were solved.

### A

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

### B

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

### C

- [Calex Multi Color Floor Lamp](https://www.calex.eu/en/products/product/CALEX-SMARTVLOERLAMP/)
- [Calex Smart RGB Reflector](https://www.calex.eu/en/product/LEDREFGU10-5W-2200-4000SMD-RGBSMART/)
- Connect SmartHome CCT Downlight

### D

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

### E

- Eachen WiFi-IR Universal Remote (SANT-IR-01)
- eLinkSmart BSD29 (packaging says Smart Plug eLinkSmart 16A - Amazon Nov 20, 2020)
- EKAZA EKNX-T005 (same product as NX-SM400) (Mercado Livre / Nova Digital - Jan 2021 2 pack)
- Etersky WF-CS01 Curtain Switch
- Etersky Wifi Smart Bulb (LDS-WF-A60-9W-E27-RGB) (Amazon Dec 2020, 2 pack)
- Esicoo Wifi Smart Plug (US package listes device model is 'YX-WS01', Amazon US May 2021, 4 pack) Suspect RelTek IC Not ESP8266 IC based

### F

- FCMILA Smart Bulb RGBW
- Feit Smart Wifi Bulb
- Feit OM100/RGBW/CA/AG (fccid: SYW-A21RGBWAGT2R - non R versions seem to be unaffected)
- Feit OM100/RGBW/CA/AG(C) (Amazon purchase in Oct 2021, `TYWE3L` module, OS SDK: `2.1.1(317e50f)`, Tuya SDK: `Apr 13 2020 10:28:31`, firmware info name: `oem_esp_light_v1_tuya version:1.1.1`, FCC ID `SYW-A12RGBWAGT2R`)
- Feit Smart Dimmer
- Feit Smart Plug (SYW-PLUGWIFIG2)
- Fitop Smart Bulb E27
- Freecube Smart Bulb E14 5W (amazon.co.uk Dec 2020)

### G

- GD.Home LED Floor Lamp (Anten, Amazon Jan 2021)
- Geeni Prisma 10W 1050lm RGBCCT Bulb
  - 17 Dec 20 - Latest firmware for GN-BW94-999 is 1.0.3. Unable to use latest Tuya-Convert from development branch - #54277bcf. Bulb connects to vtrust AP but that's it. Nothing in the logs of any use).
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

### H

- Halonix Prime Prizm 12W RGB Bulb(Amazon.in, October 28, 2020)
- Hama 10W 1050lm RGBW E27 Bulb (Amazon, October 2020)
- Hama Outdoor WiFi socket 176570
- HBN Outdoor Smart WiFi Plug U151T (Amazon, December 2020)
- Hiking DDS238-2 Wifi - Smart Meter with relay
- Hombli Smart Socket power plug - HBPP-0204

### I

- iiglo Wi-Fi Smart Power Strip – IISMART0003 (Komplett, November 2020, SKU:1174244) (Shows up with ESP_xxxxxx in the DHCP lease, returns PSK 02)

### J

- Jasco Enbrighten Smart Plug, model WFD4105E
- Jinvoo SM-AW713 Valve
- Jinvoo SM-PW713

### K

- KHSUIN A19 E26 RGBCW 7w 800lm bulb (Amazon, June 2020)
- Klas Remo SWA11
- Kogan KASMCDSKTLA 1.7L Smart Kettle
- Kogan SmarterHome Smart Plug with Energy Meter [KASPEMHA, KASPEMHUSBA] (Kogan, June 2020, but by Oct 2021, KASPEMHA now WB2S, incompatible with tasmota)
- Kogan KAB22RGBC1A Smart Bulb (B22) 10W 806LM

### L

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

### M

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

### N

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

### O

- OHLUX Smart WiFi LED (ASIN B08CL2CKW3, OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12)
- OHLUX 40W 4000LM Smart Outdoor Flood Lights (ASIN B083TZFB29)
- Olafus 10W WiFi LED (2 pack, Amazon.it, Mar 2022, Model: E10WIFI, SKU LA-E10-78FDRGBW-EU02)

### P

- Polux WI-FI SMART LED, 400lm, 5,5W, GU10 (GU10SMDWWCW+RBG) (Model: MK-010011001067, Series: SE2006MK-1)
- Polux WI-FI SMART LED, 400lm, 5,5W, E12 (E12SMDWWCW+RBG) (Model: MK-010052019005, Series: SE2004MK-1)
- Polux WI-FI SMART LED, 1055lm, 13W, E27 (E27SMDWWCW+RBG) (Model: MK-010112048001, Series: SE2006MK-1)
- Polux Wi-Fi SMART LED Strip RGB+NW 4000K 2m, 540lm, 6,5W, (Model: CL-5050RGB2835WWaaaHYbb-Wcc-WiFi, Series: SE20006CL-1)
- Powertech SL225X (firmware V3.3.16 TC compatible, V3.3.30 new PSK)
- Prime WiFi SmartOutlet Outdoor (Date Code: 08/20, from Costco.ca)

### Q

- QS-WIFI-S03 Module Switch

### S

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

### T

- TCP Smart 13A Plug (WISSINWUK)
- Teckin SB50 (firmware V1.61 new PSK, was previously TC compatible until firmware update through Tuya app).
- Teckin SB53 (some of them, even BNIB never updated)
- Teckin SS31 Outdoor smart outlet
- Teckin SS42 Outdoor smart outlet
- Teckin SR40 Wi-Fi Smart Wall Socket (Amazon Jan 2021)
- Tellur TLL331031 (emag.ro, Jan 2021)
- TopGreener TGWF15RM smart outlet with Energy Monitor (4 pack, purchased Amazon Nov 2020)
- TopGreener TGWF115PQM [4-Pack, Amazon Nov 2024]
- Treatlife A19 8W 650lm RGBCCT Bulb
- Treatlife Ceiling Fan & Light Dimmer Switch DS03
- TreatLife Smart Dimmer Switch DS01C
- Treatlife Smart Dimmer Switch DS02S
- TreatLife Smart Plug-in Dimmer DP10
- TreatLife SS01S (4 pack, purchased on Amazon Nov 2020)
- Treatlife SS01 3-Way Switch
- Treatlife SS02S Single Pole Switch

### U

- UCOMEN Outdoor Sockets PA-GEBA-01SWP2
- UFO-R1 / SRW-001 Smart Wifi Infrared Controller (tested version is labeled by MOES)
- Ultra Link UL-P01W (Takealot, 26 November 2020)

### V

- Veargree Smart Timer ATMS1601

### W

- WiFi Smart Power Strip 4 AC - SA-P402A (Zeoota)
- Wipro Garnet 9W RGBCCT Bulb
- Wipro Smart Extension DSE2150
- Wipro Smart Plug 16A
- Wofea Smart Garage Controller WG-088
- Woox r5024 (pack of 4 bought on ibood in june 2020)

### Z

- Zebronics ZEB-SP116
- Zemismart 4 inch 10W Wifi RGBW
- Zemismart 6 inch 14W WiFi RGBCW
- Zemismart Curtain Motor ZM79E-DT WiFi [here](https://www.zemismart.com/products/smart-curtain-customized-electric-curtain-motor-with-tracket-rf-remote-broadlink-control)
- Zemismart WiFi Roller Shutter [YH002](https://www.zemismart.com/products/zemismart-tuya-wifi-roller-shade-driver-diy-roller-yh002)
- Zeoota ZLD-44EU-W - WiFi Smart Power Strip

---

## Contributing Device Data

Found a device with PSK Identity 02? Help the community by reporting it!

**What to Include:**
- Device brand and model number
- Purchase date and source (Amazon, local store, etc.)
- FCC ID (if available)
- Firmware version (if visible in app)
- Any special notes (chipset, warnings, etc.)

**Where to Report:**
- [Open an issue](https://github.com/sfo2001/tuya-convert/issues) on this repository
- Include "PSK Identity 02" in the title
- Attach your `smarthack-psk.log` file if available

---

## Related Pages

- **[PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md)** - Technical details
- **[PSK Identity 02 Firmware Analysis](PSK-Identity-02-Firmware-Analysis.md)** - Firmware samples and analysis
- **[PSK Identity 02 Research Data](PSK-Identity-02-Research-Data.md)** - Network captures and research tools
- **[Helping with PSK Format](Helping-with-new-psk-format.md)** - How to contribute research
- **[Compatible Devices](Compatible-devices.md)** - Devices that work with tuya-convert

---

**Device Count:** 220+ confirmed affected devices
**Last Major Update:** November 2024
**Community Contributions:** Ongoing
