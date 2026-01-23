class FileOrganization:

    def __init__(self, list_files):
        self.__list_files = list_files
        self.__ist_word_doc_files = []
        self.__order = 1
        self.__spouse_one = ""
        self.__portfolio_inserts = "Portfolio Inserts_"
        self.__cert_of_trust = "California Certification of Trust_"
        self.__fiduciary_distribution_summary = "Fiduciary and Distribution Summary"
        self.__trust_quick_reference_page = "Trust Quick Reference Page_"
        self.__trust_summary = "Trust Summary_"
        self.__rlt = "RLT"
        self.__pour_over_will = "Pour-Over Will_"
        self.__run_logic()

    def __run_logic(self):
        self.__find_docx_files()
        self.__get_spouse_one()
        # print()
        # self.find_spouse_one_files()
        # print()
        self.__find_portfolio_inserts()
        self.__find_fiduciary_distribution_summary()
        self.__find_trust_quick_reference_page()
        self.__find_trust_summary()
        self.__find_rlt()
        self.__find_pour_over_will()

    def __find_docx_files(self):
        for file in self.__list_files:
            if file.lower().endswith('.docx'):
                self.__ist_word_doc_files.append(file)

    def __get_spouse_one(self):
        #TODO: Check for only one cert of trust.
        for file in self.__ist_word_doc_files:
            if self.__cert_of_trust in file:
                self.__spouse_one = file.removesuffix(".docx").split("_", 1)[1]
                # print(self.spouse_one)
                return

    def __find_spouse_one_files(self):
        for file in self.__ist_word_doc_files:
            if self.__spouse_one in file:
                print(file)

    def __sort_by_spouse_one(self, files):
        return sorted(files, key=lambda x: 0 if self.__spouse_one in x else 1)

    def __find_portfolio_inserts(self):
        for file in self.__ist_word_doc_files:
            if self.__portfolio_inserts.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_fiduciary_distribution_summary(self):
        for file in self.__ist_word_doc_files:
            if self.__fiduciary_distribution_summary.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_trust_quick_reference_page(self):
        for file in self.__ist_word_doc_files:
            if self.__trust_quick_reference_page.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_trust_summary(self):
        for file in self.__ist_word_doc_files:
            if self.__trust_summary.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_rlt(self):
        for file in self.__ist_word_doc_files:
            if self.__rlt.lower() in file.lower():
                file = str(self.__order) + "_" + file
                self.__order += 1
                # this is where to rename file
                print(file)

    def __find_pour_over_will(self):
        pour_over_will_files = []
        for file in self.__ist_word_doc_files:
            if self.__pour_over_will.lower() in file.lower():
                pour_over_will_files.append(file)

        pour_over_will_files = self.__sort_by_spouse_one(pour_over_will_files)

        for file in pour_over_will_files:
            file = str(self.__order) + "_" + file
            self.__order += 1
            # this is where to rename file
            print(file)
