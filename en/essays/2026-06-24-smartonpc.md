# SmartOn PC

2026/06/24 / ESP-IDF / Matter / Google Home

To acquire ESP32 technology and learn Matter, use the PC power supply as Matter.
 Build a system that operates over Wi-Fi.

## About this Project

This is a project to integrate Generic ESP32-C3 into Ubuntu PC and make it compatible with the smart home standard "**Matter**".
You can turn your PC on and off using voice commands and automation from Google Home/Nest Hub.
This is a revenge for a previous project.
We aim to seamlessly manage and operate the power status of PCs just like other home appliances.

## function

#### Step 1 — Power control

Function Means Power ON Mechanical relay → Short press of power button (500ms) Power OFF Mechanical relay → Short press of power button (500ms) + Shutdown with Ubuntu ACPI settings Factory reset GPIO9 Long press (3 seconds) 
- **WoL (Wake on LAN) is not adopted **—Even though I intended to set it up on this PC, it did not succeed. 
- **ESP32 - ○○ command → power off on PC **— Not considered because it is no different from operating a PC in the first place 
- **Power OFF**: Short press the power button on the relay to activate Ubuntu's ACPI
Setting (`HandlePowerKey=poweroff `) initiates a graceful shutdown 

#### Step 2 — Power status monitoring

Function Means Power status detection GPIO input of power LED via PC817 (active LOW) Deviation detection Polling for 2 seconds, confirmed 3 times in a row Matter attribute synchronization When deviation is confirmed, use `attribute::update() ` to adjust the OnOff attribute to the actual situation User notification via Matter subscription (automatically received by Google Home, etc.) **Fail-safe principle **: Even if deviation is detected, the system will automatically turn on/off Do not perform any operations. The actual situation is reflected in the Matter attribute and left to the user.

## Hardware configuration

#### Main parts

- **Microcontroller**: Generic ESP32-C3 
- **Host PC**: Ubuntu 
- **Power Control**: Single Channel Relay Module (ASIN: B0G4C9GMVH) short circuit PWR SW pin on motherboard 
- **Power status detection**: Read power LED via PC817 optocoupler 
- **Controller**: Google Nest Hub / Android smartphone 
- **Power Supply**: Constant power supply from PC USB port 

#### GPIO allocation

GPIO Role Circuit GPIO 20 OUTPUT: PWR SW control via mechanical relay GPIO 4 INPUT: PWR LED detection via PC817 photocoupler (active LOW) GPIO 9 INPUT: Factory reset Internal pull-up, LOW=press 

#### circuit diagram

**PWR SW (GPIO 20 → Mechanical relay → Motherboard) **

GPIO 20 → Relay control input
Relay contact → Motherboard PWR SW Header short **PWR LED (Motherboard → PC817 → GPIO 4) **

PWR_LED+ → 470Ω → PC817 Anode(pin1)
PC817 Cathode(pin2) → PWR_LED- (GND)
3.3V → 10kΩ → PC817 Collector(pin4) → GPIO 4
PC817 Emitter(pin3) → GND

PC ON: LED lit → PC817 continuity → GPIO = LOW
PC OFF: LED off → PC817 shut off → GPIO = HIGH (pullup) Polarity can be switched using the `PWR_SW_ACTIVE_HIGH ` source code of `pc_control.c `. 


#### Main material costs

Parts Price Generic ESP32-C3 539 yen Relay module 464 yen PC817 Photocoupler 388 yen **Total ****1,391 yen **
#### Standby power (estimated value)

Device status Estimated power consumption Generic ESP32-C3 Wi-Fi Always connected/standby Approx. 0.3~0.5W Relay module When not activated (coil OFF) Approx. 0.01W or less Photocoupler When not activated Approx. 0.01W or less USB adapter loss Conversion efficiency 80% Assumed +10~20% **Total ****Approx. 0.4~0.6W **The above values are estimated values. This is about the same as the standby power of a smartphone charger (0.1 to 0.3W), which is a safe level for practical use.

## software stack

Layer Name Version OS / SDK ESP-IDF 5.4.1 Matter wrapper esp-matter Specified by `$ESP_MATTER_PATH ` Matter body ConnectedHomeIP (CHIP) esp-matter submodule Matter Device type: **On/Off Plug-in Unit **

## build

#### Configuring WiFi credentials

Create `main/wifi_creds.h ` and write the SSID and password (`.gitignore ` completed): 


```
`#define WIFI_SSID     "your-ssid"
#define WIFI_PASSWORD "your-password" `
```

#### Build & Flash


```
`. $IDF_PATH/export.sh
. $ESP_MATTER_PATH/export.sh
export _PW_ACTUAL_ENVIRONMENT_ROOT

idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash `
```

#### Matter commissioning

After flashing, a QR code and setup PIN will be output on the serial monitor. Please scan and register your device using the Google Home app. 

A test DAC (Device Attestation Certificate) is used during the development and testing stages. 

Item Value Manual Pairing Code `34970112332 `Setup PIN `20202021 `Discriminator `3840 `

## design decisions

#### BLE disable/WiFi only commissioning

BLE is completely disabled in `sdkconfig.defaults ` (`CONFIG_BT_ENABLED=n `, `CONFIG_ENABLE_CHIPOBLE=n `). 

**Reason**: We have hardcoded the WiFi credentials in `store_wifi_credentials() `, so the device attempts to connect to WiFi upon startup.
                    If CHIPoBLE (Matter's BLE advertisement) operates in this state, WiFi connection may be inhibited due to BLE/WiFi radio conflict.
                    In designs that embed WiFi authentication information in advance, we disable BLE and standardize on commissioning via IP network (`kOnNetwork `). 


#### Fail-safe principle (operation when deviation is detected)

The premise of the Matter specification is that ``the actual situation can be determined definitively.'' Automatic ON/OFF in the event of deviation creates a risk of malfunction. 

Safe direction = no operation. The decision is left to the user. Behavior when the discrepancy is confirmed (no discrepancy after 3 consecutive polls): 


1. Synchronize OnOff attribute with reality in `attribute::update() ` 
2. Notify controllers (Google Home, etc.) via Matter subscription 
3. This system does not operate the power supply even with the information obtained.

## Known issues/issues

#### mDNS conflict (resolved)

In the old implementation (Ping-based aliveness monitoring), ESP-IDF `mdns_init() ` and Matter internal mDNS conflicted on port 5353.
                    Currently, mDNS is not used as it has been replaced with power LED polling using GPIO. The problem has been resolved. 


#### Freeze automatic recovery (not implemented)

Currently, we have not detected cases where the power LED remains on and the PC does not respond (freezes).
                    Manual action required. Users need to understand the system and take appropriate actions.

## Restrictions

- This project assumes a typical home router environment at home. 
- In networks that are strictly managed by authentication servers or networks that do not have sufficient security management,
                        Your use of Matter may be restricted.

## supplement
After using it for a few weeks, the Wifi connection became poor, but I don't know why.
According to the internet information, the signal is originally weak.
We also sell boards that allow you to take out the antenna separately, so you may want to use that for actual operation.
(although the price will go up)

## Resources

[View on GitHub](https://github.com/amekusa03/smarton-pc-c3)
