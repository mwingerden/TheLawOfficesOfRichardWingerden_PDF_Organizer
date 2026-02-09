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
    file_order = FileOrganization("", "")._file_order

    for base, kind in file_order:
        if kind == "multi":
            (tmp_path / f"{base}_Spouse1.docx").touch()
            (tmp_path / f"{base}_Spouse2.docx").touch()
        else:
            (tmp_path / f"{base}.docx").touch()

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

def test_find_docx_files_success(single_trust_folder):
    org = FileOrganization(single_trust_folder, "Single")
    assert org._find_docx_files() is True


def test_find_docx_files_no_folder(tmp_path, mocker):
    missing = tmp_path / "missing"
    mocker.patch("logging.warning")

    org = FileOrganization(missing, "Single")
    assert org._find_docx_files() is False


def test_find_docx_files_empty_folder(tmp_path, mocker):
    mocker.patch("tkinter.messagebox.showerror")
    org = FileOrganization(tmp_path, "Single")
    assert org._find_docx_files() is False


# =========================
# CHECK FILES
# =========================

def test_check_files_single_valid(single_trust_folder):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is True


def test_check_files_joint_valid(joint_trust_folder):
    org = FileOrganization(joint_trust_folder, "Joint")
    org._find_docx_files()
    assert org._check_files() is True


def test_check_files_missing(single_trust_folder, mocker):
    mocker.patch("tkinter.messagebox.showwarning")
    os.remove(single_trust_folder / "Trust Summary.docx")

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False


def test_check_files_extra(single_trust_folder, mocker):
    mocker.patch("tkinter.messagebox.showwarning")
    (single_trust_folder / "Trust Summary_COPY.docx").touch()

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False


def test_check_files_missing_and_extra(single_trust_folder, mocker):
    mocker.patch("tkinter.messagebox.showwarning")
    os.remove(single_trust_folder / "Trust Summary.docx")
    (single_trust_folder / "RLT_EXTRA.docx").touch()

    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    assert org._check_files() is False


# =========================
# SPOUSE + RLT
# =========================

def test_get_spouse_one_found(single_trust_folder):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._get_spouse_one()
    assert org._spouse_one == "John_Doe"


def test_get_spouse_one_not_found(tmp_path):
    (tmp_path / "Other.docx").touch()
    org = FileOrganization(tmp_path, "Single")
    org._find_docx_files()
    org._get_spouse_one()
    assert org._spouse_one == ""


def test_find_rlt_found(single_trust_folder):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._find_rlt()
    assert "RLT" in org._combined_file_name


def test_find_rlt_not_found(tmp_path):
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

def test_find_file_calls_copy(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    spy = mocker.patch.object(org, "_copy_file")

    org._find_file("Trust Summary")
    spy.assert_called()


def test_find_file_no_match(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    spy = mocker.patch.object(org, "_copy_file")

    org._find_file("Does Not Exist")
    spy.assert_not_called()


def test_find_files_multiple(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    org._spouse_one = "John"
    spy = mocker.patch.object(org, "_copy_file")

    org._find_files("Power of Attorney")
    assert spy.call_count == 1


def test_find_files_none(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    org._find_docx_files()
    spy = mocker.patch.object(org, "_copy_file")

    org._find_files("Nope")
    spy.assert_not_called()


# =========================
# COPY FILE
# =========================

def test_copy_file_adds_pages(single_trust_folder, mocker):
    mocker.patch("file_organization.convert")
    reader = mocker.patch("file_organization.PdfReader")
    reader.return_value.pages = ["p1", "p2"]

    org = FileOrganization(single_trust_folder, "Single")
    org._copy_file("Trust Summary.docx")

    assert len(org._writer.pages) == 2


# =========================
# COMBINE PDFS
# =========================

def test_combine_pdfs_writes(tmp_path, mocker):
    org = FileOrganization(tmp_path, "Single")
    org._writer = mocker.Mock()
    org._combined_file_name = "Test.docx"

    org._combine_pdfs()
    org._writer.write.assert_called_once()


# =========================
# PROCESS FILES
# =========================

def test_process_files_success(single_trust_folder, mocker):
    mocker.patch("file_organization.convert")
    mocker.patch("file_organization.PdfReader", return_value=mocker.Mock(pages=[]))

    org = FileOrganization(single_trust_folder, "Single")
    assert org.process_files() is True


def test_process_files_fail_find(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    mocker.patch.object(org, "_find_docx_files", return_value=False)

    assert org.process_files() is False


def test_process_files_fail_check(single_trust_folder, mocker):
    org = FileOrganization(single_trust_folder, "Single")
    mocker.patch.object(org, "_check_files", return_value=False)

    assert org.process_files() is False
