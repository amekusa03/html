# Control your PC power with Google Nest Hub

2026/07/24 / ESP-IDF / Matter / Google Home

We built a system to control the PC power supply using Google Nest Hub.
In this version, **dedicated wiring has been completely abolished**.
The OS is not a problem as a by-product.

## overview

Generic ESP32-C6 was integrated into the PC to make it compatible with the smart home standard "Matter."
You can turn on your PC with voice control or automation from Google Home / Nest Hub.
We aim to seamlessly manage and operate the power status of PCs just like other home appliances.

## Precautions

- Although it is possible to turn on the power, there is no OFF function.

## Main features

- **Compatible with both Windows/Ubuntu**: Can be used with both Windows/Ubuntu OS by combining USB and WOL.
- **Completely abolishing dedicated wiring**: No motherboard wiring such as mechanical relays or photocouplers is required. It can be installed simply by plugging it into the USB port of your PC.
- **Wake-on-LAN (WOL) remote startup**: When an ON operation is received from Matter, a Wake-on-LAN magic packet is sent to the configured MAC address to wake up the PC.
- **PC monitoring based on USB communication status**: Monitors the USB Serial/JTAG connection status (`usb_serial_jtag_is_connected()`) every 2 seconds and determines the actual power status (ON/OFF) of the PC.
- **Matter attribute automatic synchronization & failsafe**: When a discrepancy between the PC's actual power state and the Matter attribute value is detected, the Matter attribute is automatically updated and synchronized with a safety guard (`s_syncing_attribute`) to prevent misoperation.
- **ST7789 color LCD real-time display**: Graphically display Wi-Fi connection status, assigned IP address, PC status (ON / OFF / BOOTING), and operation status log.
- **Power saving & screen protection (5 minutes auto-off)**: 5 minutes after the PC reaches `OFF`, the LCD backlight (brightness) will automatically shift to `0` (lights off). Automatically lights up as soon as the PC starts up or returns to normal operation.
- **Google Home compatibility optimization**:
  - IPv6 mDNS (`_matter._tcp`) drop prevention by disabling Wi-Fi power saving mode (`WIFI_PS_NONE`).
  - MAC address-based deterministic UniqueID (`chip-config/unique-id`) automatic generation.

## Settings

- Set the PC's USB power supply setting to always be ON in the PC's WOL settings and BIOS settings.
- Describe the Wi-Fi settings of ESP32-C6 in `main/wifi_creds.h`

## Hardware specifications

- **Microcontroller board**: Waveshare ESP32-C6-GEEK
- **Display**: 1.14 inch ST7789 color LCD (240 x 135)
- **Connection method**: USB Type-A connection (PC USB port)
- **Physical wiring**: None (USB power supply and connection detection)
- **Reset button**: GPIO 9 (Long press BOOT button for 3 seconds to Factory Reset)

---

## software stack

| Layer | Name | Version/Settings |
| --------- | ------ | ----------------- |
| OS/SDK | ESP-IDF | v5.4.1 |
| Target | ESP32-C6 | `esp32c6` |
| Smart home standards | esp-matter / Matter | Wi-Fi (`kOnNetwork`) |
| Device Type | On/Off Plug-in Unit | Cluster: `0x0006` (OnOff) |
| Power control method | Wake-on-LAN (WOL) | UDP Port 9 / Magic Packet |

## Network settings

For security reasons, authentication information such as SSID, password, and MAC address are not managed by Git (registered in `.gitignore`).  
Before the first build, create a new `main/wifi_creds.h` and set the following contents according to your environment.

## Resources

[View on GitHub](https://github.com/amekusa03/smarton-pc-c6)

## option

### Ubuntu version power OFF function

Although it is exclusively for Ubuntu, we have also added a power off function.

#### Overview flow

1. Receives OFF operation from Google Home etc.
2. TCP connection from ESP32-C6 to PC_SHUTDOWN_PORT destination of PC via Wi-Fi.
3. Send PC_SHUTDOWN_TOKEN (principal).
4. The resident demo program (daemon) on the PC side authenticates itself and executes shutdown.

Please refer to the README on Github for details.

## Resources

[View on GitHub](https://github.com/amekusa03/smartonoff-pc-c6)
