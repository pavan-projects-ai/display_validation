# ------------------------------------------------------------
# Validator Module
# ------------------------------------------------------------
# Validates each display mode
# ------------------------------------------------------------

import time
from display_utils import apply_mode
from logger import log, write_csv


def validate_mode(mode):
    """
    Validate a single display mode
    """

    # Log current test
    log(f"Testing: {mode['width']}x{mode['height']} @{mode['frequency']}Hz")

    # Apply mode
    success, msg = apply_mode(mode)

    # Allow display to stabilize (IMPORTANT)
    time.sleep(2)

    # Log and write CSV
    if success:
        log("PASS")
        write_csv(mode, "PASS", msg)
        return True
    else:
        log(f"FAIL - {msg}")
        write_csv(mode, "FAIL", msg)
        return False