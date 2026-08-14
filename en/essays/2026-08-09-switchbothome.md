# + Use SwitchBot Smart Home

2026-08-09

## overview

Last time, I made an illuminance sensor that works with Google Home using ESP32-C3.
Controlling lighting only once a day is too underspec.
The fact that no major problems occurred may be one of the reasons why it feels inadequate.

Therefore, this time I decided to set up a web server on the illuminance sensor ESP32-C3 and add SwitchBot Smart Home functionality.
Logically it should be possible, and I've been wanting to build a web server using ESP32 for some time, so I thought this was a good opportunity and decided to take on the challenge.

## A modest but unavoidable ritual to tap SwitchBot's API

SwitchBot's Open API v1.1 requires HMAC-SHA256 signed requests. It is a beautiful form of authentication that creates a signature by combining a token, a secret, a timestamp with millisecond precision, and a random nonce. I implemented this using mbedtls on the ESP32 side.

At first, I didn't understand it, and when I pressed a button on the Web UI, I kept getting "401 unauthorized" back, but once I correctly identified the cause and dealt with it, it worked smoothly. Since accurate timestamps are essential, I used NTP to synchronize the time with ESP32. The built-in clock of the microcontroller is unreliable, so I simply leave this to esp_netif_sntp. It's a simple process, but if it goes awry, all authentications seem to fail.

## A story about kindness: UI and fallbacks

I asked AI to create the web UI, and it created a translucent glass-like design (Glassmorphism). A real-time illuminance display banner and a SwitchBot home appliance operation card are combined on one screen. If you're going to go to the trouble of making one, you'll want to pay close attention to its appearance.

If Wi-Fi settings are not yet configured or the connection fails, it will automatically start up in SoftAP mode (`ESP32-SwitchBot-Setup`, `192.168.4.1`). Setting information is written to NVS so that once it is set, it will be remembered the next time it is started. You can also reset the entire Matter and NVS settings by holding down the GPIO9 button for 3 seconds. There are tricks, but when you get stuck due to a wrong setting, the escape route may be troublesome while you're making it, but it will always help you later.

## Did it finally move?

Technically, if you look into the ADC voltage divider circuit, HMAC signature, and Matter endpoint definition, you can find information somewhere. However, the work of putting all of this together into a moving object on a single ESP32-C3 takes a certain amount of effort, and gives me a mysterious sense of accomplishment. This time as well, I spent the whole day just trying to feel that sense of accomplishment.

![Switchbot Home](/en/essays/2026-08-09-switchbothome.png)

## sauce

- [GitHub View](https://github.com/amekusa03/esp32-switchbot-sensor-webapp)
