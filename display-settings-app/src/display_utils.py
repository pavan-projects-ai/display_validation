# ------------------------------------------------------------
# Display Utilities Module
# ------------------------------------------------------------
# PURPOSE:
# This module handles all low-level display operations using
# Windows APIs.
#
# Responsibilities:
# 1. Fetch supported display modes
# 2. Remove duplicate modes
# 3. Get current display configuration
# 4. Apply display modes safely
#
# NOTE:
# This module directly interacts with GPU driver via Windows API
# ------------------------------------------------------------

import win32api
import win32con


# ============================================================
# FUNCTION: get_supported_modes
# ============================================================
def get_supported_modes():
    """
    Fetch all display modes supported by the system.

    SOURCE:
    - GPU driver
    - Monitor capabilities (via EDID indirectly)

    RETURNS:
    - List of dictionaries containing:
        width, height, color depth, refresh rate
    """

    # List to store all modes
    # WHY:
    # - Maintains order
    # - Easy to iterate later
    modes = []

    i = 0  # Index to iterate through modes

    while True:
        try:
            # Fetch display mode using index
            dm = win32api.EnumDisplaySettings(None, i)

            # Store mode details
            mode = {
                "width": dm.PelsWidth,             # Horizontal resolution
                "height": dm.PelsHeight,           # Vertical resolution
                "bits": dm.BitsPerPel,             # Color depth (bits per pixel)
                "frequency": dm.DisplayFrequency   # Refresh rate (Hz)
            }

            modes.append(mode)
            i += 1  # Move to next mode

        except:
            # No more modes available → exit loop
            break

    return modes


# ============================================================
# FUNCTION: get_unique_modes
# ============================================================
def get_unique_modes():
    """
    Remove duplicate display modes.

    WHY duplicates occur:
    - Windows API may return repeated entries
    - Same mode may appear multiple times internally

    APPROACH:
    - Use SET for fast duplicate detection
    - Use LIST to maintain ordered results
    """

    # Set used for tracking unique mode combinations
    # WHY:
    # - Fast lookup (O(1))
    # - Prevents duplicates efficiently
    # - Requires immutable type → tuple is used
    seen = set()

    # List used to store final unique modes
    # WHY:
    # - Maintains order of modes
    # - Used later for validation loop
    unique = []

    for m in get_supported_modes():

        # Create tuple as unique identifier
        # WHY:
        # - Tuple is immutable → required for set
        # - Represents complete display mode
        key = (m["width"], m["height"], m["bits"], m["frequency"])

        # Check if mode already processed
        if key not in seen:
            seen.add(key)      # Track in set
            unique.append(m)   # Store in list

    return unique


# ============================================================
# FUNCTION: get_current_mode
# ============================================================
def get_current_mode():
    """
    Fetch current active display mode.

    WHY:
    - Needed to restore original display after testing
    """

    dm = win32api.EnumDisplaySettings(
        None,
        win32con.ENUM_CURRENT_SETTINGS
    )

    return {
        "width": dm.PelsWidth,
        "height": dm.PelsHeight,
        "bits": dm.BitsPerPel,
        "frequency": dm.DisplayFrequency
    }


# ============================================================
# FUNCTION: apply_mode
# ============================================================
def apply_mode(mode):
    """
    Apply a display mode safely.

    STEPS:
    1. Update display configuration
    2. Validate using CDS_TEST
    3. Apply if valid

    WHY CDS_TEST:
    - Prevents applying unsupported modes
    - Ensures driver accepts configuration
    """

    # Get current display settings structure
    devmode = win32api.EnumDisplaySettings(
        None,
        win32con.ENUM_CURRENT_SETTINGS
    )

    # --------------------------------------------------------
    # STEP 1: Update display parameters
    # --------------------------------------------------------
    devmode.PelsWidth = mode["width"]
    devmode.PelsHeight = mode["height"]
    devmode.BitsPerPel = mode["bits"]
    devmode.DisplayFrequency = mode["frequency"]

    # Specify which fields are modified
    devmode.Fields = (
        win32con.DM_PELSWIDTH |
        win32con.DM_PELSHEIGHT |
        win32con.DM_BITSPERPEL |
        win32con.DM_DISPLAYFREQUENCY
    )

    # --------------------------------------------------------
    # STEP 2: VALIDATION (CDS_TEST)
    # --------------------------------------------------------
    result = win32api.ChangeDisplaySettings(
        devmode,
        win32con.CDS_TEST  # Test only (no actual apply)
    )

    # If validation fails → do not apply
    if result != win32con.DISP_CHANGE_SUCCESSFUL:
        return False, "Unsupported configuration"

    # --------------------------------------------------------
    # STEP 3: APPLY MODE
    # --------------------------------------------------------
    result = win32api.ChangeDisplaySettings(devmode, 0)

    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        return True, "Applied successfully"
    else:
        return False, f"Failed with code: {result}"