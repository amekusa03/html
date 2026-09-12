# The story of making a Bluetooth extension phone

2026-09-12 / Android / Bluetooth

## background

At home, I have several smartphones without SIMs, one for debugging, one for watching, and one for playing games. Since I had it lying around, I thought I could use it as an extension phone.

It's good to connect via Wi-Fi, but if you use Bluetooth, you can use it even if you go to a mountain farm and are a little far away. I also liked the fact that I didn't need an Internet connection or a router, and the devices connected directly to each other.

That's how I decided to create a P2P voice call app called ``BluePhone'' that uses Bluetooth's RFCOMM socket communication.

![BluePhone UI](essays/2026-09-12-homephone.png)

## Main features

- **P2P Bluetooth voice call**:
  - Direct connection via RFCOMM socket (no internet or Wi-Fi required).
  - Low-latency real-time two-way audio transmission using 16kHz 16-bit monaural PCM.
- **Incoming call notification**:
  - Full screen incoming call notification (Heads-up notification) when in background standby.
  - Ringtone playback and vibration.
  - You can instantly "reply" or "reject" from the notification or incoming call screen.
- **High quality audio engine**:
  - Howling reduction with echo canceller (AEC) & noise suppressor.
  - Microphone mute switching, speakerphone/earpiece switching.
  - Real-time waveform/meter display of microphone input volume.
- **Device management & customization**:
  - Displays your device's Bluetooth MAC address (can be copied with a tap).
  - Edit and save the nickname of the other person's smartphone (persistent with SharedPreferences).
  - Automatically obtain a list of paired devices and scan for peripheral devices.
- **Multilingual support**: Japanese/English (automatically switched depending on OS language settings).
- **Jetpack Compose UI**: A sophisticated design based on emerald green, and an app icon with a motif of a telephone receiver + Bluetooth signal wave.

## ending

When it was completed and I tried to install it on my family's smartphone, I received a message back.

"Was the house that big?"

……surely. It may be a big mountain farm, but your voice can be heard inside a normal house. I politely refrained from installing it on my family's smartphones.

## sauce

- [BluePhone](https://github.com/amekusa03/BluePhone)
