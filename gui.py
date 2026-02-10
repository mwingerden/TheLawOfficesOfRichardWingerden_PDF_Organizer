import file_organization
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
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
        self._trust_type = None

    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()

    def _set_up_gui(self):
        self._root.title("Combine Docs")

        self._frame = tk.Frame(self._root)
        self._frame.grid(row=0, column=0, padx=10, pady=10)

        self._source_entry = tk.Entry(self._frame, width=150)
        self._source_entry.grid(row=0, column=0, padx=10, pady=10)
        source_btn = tk.Button(self._frame,
                               text="Find Source Folder",
                               command=lambda: self._find_folder("_source_entry", "_source_folder"))
        source_btn.grid(row=0, column=1)

        self._radio_button_frame = tk.Frame(self._frame)
        self._radio_button_frame.grid(row=1, column=0, padx=10, pady=10)
        self._trust_type = tk.StringVar(value="-1")
        tk.Label(self._radio_button_frame, text="Trust Type: ").grid(row=0, column=0)
        tk.Radiobutton(self._radio_button_frame,text="Joint", variable=self._trust_type, value="Joint").grid(row=0, column=1)
        tk.Radiobutton(self._radio_button_frame,text="Single", variable=self._trust_type, value="Single").grid(row=0, column=2)


        run_btn = tk.Button(self._frame, text="Run", command=self._run_file_organizer)
        run_btn.grid(row=3, column=0, padx=10, pady=10)

    def _find_folder(self, entry_widget_attr, folder_attr):
        path = askdirectory()
        getattr(self, entry_widget_attr).config(state=NORMAL)
        getattr(self, entry_widget_attr).delete(0, tk.END)
        getattr(self, entry_widget_attr).insert(0, f".../{path.split("/")[-2]}/{path.split("/")[-1]}")
        getattr(self, entry_widget_attr).config(state=DISABLED)
        setattr(self, folder_attr, path)

    def _run_file_organizer(self):
        if self._source_folder:
            if self._trust_type.get() == "Joint" or self._trust_type.get() == "Single":
                temp = file_organization.FileOrganization(self._source_folder, self._trust_type.get())
                if temp.process_files():
                    self._root.destroy()
                # print(self._trust_type.get())
                # print("Processing Files")
                # self._root.destroy()
            else:
                tk.messagebox.showwarning("Warning", "Please select a trust type!")
        else:
            tk.messagebox.showwarning("Warning", "Please select a folder!")
