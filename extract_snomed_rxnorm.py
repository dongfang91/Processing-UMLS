import read_files as read
import numpy as np


def add_dict(term, key, value):
    if key not in term:
        term[key] = [value]
    else:
        term[key].append(value)
    return term

def process_umls():

    cui_all_snomed= {}
    cui_all_rxnorm = {}
    data = read.readfrom_txt("/extra/dongfangxu9/umls/umls_2017_subset/2017AB/META/MRCONSO.RRF")

    for line in data.splitlines():
        line_split = line.split('|')
        #### 11 = vocabulary, 12 = term type 14 = term name, 16 = suppress 0 = cui
        if "SNOMEDCT" in line_split[11]:
            if line_split[16] == "N":
                cui_all_snomed = add_dict(cui_all_snomed, line_split[0], line_split[14])

        if "RXNORM" in line_split[11]:
            if line_split[16] == "N":
                cui_all_rxnorm = add_dict(cui_all_rxnorm, line_split[0], line_split[14])

    read.save_in_json("/extra/dongfangxu9/umls/processed/snomed_dict",cui_all_snomed)
    read.save_in_json("/extra/dongfangxu9/umls/processed/rxnorm_dict", cui_all_rxnorm)

# process_umls()

def analyze():
    rxnorm_term = read.read_from_tsv("data/umls/all_rxnorm_suppress.tsv")
    snomed_term = read.read_from_tsv("data/umls/all_snowmed_suppress.tsv")
    rxnorm_term = list(set([item[0] for item in rxnorm_term]))
    snomed_term = list(set([item[0] for item in snomed_term]))

    print(len(rxnorm_term))
    print(len(snomed_term))

    rxnorm_term1 = read.read_from_json("data/umls/rxnorm_dict")
    snomed_term1= read.read_from_json("data/umls/snomed_dict")

    print(len(rxnorm_term1))
    print(len(snomed_term1))

# analyze()



def get_snomed_rxnorm_umls():

    rxnorm_term = read.read_from_json("/extra/dongfangxu9/umls/processed/rxnorm_dict")
    snomed_term = read.read_from_json("/extra/dongfangxu9/umls/processed/snomed_dict")
    cui_all = list(set(list(rxnorm_term.keys()) + list(snomed_term.keys())))

    cui_all_synonyms = {}
    # print(len(cui_all))
    data = read.readfrom_txt("/extra/dongfangxu9/umls/umls_2017_subset/2017AB/META/MRCONSO.RRF")
    for line in data.splitlines():
        line_split = line.split('|')
        if line_split[0] in cui_all:
                cui_all_synonyms = add_dict(cui_all_synonyms, line_split[0], line_split)

get_snomed_rxnorm_umls()






def get_preferred_name(cui_lists, vocab_idx):

    cui_vocab_idx = []
    vocab_tt_lists = []
    term_lists = []
    ranking_lists = []
    idx_lists = []
    for idx , cui_info in enumerate(cui_lists):
        term_lists.append(cui_info[14])
        vocab_tt  = cui_info[11] + "|" + cui_info[12]
        if vocab_tt in vocab_idx:
            idx_lists.append(idx)
            ranking_lists.append(vocab_idx[vocab_tt])
    return term_lists[idx_lists[np.argmin(ranking_lists)]]




def get_pt():
    # cuis_all = read.read_from_json("data/umls/snomed_rxnorm_dict.txt")
    ranking = read.textfile2list("data/umls_vocab_ranking")
    vocab_idx = {item:idx for idx, item in enumerate(ranking)}
    print(vocab_idx)
    idx_vocab = {idx:item for idx, item in enumerate(ranking)}


# print(get_pt())











