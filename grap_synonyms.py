import read_files as read

file_path = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"
ask = read.read_from_json("data/AskAPatient/label")
twa = read.read_from_json("data/TwADR-L/label")



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

def textfile2list_ask():
    data = read.readfrom_txt(file_path)
    cui_code_ask = {}
    codes = []
    for line in data.splitlines():
        line = line.split('|')
        if line[13] in ask:
            codes.append(line[13])
            if line[0] not in cui_code_ask:
                cui_code_ask[line[0]] = [line[13]]
            else:
                cui_code_ask[line[0]]+=[line[13]]
                # txt_list.append(line)

    # read.save_in_json("data/AskAPatient/synonyms",txt_list)
    read.save_in_json("data/AskAPatient/cui_codes",cui_code_ask)
    read.save_in_json("data/AskAPatient/codes",list(set(codes)))

# textfile2list_ask()
print(len(ask))
cui_codes = read.read_from_json("data/AskAPatient/cui_codes")
print(len(cui_codes))

for cui,codes in cui_codes.items():
    codes = list(set(codes))
    if len(codes)>=2:
        print(cui,codes)

code_cuis={}
for cui, codes in cui_codes.items():
    for code in list(set(codes)):
        if code not in code_cuis:
            code_cuis[code] = [cui]
        else:
            code_cuis[code] += [cui]
print(len(code_cuis))

for code,cuis in code_cuis.items():
    if len(cuis)>=2:
        print(code,cuis)

codes = read.read_from_json("data/AskAPatient/codes")
print(len(codes))

tsv_lines = []
for code in ask:
    line = [code]
    if code in code_cuis:
        line +=code_cuis[code]
    tsv_lines.append(line)


read.save_in_tsv("data/AskAPatient/code_cuis.tsv",tsv_lines)


# tsv_lines = []
# cuis = list(set(read.read_from_json("data/TwADR-L/cuis")))
# for code in twa:
#     line = [code]
#     if code in cuis:
#         line +=[code]
#     tsv_lines.append(line)
# read.save_in_tsv("data/TwADR-L/cui_cuis.tsv",tsv_lines)


