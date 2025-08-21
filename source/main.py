import tkinter as tk
from tkinter import ttk, messagebox
import os

from file_loader import load_files, on_open_item

BASE_PATH = os.path.expanduser("~/Documenti/piboso/mx bikes/mods/bikes")

root = tk.Tk()
root.title("MX Bikes Bike Tuner")
root.geometry("500x400")

columns = ("Name",)
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<Double-1>", lambda e: on_open_item(e, tree, root, BASE_PATH))

refresh_btn = ttk.Button(root, text="Refresh", command=lambda: load_files(tree, BASE_PATH))
refresh_btn.pack(pady=5)

load_files(tree, BASE_PATH)
root.mainloop()