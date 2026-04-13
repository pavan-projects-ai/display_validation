# ------------------------------------------------------------
# Test Runner Module
# ------------------------------------------------------------
# Runs validation for all display modes
# ------------------------------------------------------------

from display_utils import get_unique_modes, apply_mode, get_current_mode
from validator import validate_mode
from logger import log, init_csv


def run_all_tests():
    """
    Main test execution function
    """

    # ---------------- INIT ---------------- #

    log("===== STARTING DISPLAY VALIDATION =====")

    # Initialize CSV file
    init_csv()

    # Save current display mode
    original_mode = get_current_mode()

    # Fetch all supported modes
    modes = get_unique_modes()

    total = len(modes)

    pass_count = 0
    fail_count = 0

    # ---------------- TEST LOOP ---------------- #

    for index, mode in enumerate(modes, start=1):

        # Progress indicator
        log(f"\n[{index}/{total}] Running test...")

        # Validate mode
        result = validate_mode(mode)

        if result:
            pass_count += 1
        else:
            fail_count += 1

    # ---------------- SUMMARY ---------------- #

    log("\n===== TEST SUMMARY =====")
    log(f"Total Modes: {total}")
    log(f"Passed: {pass_count}")
    log(f"Failed: {fail_count}")

    # ---------------- RESTORE ---------------- #

    log("\nRestoring original display settings...")

    success, msg = apply_mode(original_mode)

    if success:
        log("Original display restored successfully")
    else:
        log(f"Restore failed - {msg}")