import tkinter as tk
from tkinter import ttk

# Function to handle submission
def submit():
    name = name_entry.get()
    age = age_entry.get()
    weight = weight_entry.get()
    notes = notes_entry.get("1.0", tk.END)
    
    # Display entered data
    display_label.config(text=f"Name: {name}\nAge: {age}\nWeight: {weight} kg\nNotes: {notes}")

# Create main window
root = tk.Tk()
root.title("User Information Form")
root.geometry("500x300")

# Left Frame for Input Fields
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Name Entry
name_label = tk.Label(left_frame, text="Name:")
name_label.pack(anchor='w')
name_entry = tk.Entry(left_frame)
name_entry.pack(fill='x')

# Age Entry
age_label = tk.Label(left_frame, text="Age:")
age_label.pack(anchor='w')
age_entry = tk.Entry(left_frame)
age_entry.pack(fill='x')

# Weight Entry
weight_label = tk.Label(left_frame, text="Weight (kg):")
weight_label.pack(anchor='w')
weight_entry = tk.Entry(left_frame)
weight_entry.pack(fill='x')

# Notes Entry
notes_label = tk.Label(left_frame, text="Notes:")
notes_label.pack(anchor='w')
notes_entry = tk.Text(left_frame, height=5, width=20)
notes_entry.pack(fill='x')

# Submit Button
submit_button = tk.Button(left_frame, text="Submit", command=submit)
submit_button.pack(pady=10)

# Right Frame for Displaying Data
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill='both', expand=True)

display_label = tk.Label(right_frame, text="", justify=tk.LEFT, anchor='w')
display_label.pack()

# Run the main loop
root.mainloop()