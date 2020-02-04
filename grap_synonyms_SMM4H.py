import read_files as read

file_path = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"

def textfile2list_twa():
    data = read.readfrom_txt(file_path)
    cuis_twa = []
    txt_list =[]
    for line in data.splitlines():
        if "SNO" in line:
            print(line)
        line = line.split('|')
        if line[0] in twa:
            cuis_twa.append(line[0])
            txt_list.append(line)

    read.save_in_json("data/TwADR-L/synonyms",txt_list)
    read.save_in_json("data/TwADR-L/cuis",list(set(cuis_twa)))

# textfile2list_twa()
# print(len(twa))
# cuis = list(set(read.read_from_json("data/TwADR-L/cuis")))
# print(len(cuis))
# print([cui for cui in twa if cui not in cuis])




