import tkinter as tk
from tkinter.constants import DISABLED
from tkinter.filedialog import askdirectory

class GUI:
    def __init__(self):
        self._root = tk.Tk()
        self._source_entry = None
        self._source_btn = None
        self._dest_entry = None
        self._dest_btn = None
        self._source_folder = None
        self._dest_folder = None

    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()
        return [self._source_folder, self._dest_folder]

    def _set_up_gui(self):
        self._root.title("Combine Docs")

        frame = tk.Frame(self._root)
        frame.grid(row=0, column=0)

        self._source_entry = tk.Entry(frame, width=150)
        self._source_entry.grid(row=0, column=0)
        source_btn = tk.Button(frame, text="Find Source Folder", command=self._find_source_folder)
        source_btn.grid(row=0, column=1)

        self._dest_entry = tk.Entry(frame, width=150)
        self._dest_entry.grid(row=1, column=0)
        dest_btn = tk.Button(frame, text="Find Destination Folder", command=self._find_dest_folder)
        dest_btn.grid(row=1, column=1)

        run_btn = tk.Button(frame, text="Run", command=self._root.destroy)
        run_btn.grid(row=2, column=0)

    def _find_source_folder(self):
        path = askdirectory()
        self._source_entry.delete(0, tk.END)
        self._source_entry.insert(0, path)
        self._source_entry.config(state=DISABLED)
        self._source_folder = path

    def _find_dest_folder(self):
        path = askdirectory()
        self._dest_entry.delete(0, tk.END)
        self._dest_entry.insert(0, path)
        self._dest_entry.config(state=DISABLED)
        self._dest_folder = path