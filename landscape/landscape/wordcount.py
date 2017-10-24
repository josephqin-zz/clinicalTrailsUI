import os
import elasticsearch
import json
import sys
from joseph.landscape.esoperations_term_vector import ESOperations
#from esoperations import ESOperations 
from joseph.landscape import gene_occurance_wordcount as gow
from joseph.landscape import config

def get_all_trial_ids():
    path = config.xml_folder
    ids = [fn for fn in os.listdir(path) if fn.endswith('xml')]
    return ids

def get_term_vector(eso, trial_ids, use_synonym):
    es = elasticsearch.Elasticsearch()
    body = {}
    body['ids'] = trial_ids
    body['parameters'] = {}
    if use_synonym:
        body['parameters']['fields'] = config.fields
    else:
        body['parameters']['fields'] = config.fields_no_synonym
    body['parameters']['positions'] = False
    body['parameters']['offsets'] = False
    body['parameters']['payloads'] = False
    body['parameters']['term_statistics'] = True
    body['parameters']['field_statistics'] = False
    print(eso.index, eso.doc_type)
    res = es.mtermvectors(index=eso.index, doc_type=eso.doc_type,body=body,request_timeout = 100)
    docs = res['docs']
    #print(json.dumps(docs,indent=4))
    return docs
    
def LandScape(term, use_synonym=False):
    eso = ESOperations()
    res = {}
    if use_synonym:
        fields = config.fields
    else:
        fields = config.fields_no_synonym
    ids, doc_count = gow.main(term, use_synonym, size=2000) # get doc ids that contain this term
    docs = get_term_vector(eso, ids, use_synonym) # get term vectors of each doc
    #print('term: ', term)
    #print('number of doc: ', doc_count)
    res['term'] = term
    res['doc_count'] = doc_count
    get_total=True
    total = 0
    total_each_field = {}
    counts_in_doc = {}
    #total2 = 0

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
        #total2 += cur_count
    res['total_word_count'] = total
    res['word_count_each_doc'] = counts_in_doc
    res['total_word_count_each_field'] = total_each_field
    #print('total word count: ', total)
    #print('total count 2 :', total2)
    #print('--------------')
    #for key,value in counts_in_doc.items():
    #    print(key + ': ' + str(value))
    return res

