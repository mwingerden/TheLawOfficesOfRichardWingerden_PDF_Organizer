import file_organization
import tkinter as tk
from tkinter.constants import DISABLED
from tkinter.filedialog import askdirectory
from tkinter import messagebox

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

    def _set_up_gui(self):
        self._root.title("Combine Docs")

        frame = tk.Frame(self._root)
        frame.grid(row=0, column=0, padx=10, pady=10)

        self._source_entry = tk.Entry(frame, width=150)
        self._source_entry.grid(row=0, column=0, padx=10, pady=10)
        source_btn = tk.Button(frame,
                               text="Find Source Folder",
                               command=lambda: self._find_folder("_source_entry", "_source_folder"))
        source_btn.grid(row=0, column=1)

        self._dest_entry = tk.Entry(frame, width=150)
        self._dest_entry.grid(row=1, column=0, padx=10, pady=10)
        dest_btn = tk.Button(frame,
                             text="Find Destination Folder",
                             command=lambda: self._find_folder("_dest_entry", "_dest_folder"))
        dest_btn.grid(row=1, column=1)

        run_btn = tk.Button(frame, text="Run", command=self._run_file_organizer)
        run_btn.grid(row=2, column=0, padx=10, pady=10)

    def _find_folder(self, entry_widget_attr, folder_attr):
        path = askdirectory()
        getattr(self, entry_widget_attr).delete(0, tk.END)
        getattr(self, entry_widget_attr).insert(0, path)
        getattr(self, entry_widget_attr).config(state=DISABLED)
        setattr(self, folder_attr, path)

    def _run_file_organizer(self):
        if self._source_folder and self._dest_folder:
            temp = file_organization.FileOrganization(self._source_folder, self._dest_folder)
            if temp.check_files():
                temp.process_files()
                self._root.destroy()
        else:
            tk.messagebox.showwarning("Warning", "Please select both folders!")
