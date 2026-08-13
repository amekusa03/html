# I created a GUI filer with music management function.

2026.06.28 ・Python / PySide6

---

## motive

Based on the previous article's ``Python GUI filer template'', I created ``PythonpicMusic'', a hybrid file manager application that also has automatic music library organization and management functions.

In addition to hierarchical browsing using a normal file system, we aimed for a system that would recursively scan a large amount of media files, display a flat list based on metadata, and automatically organize the folder structure in conjunction with tag editing.

---

## composition

It follows a design that clearly separates roles and keeps the GUI and logic loosely coupled.

**Model — `BaseNodeObject.py`**
Data model definition for files, images, and MP3 objects. By using a pure Python implementation that does not depend on PySide6's `QObject`, we completely prevent memory and thread collisions (core dumps) during scan/read processing from another thread. `PythonSignal`, which maintains the same writing style as Qt signal slots, has been created in-house to supplement it.

**Repository — `FilerRepository.py` & `MusicFilerRepository.py`**
Encapsulates file operations and scanning processing. The base `FilerRepository` is responsible for basic CRUD operations (non-recursive loading, etc.), and the inherited `MusicFilerRepository` implements the music domain logic unique to this app, such as media recursive scanning, ID3 tag analysis, and automatic cleanup.

**UI — `main.py`**
A desktop GUI that allows you to switch between a normal hierarchical display mode and a flat display (library view) that recursively lists media. It uses the Tokyo Night theme and uses asynchronous thread processing to load thousands to tens of thousands of music files without freezing the UI.

---

## Main features

### 1. Hierarchical display mode (standard filer)

- Browse folder hierarchy. It uses non-recursive loading using `os.scandir`, so even huge folders open instantly without any delay.

### 2. Flat display mode (Library view)

- Recursively scans media files under the specified folder and displays a list of ID3 metadata (artist, album, title, etc.) in a grid.

### 3. ID3 tag editing and library automatic organization

- MP3 tag editing dialog.

- The file is automatically moved to `[ライブラリパス]/[アーティスト名]/[アルバム名]/[ファイル名]` when the tag is saved. Automatically recursively cleans up empty old folders.

### 4. Preview function

- Thumbnail previews of images and automatic parsing and drawing of cover art embedded in MP3s.

---

## Project configuration

```bash
PythonpicMusic/
├── BaseNodeObject.py         # ピュアPythonによるデータモデル
├── FilerRepository.py        # 汎用リポジトリ
├── MusicFilerRepository.py   # 音楽専用リポジトリ
├── main.py                   # GUIアプリケーション
├── test_filer.py             # 自動テスト
└── README.md                 # 説明書
```

---

## until you move it

1. Create a virtual environment

   ```bash
   python3 -m venv venv
   ```

2. include dependencies

   ```bash
   ./venv/bin/pip install PySide6 mutagen
   ```

3. boot

   ```bash
   ./venv/bin/python main.py
   ```

4. Running the test

   ```bash
   xvfb-run ./venv/bin/python test_filer.py
   ```

---

Source: [github.com/amekusa03/PythonpicMusic](https://github.com/amekusa03/PythonpicMusic)
