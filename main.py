import os
import doc_file_logic

list_files = os.listdir('.')
list_word_doc_files = doc_file_logic.set_up(list_files)

# for file in list_word_doc_files:
#     print(file)

doc_file_logic.run_logic(list_word_doc_files)