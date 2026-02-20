import os
import pytest
from unittest import mock
from unittest.mock import patch, MagicMock
from pypdf import PdfWriter, PdfReader
from file_organization import FileOrganization  # replace with your actual module name

@pytest.fixture
def temp_folder(tmp_path):
    folder = tmp_path / "docs"
    folder.mkdir()
    return folder

@pytest.fixture
def sample_files(temp_folder):
    files = [
        "Portfolio Inserts.docx",
        "RLT.docx",
        "Pour-Over Will.docx",
        "California Certification of Trust_John.docx"
    ]
    for f in files:
        (temp_folder / f).write_text("dummy content")
    return files

def test_init_creates_folder(tmp_path):
    folder = tmp_path / "new_folder"
    fo = FileOrganization(str(folder), trust_type="Single", guardianship=False)
    assert os.path.exists(folder)
    assert isinstance(fo._writer, PdfWriter)
    assert fo._trust_type == "Single"
    assert fo._guardianship is False

@patch("file_organization.pythoncom.CoInitialize")
@patch("file_organization.win32com.client.Dispatch")
@patch("file_organization.pythoncom.CoUninitialize")
def test_check_word_installed_success(mock_uninit, mock_dispatch, mock_init):
    fo = FileOrganization("dummy_path", "Single", False)
    mock_dispatch.return_value.Quit = MagicMock()
    result = fo._check_word_installed()
    assert result is True
    mock_dispatch.assert_called_once()

@patch("file_organization.pythoncom.CoInitialize")
@patch("file_organization.win32com.client.Dispatch", side_effect=Exception("fail"))
@patch("file_organization.pythoncom.CoUninitialize")
@patch("file_organization.messagebox.showerror")
def test_check_word_installed_failure(mock_msg, mock_uninit, mock_dispatch, mock_init):
    fo = FileOrganization("dummy_path", "Single", False)
    result = fo._check_word_installed()
    assert result is False
    mock_msg.assert_called_once()

def test_find_docx_files_success(temp_folder, sample_files):
    fo = FileOrganization(str(temp_folder), "Single", False)
    assert fo._find_docx_files() is True
    assert set(fo._list_word_doc_files) == set(sample_files)

def test_find_docx_files_no_folder(tmp_path):
    folder = tmp_path / "nonexistent"
    fo = FileOrganization(str(folder), "Single", False)
    assert fo._find_docx_files() is False

@patch("file_organization.messagebox.showerror")
def test_find_docx_files_no_docx(mock_msg, tmp_path):  # mock first, tmp_path second
    folder = tmp_path / "empty"
    folder.mkdir()
    fo = FileOrganization(str(folder), "Single", False)
    assert fo._find_docx_files() is False
    mock_msg.assert_called_once()

def test_get_spouse_one(temp_folder, sample_files):
    fo = FileOrganization(str(temp_folder), "Single", False)
    fo._list_word_doc_files = sample_files
    fo._get_spouse_one()
    assert fo._spouse_one == "John"

def test_find_rlt(temp_folder, sample_files):
    fo = FileOrganization(str(temp_folder), "Single", False)
    fo._list_word_doc_files = sample_files
    fo._find_rlt()
    assert fo._combined_file_name == "RLT.docx"

def test_sort_by_spouse_one():
    fo = FileOrganization("dummy_path", "Single", False)
    fo._spouse_one = "John"
    files = ["File_A_John.docx", "File_B_Mary.docx"]
    sorted_files = fo._sort_by_spouse_one(files)
    assert sorted_files[0] == "File_A_John.docx"

@patch("file_organization.FileOrganization._copy_file", return_value=True)
def test_find_file(mock_copy):
    fo = FileOrganization("dummy", "Single", False)
    fo._list_word_doc_files = ["MyDoc.docx"]
    assert fo._find_file("mydoc") is True
    mock_copy.assert_called_once()

