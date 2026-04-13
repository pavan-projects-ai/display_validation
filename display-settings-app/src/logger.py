# ------------------------------------------------------------
# Logger Module
# ------------------------------------------------------------
# Responsibilities:
# 1. Print logs to console
# 2. Write logs to text file
# 3. Write structured results to CSV file
# ------------------------------------------------------------

import os
import csv

LOG_FILE = "logs/results.txt"
CSV_FILE = "logs/results.csv"


def log(message):
    """
    Log message to console + text file
    """

    # Ensure logs folder exists
    os.makedirs("logs", exist_ok=True)

    # Write to text file using UTF-8 (supports all characters)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

    # Print to console
    print(message)


def init_csv():
    """
    Initialize CSV file with headers
    """

    os.makedirs("logs", exist_ok=True)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header row
        writer.writerow(["Width", "Height", "RefreshRate", "Status", "Message"])


def write_csv(mode, status, message):
    """
    Write each test result into CSV
    """

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            mode["width"],
            mode["height"],
            mode["frequency"],
            status,
            message
        ])