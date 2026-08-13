# Android Auto Music Player

2026/05/21 / kotlin

I wanted to reuse my old smartphone as a music player, so I developed an android app.
We've also made it compatible with Android Auto so you can use it in your car.

## About this Project

You can play MP3 files by specifying a folder, and it also supports Android Auto.

Almost every step of the process, from design to code generation and debugging, was carried out in dialogue with Claude Code.
AI also took the lead in investigating and fixing issues such as Android Auto's artwork display and shuffle button issues.
The generated code is reviewed by humans and its operation is confirmed on actual machines.

## Key Features

- **Folder selection playback:** You can specify a folder and play MP3 files all at once.
- **Album art display:** Album art embedded in songs can be displayed on the screen.
- **Shuffle Play:** You can play songs in random order.
- **Search function:** You can narrow down your search by song title, artist name, or album name.
- **Background playback:** Playback can continue in the foreground service even if the app is closed.
- **Android Auto compatible:** Songs can be controlled from the in-car display.
- **Scan result caching:** Keeps startup quick and can be automatically updated when changing folders.

## Known Issues / Out of Scope

- **Google Assistant's voice operation (``Put 〇〇''):** Adding an intent filter and receiving processing have been implemented, but which app the Assistant delegates playback to depends on the OS's decision.
Substantive verification has not been possible as YouTube Music and Spotify may be prioritized and we cannot guarantee that users will be directed to this app.

## Resource

[View on GitHub](https://github.com/amekusa03/MusicPlayer)
