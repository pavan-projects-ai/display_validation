# ------------------------------------------------------------
# Main Entry Point for Display Validation Framework
# ------------------------------------------------------------
# This file is responsible for:
# 1. Starting the validation process
# 2. Calling the test runner
# 3. Acting as the execution entry point of the application
# ------------------------------------------------------------


# Import the function that runs all validation tests
from test_runner import run_all_tests


# ------------------------------------------------------------
# Python Entry Point
# ------------------------------------------------------------
# This ensures that the code runs only when this file
# is executed directly (not when imported as a module)
# ------------------------------------------------------------
if __name__ == "__main__":

    # Print message to console for user awareness
    print("Starting Display Validation Framework...\n")

    # Call the main test runner function
    # This will:
    # - Fetch all supported display modes
    # - Apply each mode
    # - Validate success/failure
    # - Log results to file
    run_all_tests()

    # Print completion message
    print("\nDisplay Validation Completed. Check logs for results.")