import os
import pytest
from file_organization import FileOrganization

# =========================
# FIXTURES
# =========================

@pytest.fixture
def single_trust_folder(tmp_path):
    files = [
        "Portfolio Inserts.docx",
        "Fiduciary and Distribution Summary.docx",
        "Trust Quick Reference Page.docx",
        "Trust Summary.docx",
        "RLT_John_Doe.docx",
        "Pour-Over Will_John_Doe.docx",
        "Funding Instructions.docx",
        "Power of Attorney_John_Doe.docx",
        "California Certification of Trust_John_Doe.docx",
        "Assignment of Personal Property_John_Doe.docx",
        "California Advance Health Care Directive_John_Doe.docx",
        "California HIPAA Authorization_John_Doe.docx",
        "California Nomination of Conservator_John_Doe.docx",
        "Remembrance and Services Memorandum_John_Doe.docx",
        "Personal Property Memo_John_Doe.docx",
        "California Nomination of Guardian_John_Doe.docx",
    ]
    for f in files:
        (tmp_path / f).touch()
    return tmp_path


@pytest.fixture
def joint_trust_folder(tmp_path):
    file_order = FileOrganization(tmp_path, "Single")._file_order

    for base, kind in file_order:
        if kind == "multi":
            # 2 files for joint
            (tmp_path / f"{base}_Spouse1.docx").touch()
            (tmp_path / f"{base}_Spouse2.docx").touch()
        else:
            # 1 file for joint single
            (tmp_path / f"{base}.docx").touch()

    # Ensure _get_spouse_one finds spouse
    # Pick any single file for spouse1 naming convention
    # For example: "California Certification of Trust_Spouse1.docx"
    os.remove(tmp_path / "California Certification of Trust.docx")
    (tmp_path / "California Certification of Trust_Spouse1.docx").touch()

    return tmp_path

# =========================
# INIT
# =========================

def test_init_creates_directory(tmp_path):
    org = FileOrganization(tmp_path, "Single")
    assert os.path.exists(tmp_path)
    assert org._trust_type == "Single"
    assert org._combined_file_name == "Combined.pdf"

# =========================
# FIND DOCX FILES
# =========================

