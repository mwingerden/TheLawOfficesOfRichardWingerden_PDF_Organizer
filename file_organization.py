class FileOrganization:

    def __init__(self, list_files):
        self.__list_files = list_files
        self.__list_word_doc_files = []
        self.__order = 1
        self.__spouse_one = ""
        self.__portfolio_inserts = "Portfolio Inserts_"
        self.__fiduciary_distribution_summary = "Fiduciary and Distribution Summary"
        self.__trust_quick_reference_page = "Trust Quick Reference Page_"
        self.__trust_summary = "Trust Summary_"
        self.__rlt = "RLT"
        self.__pour_over_will = "Pour-Over Will_"
        self.__funding_instructions = "Funding Instructions -"
        self.__power_of_attorney = "Power of Attorney_"
        self.__cert_of_trust = "California Certification of Trust_"
        self.__assign_of_personal_property = "Assignment of Personal Property_"
        self.__ahcd = "California Advance Health Care Directive_"
        self.__hippa = "California HIPAA Authorization_"
        self.__conservatorship = "California Nomination of Conservator_"
        self.__remembrance_memorandum = "Remembrance and Services Memorandum_"
        self.__personal_property_memo = "Personal Property Memo"
        self.__guardianship = "California Nomination of Guardian_"
        self.__run_logic()

    def __run_logic(self):
        self.__find_docx_files()
        self.__get_spouse_one()
        self.__find_file(self.__portfolio_inserts)
        self.__find_file(self.__fiduciary_distribution_summary)
        self.__find_file(self.__trust_quick_reference_page)
        self.__find_file(self.__trust_summary)
        self.__find_file(self.__rlt)
        self.__find_files(self.__pour_over_will)
        self.__find_files(self.__power_of_attorney)
        self.__find_file(self.__cert_of_trust)
        self.__find_files(self.__assign_of_personal_property)
        self.__find_files(self.__ahcd)
        self.__find_files(self.__hippa)
        self.__find_files(self.__conservatorship)
        self.__find_files(self.__remembrance_memorandum)
        self.__find_files(self.__personal_property_memo)
        self.__find_files(self.__guardianship)

    def __find_docx_files(self):
        for file in self.__list_files:
            if file.lower().endswith('.docx'):
                self.__list_word_doc_files.append(file)

    def __get_spouse_one(self):
        #TODO: Check for only one cert of trust.
        for file in self.__list_word_doc_files:
            if self.__cert_of_trust in file:
                self.__spouse_one = file.removesuffix(".docx").split("_", 1)[1]
                # print(self.spouse_one)
                return

    def __find_spouse_one_files(self):
        for file in self.__list_word_doc_files:
            if self.__spouse_one in file:
                print(file)

    def __sort_by_spouse_one(self, files):
        return sorted(files, key=lambda x: 0 if self.__spouse_one in x else 1)

    def __find_file(self, file_name):
        for file in self.__list_word_doc_files:
            if file_name.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_files(self, file_name):
        files = []
        for file in self.__list_word_doc_files:
            if file_name.lower() in file.lower():
                files.append(file)

        pour_over_will_files = self.__sort_by_spouse_one(files)

        for file in pour_over_will_files:
            file = str(self.__order) + "_" + file
            self.__order += 1
            # this is where to rename file
            print(file)