from __future__ import print_function

import os
import sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import xml.etree.ElementTree as etree
from joseph.landscape.esoperations_term_vector import ESOperations
from joseph.landscape import config

def gene_count(es, gene, size, use_synonym):

    body = {}
    body["query"] = {}
    body["query"]["bool"] = {}
    body["query"]["bool"]["must"] = []
    body["query"]["bool"]["should"] = []

    search_factors = []

    #landscape_fields = ["Inclusion Criteria", "Inclusion Criteria.whitespace", "Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
    if use_synonym:
        landscape_fields = config.fields
    else:
        landscape_fields = config.fields_no_synonym
    #landscape_fields = ["Purpose","description","Inclusion Criteria","official_title","brief_title","Conditions","Inclusion Criteria.normal",
    #                    "Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace",
    #                    "brief_title.whitespace","Conditions.whitespace", "Exclusion Criteria","Exclusion Criteria.whitespace",
    #                    "Exclusion Criteria.normal"]

    if gene is not None:
        search_factors.append('--gene')
        search_factors.append(gene)
        body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": gene,
                            "type": "phrase",
                            "fields": landscape_fields
                        }})


    response = es.queryES(body,size)
    return response['hits']

#Query the ES index with the search body that we have created

def main(gene,use_synonym,size=50):
    #counts = {}
    #hits_ids = {}
    es = ESOperations()
    #gene_file = 'genes_new_syn.txt'
    #count_file = 'genes_count_new_syn2.txt'
    if len(gene) < 3:
        return []
    res_hits = gene_count(es, gene, size,use_synonym)
    doc_count = res_hits['total']
    ids = [i['_id'] for i in res_hits['hits']]
    #hits_ids[gene] = ids

    return ids, doc_count

if __name__ == '__main__':
    main()
