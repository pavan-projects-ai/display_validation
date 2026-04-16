# ------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------
# PURPOSE:
# This is the starting point of the application.
#
# Responsibilities:
# 1. Parse command-line arguments
# 2. Validate user input
# 3. Trigger test execution via test_runner
#
# NOTE:
# This file should remain lightweight (no business logic here)
# ------------------------------------------------------------

import sys
from test_runner import run_all_tests


# ============================================================
# FUNCTION: parse_mode
# ============================================================
def parse_mode(arg):
    """
    Parse mode string from CLI input.

    EXPECTED FORMAT:
        WIDTHxHEIGHT@REFRESH
        Example → 1920x1080@60

    RETURNS:
        (width, height, frequency) → tuple

    WHY:
    - Converts user-friendly input into structured data
    - Required for filtering supported modes
    """

    try:
        # Split resolution and refresh rate
        resolution, freq = arg.split("@")

        # Split width and height
        width, height = resolution.split("x")

        return int(width), int(height), int(freq)

    except Exception:
        print("Invalid mode format. Use: 1920x1080@60")
        return None


def main():
    """
    Entry point for display validation framework.

    Supports:
        python main.py              → run all modes
        python main.py 5            → run first N modes
        python main.py --mode 1920x1080@60 → run single mode
    """

    # ========================================================
    # STEP 1: INITIALIZE INPUT PARAMETERS
    # ========================================================

    limit = None         # Number of modes to test
    single_mode = None   # Specific mode (width, height, freq)

    # Extract CLI arguments (skip script name)
    args = sys.argv[1:]

    # ========================================================
    # STEP 2: PARSE COMMAND LINE ARGUMENTS
    # ========================================================

    i = 0

    while i < len(args):

        # ---------------- LIMIT ---------------- #
        # If argument is a number → treat as limit
        if args[i].isdigit():

            limit = int(args[i])

            # WHY:
            # - Allows faster execution
            # - Useful for quick testing

        # ---------------- SINGLE MODE ---------------- #
        elif args[i] == "--mode":

            # Ensure value exists after --mode
            if i + 1 < len(args):

                parsed = parse_mode(args[i + 1])

                if parsed:
                    single_mode = parsed
                else:
                    return  # stop if invalid format

                i += 1  # skip next argument

            else:
                print("Missing value for --mode")
                return

        # ---------------- INVALID INPUT ---------------- #
        else:
            print(f"Unknown argument: {args[i]}")
            return

        i += 1

    # ========================================================
    # STEP 3: START VALIDATION PROCESS
    # ========================================================

    # WHY:
    # - Keeps main.py clean and focused
    # - Delegates execution to test runner
    run_all_tests(limit=limit, single_mode=single_mode)


# ============================================================
# PROGRAM ENTRY CHECK
# ============================================================

if __name__ == "__main__":
    main()