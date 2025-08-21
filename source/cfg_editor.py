import tkinter as tk
from tkinter import ttk, messagebox
from utils import parse_cfg, dump_cfg

def build_cfg_editor(container, cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        text = f.read()
    cfg_data = parse_cfg(text)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entries = {}

    def build_entries(data, parent_frame, path=()):
        for k, v in data.items():
            if isinstance(v, dict):
                lbl = ttk.Label(parent_frame, text=f"{'.'.join(path+(k,))}", font=("Arial", 11, "bold"))
                lbl.pack(anchor="w", pady=(8, 2))
                subframe = ttk.Frame(parent_frame)
                subframe.pack(fill="x", padx=20)
                build_entries(v, subframe, path+(k,))
            else:
                row = ttk.Frame(parent_frame)
                row.pack(fill="x", pady=2)
                lbl = ttk.Label(row, text=k, width=20)
                lbl.pack(side="left")
                entry = ttk.Entry(row)
                entry.insert(0, v)
                entry.pack(side="left", fill="x", expand=True)
                entries[path+(k,)] = entry

    build_entries(cfg_data, frame)

    def save_cfg_file():
        def update_dict(data, path=()):
            for k, v in data.items():
                if isinstance(v, dict):
                    update_dict(v, path+(k,))
                else:
                    entry = entries[path+(k,)]
                    data[k] = entry.get()
        update_dict(cfg_data)
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(dump_cfg(cfg_data))
        messagebox.showinfo("Saved", "CFG saved successfully.")

    save_btn = ttk.Button(frame, text="Save", command=save_cfg_file)
    save_btn.pack(pady=10)