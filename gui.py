import file_organization
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askdirectory
from tkinter import messagebox, ttk
import threading

class GUI:
    def __init__(self):
        self._root = tk.Tk()
        self._frame = tk.Frame(self._root)
        self._source_entry = None
        self._source_btn = None
        self._source_folder = None
        self._dest_folder = None
        self._trust_type = None
        self._guardianship = False
        self._guardianship_button = None
        self._selected = None
        self._progress_bar = None
        self._status_label = None
        self._enable_btn = "normal"
        self._disable_btn = "disabled"
        self._cancel_requested = False


    def run_gui(self):
        self._set_up_gui()
        self._root.mainloop()

    def _set_up_gui(self):
        self._root.title("Combine Docs")

        self._frame.pack(padx=10, pady=10, fill="x", expand=True)

        source_folder_frame = tk.Frame(self._frame)
        source_folder_frame.pack(fill="x", padx=5, pady=5)
        self._source_entry = tk.Entry(source_folder_frame, width=100)
        self._source_entry.grid(row=0, column=0)
        self._source_btn = tk.Button(source_folder_frame,
                               text="Find Source Folder",
                               command=lambda: self._find_folder("_source_entry", "_source_folder"))
        self._source_btn.grid(row=0, column=1, padx=5, pady=5)

        trust_type_frame = tk.Frame(self._frame)
        trust_type_frame.pack(fill="x", padx=5, pady=5)
        self._trust_type = tk.StringVar(value="-1")
        tk.Label(trust_type_frame, text="Trust Type: ").grid(row=0, column=0)
        self._joint_rb = tk.Radiobutton(trust_type_frame, text="Joint", variable=self._trust_type, value="Joint")
        self._joint_rb.grid(row=0, column=1)
        self._single_rb = tk.Radiobutton(trust_type_frame, text="Single", variable=self._trust_type, value="Single")
        self._single_rb.grid(row=0, column=2)

        guardianship_frame = tk.Frame(self._frame)
        guardianship_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(guardianship_frame, text="Guardianship?: ").grid(row=0, column=0)
        self._selected = tk.BooleanVar()
        self._guardianship_button = tk.Checkbutton(guardianship_frame, text="Yes",
                                                   variable=self._selected, indicatoron=False,
                                                   width=15, command=self._on_toggle)
        self._guardianship_button.grid(row=0, column=1)

        self._run_btn = tk.Button(self._frame, text="Run", command=self._run_file_organizer)
        self._run_btn.pack(fill="x", padx=5, pady=5)

        self._exit_btn = tk.Button(self._frame, text="Exit", command=self._close_application)
        self._exit_btn.pack(fill="x", padx=5, pady=5)

        self._status_label = tk.Label(self._frame, text="Processing...")
        self._status_label.pack(fill="x", padx=10, pady=5)
        self._progress_bar = ttk.Progressbar(self._root, orient="horizontal",
                                         mode="determinate", length=300)
        self._progress_bar.pack(fill="x", padx=5, pady=5)
        self._status_label.pack_forget()
        self._progress_bar.pack_forget()

    def _reveal_progress_bar(self):
        self._status_label.pack_forget()
        self._progress_bar.pack_forget()

        self._status_label.config(text="Processing...")
        self._status_label.pack(fill="x", padx=10, pady=5)
        self._progress_bar = ttk.Progressbar(self._root, orient="horizontal",
                                         mode="determinate", length=300)
        self._progress_bar.pack(fill="x", padx=5, pady=5)

    def _on_toggle(self):
        if self._selected.get():
            self._guardianship_button.config(background="yellow")
            self._guardianship = True
        else:
            self._guardianship_button.config(bg="SystemButtonFace")
            self._guardianship = False

    def _find_folder(self, entry_widget_attr, folder_attr):
        path = askdirectory()
        if not path:
            setattr(self, folder_attr, None)
            getattr(self, entry_widget_attr).config(state=NORMAL)
            getattr(self, entry_widget_attr).delete(0, tk.END)
            getattr(self, entry_widget_attr).config(state=DISABLED)
            return
        getattr(self, entry_widget_attr).config(state=NORMAL)
        getattr(self, entry_widget_attr).delete(0, tk.END)
        getattr(self, entry_widget_attr).insert(0, f".../{path.split("/")[-2]}/{path.split("/")[-1]}")
        getattr(self, entry_widget_attr).config(state=DISABLED)
        setattr(self, folder_attr, path)

    def _close_application(self):
        self._root.destroy()

    def _run_file_organizer(self):
        self._enable_disable_gui(self._disable_btn)

        if not self._source_folder:
            messagebox.showwarning("Warning", "Please select a folder!")
            self._enable_disable_gui(self._enable_btn)
            return

        if self._trust_type.get() not in ("Joint", "Single"):
            messagebox.showwarning("Warning", "Please select a trust type!")
            self._enable_disable_gui(self._enable_btn)
            return

        thread = threading.Thread(target=self._process_files_thread)
        thread.start()

    def _enable_disable_gui(self, enable_disable):
        if enable_disable == self._enable_btn or enable_disable == self._disable_btn:
            self._source_btn.config(state=enable_disable.lower())
            self._joint_rb.config(state=enable_disable.lower())
            self._single_rb.config(state=enable_disable.lower())
            self._guardianship_button.config(state=enable_disable)
            self._run_btn.config(state=enable_disable.lower())
            self._exit_btn.config(state=enable_disable.lower())

    def _update_progress(self, value):
        self._root.after(0, lambda: self._progress_bar.step(value))

    def _update_status(self, text):
        self._root.after(0, lambda: self._status_label.config(text=text))

    def _set_progress_max(self, maximum):
        self._root.after(0, lambda: self._progress_bar.config(maximum=maximum, value=0))

    def _process_files_thread(self):
        self._reveal_progress_bar()
        self._progress_bar["value"] = 0
        temp = file_organization.FileOrganization(
            self._source_folder,
            self._trust_type.get(),
            self._guardianship,
            progress_callback=self._update_progress,
            status_callback=self._update_status,
            max_callback=self._set_progress_max
        )

        if temp.process_files():
            self._status_label.config(text="Completed!")

        self._enable_disable_gui(self._enable_btn)