@patch("file_organization.FileOrganization._copy_file", return_value=True)
def test_find_files(mock_copy):
    fo = FileOrganization("dummy", "Single", False)
    fo._list_word_doc_files = ["Doc1.docx", "Doc2.docx"]
    assert fo._find_files("doc") is True
    assert mock_copy.call_count == 2


@patch("file_organization.PdfWriter.add_page")  # mock add_page so PyPDF never sees MagicMock
@patch("file_organization.PdfReader")
@patch("file_organization.pythoncom.CoInitialize")
@patch("file_organization.win32com.client.Dispatch")
@patch("file_organization.pythoncom.CoUninitialize")
@patch("file_organization.os.remove")
@patch("file_organization.messagebox.showerror")
def test_copy_file_success(mock_msg, mock_remove, mock_uninit, mock_dispatch, mock_init, mock_reader, mock_add_page,
                           tmp_path):
    # create dummy Word file
    file_path = tmp_path / "file.docx"
    file_path.write_text("dummy")

    # instantiate FileOrganization
    fo = FileOrganization(str(tmp_path), "Single", False)

    # override the list of Word docs
    fo._list_word_doc_files = [str(file_path.name)]

    # mock Word COM behavior
    mock_dispatch.return_value.Documents.Open.return_value.SaveAs = MagicMock()
    mock_dispatch.return_value.Documents.Open.return_value.Close = MagicMock()

    # mock PdfReader pages (won't be added because add_page is mocked)
    mock_reader.return_value.pages = [MagicMock()]

    # run _copy_file
    result = fo._copy_file(file_path.name)

    # check result
    assert result is True

    # optional: confirm add_page was called
    mock_add_page.assert_called()


def test_combine_pdfs(tmp_path):
    fo = FileOrganization(str(tmp_path), "Single", False)

    # Patch the _writer to avoid real PDF writing
    fo._writer = MagicMock()

    # Set some fake values for combined file name and dest folder
    fo._combined_file_name = "combined.docx"
    fo._dest_file_path = str(tmp_path)

    # Call the method (no arguments!)
    fo._combine_pdfs()

    # Make sure the writer's write() was called
    fo._writer.write.assert_called_once()

def test_check_files_missing_and_extra(tmp_path):
    # Create instance for "Single" trust
    fo = FileOrganization(str(tmp_path), "Single", False)

    # Make sure the required file exists in the temp directory
    required_file_name = "Portfolio Inserts.docx"
    required_file_path = tmp_path / required_file_name
    required_file_path.write_text("dummy content")  # dummy file

    # Assign the file to _list_word_doc_files exactly as _check_files() expects
    # Using the full path is safest
    fo._list_word_doc_files = [str(required_file_path)]

    # Patch messagebox to prevent Tkinter GUI during test
    with patch("file_organization.messagebox.showwarning") as mock_warn:
        result = fo._check_files()

    # Assert it returns True, because all required files are present
    assert result is True

    # Optionally, check that messagebox was NOT called
    mock_warn.assert_not_called()

@patch("file_organization.tk.messagebox.showwarning")
def test_print_file_information(mock_msg):
    fo = FileOrganization("dummy", "Single", False)
    fo._print_file_information(["Missing"], ["Extra"])
    mock_msg.assert_called_once()

@patch("file_organization.FileOrganization._check_word_installed", return_value=True)
@patch("file_organization.FileOrganization._find_docx_files", return_value=True)
@patch("file_organization.FileOrganization._check_files", return_value=True)
@patch("file_organization.FileOrganization._get_spouse_one")
@patch("file_organization.FileOrganization._find_rlt")
@patch("file_organization.FileOrganization._find_file", return_value=True)
@patch("file_organization.FileOrganization._find_files", return_value=True)
@patch("file_organization.FileOrganization._combine_pdfs")
def test_process_files(mock_combine, mock_find_files, mock_find_file, mock_rlt, mock_spouse, mock_check_files, mock_find_docx, mock_word):
    fo = FileOrganization("dummy", "Single", False)
    result = fo.process_files()
    assert result is True