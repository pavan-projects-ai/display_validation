# Import Windows API modules from pywin32 package
import win32api
import win32con


def get_supported_modes():
    """
    This function fetches ALL display modes supported by the system.

    Each mode includes:
    - Resolution (width, height)
    - Color depth (bits per pixel)
    - Refresh rate (Hz)

    These modes come from:
    - Monitor (EDID)
    - GPU driver
    """

    modes = []  # List to store all modes
    i = 0       # Index used to iterate through modes

    while True:
        try:
            # Get display mode at index 'i'
            dm = win32api.EnumDisplaySettings(None, i)

            # Extract important fields and store in dictionary
            mode = {
                "width": dm.PelsWidth,             # Screen width (e.g., 1920)
                "height": dm.PelsHeight,           # Screen height (e.g., 1080)
                "bits": dm.BitsPerPel,             # Color depth (usually 32)
                "frequency": dm.DisplayFrequency   # Refresh rate (e.g., 60Hz)
            }

            modes.append(mode)  # Add mode to list

            i += 1  # Move to next mode index

        except:
            # When no more modes exist, EnumDisplaySettings throws exception
            # We break the loop here
            break

    return modes


def get_unique_modes():
    """
    Remove duplicate modes.

    Sometimes Windows returns repeated modes,
    so we filter them using a set.
    """

    seen = set()   # To track unique combinations
    unique = []    # Final filtered list

    for m in get_supported_modes():

        # Create unique key for each mode
        key = (m["width"], m["height"], m["bits"], m["frequency"])

        # Add only if not already seen
        if key not in seen:
            seen.add(key)
            unique.append(m)

    return unique


def apply_mode(mode):
    """
    Apply a selected display mode safely.

    Steps:
    1. Load current display settings
    2. Update with selected mode values
    3. Test configuration (CDS_TEST)
    4. Apply if valid
    """

    # Get current display configuration
    devmode = win32api.EnumDisplaySettings(
        None,
        win32con.ENUM_CURRENT_SETTINGS
    )

    # Set new resolution
    devmode.PelsWidth = mode["width"]
    devmode.PelsHeight = mode["height"]

    # Set color depth
    devmode.BitsPerPel = mode["bits"]

    # Set refresh rate
    devmode.DisplayFrequency = mode["frequency"]

    # Tell Windows which fields we are modifying
    devmode.Fields = (
        win32con.DM_PELSWIDTH |        # Width
        win32con.DM_PELSHEIGHT |       # Height
        win32con.DM_BITSPERPEL |       # Color depth
        win32con.DM_DISPLAYFREQUENCY   # Refresh rate
    )

    # ---------------- TEST PHASE ---------------- #

    # Validate configuration without applying it
    result = win32api.ChangeDisplaySettings(
        devmode,
        win32con.CDS_TEST
    )

    # If not supported → return error
    if result != win32con.DISP_CHANGE_SUCCESSFUL:
        return False, "Unsupported configuration ❌"

    # ---------------- APPLY PHASE ---------------- #

    # Apply actual display settings
    result = win32api.ChangeDisplaySettings(devmode, 0)

    # Check result
    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        return True, "Display settings applied successfully ✅"
    else:
        return False, f"Failed with error code: {result}"