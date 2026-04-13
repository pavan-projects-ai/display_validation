# Import Tkinter for GUI
import tkinter as tk
from tkinter import ttk, messagebox

# Import our display functions
from display_utils import get_unique_modes, apply_mode


# ---------------- CREATE MAIN WINDOW ---------------- #

# Create main application window
root = tk.Tk()

# Set window title
root.title("Display Settings UI (Safe Mode)")

# Set window size
root.geometry("400x220")


# ---------------- FETCH SUPPORTED MODES ---------------- #

# Get all valid display modes from system
modes = get_unique_modes()

# Convert modes into readable strings for dropdown
# Example: "1920x1080 @60Hz"
mode_strings = [
    f'{m["width"]}x{m["height"]} @{m["frequency"]}Hz'
    for m in modes
]


# ---------------- UI COMPONENTS ---------------- #

# Label for dropdown
tk.Label(
    root,
    text="Select Display Mode",
    font=("Arial", 12)
).pack(pady=10)


# Variable to store selected value
mode_var = tk.StringVar()


# Dropdown (Combobox)
mode_dropdown = ttk.Combobox(
    root,
    textvariable=mode_var,   # Store selected value
    values=mode_strings,     # List of modes
    width=35
)

# Add dropdown to UI
mode_dropdown.pack()


# ---------------- APPLY BUTTON FUNCTION ---------------- #

def apply_settings():
    """
    This function is triggered when user clicks 'Apply'.

    Steps:
    1. Get selected dropdown value
    2. Match it with actual mode dictionary
    3. Call apply_mode()
    4. Show result message
    """

    # Get selected string
    selected = mode_var.get()

    # If user didn't select anything
    if not selected:
        messagebox.showwarning("Warning", "Please select a display mode")
        return

    # Find matching mode from list
    for m in modes:

        # Convert mode to string format
        text = f'{m["width"]}x{m["height"]} @{m["frequency"]}Hz'

        # Match selected value
        if text == selected:

            # Apply selected mode
            success, msg = apply_mode(m)

            # Show result to user
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

            return


# ---------------- APPLY BUTTON ---------------- #

tk.Button(
    root,
    text="Apply",
    command=apply_settings,  # Function to call on click
    bg="green",
    fg="white",
    padx=10,
    pady=5
).pack(pady=20)


# ---------------- START APPLICATION ---------------- #

# Keeps UI running
root.mainloop()