# Temperature and humidity data logger for mountain fields (Hata logger)

2026/06/14 / C / Arduino / ESP32

Specifications for a temperature/humidity logger installed in a field on top of a mountain with no power or internet connection.

## 1. System overview

- **Application:** Fixed point observation of temperature and humidity in mountain fields
- **Measurement interval:**Every hour (power saving operation using deep sleep)
- **Data saving:**Save in CSV format to the internal flash memory (LittleFS) of ESP32-C3
- **Data collection:**Download from your smartphone browser via Wi-Fi (access point mode) on-site
- **Power:** Powered by installed solar charge controller (USB 5V)

## 2. Hardware configuration (parts list)

### ① Microcomputer board

- **Model number:**ESP32-C3 development board (recommended: Seeed Studio XIAO ESP32C3 or other power-saving design)
- **Features:**Low power consumption (approximately 50μA or less during sleep), Wi-Fi installed, small size

### ② Temperature and humidity sensor

- **Model number:**GY-SHT31-D (Module equipped with Sensirion SHT31)
- **Features:** High precision (temperature ±0.2℃ / humidity ±2%), high resistance to condensation

### ③ Other parts

- **Data collection switch:**Tact switch x 1 (for mode switching at hand)
- **Case:**Waterproof/dustproof plastic box (manufactured by Takachi Electric Industries, etc.)
- **Wiring materials:** 4-core cable for sensor extension, solder, heat shrink tubing
- **Rust/waterproofing measures: **Self-adhesive tape, putty (or silicone sealant), moisture-proof coating agent (Hayacoat)

## 3. Pin wiring diagram (connection table)

Connection source (ESP32-C3 side) Connection destination (sensor switch) Role Remarks 3.3V GY-SHT31-D: VIN Sensor power supply 3.3V supplied GND GY-SHT31-D: GND Ground Negative power supply GPIO 5 (SCL) GY-SHT31-D: SCL I2C clock signal Communication timing GPIO 4 (SDA) GY-SHT31-D: SDA I2C data signal For sending and receiving temperature and humidity data GPIO 9 Tact switch foot ① Collection mode detection Check the status at startup GND Tact switch foot ② Ground Set to LOW when the switch is pressed *Note: Connect the USB cable from the solar controller to the USB Type-C port of ESP32-C3.

## 4. Operation specifications (software processing flow)

### [Normal: Logger mode]

1. **Wake up:** Built-in timer automatically wakes up every hour.
2. **Initialization:** LittleFS and SHT31 sensor initialization.
3. **Data measurement:**Measures temperature and humidity.
4. **Save data: Add data to the end of **`log.csv` (format: serial number, temperature, humidity).
5. **Bedtime:** Set a timer for 1 hour (3,600 seconds) and immediately go into deep sleep.

### [When collecting: Wi-Fi mode]

1. **Start trigger:** While pressing the switch connected to GPIO 9, press the "EN (reset) button" on the main unit.
2. **Mode branching:** Immediately after startup, it detects that GPIO 9 is LOW and starts as a Wi-Fi base unit.
3. **Wi-Fi activation:** SSID: `Hata_Logger` / PASS: `12345678` Expand the access point.
4. **Web server startup:**Start the web server on CODE_PH_0__.
5. **Smartphone connection/collection:**
   - Connect your smartphone's Wi-Fi to `Hata_Logger`.
   - Access `http://192.168.4.1` in your browser.
   - Execute "CSV download" and "data deletion" from the buttons on the screen.

6. **How ​​to exit:** After collection is complete, press the "EN button" again without pressing the switch (return to normal mode).

## 5. Special notes/long-term operational measures

- **Operation not confirmed:** GY-SHT31-D has not been obtained and operation has not been verified.
- **Time accuracy:** Since an external RTC (clock module) is omitted, it is operated on the assumption that there will be a cumulative error (discrepancy) of about 1 hour per week due to the temperature characteristics of the built-in timer (count back against the actual time at the time of collection).
- **Sensor protection:** When soldering, protect the sensor with masking tape to prevent solder smoke (flux gas) from entering the hole in the center of the sensor.
- **Moisture-proofing/Insect-proofing:** Apply a moisture-proofing agent such as Hayacoat to the board (other than the sensor) to prevent condensation. Completely fill the hole for the wire that runs from the case to the sensor with putty to prevent insects from entering.
- **Anti-rust:** The USB connection between the solar controller and ESP32-C3 should be sealed with self-adhesive tape to prevent corrosion due to moisture.

## 6. Resources

- **GitHub repository:** [https://github.com/amekusa03/esp32-field-logger](https://github.com/amekusa03/esp32-field-logger)
