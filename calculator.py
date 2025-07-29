import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import math

# Initialize window first
root = tk.Tk()
root.title("Tech Calculator")
root.geometry("350x520")
root.resizable(False, False)

# Load and blur the background image
original_image = Image.open("background.jpg")
blurred_image = original_image.resize((350, 520)).filter(ImageFilter.GaussianBlur(radius=4))
bg_photo = ImageTk.PhotoImage(blurred_image)

# Place background
canvas = tk.Canvas(root, width=350, height=520, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Globals
expression = ""
history = []

# Display
display = tk.Entry(root, font=("Consolas", 22, "bold"), bg="#000000", fg="#00ffff",
                   borderwidth=0, justify="right", insertbackground="#00ffff")
display.place(x=10, y=20, width=330, height=50)

# History box
history_box = tk.Listbox(root, font=("Consolas", 10), bg="#1a1a1a", fg="#39FF14",
                         height=3, borderwidth=0)
history_box.place(x=10, y=75, width=330, height=60)

# Functions
def press(value):
    global expression
    expression += str(value)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def clear():
    global expression
    expression = ""
    display.delete(0, tk.END)

def evaluate():
    global expression
    try:
        result = str(eval(expression, {"__builtins__": None}, math.__dict__))
        history.append(expression + " = " + result)
        update_history()
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = result
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")
        expression = ""

def update_history():
    history_box.delete(0, tk.END)
    for item in reversed(history[-3:]):
        history_box.insert(tk.END, item)

def on_key(event):
    char = event.char
    if char.isdigit() or char in "+-*/().":
        press(char)
    elif event.keysym == "Return":
        evaluate()
    elif event.keysym == "BackSpace":
        global expression
        expression = expression[:-1]
        display.delete(0, tk.END)
        display.insert(tk.END, expression)

# Button layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', 'C', '+'],
    ['(', ')', 'sqrt', 'sin'],
    ['cos', 'tan', 'log', 'pow']
]

# Create button grid
start_y = 140
for row in buttons:
    frame = tk.Frame(root, bg="", highlightthickness=0)
    frame.place(x=10, y=start_y, width=330, height=45)
    for char in row:
        if char == 'C':
            cmd = clear
        else:
            cmd = lambda x=char: press(x + '(') if x in ['sqrt', 'sin', 'cos', 'tan', 'log', 'pow'] else press(x)
        tk.Button(
            frame,
            text=char,
            command=cmd,
            font=("Consolas", 12, "bold"),
            bg="#101820",       # deep dark grey
            fg="#00ffff" if char.isdigit() else "#39FF14",
            activebackground="#1f1f1f",
            activeforeground="#00ffff",
            relief="flat"
        ).pack(side="left", expand=True, fill="both", padx=2, pady=2)
    start_y += 47

# Equals button
tk.Button(
    root,
    text="=",
    command=evaluate,
    font=("Consolas", 16, "bold"),
    bg="#1F51FF",  # Royal Blue
    fg="white",
    activebackground="#27408b",
    relief="flat"
).place(x=10, y=start_y + 5, width=330, height=50)

# Keyboard bindings
root.bind("<Key>", on_key)

# Start
root.mainloop()
