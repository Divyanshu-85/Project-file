import time
import tkinter as tk

# Function to convert seconds into minutes and seconds format
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Countdown Timer Function
def countdown_timer(start_time):
    while start_time >= 0:
        formatted_time = format_time(start_time)
        label_time.config(text=formatted_time)  # Update the label with formatted time
        root.update()  # Update the GUI window
        time.sleep(1)  # Wait for 1 second
        start_time -= 1

    label_time.config(text="Time's up!")  # Display when the timer is up

# Start countdown when the button is clicked
def start_countdown():
    try:
        user_time = int(entry_time.get())  # Get the input time
        countdown_timer(user_time)  # Start the countdown
    except ValueError:
        label_time.config(text="Please enter a valid integer.")

# Initialize GUI window
root = tk.Tk()
root.title("Countdown Timer")
root.geometry("300x200")

# Label for instructions
label_instructions = tk.Label(root, text="Enter countdown time in seconds:")
label_instructions.pack(pady=10)

# Entry widget for the user to input the time
entry_time = tk.Entry(root, width=10)
entry_time.pack(pady=5)

# Button to start the countdown
start_button = tk.Button(root, text="Start Countdown", command=start_countdown)
start_button.pack(pady=10)

# Label to display the remaining time
label_time = tk.Label(root, text="00:00", font=("Helvetica", 24))
label_time.pack(pady=20)

# Run the tkinter main loop
root.mainloop()
