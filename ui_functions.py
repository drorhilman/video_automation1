import tkinter as tk
from tkinter import ttk


def create_slider(root, label, from_, to_, initial_value):
    frame = tk.Frame(root, padx=10, pady=2)  # Create a frame with padding
    frame.pack(padx=20, pady=2)

    ttk.Label(frame, text=label).pack(side=tk.LEFT)

    var = tk.StringVar()
    var.set(initial_value)

    def update_slider(val):
        if val == "":
            val = 0
        slider.set(float(val))

    def update_var(val):
        var.set(str(slider.get()))

    entry = ttk.Entry(frame, textvariable=var, width=10)
    entry.pack(side=tk.RIGHT)

    slider = ttk.Scale(frame, from_=from_, to_=to_, orient="horizontal")
    slider.set(initial_value)
    slider.pack(fill=tk.X, side=tk.RIGHT)

    var.trace_add("write", lambda *args: update_slider(var.get()))
    slider.bind("<Motion>", lambda *args: update_var(slider.get()))

    return slider, var


def create_entry_with_label(
    root, label_text, initial_value, width=200, padx=10, pady=2
):
    ttk.Label(root, text=label_text).pack(padx=padx, pady=pady)
    entry = ttk.Entry(root, width=width)
    entry.insert(0, initial_value)
    entry.pack(fill=tk.X, padx=padx, pady=pady)
    return entry


def center_window(root, width=500, height=400):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
