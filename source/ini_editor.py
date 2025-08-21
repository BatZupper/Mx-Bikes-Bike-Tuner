import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
from cfg_editor import build_cfg_editor

def open_bike_editor(root, name, ini_path, cfg_path):
    editor = tk.Toplevel(root)
    editor.title(f"Editing {name}")
    editor.geometry("700x600")

    notebook = ttk.Notebook(editor)
    notebook.pack(fill="both", expand=True)

    if ini_path and os.path.exists(ini_path):
        frame_ini = ttk.Frame(notebook)
        notebook.add(frame_ini, text="Info")
        build_ini_editor(frame_ini, ini_path)

    if cfg_path and os.path.exists(cfg_path):
        frame_cfg = ttk.Frame(notebook)
        notebook.add(frame_cfg, text="Stats")
        build_cfg_editor(frame_cfg, cfg_path)

def build_ini_editor(container, ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path, encoding="utf-8")

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entries = {}
    for section in config.sections():
        section_label = ttk.Label(frame, text=f"[{section}]", font=("Arial", 12, "bold"))
        section_label.pack(anchor="w", pady=(10, 2))

        for key, value in config.items(section):
            row = ttk.Frame(frame)
            row.pack(fill="x", pady=2)
            lbl = ttk.Label(row, text=key, width=20)
            lbl.pack(side="left")
            entry = ttk.Entry(row)
            entry.insert(0, value)
            entry.pack(side="left", fill="x", expand=True)
            entries[(section, key)] = entry

    def save_ini():
        for (section, key), entry in entries.items():
            config.set(section, key, entry.get())
        with open(ini_path, "w", encoding="utf-8") as f:
            config.write(f)
        messagebox.showinfo("Saved", "INI saved successfully.")

    save_btn = ttk.Button(frame, text="Save", command=save_ini)
    save_btn.pack(pady=10)