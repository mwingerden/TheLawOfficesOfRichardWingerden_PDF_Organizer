import os
import logging
from docx2pdf import convert
from pypdf import PdfWriter, PdfReader
import tempfile
import tkinter as tk
from tkinter import messagebox

class FileOrganization:

    def __init__(self, source_file_path, dest_file_path):
        self._writer = PdfWriter()
        self._source_file_path = source_file_path
        self._dest_file_path = dest_file_path
        os.makedirs(self._dest_file_path, exist_ok=True)
        self._list_word_doc_files = []
        self._spouse_one = ""
        self._file_order = [
            ("Portfolio Inserts", "single"),
            ("Fiduciary and Distribution Summary", "single"),
            ("Trust Quick Reference Page", "single"),
            ("Trust Summary", "single"),
            ("RLT", "single"),
            ("Pour-Over Will", "multi"),
            ("Funding Instructions", "single"),
            ("Power of Attorney", "multi"),
            ("California Certification of Trust", "single"),
            ("Assignment of Personal Property", "multi"),
            ("California Advance Health Care Directive", "multi"),
            ("California HIPAA Authorization", "multi"),
            ("California Nomination of Conservator", "multi"),
            ("Remembrance and Services Memorandum", "multi"),
            ("Personal Property Memo", "multi"),
            ("California Nomination of Guardian", "multi")
        ]
        self._combined_file_name = "Combined.pdf"
        self._find_docx_files()

    def process_files(self):
        if self._find_docx_files() and self._check_files():
            self._get_spouse_one()
            self._find_rlt()

            for doc, doc_type in self._file_order:
                if doc_type == "single":
                    self._find_file(doc)
                else:
                    self._find_files(doc)

            self._combine_pdfs()
            return True
        else:
            return False

    def _check_files(self):
        missing = [
            base for base, base_type in self._file_order
            if not any(filled_file.startswith(base) for filled_file in self._list_word_doc_files)
        ]

        if not missing:
            return True
        else:
            message = (
                    "The following required files are missing:\n\n"
                    + "\n".join(f"• {name}" for name in missing)
            )
            tk.messagebox.showwarning("Warning", message)
            return False

    def _find_docx_files(self):
        if not os.path.exists(self._source_file_path):
            logging.warning("Folder not found: %s", self._source_file_path)
        else:
            self._list_word_doc_files = [
                f for f in os.listdir(self._source_file_path) if f.endswith(".docx")
            ]

        if not self._list_word_doc_files:
            messagebox.showerror(
                "Error",
                "No .docx files were found in the selected folder."
            )
            return False
        else:
            return True

    def _get_spouse_one(self):
        #TODO: Check for only one cert of trust.
        for file in self._list_word_doc_files:
            if "California Certification of Trust" in file:
                self._spouse_one = file.removesuffix(".docx").split("_", 1)[1]
                return

    def _find_rlt(self):
        for file in self._list_word_doc_files:
            if "RLT".lower() in file.lower():
                self._combined_file_name = file

    def _sort_by_spouse_one(self, files):
        return sorted(files, key=lambda x: 0 if self._spouse_one in x else 1)

    def _find_file(self, file_name):
        for file in self._list_word_doc_files:
            if file_name.lower() in file.lower():
                self._copy_file(file)

    def _find_files(self, file_name):
        files = []
        for file in self._list_word_doc_files:
            if file_name.lower() in file.lower():
                files.append(file)

        pour_over_will_files = self._sort_by_spouse_one(files)

        for file in pour_over_will_files:
            self._copy_file(file)

    def _copy_file(self, file):

        src = os.path.join(self._source_file_path, file)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            temp_pdf_path = tmp.name

        convert(src, temp_pdf_path)

        reader = PdfReader(temp_pdf_path)
        for page in reader.pages:
            self._writer.add_page(page)

        os.remove(temp_pdf_path)

    def _combine_pdfs(self):
        output_path = os.path.join(self._dest_file_path, self._combined_file_name.replace(".docx", ".pdf"))
        with open(output_path, "wb") as f:
            self._writer.write(f)

