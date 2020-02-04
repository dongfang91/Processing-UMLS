import read_files as read

file_path_synonym = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"
file_path_st = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRSTY.RRF"
ask = read.read_from_json("data/AskAPatient/label")


cui_codes = read.read_from_json("data/AskAPatient/cui_codes")
ask_cuis = [cui for cui,_ in cui_codes.items()]
print(len(cui_codes))



def textfile2list_twa():
    data = read.readfrom_txt(file_path_synonym)
    txt_list ={}
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in ask_cuis:
            if line[0] not in txt_list:
                txt_list[line[0]] = [line[14]]
            else:
                txt_list[line[0]] += [line[14]]

    read.save_in_json("data/AskAPatient/cui_dict",txt_list)

# textfile2list_twa()

def textfile2list_twa_st():
    data = read.readfrom_txt(file_path_st)
    txt_list ={}
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in ask_cuis:
            txt_list[line[0]] = line[2]
    read.save_in_json("data/AskAPatient/cui_st_dict",txt_list)

# textfile2list_twa_st()

def add_oov():
    code_cuis = read.read_from_tsv("data/AskAPatient/code_cuis.tsv")
    code_cuis_dict = {line[0]:line[1:] for line in code_cuis if len(line[:-1]) >0}
    cui_synonyms = read.read_from_json("data/AskAPatient/cui_dict")
    cui_st = read.read_from_json("data/AskAPatient/cui_st_dict")

    code_labels = read.read_from_json("data/AskAPatient/label_texts_dict_AskAPatient")

    codes_synonyms_tsv = []
    codes_st_tsv = []

    for code in ask:
        code_synonyms_tsv = [code,code_labels[code]]
        code_st_tsv = [code,code_labels[code]]
        if code in ask:
            if code in code_cuis_dict:
                cuis = code_cuis_dict[code]
                for cui in cuis:
                    code_synonyms_tsv+=[cui," [SEP] ".join(cui_synonyms[cui])[:100]]
                    code_st_tsv +=[cui, " [SEP] ".join(cui_synonyms[cui])[:100], cui_st[cui]]
        codes_synonyms_tsv.append(code_synonyms_tsv)
        codes_st_tsv.append(code_st_tsv)

    read.save_in_tsv("data/AskAPatient/codes_synonyms_tsv.tsv",codes_synonyms_tsv)
    read.save_in_tsv("data/AskAPatient/codes_st_tsv.tsv",codes_st_tsv)


# add_oov()

def add_oov_processed():
    code_cuis = read.read_from_tsv("data/AskAPatient/codes_single_synonyms_tsv.tsv")
    code_cuis_dict = {line[0]:line[2] for line in code_cuis if len(line[3]) >2}
    cui_synonyms = read.read_from_json("data/AskAPatient/cui_dict")
    cui_st = read.read_from_json("data/AskAPatient/cui_st_dict")

    code_labels = read.read_from_json("data/AskAPatient/label_texts_dict_AskAPatient")

    codes_synonyms_tsv = {}
    codes_st_tsv = []

    for code in ask:
        code_st_tsv = [code,code_labels[code]]
        if code in ask:
            if code in code_cuis_dict:
                cui = code_cuis_dict[code]
                synonym = list(set(cui_synonyms[cui]))
                code_st_tsv +=[cui, " [SEP] ".join(synonym)[:100], cui_st[cui]]
            else:
                synonym = code_labels[code]

        codes_synonyms_tsv[code] = synonym
        codes_st_tsv.append(code_st_tsv)

    read.save_in_json("data/AskAPatient/code_dict_complete",codes_synonyms_tsv)
    read.save_in_tsv("data/AskAPatient/codes_st_tsv.tsv",codes_st_tsv)

# add_oov_processed()

def add_ooc_st():
    code_cuis = read.read_from_tsv("data/AskAPatient/codes_st_tsv_processed.tsv")
    code_cuis_dict = {line[0]:line[4] for line in code_cuis}
    read.save_in_json("data/AskAPatient/code_st_dict_complete", code_cuis_dict)

add_ooc_st()
