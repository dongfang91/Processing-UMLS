import read_files as read

def get_label(items):
    labels = []
    data= []
    for item in items:
        item = item.split("\t")
        labels.append(item[2])
        data.append([item[1],item[2]])
    return data,labels

##################### attention: MEDDRA PT  as label ############

def read_training():
    training1 = read.textfile2list("data/SMM4H/subtask3/task_3_normalization_training1.txt")
    training2 = read.textfile2list("data/SMM4H/subtask3/task_3_normalization_training2.txt")
    training3 = read.textfile2list("data/SMM4H/subtask3/task_3_normalization_training3.txt")
    training4 = read.textfile2list("data/SMM4H/subtask3/task_3_normalization_training4.txt")
    data1, labels1 = get_label(training1)
    data2, labels2 = get_label(training2)
    data3, labels3 = get_label(training3)
    data4, labels4 = get_label(training4)


    test_data = read.textfile2list("data/SMM4H/subtask3/task_3_normalization_evaluation.txt")
    data_test, labels_test = get_label(test_data)
    data_train = data1 + data2+ data3 + data4
    labels_all = list(set(labels1 + labels2 + labels3 + labels4 + labels_test))

    read.save_in_json("data/SMM4H/train_ori",data_train)
    read.save_in_json("data/SMM4H/test", data_test)
    read.save_in_json("data/SMM4H/labels_ori",labels_all)

# read_training()






def textfile2list_smm4h():
    file_path = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"
    smm4h = read.read_from_json("data/SMM4H/labels_ori")

    data = read.readfrom_txt(file_path)
    cuis_smm4h = []
    txt_list =[]
    for line in data.splitlines():
        # if "MDR" in line:
        #     print(line)
        line = line.split('|')
        if "MDR" in line[11]:
            cuis_smm4h.append(line[0])
            txt_list.append(line)

    read.save_in_json("data/SMM4H/synonyms",txt_list)
    read.save_in_json("data/SMM4H/cuis",list(set(cuis_smm4h)))

# textfile2list_smm4h()

def cui_labels():
    code_cuis = {}
    cui_infos = read.read_from_json("data/SMM4H/synonyms")
    print(len(cui_infos))
    for line in cui_infos:
        code = line[10]
        cui = line[0]
        if line[12] == "PT":
            if code in code_cuis:
                code_cuis[code] +=[cui]
            else:
                code_cuis[code] =[cui]
    print(len(code_cuis))

    extra = {"10012259": ["C0011253"],
             "10024130":["C0023222"],
             "10000497":["C0702166"],
             "1002243744151": ["C0917801"],
             "10040991": ["C0851578"],
             "10007541": ["C0018799"],
             "10027433": ["C0851358"],
             "10014698": ["C0014130"],
             "10044027": ["C0011334 "],
             "10013663": ["C1510472"],
             "MEDDRA PT": ["MEDDRA PT"]
             }

    code_cuis.update(extra)
    for code, cuis in code_cuis.items():
        if len(cuis)>1:
            print(code)
    read.save_in_json("data/SMM4H/code_cuis",code_cuis)
    read.save_in_json("data/SMM4H/label",list(code_cuis.keys()))

# cui_labels()

def textfile2list_smm4h():
    code_cuis = read.read_from_json("data/SMM4H/code_cuis")
    cuis = [cuis[0] for _,cuis in code_cuis.items()]
    file_path_synonym = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRCONSO.RRF"
    data = read.readfrom_txt(file_path_synonym)
    txt_list =[]
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in cuis:
            txt_list.append(line)

    read.save_in_json("data/SMM4H/synonyms_all",txt_list)

# textfile2list_smm4h()

def code_synonyms():
    txt_list = read.read_from_json("data/SMM4H/synonyms_all")
    code_synonyms = {}
    code_synonyms_new = {}
    for line in txt_list:
        if line[0] not in code_synonyms:
            code_synonyms[line[0]] = [line[14]]
        else:
            code_synonyms[line[0]] += [line[14]]

    for code,synonyms in code_synonyms.items():
        code_synonyms_new[code] = list(set(synonyms))
    read.save_in_json("data/SMM4H/cui_synonyms", code_synonyms_new)

# code_synonyms()

def textfile2list_smm4h_st():
    file_path_st = "/home/dongfang/umls_2017_AB_subset_test/2017AB/META/MRSTY.RRF"
    code_cuis = read.read_from_json("data/SMM4H/code_cuis")
    cuis = [cuis[0] for _,cuis in code_cuis.items()]
    data = read.readfrom_txt(file_path_st)
    txt_list ={}
    for line in data.splitlines():
        line = line.split('|')
        if line[0] in cuis:
            txt_list[line[0]] = line[2]
    read.save_in_json("data/SMM4H/cui_st_dict",txt_list)

# textfile2list_smm4h_st()

def add_oov_smm4h():
    cui_st = read.read_from_json("data/SMM4H/cui_st_dict")
    cui_synonyms = read.read_from_json("data/SMM4H/cui_synonyms")

    cui_st["MEDDRA PT"] =["df1"]
    cui_synonyms["MEDDRA PT"] = ["Extracted ADR"]

    code_cuis = read.read_from_json("data/SMM4H/code_cuis")
    codes = read.read_from_json("data/SMM4H/label")

    code_st = {}
    code_synonyms = {}


    for code in codes:
        cui = code_cuis[code][0]
        if cui == 'C0011334 ':
            cui = 'C0011334'
        code_st[code] = cui_st[cui]
        code_synonyms[code] = cui_synonyms[cui]
    read.save_in_json("data/SMM4H/code_dict_complete",code_synonyms)
    read.save_in_json("data/SMM4H/code_st_dict_complete",code_st)

# add_oov_smm4h()


