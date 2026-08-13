# Make your own “sky pattern sensor” with just one coin

## overview

This is a craft that uses a single CdS cell (photoconductive element) to create an illuminance sensor that works with Google Home. The total parts cost is less than 500 yen. I wrote Matter firmware on the ESP32-C6 to incorporate weather effects into the automatic lighting logic of my home's lights.

![Light sensor in Google Home app](__HTML_PH_0__)

### parts

|Part name|Price|Model number|
|:---|:---|:---|
|ESP32-C6|449 yen|Generic-RP030MERU6D5SHUL4A|
|CdS cell|40 yen|Standard photoconductive element such as GL5528|
|10kΩ resistor|1 yen|100 yen for 100 pieces|

### App overview

Matter compatible Ambient Light Sensor firmware using ESP32-C3. The voltage of the voltage divider circuit consisting of the CdS cell (photoconductive element) and fixed resistance is acquired by the ADC, converted to illuminance (Lux), and then provided on the network as the `IlluminanceMeasurement` attribute (`MeasuredValue`) of the Matter standard.

### Connection table (Pin Mapping)

| ESP32-C6 pin | Connection destination | Role |
| :--- | :--- | :--- |
| **3.3V** | One leg of CdS cell | Power supply |
| **GPIO1 (ADC1_CH1)** | Connection point between CdS cell and 10kΩ resistor | ADC voltage measurement input |
| **GND** | One leg of 10kΩ resistor | Ground |

## background

I wanted to make something, so I was looking for parts and found a CdS cell. Now that I think about it, the weather has been unseasonable lately, and I remembered that the lights that used to turn on automatically when the sun sets would turn on while it was still bright on cloudy or rainy days, or wouldn't turn on even when it got dark, so I ended up having to turn them on and off manually.

In that case, it would be better to make the judgment based on the ``actual brightness'' instead of the time. This project started when I decided to make my own optical sensor for Google Home using CdS cells.

## work process

1. We measured the CdS cell with a circuit tester and confirmed that the resistance value changes depending on the amount of light. Although it is new, it was discovered after being buried in a parts box for over 10 years, so the first thing to do is to make sure it is still alive.
2. Create a voltage divider circuit using a CdS cell and a 10kΩ resistor.
3. Connect the output of the voltage divider circuit to the ADC1_CH1 pin of ESP32-C3.
4. Write the illuminance sensor firmware for the Matter test to the ESP32-C3 and roughly calculate the Lux value by comparing it with the actual measurement value.
5. Create firmware for Google Home. Modified the sensor-related parts based on the code for converting the PC to Matter that was done previously.
6. Register the illuminance sensor to Google Home.
7. Display and check the illuminance sensor value on your smartphone.
8. Add automation logic to Google Home with YAML.

```yaml
metadata:
  name: 暗くなったら照明をつける
  description: 16:00~20:00に50lux以下となったら、照明を点灯し、「暗くなりました」と言います。
automations:
  - starters:
      - type: device.state.SensorState
        device: 光量 - リビングルーム
        # センサーの種類（LightLevel 等）の指定形式はデバイスによって異なる場合があります
        state: currentSensorStateData.LightLevel.rawValue
        lessThanOrEqualTo: 50
    condition:
      type: time.between
      after: 16:00
      before: 20:00
    actions:
      - type: device.command.OnOff
        devices:
          - ライト - リビングルーム
        on: true
      - type: assistant.command.Broadcast
        message: "暗くなりました"
```

## General review

It was completed in a few hours without any major problems. If I had to point out something I regret, I would say that I mistakenly connected the V3.3 and P3 pins during soldering. To prevent this from happening again, write down the units in your circuit diagram notes, like "V3.3" instead of "3.3", and above all, wear reading glasses👓😅

## sauce

[GitHub Repository](https://github.com/amekusa03/smartOptSensor)
