# I created a template for a Python GUI filer.

2026.06.26 ・Python / PySide6

---

## motive

When writing a GUI application with PySide6, file system operations and UI drawing become mixed up before you know it. If the boundaries between where to read and where to display become blurred, you will end up having to make changes every time you add a small feature.

After repeating the same mistake several times, I decided to create a well-organized base class.

---

## composition

The roles were divided into three layers. Loosely coupling the GUI and logic makes it easier to test and extend.

**Model — `BaseNodeObject.py`**
Represent files and directories as objects. Information for the UI, such as icons, type names, and size display, is contained here.

**Repository — `FilerRepository.py`**
All reading and writing to the file system is consolidated here. Do not allow standard modules to be touched directly from the GUI layer.

**UI — `main.py`**
Desktop GUI made by PySide6. Implemented sidebar, sortable table, context menu, and details panel. The theme is Tokyo Night.

---

## use

With this base class, applications that handle files, such as image viewers, music library managers, and cloud sync filers, don't have to be rewritten from scratch. A GUI app that works as a sample is also included, so you can expand it as you like while checking its operation.

---

## Project configuration

```bash
PythonBaseClasses/
├── BaseNodeObject.py    # データモデル
├── FilerRepository.py   # リポジトリ
├── main.py              # GUIアプリ
└── README.md
```

---

## until you move it

1. Create a virtual environment

   ```bash
   python3 -m venv venv
   ```

2. include dependencies

   ```bash
   ./venv/bin/pip install PySide6
   ```

3. boot

   ```bash
   ./venv/bin/python main.py
   ```

---

Source:>[github.com/amekusa03/PythonBaseClasses](https://github.com/amekusa03/PythonBaseClasses)
