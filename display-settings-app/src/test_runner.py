# ------------------------------------------------------------
# Test Runner Module
# ------------------------------------------------------------
# PURPOSE:
# This module orchestrates the entire display validation flow.
#
# It does NOT perform validation itself.
# Instead, it:
# - Controls execution
# - Tracks progress
# - Collects results
# - Measures timing
# - Handles retry phase
# - Restores system state
# ------------------------------------------------------------

from datetime import datetime
from display_utils import get_unique_modes, apply_mode, get_current_mode
from validator import validate_mode
from logger import log, init_csv


def run_all_tests(limit=None, single_mode=None):
    """
    Run full display validation.

    PARAMETERS:
    - limit (int, optional):
        Limits number of modes to test (useful for quick testing)

    - single_mode (tuple, optional):
        (width, height, frequency)
        Runs only one specific mode

    HIGH LEVEL FLOW:
    1. Initialize system
    2. Capture original display state
    3. Fetch supported modes
    4. Apply single mode filter (if provided)
    5. Optionally limit scope
    6. Run validation (Phase 1)
    7. Retry failed modes (Phase 2)
    8. Restore original display
    """

    # ========================================================
    # STEP 1: INITIALIZATION
    # ========================================================

    log("===== STARTING DISPLAY VALIDATION =====")

    # Initialize CSV file (overwrite previous results)
    # WHY:
    # - Ensures fresh reporting for each execution
    init_csv()

    # Capture start time for INITIAL RUN ONLY
    overall_start = datetime.now()

    # ========================================================
    # STEP 2: SAVE CURRENT DISPLAY STATE
    # ========================================================

    # Store current display configuration
    original_mode = get_current_mode()

    # ========================================================
    # STEP 3: FETCH SUPPORTED MODES
    # ========================================================

    modes = get_unique_modes()

    # ========================================================
    # STEP 4: SINGLE MODE FILTER (OPTIONAL)
    # ========================================================

    # WHY:
    # - Allows testing only one specific mode
    # - Useful for debugging and targeted validation
    if single_mode:

        target_width, target_height, target_freq = single_mode

        filtered = []

        # Search for matching mode
        for m in modes:
            if (
                m["width"] == target_width and
                m["height"] == target_height and
                m["frequency"] == target_freq
            ):
                filtered.append(m)

        # If no match found → stop execution
        if not filtered:
            log("Specified mode not found in supported modes.")
            return

        modes = filtered

        log(f"Running single mode: {target_width}x{target_height}@{target_freq}")

    # ========================================================
    # STEP 5: LIMIT TEST SCOPE (OPTIONAL)
    # ========================================================

    # Apply limit ONLY if single_mode is not used
    # WHY:
    # - Single mode should always take priority
    if limit is not None and not single_mode:
        modes = modes[:limit]
        log(f"Running limited test: first {limit} modes")

    total = len(modes)

    pass_count = 0
    fail_count = 0

    # Store failed modes for retry phase
    failed_modes = []

    # ========================================================
    # STEP 6: MAIN VALIDATION LOOP (PHASE 1)
    # ========================================================

    for index, mode in enumerate(modes, start=1):

        progress_percent = (index / total) * 100
        log(f"\n[{index}/{total}] ({progress_percent:.1f}%) Running test...")

        result = validate_mode(mode)

        if result:
            pass_count += 1
        else:
            fail_count += 1
            failed_modes.append(mode)

    # ========================================================
    # STEP 7: MAIN EXECUTION SUMMARY
    # ========================================================

    log("\n===== TEST SUMMARY =====")
    log(f"Total Modes: {total}")
    log(f"Passed: {pass_count}")
    log(f"Failed: {fail_count}")

    # ========================================================
    # STEP 8: MAIN EXECUTION TIME
    # ========================================================

    overall_end = datetime.now()
    total_duration = (overall_end - overall_start).total_seconds()

    log("\n===== EXECUTION TIME =====")
    log(f"Initial Run Duration: {total_duration:.2f} seconds")

    # ========================================================
    # STEP 9: RETRY FAILED MODES (PHASE 2)
    # ========================================================

    if failed_modes:

        log("\n===== RETRYING FAILED MODES =====")

        retry_start = datetime.now()

        retry_pass = 0
        retry_fail = 0

        for index, mode in enumerate(failed_modes, start=1):

            log(f"\n[Retry {index}/{len(failed_modes)}] Retesting failed mode...")

            result = validate_mode(mode)

            if result:
                retry_pass += 1
            else:
                retry_fail += 1

        retry_end = datetime.now()
        retry_duration = (retry_end - retry_start).total_seconds()

        log("\n===== RETRY SUMMARY =====")
        log(f"Retried: {len(failed_modes)}")
        log(f"Passed After Retry: {retry_pass}")
        log(f"Still Failed: {retry_fail}")

        log("\n===== RETRY TIME =====")
        log(f"Retry Duration: {retry_duration:.2f} seconds")

    else:
        log("\nNo failed modes to retry.")

    # ========================================================
    # STEP 10: RESTORE ORIGINAL DISPLAY SETTINGS
    # ========================================================

    log("\nRestoring original display settings...")

    success, msg = apply_mode(original_mode)

    if success:
        log("Original display restored successfully")
    else:
        log(f"Restore failed - {msg}")