
 # <------- Female Voice Code ----->

import tkinter as tk
import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Optional: Sets speed rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose a female voice (change index if necessary)
    engine.say(message)
    engine.runAndWait()

def Login():
    userid = username_entry.get()
    password = password_entry.get()

    # You can add your own validation logic here
    if userid == "Hacker@85" and password == "08052008":
        speak("Access granted!")
        parent.destroy()  # Close the application window
    else:
        speak("Access denied.")

# Create the main window
parent = tk.Tk()
parent.title("Login Form")

# Adjust window size and position (optional)
parent.geometry("300x200+500+300") 

# Create and place the username label and entry
username_label = tk.Label(parent, text="User ID:")
username_label.pack(pady=10)

username_entry = tk.Entry(parent)
username_entry.pack(pady=5)

# Create and place the password label and entry
password_label = tk.Label(parent, text="Password:")
password_label.pack(pady=10)

password_entry = tk.Entry(parent, show="*")  # Show asterisks for password
password_entry.pack(pady=5)

# Create and place the login button
login_button = tk.Button(parent, text="Login", command=Login)
login_button.pack(pady=10)

# Run the main loop
parent.mainloop()


