import os
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import io

# Path to MX Bikes mods folder
BASE_PATH = os.path.expanduser("~/Documenti/piboso/mx bikes/mods/bikes")


def load_files():
    tree.delete(*tree.get_children())
    if not os.path.exists(BASE_PATH):
        messagebox.showerror("Error", f"Path not found:\n{BASE_PATH}")
        return

    for item in os.listdir(BASE_PATH):
        tree.insert("", "end", values=(item,))


def on_open_item(event):
    selected = tree.selection()
    if not selected:
        return

    item_name = tree.item(selected[0])["values"][0]
    full_path = os.path.join(BASE_PATH, item_name)

    if os.path.isdir(full_path):
        ini_path = os.path.join(full_path, f"{item_name}.ini")
        if os.path.exists(ini_path):
            open_ini_editor(ini_path)
        else:
            messagebox.showwarning("Warning", f"No INI file found for {item_name}")
    elif item_name.endswith(".pkz"):
        open_pkz_ini(full_path)
    else:
        messagebox.showinfo("Info", "Not a valid bike folder or .pkz file")


def open_ini_editor(ini_path, zip_archive=None, zip_filename=None):
    """Open INI in form editor with sections and key-value pairs."""

    config = configparser.ConfigParser()
    data = {}

    try:
        if zip_archive and zip_filename:
            with zipfile.ZipFile(zip_archive, "r") as z:
                with z.open(zip_filename) as f:
                    ini_text = f.read().decode("utf-8")
            config.read_string(ini_text)
        else:
            config.read(ini_path, encoding="utf-8")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    editor = tk.Toplevel(root)
    editor.title(f"Editing {os.path.basename(ini_path)}")
    editor.geometry("600x500")

    canvas = tk.Canvas(editor)
    scrollbar = ttk.Scrollbar(editor, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entries = {}

    # Create entry widgets for each key
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

    def save_changes():
        for (section, key), entry in entries.items():
            config.set(section, key, entry.get())

        try:
            if zip_archive and zip_filename:
                output = io.StringIO()
                config.write(output)
                with zipfile.ZipFile(zip_archive, "a") as z:
                    z.writestr(zip_filename, output.getvalue())
            else:
                with open(ini_path, "w", encoding="utf-8") as f:
                    config.write(f)
            messagebox.showinfo("Saved", "INI file saved successfully.")
            editor.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    save_btn = ttk.Button(frame, text="Save", command=save_changes)
    save_btn.pack(pady=10)


def open_pkz_ini(pkz_path):
    """Open .pkz and load ini inside."""
    try:
        with zipfile.ZipFile(pkz_path, "r") as z:
            name_no_ext = os.path.splitext(os.path.basename(pkz_path))[0]
            ini_name = f"{name_no_ext}/{name_no_ext}.ini"
            if ini_name in z.namelist():
                open_ini_editor(ini_name, zip_archive=pkz_path, zip_filename=ini_name)
            else:
                messagebox.showwarning("Warning", f"No INI file found in {pkz_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Main window
root = tk.Tk()
root.title("MX Bikes Bike Tuner")
root.geometry("500x400")

columns = ("Name",)
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<Double-1>", on_open_item)

refresh_btn = ttk.Button(root, text="Refresh", command=load_files)
refresh_btn.pack(pady=5)

load_files()
root.mainloop()