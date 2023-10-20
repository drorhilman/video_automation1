import customtkinter as ctk


def create_slider(root, label, from_, to_, initial_value):
    frame = ctk.CTkFrame(root)  # Create a frame without padding
    frame.pack(padx=10, pady=2, fill=ctk.X, expand=True)  # Apply padding during packing

    ctk.CTkLabel(frame, text=label, font=("Arial", 12), width=80).pack(side=ctk.LEFT, padx=5, anchor='w')

    var = ctk.StringVar()
    var.set(initial_value)

    def update_slider(*args):
        val = var.get()
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
            slider.set(int(val))
        else:
            var.set(slider.get())

    def update_var(*args):
        var.set(int(slider.get()))

    validate_cmd = root.register(
        lambda value: value.isdigit()
        or (value.startswith("-") and value[1:].isdigit())
        or value == ""
    )
    entry = ctk.CTkEntry(
        frame,
        textvariable=var,
        width=80,
        validate="key",
        validatecommand=(validate_cmd, "%P"),
    )
    entry.pack(side=ctk.RIGHT, padx=5)

    slider = ctk.CTkSlider(frame, from_=from_, to=to_)
    slider.set(initial_value)
    slider.pack(fill=ctk.X, side=ctk.RIGHT, expand=True, padx=5)

    var.trace_add("write", update_slider)
    slider.bind("<B1-Motion>", lambda *args: update_var())  # Adjusted event binding

    return slider, var


def create_entry_with_label(
    root, label_text, initial_value, width=200, padx=10, pady=2
):
    container_frame = ctk.CTkFrame(root)
    container_frame.pack(fill=ctk.X, padx=padx, pady=pady)
    
    # Set label with fixed width of 100 pixels in the constructor
    label = ctk.CTkLabel(container_frame, text=label_text, width=100)
    label.grid(row=0, column=0, sticky='w', padx=(0, 5))
    
    entry = ctk.CTkEntry(container_frame, width=width)
    entry.insert(0, initial_value)
    entry.grid(row=0, column=1, sticky='ew')  # Make the entry expand horizontally

    # Configure the column containing the entry to expand and fill available space
    container_frame.grid_columnconfigure(1, weight=1)

    return entry




def center_window(root, width=400, height=450):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
