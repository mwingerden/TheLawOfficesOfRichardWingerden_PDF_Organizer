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
        self._guardianship = False
        self._guardianship_button = None
        self._selected = None

    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()

    def _set_up_gui(self):
        self._root.title("Combine Docs")

        self._frame = tk.Frame(self._root)
        self._frame.grid(row=0, column=0, padx=10, pady=10)

        self._source_entry = tk.Entry(self._frame, width=100)
        self._source_entry.grid(row=0, column=0, padx=10, pady=10)
        source_btn = tk.Button(self._frame,
                               text="Find Source Folder",
                               command=lambda: self._find_folder("_source_entry", "_source_folder"))
        source_btn.grid(row=0, column=1)

        self._trust_type_frame = tk.Frame(self._frame)
        self._trust_type_frame.grid(row=1, column=0, padx=10, pady=10)
        self._trust_type = tk.StringVar(value="-1")
        tk.Label(self._trust_type_frame, text="Trust Type: ").grid(row=0, column=0)
        tk.Radiobutton(self._trust_type_frame, text="Joint", variable=self._trust_type, value="Joint").grid(row=0, column=1)
        tk.Radiobutton(self._trust_type_frame, text="Single", variable=self._trust_type, value="Single").grid(row=0, column=2)

        guardianship_frame = tk.Frame(self._frame)
        guardianship_frame.grid(row=2, column=0, padx=10, pady=10)
        tk.Label(guardianship_frame, text="Guardianship?: ").grid(row=0, column=0)
        self._selected = tk.BooleanVar()
        self._guardianship_button = tk.Checkbutton(guardianship_frame, text="Yes",
                                                   variable=self._selected, indicatoron=False,
                                                   width=15, command=self._on_toggle)
        self._guardianship_button.grid(row=0, column=1)

        run_btn = tk.Button(self._frame, text="Run", command=self._run_file_organizer)
        run_btn.grid(row=4, column=0, padx=10, pady=10)

    def _on_toggle(self):
        if self._selected.get():
            self._guardianship_button.config(bg="yellow")
            self._guardianship = True
        else:
            self._guardianship_button.config(bg="SystemButtonFace")
            self._guardianship = False

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
                temp = file_organization.FileOrganization(self._source_folder, self._trust_type.get(), self._guardianship)
                if temp.process_files():
                    self._root.destroy()
            else:
                tk.messagebox.showwarning("Warning", "Please select a trust type!")
        else:
            tk.messagebox.showwarning("Warning", "Please select a folder!")
