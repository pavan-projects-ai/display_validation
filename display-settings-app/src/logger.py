# ------------------------------------------------------------
# Logger Module
# ------------------------------------------------------------
# Responsibilities:
# 1. Log messages to console
# 2. Save logs to a text file (results.txt)
# 3. Save structured results to a CSV file (results.csv)
# 4. Support timestamp and duration tracking
# ------------------------------------------------------------

import os
import csv

# File paths for logs
LOG_FILE = "logs/results.txt"
CSV_FILE = "logs/results.csv"


def log(message):
    """
    Log a message to:
    1. Console (print)
    2. Text file (results.txt)

    UTF-8 encoding is used to support all characters.
    """

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Write message to text log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

    # Print message to console
    print(message)


def init_csv():
    """
    Initialize CSV file with header row.

    This will overwrite existing CSV file each run.
    """

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header includes all display mode + timing details
        writer.writerow([
            "Width",        # Screen width
            "Height",       # Screen height
            "ColorDepth",   # Bits per pixel
            "RefreshRate",  # Hz
            "Status",       # PASS / FAIL
            "Message",      # Result message
            "StartTime",    # Test start time
            "EndTime",      # Test end time
            "DurationSec"   # Time taken for test
        ])


def write_csv(mode, status, message, start_time, end_time, duration):
    """
    Append a test result to CSV file.

    Parameters:
    - mode: dictionary containing display mode details
    - status: PASS / FAIL
    - message: result message
    - start_time: test start timestamp
    - end_time: test end timestamp
    - duration: total time taken (seconds)
    """

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            mode["width"],      # Resolution width
            mode["height"],     # Resolution height
            mode["bits"],       # Color depth (important)
            mode["frequency"],  # Refresh rate
            status,             # PASS or FAIL
            message,            # Detailed message
            start_time,         # Start time
            end_time,           # End time
            duration            # Duration in seconds
        ])