def test_find_docx_files_success(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    assert org._find_docx_files() is True


def test_find_docx_files_no_folder(tmp_path, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    missing = tmp_path / "missing"
    import logging
    monkeypatch.setattr(logging, "warning", lambda *a, **k: None)

    org = FileOrganization(missing, "Single")
    assert org._find_docx_files() is False


def test_find_docx_files_empty_folder(tmp_path, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(tmp_path, "Single")
    assert org._find_docx_files() is False

# =========================
# CHECK FILES
# =========================

def test_check_files_single_valid(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is True


def test_check_files_joint_valid(joint_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    org = FileOrganization(joint_trust_folder, "Joint")
    org._find_docx_files()
    assert org._check_files() is True


def test_check_files_missing(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    os.remove(single_trust_folder / "Trust Summary.docx")

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False


def test_check_files_extra(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    (single_trust_folder / "Trust Summary_COPY.docx").touch()

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False


def test_check_files_missing_and_extra(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    os.remove(single_trust_folder / "Trust Summary.docx")
    (single_trust_folder / "RLT_EXTRA.docx").touch()

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False

# =========================
# SPOUSE + RLT
# =========================

def test_get_spouse_one_found(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._get_spouse_one()
    assert org._spouse_one == "John_Doe"


def test_get_spouse_one_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    (tmp_path / "Other.docx").touch()
    org = FileOrganization(tmp_path, "Single")
    org._find_docx_files()
    org._get_spouse_one()
    assert org._spouse_one == ""


def test_find_rlt_found(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._find_rlt()
    assert "RLT" in org._combined_file_name


def test_find_rlt_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    (tmp_path / "Other.docx").touch()
    org = FileOrganization(tmp_path, "Single")
    org._find_docx_files()
    org._find_rlt()
    assert org._combined_file_name == "Combined.pdf"

# =========================
# SORTING
# =========================

def test_sort_by_spouse_one_prioritizes():
    org = FileOrganization("x", "Single")
    org._spouse_one = "Jane"
    files = ["Doc_John.docx", "Doc_Jane.docx"]
    assert org._sort_by_spouse_one(files)[0] == "Doc_Jane.docx"


def test_sort_by_spouse_one_no_match():
    org = FileOrganization("x", "Single")
    files = ["A.docx", "B.docx"]
    assert org._sort_by_spouse_one(files) == files


def test_sort_by_spouse_one_empty():
    org = FileOrganization("x", "Single")
    assert org._sort_by_spouse_one([]) == []

# =========================
# FIND FILE(S)
# =========================

def test_find_file_calls_copy(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    called = []

    org._copy_file = lambda f: called.append(f)
    org._find_file("Trust Summary")
    assert called


def test_find_file_no_match(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    called = []

    org._copy_file = lambda f: called.append(f)
    org._find_file("Does Not Exist")
    assert not called


def test_find_files_multiple(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._spouse_one = "John"
    called = []

    org._copy_file = lambda f: called.append(f)
    org._find_files("Power of Attorney")
    assert len(called) == 1


def test_find_files_none(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    called = []

    org._copy_file = lambda f: called.append(f)
    org._find_files("Nope")
    assert not called

# =========================
# COPY FILE
# =========================

def test_copy_file_adds_pages(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    monkeypatch.setattr("file_organization.convert", lambda src, dest: None)

    class DummyReader:
        pages = ["page1", "page2"]

    monkeypatch.setattr("file_organization.PdfReader", lambda path: DummyReader())
    called_pages = []
    org = FileOrganization(single_trust_folder, "Single")
    original_add_page = org._writer.add_page
    org._writer.add_page = lambda page: called_pages.append(page)
    org._copy_file("Trust Summary.docx")
    org._writer.add_page = original_add_page
    assert len(called_pages) == 2


# =========================
# COMBINE PDFS
# =========================

def test_combine_pdfs_writes(tmp_path):
    org = FileOrganization(tmp_path, "Single")
    class DummyWriter:
        def __init__(self): self.pages = []
        def write(self, f): self.called = True
    dummy = DummyWriter()
    org._writer = dummy
    org._combined_file_name = "Test.docx"

    org._combine_pdfs()
    assert hasattr(dummy, "called")

# =========================
# PROCESS FILES
# =========================

def test_process_files_success(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    monkeypatch.setattr("file_organization.convert", lambda src, dest: None)
    class DummyReader:
        pages = []
    monkeypatch.setattr("file_organization.PdfReader", lambda path: DummyReader())

    org = FileOrganization(single_trust_folder, "Single")
    assert org.process_files() is True


def test_process_files_fail_find(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files = lambda: False
    assert org.process_files() is False


def test_process_files_fail_check(single_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files = lambda: True
    org._check_files = lambda: False
    assert org.process_files() is False

# =========================
# CHECK FILES - JOINT
# =========================

def test_check_files_joint_missing(joint_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    # remove one multi file
    os.remove(joint_trust_folder / "Pour-Over Will_Spouse1.docx")

    org = FileOrganization(joint_trust_folder, "Joint")
    org._find_docx_files()
    assert org._check_files() is False


def test_get_spouse_one_joint(joint_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(joint_trust_folder, "Joint")
    org._find_docx_files()
    org._get_spouse_one()
    assert org._spouse_one == "Spouse1"

# =========================
# FIND FILES - JOINT
# =========================

def test_find_files_joint_order(joint_trust_folder, monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    org = FileOrganization(joint_trust_folder, "Joint")
    org._find_docx_files()
    org._spouse_one = "Spouse1"

    called = []
    org._copy_file = lambda f: called.append(f)
    org._find_files("Pour-Over Will")  # multi file
    # check that Spouse1 file is first
    assert called[0].endswith("Spouse1.docx")
    assert called[1].endswith("Spouse2.docx")