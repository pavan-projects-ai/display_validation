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
* 🔁 Retry mechanism for failed modes (handles transient failures)
* ⏱️ Progress indicator with percentage during execution
* ⏱️ Per-mode timestamp tracking (start time, end time, duration)
* 📊 CSV report generation (`results.csv`) with detailed metrics
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
│   ├── validator.py         # Mode validation logic (retry + timing)
│   ├── test_runner.py       # Test execution engine (progress + summary)
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

   * Show progress (`[current/total] %`)
   * Apply mode
   * Validate using `CDS_TEST`
   * Retry on failure (up to configured attempts)
   * Wait for stabilization
   * Capture timing (start, end, duration)
   * Log result (PASS / FAIL)
   * Write detailed result to CSV

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

### ✅ Retry Handling

Transient failures during mode switching are handled using a retry mechanism, improving reliability.

---

### ✅ Timing Metrics

Each test captures:

* Start time
* End time
* Execution duration

This helps in analyzing performance and stability.

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

[1/10] (10.0%) Running test...
Testing: 1920x1080 @60Hz
PASS (attempt 1)
```

---

### CSV (`logs/results.csv`)

```text
Width,Height,ColorDepth,RefreshRate,Status,Message,StartTime,EndTime,DurationSec
1920,1080,32,60,PASS,Applied successfully,2026-04-15 12:01:00,2026-04-15 12:01:02,2.1
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
* Basic performance tracking using timing metrics

---

## 🔮 Future Enhancements

* 🎯 Limit test scope (run subset of modes)
* 🔁 Retry failed modes separately
* 🖥️ Multi-monitor validation
* 📈 Advanced performance metrics
* 🧾 EDID parsing (advanced)
* 🎛️ GUI dashboard

---

## 📄 License

This project is open-source and free to use.

---

## 🙌 Author

Developed as part of learning and implementing display validation concepts.
