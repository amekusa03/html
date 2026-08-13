# Cockpit Scope

2026/06/18 / kotlin

ELM327 / Real-time telemetry display application using smartphone sensors

## overview

An app that acquires vehicle OBD-II data (ELM327) via Bluetooth Classic and displays it as a time series graph. It also supports G-Force measurement using the smartphone's built-in acceleration sensor. We aim to create a telemetry display that specializes in visualizing driving.

## Main features

- Real-time multi-graph display (display multiple data on the same time axis)
- Get RPM, speed, throttle opening, water temperature, etc. via ELM327 adapter
- G-Force measurement using smartphone acceleration sensor (0.1G unit)
- Customization of display items and colors 
- Telemetry log storage function (placeholder)

## How to use

1. Pair with the ELM327 adapter from Android settings.
2. Launch the app and open "Display settings" from the toolbar settings.
3. Select the adapter to connect from "Select Bluetooth device".
4. Check the items you want to display and set colors as necessary.
5. When you return to the main screen, a connection will be attempted and real-time display will begin.

## Display item list

- Engine speed (RPM) 
- Vehicle speed (Speed) [km/h] 
- Accelerator opening (Throttle) [%] 
- Engine water temperature (Water Temp) [°C] 
- Voltage (Voltage) [V] (0.1V unit)
- Acceleration (G-Force) [G] (0.1G unit)
- Engine load (Load) [%]
- Intake manifold pressure (MAP) [kPa]
- Intake air amount (MAF) [g/s]

## Operation not confirmed

As of July 15, 2026, the OBD2 adapter I ordered from Amazon has not arrived, so I have not been able to confirm its operation in an actual vehicle.
I canceled my order and am planning to order a product that has a separate Technical Conformity Mark.

## Disclaimer

This app is intended as an auxiliary display while driving, and does not guarantee the accuracy of diagnosis or maintenance. It is dangerous to operate while driving, so be sure to operate in a safe place.

## Resource

[View on GitHub](https://github.com/amekusa03/cockpitScope)
