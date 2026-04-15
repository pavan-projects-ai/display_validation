# ------------------------------------------------------------
# Validator Module
# ------------------------------------------------------------
# Responsibilities:
# 1. Apply display mode
# 2. Retry if failed
# 3. Track timing (start, end, duration)
# 4. Log results
# 5. Write results to CSV
# ------------------------------------------------------------

import time
from datetime import datetime
from display_utils import apply_mode
from logger import log, write_csv


# Maximum number of retries for each mode
MAX_RETRIES = 2


def validate_mode(mode):
    """
    Validate a single display mode with:
    - Retry logic
    - Timestamp tracking
    - CSV reporting
    """

    # --------------------------------------------------------
    # STEP 1: Capture start time (VERY IMPORTANT)
    # --------------------------------------------------------
    # This marks when the test for this mode begins
    start_dt = datetime.now()

    # Log current mode being tested
    log(f"Testing: {mode['width']}x{mode['height']} @{mode['frequency']}Hz")

    # Initialize retry counter
    attempt = 0

    # --------------------------------------------------------
    # STEP 2: Try applying mode (with retries)
    # --------------------------------------------------------
    while attempt <= MAX_RETRIES:

        # Apply display mode using Windows API
        success, msg = apply_mode(mode)

        # Wait for display to stabilize (prevents flickering issues)
        time.sleep(2)

        # ----------------------------------------------------
        # SUCCESS CASE
        # ----------------------------------------------------
        if success:
            # Capture end time
            end_dt = datetime.now()

            # Calculate duration in seconds
            duration = (end_dt - start_dt).total_seconds()

            # Log success with attempt number
            log(f"PASS (attempt {attempt + 1})")

            # Write result to CSV
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
            time.sleep(1)  # Small delay before retry

    # --------------------------------------------------------
    # FINAL FAILURE AFTER ALL RETRIES
    # --------------------------------------------------------

    # Capture end time
    end_dt = datetime.now()

    # Calculate duration
    duration = (end_dt - start_dt).total_seconds()

    # Log failure
    log("FAIL after retries")

    # Write failure to CSV
    write_csv(
        mode,
        "FAIL",
        f"{msg} after {MAX_RETRIES + 1} attempts",
        start_dt,
        end_dt,
        duration
    )

    return False