# I turned my old smartphone into a GPS logger for mountain climbing.

2026-08-14

## To protect the main terminal battery

When going into the mountains, I want to conserve the battery of my main smartphone as much as possible. This is because I want to avoid unnecessary wear and tear because I use it for contacting people or checking maps in case of an emergency. But at the same time, I also want to keep a log of my walking path.

There are existing apps and activity tracking services, but because of their multiple functions, they eat up too much battery and the screen is too busy. What I want is a simple mechanism that only retrieves location information once a minute and saves it in KML format.

Then you can turn your old smartphone sitting in your drawer into a dedicated GPS logger.

## Thorough and simple

There's no complicated logic whatsoever. Since I only need to add GPS coordinates every minute, I decided to quickly create one myself using Android Studio and AI assistant.

We focused on the following points.

- **Power saving design**: Location information acquisition interval is 1 minute by default. Unnecessary positioning has been minimized and screen display has been minimized.
- **Background recording**: Runs as a foreground service, ensuring recording continues even when the screen is off or the app is in the background.
- **Immediate event recording**: The coordinates at the moment you press the "Start", "Pause", "Resume", or "Stop" buttons are recorded immediately without waiting for a 1-minute interval.
- **Output in KML format**: Data saved is in standard KML format. It is also easy to import it to your PC and look back on your travel route.
- **Real-time display and name customization**: Acquired coordinates and status can be checked in real time on the screen, and the file name can be changed from the default start date and time.

## This is enough tools

It's much better for your mental health to let your old device take on a second life as a single-function logger, rather than fretting over the remaining battery life of your main device while taking logs.

We plan to have it move quietly as a companion while hiking in the mountains.

## sauce

[GitHub View](https://github.com/amekusa03/AndroidGPSKmlLogger)
