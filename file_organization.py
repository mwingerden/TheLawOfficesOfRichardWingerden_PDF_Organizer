import os
import shutil

class FileOrganization:

    def __init__(self, source_file_path, dest_file_path):
        self._source_file_path = source_file_path
        self._dest_file_path = dest_file_path
        os.makedirs(self._dest_file_path, exist_ok=True)
        self._list_word_doc_files = []
        self._order = 1
        self._spouse_one = ""
        self._portfolio_inserts = "Portfolio Inserts_"
        self._fiduciary_distribution_summary = "Fiduciary and Distribution Summary"
        self._trust_quick_reference_page = "Trust Quick Reference Page_"
        self._trust_summary = "Trust Summary_"
        self._rlt = "RLT"
        self._pour_over_will = "Pour-Over Will_"
        self._funding_instructions = "Funding Instructions -"
        self._power_of_attorney = "Power of Attorney_"
        self._cert_of_trust = "California Certification of Trust_"
        self._assign_of_personal_property = "Assignment of Personal Property_"
        self._ahcd = "California Advance Health Care Directive_"
        self._hippa = "California HIPAA Authorization_"
        self._conservatorship = "California Nomination of Conservator_"
        self._remembrance_memorandum = "Remembrance and Services Memorandum_"
        self._personal_property_memo = "Personal Property Memo"
        self._guardianship = "California Nomination of Guardian_"
        self._run_logic()

    def _run_logic(self):
        self._find_docx_files()
        self._get_spouse_one()

        self._file_order = [
            (self._portfolio_inserts, "single"),
            (self._fiduciary_distribution_summary, "single"),
            (self._trust_quick_reference_page, "single"),
            (self._trust_summary, "single"),
            (self._rlt, "single"),
            (self._pour_over_will, "multi"),
            (self._funding_instructions, "single"),
            (self._power_of_attorney, "multi"),
            (self._cert_of_trust, "single"),
            (self._assign_of_personal_property, "multi"),
            (self._ahcd, "multi"),
            (self._hippa, "multi"),
            (self._conservatorship, "multi"),
            (self._remembrance_memorandum, "multi"),
            (self._personal_property_memo, "multi"),
            (self._guardianship, "multi")
        ]

        for doc, doc_type in self._file_order:
            if doc_type in "single":
                self._find_file(doc)
            else:
                self._find_files(doc)

    def _find_docx_files(self):
        if not os.path.exists(self._source_file_path):
            print("Folder not found:", self._source_file_path)
        else:
            for file in os.listdir(self._source_file_path):
                if file.endswith(".docx"):
                    self._list_word_doc_files.append(file)

    def _get_spouse_one(self):
        #TODO: Check for only one cert of trust.
        for file in self._list_word_doc_files:
            if self._cert_of_trust in file:
                self._spouse_one = file.removesuffix(".docx").split("_", 1)[1]
                # print(self.spouse_one)
                return

    def _find_spouse_one_files(self):
        for file in self._list_word_doc_files:
            if self._spouse_one in file:
                print(file)

    def _sort_by_spouse_one(self, files):
        return sorted(files, key=lambda x: 0 if self._spouse_one in x else 1)

    def _find_file(self, file_name):
        for file in self._list_word_doc_files:
            if file_name.lower() in file.lower():
                # file_name = str(self._order) + "_" + file
                new_file_name = f"{self._order}_{file}"
                self._order += 1
                src = os.path.join(self._source_file_path, file)
                dst = os.path.join(self._dest_file_path, new_file_name)

                shutil.copyfile(src, dst)


    def _find_files(self, file_name):
        files = []
        for file in self._list_word_doc_files:
            if file_name.lower() in file.lower():
                files.append(file)

        pour_over_will_files = self._sort_by_spouse_one(files)

        for file in pour_over_will_files:
            new_file_name = f"{self._order}_{file}"
            self._order += 1
            src = os.path.join(self._source_file_path, file)
            dst = os.path.join(self._dest_file_path, new_file_name)

            shutil.copyfile(src, dst)