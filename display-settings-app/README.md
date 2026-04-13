# 🖥️ Display Validation Framework (Windows)

A Python-based **Display Validation Framework** that automatically tests all supported display modes, validates them using Windows APIs, and generates both **debug logs** and **CSV reports**.

---

## 🚀 Overview

This project evolved from a simple display settings UI into a **mini validation framework**, simulating real-world display validation workflows.

It ensures that only **driver-supported display modes** are applied and validated, avoiding unsupported configurations.

---

## ✨ Features

* 📺 Fetch all supported display modes using `EnumDisplaySettings`
* ⚙️ Apply display modes safely using `ChangeDisplaySettings`
* ✅ Validate configurations using `CDS_TEST`
* 🔁 Automated testing of all modes
* ⏱️ Progress indicator during execution
* 📊 CSV report generation (`results.csv`)
* 📄 Detailed log file (`results.txt`)
* 🔄 Restore original display settings after testing
* ⚡ Delay handling for display stabilization

---

## 🧱 Project Structure

```text
display-settings-app/
│
├── src/
│   ├── main.py              # Entry point
│   ├── display_utils.py     # Core display operations
│   ├── validator.py         # Mode validation logic
│   ├── test_runner.py       # Test execution engine
│   └── logger.py            # Logging + CSV reporting
│
├── logs/
│   ├── results.txt          # Debug logs
│   └── results.csv          # Structured report
│
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 🔄 Execution Flow

```text
main.py
   ↓
test_runner.py
   ↓
validator.py
   ↓
display_utils.py
   ↓
Windows API → GPU Driver → Display
```

---

### 🔍 Step-by-Step Process

1. Start the framework (`main.py`)
2. Initialize CSV logging
3. Save current display configuration
4. Fetch all supported display modes
5. Loop through each mode:

   * Apply mode
   * Validate using `CDS_TEST`
   * Wait for stabilization
   * Log result (PASS / FAIL)
   * Write to CSV
6. Generate summary report
7. Restore original display settings

---

## 🧠 Key Concepts

### ✅ Driver-Based Validation

Display modes are not manually combined. Instead, they are fetched using:

```python
EnumDisplaySettings()
```

This ensures only **valid, driver-supported configurations** are used.

---

### ✅ Safe Mode Application

Before applying any display mode:

```python
ChangeDisplaySettings(..., CDS_TEST)
```

This prevents unsupported configurations.

---

### ✅ Logging vs Reporting

| Type          | Purpose                         |
| ------------- | ------------------------------- |
| `results.txt` | Debugging & trace logs          |
| `results.csv` | Structured reporting & analysis |

---

## ▶️ How to Run

### 1. Navigate to project

```bash
cd display-settings-app/src
```

### 2. Activate virtual environment

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r ../requirements.txt
```

### 4. Run the framework

```bash
python main.py
```

---

## 📊 Sample Output

### Console

```text
===== STARTING DISPLAY VALIDATION =====

[1/10] Running test...
Testing: 1920x1080 @60Hz
PASS
```

---

### CSV (`logs/results.csv`)

```text
Width,Height,RefreshRate,Status,Message
1920,1080,60,PASS,Applied successfully
1280,720,60,FAIL,Unsupported configuration
```

---

## ⚠️ Important Notes

* Works only on **Windows OS**
* Screen flickering during execution is **normal**
* Taskbar may temporarily disappear due to display reset
* Delay is added to allow monitor stabilization
* Always restores original display settings after execution

---

## 🎯 Use Case

This project demonstrates:

* Display mode validation
* Driver-level API usage
* Automated testing workflows
* Logging and reporting mechanisms

---

## 🔮 Future Enhancements

* 🔁 Retry failed modes
* 🖥️ Multi-monitor validation
* 📈 Performance metrics tracking
* 🧾 EDID parsing (advanced)
* 🎛️ GUI dashboard

---

## 📄 License

This project is open-source and free to use.

---

## 🙌 Author

Developed as part of learning and implementing **Display Validation Engineering concepts**.
