import os
import file_organization

source_file_path = os.path.join(os.getcwd(), "Source Files")
destination_folder = os.path.join(os.getcwd(), "Modified Files")
# list_word_doc_files = doc_file_logic.set_up(list_files)

# for file in list_word_doc_files:
#     print(file)

# doc_file_logic.run_logic(list_files)
file_organization.FileOrganization(source_file_path, destination_folder)