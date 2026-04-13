# 🖥️ Display Settings UI (Windows)

A simple Python-based GUI application to view and modify display settings such as **resolution**, **rotation**, and **color depth** using Windows APIs.

---

## 🚀 Features

* 📺 List all supported display resolutions
* 🔄 Change screen rotation (0°, 90°, 180°, 270°)
* 🎨 Modify color depth (16 / 24 / 32-bit)
* ✅ Safe validation before applying settings
* 🖥️ Simple and clean UI using Tkinter

---

## 🛠️ Tech Stack

* Python 3.x
* Tkinter (GUI)
* pywin32 (Windows API access)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/display-settings-app.git
cd display-settings-app
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python src/main.py
```

---

## ⚙️ How It Works

1. The application retrieves available display modes using:

   * `EnumDisplaySettings()`

2. User selects:

   * Resolution
   * Rotation
   * Color depth

3. Before applying settings:

   * Uses `ChangeDisplaySettings()` with `CDS_TEST` to validate

4. If valid:

   * Applies settings using Windows API

---

## 🧠 Architecture

```text
UI (Tkinter)
   ↓
Application Logic
   ↓
Windows API (pywin32)
   ↓
Graphics Driver
   ↓
GPU → Display
```

---

## ⚠️ Important Notes

* Works **only on Windows OS**
* Screen may flicker when applying settings (normal behavior)
* Unsupported configurations will be rejected safely

---

## 📸 Screenshot (Optional)

*Add your UI screenshot here*

---

## 🔮 Future Enhancements

* Multi-monitor support (`ChangeDisplaySettingsEx`)
* Refresh rate selection
* Restore previous settings option
* CLI version

---

## 📄 License

This project is open-source and free to use.
