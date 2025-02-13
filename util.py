import tkinter as tk
from tkinter import messagebox

def get_button(window, text, bg_color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground='black',
        activeforeground='white',
        fg=fg,
        bg=bg_color,
        command=command,
        height=2,
        width=15,
        font=('Helvetica bold', 14)
    )
    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=('sans-serif', 14), justify='left')
    return label

def get_entry_text(window):
    input_text = tk.Text(
        window,
        height=2,
        width=15,
        font=('Arial', 14)
    )
    return input_text

def msg_box(title, description):
    messagebox.showinfo(title, description)