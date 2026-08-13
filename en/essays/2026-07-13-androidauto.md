# Summary of vehicle information that can be obtained with Android Auto

I ordered OBD-II, but it was not delivered, so I looked into whether it was possible to obtain it from Android Auto.

2026-07-13 / Android Auto

## Basic vehicle information (CarInfo)

CarInfo allows you to obtain static specifications and dynamic status of a vehicle.

| Category | Information that can be obtained | Notes |
| :--- | :--- | :--- |
| **Vehicle model** | Manufacturer name (Make), model name (Model), year (Year) | `fetchModel()` |
| **Energy configuration** | Fuel type (gasoline, diesel, etc.), EV connector type | `fetchEnergyProfile()` |
| **Fuel/Battery** | Fuel remaining, battery remaining, low fuel warning, estimated cruising distance | `addEnergyLevelListener()` |
| **Running speed** | Actual speed (Raw Speed), meter display speed (Display Speed) | `addSpeedListener()` |
| **Distance** | Odometer (total mileage) | Available for Android Auto |
| **ETC/Toll road** | Toll road card insertion status, card type | `addTollListener()` |
| **Exterior dimensions** | Vehicle width, vehicle height, overall length, etc. | API Level 7 or later (mainly AAOS) |

## Sensor information (CarSensors)

CarSensors allows you to obtain the values ​​of physical sensors installed in a vehicle.

| Category | Information that can be obtained | Notes |
| :--- | :--- | :--- |
| **Accelerometer** | 3-axis acceleration data. |
| **Gyroscope** | 3-axis rotational speed data. |
| **Compass** | Direction (azimuth) of the vehicle. |
| **Location information (Location)** | Highly accurate location information obtained from the vehicle's GPS antenna. It may be more accurate than the GPS on your smartphone, or it may provide data that is effective for autonomous navigation (dead reckoning) in tunnels. |

## Air conditioning/client settings (CarClimate)

A relatively new feature available starting with CarApp API Level 5.

| Category | Information that can be obtained |
| :--- | :--- |
| **HVAC (air conditioner)** | Switching ON/OFF of AC, maximum cooling (Max AC), and internal air circulation. |
| **Fan** | Air volume level, blowing direction. |
| **Temperature Setting** | Set temperature inside the car. |
| **Defroster** | Front/rear anti-fog condition. |

## Notes on development

### Permissions

To obtain information, in addition to the declaration in `AndroidManifest.xml`, permission permission from the user is required at runtime.

* Example: `com.google.android.gms.permission.CAR_FUEL` (fuel information)
* Example: `com.google.android.gms.permission.CAR_SPEED` (speed information)

### Vehicle response status

Not all vehicles provide all data.
When acquiring data, it is necessary to check `CarValue.getStatus()` and check that it is `STATUS_SUCCESS`.

### API level

The available methods may be limited depending on the API level of the Car App Library you are using (for example, air conditioning is level 5 or higher).

## remarks

It was not possible to obtain the throttle opening/closing degree and engine speed, so we had no choice but to wait for the ODB-II to be delivered.

## sauce

[https://developer.android.com/training/cars/apps/library?hl=ja](https://developer.android.com/training/cars/apps/library?hl=ja)
