import os
from tkinter import messagebox
from ini_editor import open_bike_editor

def load_files(tree, base_path):
    tree.delete(*tree.get_children())
    if not os.path.exists(base_path):
        messagebox.showerror("Error", f"Path not found:\n{base_path}")
        return

    for item in os.listdir(base_path):
        tree.insert("", "end", values=(item,))

def on_open_item(event, tree, root, base_path):
    selected = tree.selection()
    if not selected:
        return

    item_name = tree.item(selected[0])["values"][0]
    full_path = os.path.join(base_path, item_name)

    if os.path.isdir(full_path):
        ini_path = os.path.join(full_path, f"{item_name}.ini")
        cfg_path = os.path.join(full_path, f"{item_name}.cfg")
        open_bike_editor(root, item_name, ini_path, cfg_path)
    elif item_name.endswith(".pkz"):
        messagebox.showinfo("Info", ".pkz not yet supported for cfg parsing")
    else:
        messagebox.showinfo("Info", "Not a valid bike folder or .pkz file")