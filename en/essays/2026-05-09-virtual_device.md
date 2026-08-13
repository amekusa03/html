# Virtual Smart Device Control System

2026/05/09  ESP32 / Matter / Esp-idf /LovyanGFX / C

Matter compatible virtual smart device development detailed report

## 1. Project overview

### Purpose and concept

This project uses Waveshare's ``ESP32-C6-GEEK'' as a platform and aims to implement a ``virtual smart device'' via the Matter protocol. The biggest feature is that ON/OFF state animation and operation verification can be completed on the built-in LCD without involving the actual PC hardware. This allows Apple
Interoperability with major smart home ecosystems such as Home, Google Home, and Amazon Alexa can be safely and precisely verified using a single device.

### Summary of key features

1. **Multi-platform operation with Matter Protocol: **Achieve seamless operation from a diverse ecosystem without relying on a specific vendor.
2. **Real-time status animation with LCD: **Draw device dynamics in 20fps low-latency graphics to provide visual feedback.
3. **Intelligent Backlight Dimming:** Event-driven automatic dimming logic for efficient power management and panel protection.
4. **Seamless switching between virtual and real modes: ** Software-defined changes allow instant transition from simulation environments to physical PC power control.

## 2. 5-layer system hierarchy structure

This system consists of the following five-layer architecture for the purpose of hardware abstraction and protocol stack separation.

1. **Physical Layer (Hardware Layer):** ESP32-C6-GEEK is used as the main microcontroller, and ST7789 built-in LCD with a resolution of 135 x 240 px is used as the output interface. Note that when operating in real machine mode (physical control), a separate photocoupler circuit must be connected to the outside of the board.
2. **Driver/Abstraction Layer:** Introduced high-speed drawing library "LovyanGFX" and applied SPI bus and DMA (Direct Memory Access) for communication with ST7789. This ensures the 20fps drawing performance required by the application layer. Also, in real machine mode, it provides a physical switch control interface via GPIO 20.
3. **Communication/Protocol Layer:** The layer in which the Matter protocol stack based on WiFi connections functions. Controls secure pairing and command communication with top smart home apps (Apple Home, Google Home, etc.).
4. **System Service Layer:** Provides an OTA (Over-the-Air) update function that enables wireless functionality expansion and dimming logic that dynamically manages backlight brightness. The 32-second dimming timeline described below is managed in this layer.
5. **Application Layer:** As the top layer, it is responsible for driving the 20fps animation drawing engine, synchronizing the ON/OFF state of the device, and switching the logic between virtual and real devices.

## 3. Technical specifications

### Hardware specification table

Parts Model number Microcontroller Waveshare ESP32-C6-GEEK LCD ST7789 (Built-in board 135×240px)

### Software requirements table

Tool version ESP-IDF v5.4.1 ESP-Matter Latest (GN required) Python 3.12.3 or higher Included in LovyanGFX components/

## 4. Development points

### 1.Matter operation and pairing

This device performs initial setup and operation based on the Matter standard.

- **Manual pairing code:** Assuming an environment where QR codes cannot be used, use the 11-digit code "06242023267" for manual input.
- **Ready Identification:** After startup, the IP address will be displayed in the LCD footer area. When this appears, it is a signal that Matter is ready for commissioning (pairing). Detailed logs can be checked on the "Manual pairing code:" line on the serial monitor.

### 2. LCD animation display

In order to improve the user experience, 20fps drawing is realized using DMA drive.

- **Displayed items:** Device ON/OFF status, WiFi connection status, and acquired IP address are always displayed in the footer.
- **Visibility:** Adopts an interface design that allows you to understand communication status and device status at a glance.

### 3. Backlight automatic dimming logic

In order to extend the lifespan of the LCD and optimize power consumption, we have implemented dimming control based on the 32-second timeline below.

- **Full brightness maintenance phase (0–10s):** Maintains 100% brightness for 10 seconds after an event such as an operation input occurs.
- **Dimming phase (10–32s):** The brightness decreases linearly over the next 22 seconds, eventually transitioning to the off (dimming) state.

### 4. Function to switch between virtual mode and real machine mode

The compile switch in `main/pc_control.h` defines the operating mode.

- **Virtual mode:** `#define PC_VIRTUAL_MODE 1` — Performs only software simulation and completes the operation with LCD animation.
- **Real machine mode:** `#define PC_VIRTUAL_MODE 0` — Works with the LCD display to physically control the actual PC power button via the optocoupler circuit from GPIO 20. *This mode requires separate construction of an external circuit.

## 5. Architecture considerations

### Main configuration file

Developers should refer to and edit the following files as necessary.

- `main/wifi_creds.h`: Define the SSID and password of the connected WiFi.
- `main/pc_control.h`: Operation mode (PC_VIRTUAL_MODE) selection.
- `main/lcd_display.cpp`: Control of dimming timing and animation parameters.

### Build/deployment flow

1. **Environment construction:**Set up the environment for ESP-IDF and ESP-Matter. GN is required to build ESP-Matter.
2. **Reflect settings:** Write network information in `wifi_creds.h`.
3. **Build execution:** Execute `idf.py build`. Ensure that dependencies including GN are resolved correctly.
4. **Flash:** Write to the device using `idf.py flash` and confirm the start of operation by seeing the IP address displayed on the LCD footer.

## 6. Source code

[https://github.com/amekusa03/Virtualdev](https://github.com/amekusa03/Virtualdev)
