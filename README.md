# TheLawOfficesOfRichardWingerden_PDF_Organizer
A desktop GUI application built with **Tkinter** that validates, organizes, and combines estate planning `.docx` files into a single PDF in the correct order.

This tool is designed to streamline document assembly for trust packages by ensuring required files are present and correctly formatted before combining them.

---

## ✨ Features

- 📂 Select a source folder containing `.docx` files
- ⚖️ Choose trust type:
  - Joint
  - Single
- 👶 Optional Guardianship toggle
- ✅ Validates:
  - Missing required documents
  - Extra duplicate documents
  - Required file counts based on trust type
- 📑 Converts `.docx` files to PDF
- 📎 Combines all PDFs into one ordered `Combined.pdf`

---

## 🏗 Project Structure

```
.
├── gui.py
├── file_organization.py
└── README.md
```

### `gui.py`
Handles:
- Tkinter UI
- Folder selection
- Trust type selection
- Guardianship toggle
- Running the file processor

### `file_organization.py`
Handles:
- File validation
- Document counting logic
- Required file rules
- DOCX → PDF conversion
- PDF combination

---

## 📋 Required File Order

Documents are processed in the following order:

- Portfolio Inserts
- Fiduciary and Distribution Summary
- Trust Quick Reference Page
- Trust Summary
- RLT
- Pour-Over Will
- Funding Instructions
- Power of Attorney
- California Certification of Trust
- Assignment of Personal Property
- California Advance Health Care Directive
- California HIPAA Authorization
- California Nomination of Conservator
- Remembrance and Services Memorandum
- Personal Property Memo
- California Nomination of Guardian (optional if Guardianship not selected)

---

## ⚖️ Trust Type Rules

### Single Trust
- All required documents must appear once.

### Joint Trust
- Documents marked as `"multi"` require **two versions** (one per spouse).
- Documents marked as `"single"` require only one.

### Guardianship
- If selected:
  - "California Nomination of Guardian" is required.
- If not selected:
  - It is not required.

---

## 🛠 Dependencies

Install required packages:

```bash
pip install docx2pdf pypdf
```

### Python Version
- Python 3.9+

---

## ▶️ Running the Application

```bash
python gui.py
```

Steps:
1. Click **Find Source Folder**
2. Select trust type (Joint or Single)
3. Toggle Guardianship if applicable
4. Click **Run**

If validation passes:
- The program combines all documents into a single PDF.
- The application closes.

If validation fails:
- A warning dialog shows missing or extra files.

---

## 🔍 Validation Logic Overview

The program:

1. Collects all `.docx` files in the selected folder
2. Counts occurrences of each required document base name
3. Determines required quantity based on:
   - Trust type
   - Document type (single vs multi)
   - Guardianship toggle
4. Displays a detailed warning if:
   - Files are missing
   - There are too many copies

---

## 📌 Design Decisions

- Uses `Counter` for clean file count tracking
- Separates GUI logic from business logic
- Uses temporary files for safe PDF conversion
- Prevents invalid runs before processing

---

## 🚀 Future Improvements

- Destination folder selection
- Progress bar during conversion
- Logging system for production use
- Unit test expansion
- Executable packaging (PyInstaller)
- File preview before combine
- Automatic spouse name detection improvements

---

## 📄 License

Private/internal tool.

