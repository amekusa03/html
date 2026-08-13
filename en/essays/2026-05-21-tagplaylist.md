# TagPlaylist Generator

2026/05/21 / Python / GUI / CLI

Automatically generate playlists by genre from MP3 tag information.

This is a tool developed to streamline the organization of your music library. Scans ID3 tags (genres) from a large number of MP3 files and automatically creates `.m3u` playlists for each genre. It supports both GUI and CLI, and exports playlists with relative paths for portability.

## Key Features

* **Automatic genre classification:** Classify based on TCON frame of ID3v2 tag.
* **Relative path generation:** Since it is written as a relative path from the playlist, it will not break even if you move the entire folder.
* **GUI/CLI compatible:** Equipped with a GUI that can be used with a drag-and-drop feel and a CLI that is convenient for automation.
* **Recursive scan:** Also searches all subfolders under the specified folder.

## Resource

[View on GitHub](https://github.com/amekusa03/tagplaylist)
