# ------------------------------------------------------------
# Validator Module
# ------------------------------------------------------------
# Responsibilities:
# 1. Apply display modes
# 2. Handle retry logic for failures
# 3. Track timing (start, end, duration)
# 4. Log results
# 5. Write structured results to CSV
#
# NOTE:
# This module focuses on validation logic only.
# It does NOT deal with how modes are fetched or stored.
# ------------------------------------------------------------

import time
from datetime import datetime
from display_utils import apply_mode
from logger import log, write_csv


# Maximum number of retries for a failed mode
# WHY:
# - Display mode application may fail temporarily due to timing or driver state
# - Retry improves reliability and avoids false failures
MAX_RETRIES = 2


def validate_mode(mode):
    """
    Validate a single display mode.

    Flow:
    1. Capture start time
    2. Apply mode
    3. Retry on failure
    4. Capture end time
    5. Calculate duration
    6. Log + store result
    """

    # --------------------------------------------------------
    # STEP 1: Capture start time
    # --------------------------------------------------------
    # WHY:
    # - Needed to measure how long a mode takes to apply
    # - Helps in performance and stability analysis
    start_dt = datetime.now()

    # Log the mode being tested
    log(f"Testing: {mode['width']}x{mode['height']} @{mode['frequency']}Hz")

    # Initialize retry counter
    attempt = 0

    # --------------------------------------------------------
    # STEP 2: Apply mode with retry logic
    # --------------------------------------------------------
    while attempt <= MAX_RETRIES:

        # Try applying the display mode
        success, msg = apply_mode(mode)

        # Allow display pipeline to stabilize
        # WHY:
        # - GPU + monitor need time to sync after mode change
        # - Without delay → flicker / unstable behavior
        time.sleep(2)

        # ----------------------------------------------------
        # SUCCESS CASE
        # ----------------------------------------------------
        if success:
            # Capture end time
            end_dt = datetime.now()

            # Calculate duration (in seconds)
            duration = (end_dt - start_dt).total_seconds()

            # Log success with attempt info
            log(f"PASS (attempt {attempt + 1})")

            # Write result to CSV
            # WHY:
            # - Structured reporting for analysis
            write_csv(
                mode,
                "PASS",
                f"{msg} (attempt {attempt + 1})",
                start_dt,
                end_dt,
                duration
            )

            return True

        # ----------------------------------------------------
        # FAILURE → RETRY
        # ----------------------------------------------------
        attempt += 1

        if attempt <= MAX_RETRIES:
            log(f"Retrying... (attempt {attempt + 1})")

            # Small delay before retry
            # WHY:
            # - Avoid immediate re-application issues
            time.sleep(1)

    # --------------------------------------------------------
    # FINAL FAILURE AFTER ALL RETRIES
    # --------------------------------------------------------

    # Capture end time
    end_dt = datetime.now()

    # Calculate total duration
    duration = (end_dt - start_dt).total_seconds()

    # Log failure
    log("FAIL after retries")

    # Write failure result to CSV
    write_csv(
        mode,
        "FAIL",
        f"{msg} after {MAX_RETRIES + 1} attempts",
        start_dt,
        end_dt,
        duration
    )

    return False