cert_of_trust = "California Certification of Trust_"

def set_up(files):
    file_list = []
    for file in files:
        if file.lower().endswith('.docx'):
            file_list.append(file)
    return file_list

def get_spouse_one(list_word_doc_files):
    # for file in list_word_doc_files:
    #     print(file)
    for file in list_word_doc_files:
        if cert_of_trust in file:
            return file.removesuffix(".docx").split("_", 1)[1]
    return None

def find_spouse_one_files(spouse_one, list_word_doc_files):
    for file in list_word_doc_files:
        if spouse_one in file:
            print(file)


def run_logic(list_word_doc_files):
    # for file in list_word_doc_files:
    #     print(file)
    spouse_one = get_spouse_one(list_word_doc_files)
    find_spouse_one_files(spouse_one, list_word_doc_files)

