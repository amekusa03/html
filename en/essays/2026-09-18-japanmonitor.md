# Building a Real-Time Weather and Earthquake Monitor Using the Japan Meteorological Agency's Backend JSON

2026-09-18 / Python / PySide6 / Qt

## background

While I'm working, I sometimes find myself wondering about changes in the weather or rain clouds approaching. But opening my browser just to check the Japan Meteorological Agency's website is actually a bit of a hassle.

As many of you may already know, the Japan Meteorological Agency’s official website (jma.go.jp) has a front end that directly accesses lightweight JSON endpoints behind the scenes to retrieve data. This allows you to obtain official raw data directly in JSON format without having to perform any unnecessary HTML scraping.

So, I decided to create my own personal monitor that would run quietly in the system tray, stay out of the way most of the time, and only pop up with a quick notification when an alert or earthquake occurred.

## Japan Meteorological Agency Internal JSON Endpoint

The Japan Meteorological Agency's system is well-designed and allows for immediate data retrieval from the following endpoints.

- **Area Definition Master**: `https://www.jma.go.jp/bosai/common/const/area.json`
- **Weather Forecast (3rd/7th)**: `https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json`
- **Alerts, Advisories, and Special Alerts**: `https://www.jma.go.jp/bosai/warning/data/warning/{area_code}.json`
- **Real-Time Earthquake Alerts**: `https://www.jma.go.jp/bosai/quake/data/list.json`

No API key required, and the response is very fast.

## Implementation

We adopted **PySide6 (Qt for Python)** as our UI framework.

Even when the window is closed, the system continues to monitor in the background and is set to automatically send OS desktop notifications when alerts for heavy rain, strong winds, or other weather conditions are issued, or when a new earthquake occurs.

To ensure usability both domestically and internationally, we’ve enabled one-click switching between Japanese and English. This feature extends beyond the UI to automatically convert terms such as “Heavy Rain Warning” and seismic intensity notations via dictionary definitions. It also features a debug view that allows users to check and copy JSON payloads received from the Japan Meteorological Agency in real time, and incorporates a dark mode (QSS) that is easy on the eyes even during long work sessions.

## Publishing to GitHub

Since I’d finally gotten it into a presentable form, I organized the English documentation and published it on GitHub. Using the GitHub CLI (`gh`), you can complete everything from initializing the repository to publishing it and setting up topic tags in an instant.

```bash
gh repo create JapanMonitor --public --source=. --remote=origin \
  --description "Real-time Japan Meteorological Agency (JMA) weather forecast, emergency warning & earthquake monitor desktop app built with PySide6 (Qt)" \
  --push
```

When I set it to run automatically in the background upon logging into my PC, it became a reliable partner that never interfered with my work and provided accurate information only when I needed it.

## sauce

- [JapanMonitor (GitHub)](https://github.com/amekusa03/JapanMonitor)
