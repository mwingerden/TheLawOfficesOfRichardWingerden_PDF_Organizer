class FileOrganization:

    def __init__(self, list_files):
        self._list_files = list_files
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

        self._single_docs = [
            self._portfolio_inserts,
            self._fiduciary_distribution_summary,
            self._trust_quick_reference_page,
            self._trust_summary,
            self._rlt,
            self._cert_of_trust
        ]

        self._multi_docs = [
            self._pour_over_will,
            self._power_of_attorney,
            self._assign_of_personal_property,
            self._ahcd,
            self._hippa,
            self._conservatorship,
            self._remembrance_memorandum,
            self._personal_property_memo,
            self._guardianship
        ]

        for doc in self._single_docs:
            self._find_file(doc)

        for doc in self._multi_docs:
            self._find_files(doc)

    def _find_docx_files(self):
        for file in self._list_files:
            if file.lower().endswith('.docx'):
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
                file = str(self._order) + "_" + file
                self._order += 1
                # this is where to rename file
                print(file)

    def _find_files(self, file_name):
        files = []
        for file in self._list_word_doc_files:
            if file_name.lower() in file.lower():
                files.append(file)

        pour_over_will_files = self._sort_by_spouse_one(files)

        for file in pour_over_will_files:
            file = str(self._order) + "_" + file
            self._order += 1
            # this is where to rename file
            print(file)