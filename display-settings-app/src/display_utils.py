# Import Windows API modules
import win32api
import win32con


def get_supported_modes():
    """
    Fetch all display modes supported by the system.

    These modes come from:
    - GPU driver
    - Monitor EDID (indirectly via driver)
    """

    modes = []
    i = 0

    while True:
        try:
            # Get mode using index
            dm = win32api.EnumDisplaySettings(None, i)

            # Store mode details
            mode = {
                "width": dm.PelsWidth,
                "height": dm.PelsHeight,
                "bits": dm.BitsPerPel,
                "frequency": dm.DisplayFrequency
            }

            modes.append(mode)
            i += 1

        except:
            # No more modes available
            break

    return modes


def get_unique_modes():
    """
    Remove duplicate modes.

    Windows may return duplicate entries,
    so we filter them.
    """

    seen = set()
    unique = []

    for m in get_supported_modes():
        key = (m["width"], m["height"], m["bits"], m["frequency"])

        if key not in seen:
            seen.add(key)
            unique.append(m)

    return unique


def get_current_mode():
    """
    Get current display configuration.

    Used to restore original settings after testing.
    """

    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)

    return {
        "width": dm.PelsWidth,
        "height": dm.PelsHeight,
        "bits": dm.BitsPerPel,
        "frequency": dm.DisplayFrequency
    }


def apply_mode(mode):
    """
    Apply a display mode safely.

    Steps:
    1. Set values
    2. Test using CDS_TEST
    3. Apply if valid
    """

    # Get current display structure
    devmode = win32api.EnumDisplaySettings(
        None,
        win32con.ENUM_CURRENT_SETTINGS
    )

    # Set new values
    devmode.PelsWidth = mode["width"]
    devmode.PelsHeight = mode["height"]
    devmode.BitsPerPel = mode["bits"]
    devmode.DisplayFrequency = mode["frequency"]

    # Specify modified fields
    devmode.Fields = (
        win32con.DM_PELSWIDTH |
        win32con.DM_PELSHEIGHT |
        win32con.DM_BITSPERPEL |
        win32con.DM_DISPLAYFREQUENCY
    )

    # ---------------- TEST ---------------- #

    result = win32api.ChangeDisplaySettings(
        devmode,
        win32con.CDS_TEST
    )

    if result != win32con.DISP_CHANGE_SUCCESSFUL:
        return False, "Unsupported configuration"

    # ---------------- APPLY ---------------- #

    result = win32api.ChangeDisplaySettings(devmode, 0)

    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        return True, "Applied successfully"
    else:
        return False, f"Failed with code: {result}"