# I made my own Android SwitchBot app.

2026-08-13

## A common motivation: dissatisfaction with the original app

The Android SwitchBot app was a bit of a hassle for me. It has a two-step structure: select the remote control, then turn it on/off, so you can't use it quickly when you want to use it quickly. Having to tap the screen twice when you just want to turn off the lights while you're sleeping can be quite frustrating.

Therefore, I decided to use SwitchBot Open API v1.1 to create my own app to control smart home devices directly from Android.

![SmartSwitchBot](/en/essays/2026-08-13-smartswichbot.png)

## An example of the ritual of authentication

SwitchBot's API requires HMAC-SHA256 signed requests. I followed the same ritual last time when I implemented it on ESP32, but this time I will implement it on the Android (Kotlin) side. The process remains the same, combining a millisecond-accurate timestamp with a random nonce to generate the signature. The implementation itself is not difficult, but it can be a bit nerve-wracking since it immediately returns a 401 if even one value is off.

## Obsession with one step of operation

The UI uses a card-type design. A dedicated control panel changes depending on the type of device (bot, plug, air conditioner, TV, etc.), and only the necessary controls are displayed for each device. For an air conditioner, you can adjust the temperature and turn off the button; for a TV, you can simply set the channel, volume, and power; and for a bot or plug, simply turn it on and off. Registered scenes can also be executed with one tap.

API Token and Secret can be registered and updated from the in-app settings dialog and are saved in the device's DataStore. Troublesome settings only need to be done once.

In the end, the original goal of "controlling the device with a single tap" was achieved. It's a trivial thing, but I believe that the more trivial things are, the more important it is when it comes to things we use every day.

## sauce

[GitHub View](https://github.com/amekusa03/AndroidSmartSwitchbot)