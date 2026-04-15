# ------------------------------------------------------------
# Test Runner Module
# ------------------------------------------------------------
# Responsibilities:
# 1. Control full validation execution
# 2. Initialize CSV reporting
# 3. Track progress of tests
# 4. Call validator for each mode
# 5. Maintain pass/fail counts
# 6. Measure total execution time
# 7. Restore original display settings
# ------------------------------------------------------------

# Import required modules
from datetime import datetime
from display_utils import get_unique_modes, apply_mode, get_current_mode
from validator import validate_mode
from logger import log, init_csv


def run_all_tests():
    """
    Main function to execute display validation for all supported modes.

    Flow:
    1. Initialize logging and CSV
    2. Save current display mode
    3. Fetch supported modes
    4. Iterate and validate each mode
    5. Track results
    6. Print summary
    7. Restore original display
    """

    # ---------------- INITIALIZATION ---------------- #

    log("===== STARTING DISPLAY VALIDATION =====")

    # Initialize CSV file (overwrite previous results)
    init_csv()

    # Record overall start time
    overall_start = datetime.now()

    # Save current display mode (for restore later)
    original_mode = get_current_mode()

    # Fetch all supported display modes
    modes = get_unique_modes()

    total = len(modes)  # Total number of modes

    # Counters for results
    pass_count = 0
    fail_count = 0

    # ---------------- TEST EXECUTION LOOP ---------------- #

    for index, mode in enumerate(modes, start=1):

        # Calculate progress percentage
        progress_percent = (index / total) * 100

        # Log progress
        log(f"\n[{index}/{total}] ({progress_percent:.1f}%) Running test...")

        # Validate current mode
        result = validate_mode(mode)

        # Update counters
        if result:
            pass_count += 1
        else:
            fail_count += 1

    # ---------------- SUMMARY ---------------- #

    log("\n===== TEST SUMMARY =====")
    log(f"Total Modes: {total}")
    log(f"Passed: {pass_count}")
    log(f"Failed: {fail_count}")

    # ---------------- EXECUTION TIME ---------------- #

    # Record overall end time
    overall_end = datetime.now()

    # Calculate total duration in seconds
    total_duration = (overall_end - overall_start).total_seconds()

    log("\n===== EXECUTION TIME =====")
    log(f"Start Time: {overall_start}")
    log(f"End Time: {overall_end}")
    log(f"Total Duration: {total_duration:.2f} seconds")

    # ---------------- RESTORE ORIGINAL MODE ---------------- #

    log("\nRestoring original display settings...")

    # Apply original display settings
    success, msg = apply_mode(original_mode)

    if success:
        log("Original display restored successfully ✅")
    else:
        log(f"Restore failed ❌ - {msg}")