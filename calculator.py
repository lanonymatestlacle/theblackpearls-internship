import tkinter as tk
from tkinter import messagebox
import math

# Function to handle button click
def on_button_click(char):
    if char == '=':
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    elif char == 'C':
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, char)

# Function for square root
def sqrt():
    try:
        value = float(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(math.sqrt(value)))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Function for exponentiation
def exp():
    entry.insert(tk.END, '**')

# Function for memory recall
def mem_recall():
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(memory))

# Function for memory save
def mem_save():
    global memory
    try:
        memory = eval(entry.get())
        messagebox.showinfo("Memory", "Value saved to memory")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Initialize memory
memory = 0

# Create the main window
root = tk.Tk()
root.title("theblackpearls-Calculator")
root.geometry("400x500")
root.configure(bg="#2e2e2e")

# Entry widget for displaying calculations
entry = tk.Entry(root, font=("Arial", 24), bg="#1e1e1e", fg="#ffffff", borderwidth=0, justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

# Buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
    'C', '√', '**', 'M'
]

# Create and place buttons
row_val = 1
col_val = 0
for char in buttons:
    if char == '√':
        button = tk.Button(root, text=char, font=("Arial", 18), command=sqrt, bg="#1e1e1e", fg="#ffffff", activebackground="#333333")
    elif char == '**':
        button = tk.Button(root, text=char, font=("Arial", 18), command=exp, bg="#1e1e1e", fg="#ffffff", activebackground="#333333")
    elif char == 'M':
        mem_menu = tk.Menu(root, tearoff=0)
        mem_menu.add_command(label="Recall", command=mem_recall)
        mem_menu.add_command(label="Save", command=mem_save)
        button = tk.Menubutton(root, text=char, font=("Arial", 18), relief='raised', bg="#1e1e1e", fg="#ffffff", activebackground="#333333", menu=mem_menu)
    else:
        button = tk.Button(root, text=char, font=("Arial", 18), command=lambda ch=char: on_button_click(ch), bg="#1e1e1e", fg="#ffffff", activebackground="#333333")
    
    button.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew")
    
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Adjust grid weights for responsiveness
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

# Run the application
root.mainloop()
