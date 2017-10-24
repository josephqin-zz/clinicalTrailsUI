import os
import elasticsearch
import json
import sys
import string
import re
from landscape.landscape_v2.esoperations_term_vector import ESOperations
#from esoperations import ESOperations
from landscape.landscape_v2 import gene_occurance_wordcount as gow
from landscape.landscape_v2 import config

punctuation = list(string.punctuation)
punctuation.append(' ')

def get_all_trial_ids():
    path = config.xml_folder
    ids = [fn for fn in os.listdir(path) if fn.endswith('xml')]
    return ids

def get_term_vector(eso, trial_ids, use_synonym, case_sensitive=False):
    es = elasticsearch.Elasticsearch()
    body = {}
    body['ids'] = trial_ids
    body['parameters'] = {}
    if use_synonym:
        body['parameters']['fields'] = config.fields
    elif case_sensitive:
        body['parameters']['fields'] = config.fields_no_syn_case_sstv
    else:
        body['parameters']['fields'] = config.fields_no_synonym
    #body['parameters']['positions'] = False
    body['parameters']['positions'] = True
    body['parameters']['offsets'] = False
    body['parameters']['payloads'] = False
    body['parameters']['term_statistics'] = True
    body['parameters']['field_statistics'] = False
    print(eso.index, eso.doc_type)
    res = es.mtermvectors(index=eso.index, doc_type=eso.doc_type,body=body,request_timeout = 100)
    docs = res['docs']
    #print(json.dumps(docs,indent=4))
    return docs
    
def LandScape(term, case_sensitive=False,use_synonym=False):
    eso = ESOperations()
    res = {}
    size = 2000
    if use_synonym:
        fields = config.fields
    else:
        if case_sensitive:
            fields = config.fields_no_syn_case_sstv
        else:
            fields = config.fields_no_synonym
    if not case_sensitive:
        term = term.lower()
    ids, doc_count = gow.main(term, case_sensitive, use_synonym, size=size) # get doc ids that contain this term
    res['term'] = term
    res['doc_count'] = doc_count
    if ids == []:   # if no doc contains this term
        return {} 
    docs = get_term_vector(eso, ids, use_synonym, case_sensitive) # get term vectors of each doc

    get_total=True
    total = 0
    total_each_field = {}
    counts_in_doc = {}
    total2 = 0

    saw_fields = []
    for d in docs:
        cur_count = 0
        doc_id = d['_id']
        for tv in d['term_vectors']:
            doc_terms = d['term_vectors'][tv]['terms']
            if term in doc_terms:
                cur_count += doc_terms[term]['term_freq']  # term_freq : in this sec in this doc
                if saw_fields!=fields and tv not in saw_fields:
                    total_each_field[tv] = doc_terms[term]['ttf'] # ttf : in this sec in all docs
                    total += doc_terms[term]['ttf']
                    saw_fields.append(tv)
        counts_in_doc[doc_id] = cur_count
        total2 += cur_count
    res['total_word_count'] = total
    res['word_count_each_doc'] = counts_in_doc
    res['total_word_count_each_field'] = total_each_field
    print('total word count: ', total)
    print('total count 2 :', total2)
    #print('--------------')
    #for key,value in counts_in_doc.items():
    #    print(key + ': ' + str(value))
    return res

def ls_phrase(term, use_synonym=False, case_sensitive=False):
    term = term.lower()
    eso = ESOperations()
    res = {}
    if use_synonym:
        fields = config.fields
    else:
        fields = config.fields_no_synonym
    ids, doc_count = gow.main(term, case_sensitive, use_synonym, size=2000) # get doc ids that contain this term
    res['term'] = term
    res['doc_count'] = doc_count
    if ids == []:   # if no doc contains this term
        return {} 
    docs = get_term_vector(eso, ids, use_synonym, case_sensitive) # get term vectors of each doc

    get_total=True
    total = 0
    total_each_field = {}
    counts_in_doc = {}
    #total2 = 0
    terms = list(filter(None, re.split("[{0}]+".format(''.join(punctuation)), term)))
    positions = {}
    len_terms = len(terms)
    for i in range(0, len_terms):
        positions[i] = []
    saw_fields = []
    for d in docs:
        cur_count = 0
        doc_id = d['_id']
        for tv in d['term_vectors']:
            print(tv)
            positions = {}
            for i in range(0, len_terms):
                positions[i] = []
            doc_terms = d['term_vectors'][tv]['terms']
            for j in range(0, len_terms):
                t = terms[j]
                if t in doc_terms:
                    #print(doc_terms)
                    tokens = doc_terms[t]['tokens']
                    if j == 0:
                        for token in tokens:
                            positions[j].append(token['position'])
                    else:
                        for token in tokens:
                            token_pos = token['position']
                            if token_pos-1 in positions[j-1]:
                                positions[j].append(token_pos)
            cur_count += len(positions[len_terms-1])
            total_each_field[tv] = total_each_field.setdefault(tv, 0) + len(positions[len_terms-1])
        counts_in_doc[doc_id] = cur_count
        total += cur_count
    res['total_word_count'] = total
    res['word_count_each_doc'] = counts_in_doc
    res['total_word_count_each_field'] = total_each_field
    return res

# if __name__ == '__main__':
#     term = sys.argv[1]
#     case_sensitive = False
#     if len(sys.argv) > 2:
#         case_sensitive = True
#     else:
#         term = term.lower()
#     if any((p in term) for p in punctuation):
#         res = ls_phrase(term)
#     else:
#         res = LandScape(term, case_sensitive)
#     print(json.dumps(res, indent=4))
#     #for key,value in res.items():
#     #    print(key + ':')
#     #    print(value)
