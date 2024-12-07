import random
import time
import tkinter as tk
from tkinter import messagebox

# List of sentences for the typing test
SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing tests help improve speed and accuracy.",
    "Practice makes perfect when it comes to typing.",
    "Python is a versatile programming language.",
    "Learning to type faster can save you time."
]

# Global variables to track performance
start_time = None
best_score = {"wpm": 0, "accuracy": 0}

# Function to start the typing test
def start_typing_test():
    global start_time
    start_time = time.time()  # Record start time
    sentence = random.choice(SENTENCES)  # Pick a random sentence
    lbl_sentence.config(text=sentence)
    entry_text.delete(0, tk.END)  # Clear the entry box
    lbl_result.config(text="")  # Clear previous results

# Function to calculate results
def calculate_results():
    global best_score
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate time taken
    
    # Get the displayed sentence and user input
    given_sentence = lbl_sentence.cget("text")
    typed_sentence = entry_text.get()
    
    # Calculate words per minute (WPM)
    words_typed = len(typed_sentence.split())
    wpm = round(words_typed / (elapsed_time / 60))
    
    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(given_sentence, typed_sentence) if a == b)
    accuracy = round((correct_chars / len(given_sentence)) * 100) if given_sentence else 0
    
    # Update best score
    if wpm > best_score["wpm"]:
        best_score["wpm"] = wpm
    if accuracy > best_score["accuracy"]:
        best_score["accuracy"] = accuracy

    # Display results
    lbl_result.config(
        text=f"WPM: {wpm}\nAccuracy: {accuracy}%\nBest WPM: {best_score['wpm']}\nBest Accuracy: {best_score['accuracy']}%"
    )
    messagebox.showinfo("Results", f"Typing Test Complete!\n\nWPM: {wpm}\nAccuracy: {accuracy}%")

# GUI setup
root = tk.Tk()
root.title("Typing Test")
root.geometry("600x400")

# Widgets
lbl_title = tk.Label(root, text="Typing Test", font=("Arial", 24))
lbl_title.pack(pady=10)

lbl_sentence = tk.Label(root, text="", font=("Arial", 14), wraplength=500, justify="center")
lbl_sentence.pack(pady=20)

entry_text = tk.Entry(root, font=("Arial", 14), width=50)
entry_text.pack(pady=10)

btn_start = tk.Button(root, text="Start Test", font=("Arial", 14), command=start_typing_test)
btn_start.pack(pady=10)

btn_submit = tk.Button(root, text="Submit", font=("Arial", 14), command=calculate_results)
btn_submit.pack(pady=10)

lbl_result = tk.Label(root, text="", font=("Arial", 14))
lbl_result.pack(pady=20)

# Run the application
root.mainloop()
