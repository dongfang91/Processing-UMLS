import read_files as read

file_path_synonym = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"
file_path_st = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRSTY.RRF"
ask = read.read_from_json("data/AskAPatient/label")
twa = read.read_from_json("data/TwADR-L/label")
twa_cuis_all = read.read_from_tsv("data/TwADR-L/cui_cuis - cui_cuis.tsv")
twa_cuis = [item[1] for item in twa_cuis_all]
twa_cuis_dict = {item[0]:item[1] for item in twa_cuis_all}



def textfile2list_twa():
    data = read.readfrom_txt(file_path_synonym)
    txt_list ={}
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in twa_cuis:
            if line[0] not in txt_list:
                txt_list[line[0]] = [line[14]]
            else:
                txt_list[line[0]] += [line[14]]

    read.save_in_json("data/TwADR-L/cui_dict",txt_list)

# textfile2list_twa()

def textfile2list_twa_st():
    data = read.readfrom_txt(file_path_st)
    txt_list ={}
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in twa_cuis:
            txt_list[line[0]] = line[2]
    read.save_in_json("data/TwADR-L/cui_st_dict",txt_list)

# textfile2list_twa_st()
def add_oov():
    cui_st = read.read_from_json("data/TwADR-L/cui_st_dict")
    cui_synonyms = read.read_from_json("data/TwADR-L/cui_dict")
    ##### some cuis is out of vocabulary #########
    cui_extra = [cui for cui in twa if cui not in twa_cuis]
    for cui in cui_extra:
        cui_st[cui] = cui_st[twa_cuis_dict[cui]]
        cui_synonyms[cui] = cui_synonyms[twa_cuis_dict[cui]]
    read.save_in_json("data/TwADR-L/cui_dict_complete",cui_synonyms)
    read.save_in_json("data/TwADR-L/cui_st_dict_complete",cui_st)

# add_oov()
# cui_synonyms = read.read_from_json("data/TwADR-L/cui_dict_complete")
# print(len(cui_synonyms))
# for cui in twa:
#     if cui not in cui_synonyms:
#         print(cui)



# print(len(cui_synonyms))