import argparse
import os
import sys
import json
import re
from operator import itemgetter

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import xml.etree.ElementTree as etree
from joseph.ElasticSearch.esoperations_disease import ESOperations
from joseph.ElasticSearch import config
# from weights_config import *
from joseph.ElasticSearch import weights_config as wconf

from joseph.ElasticSearch import outputs_for_front as outff
from joseph.ElasticSearch import tree_build_out as tb

RES_NUM = 50
MAX_NUM = 2000
disease_multi_query_fields = ["Purpose.disease^" + wconf.w_purpose, "description.disease^" + wconf.w_des,
                                  "Inclusion Criteria.disease^" + wconf.w_ic,
                                  "official_title.disease^" + wconf.w_ot, "brief_title.disease^" + wconf.w_bt,
                                  "Conditions.disease^" + wconf.w_con, "Conditions.disease_whitespace","Conditions","Conditions.whitespace",
                                  "Purpose.disease_whitespace^" + wconf.w_purpose,
                                  "description.disease_whitespace^" + wconf.w_des]

gene_multi_query_fields = ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
                               "Conditions",
                               "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
                               "official_title.whitespace", "brief_title.whitespace", "Conditions.whitespace"]

class myargs:
    def __init__(self):
        self.disease = None
        self.gene = None
        self.age = None
        self.gender = None
        self.results = RES_NUM
        self.aas = None
        self.stage = None
        self.grade = None
        self.start = None
        self.end = None
        self.slop = None
        self.must = None
        self.must_not = None


def query_body(myargs):
    body = {}
    body["query"] = {}
    body["query"]["bool"] = {}
    body["query"]["bool"]["filter"] = []
    body["query"]["bool"]["must"] = []
    body["query"]["bool"]["should"] = []
    body["query"]["bool"]["must_not"] = []
    # body["query"]["range"]["update_date"] = {}

    search_factors = []

    if myargs.aas is not None:
        myargs.aas = myargs.aas.replace("/", "//")
    """
    disease_multi_query_fields = ["Purpose.disease^"+w_purpose,"description.disease^"+w_des,"Inclusion Criteria.disease^"+w_ic,
                          "official_title.disease^"+w_ot,"brief_title.disease^"+w_bt,"Conditions.disease^"+w_con,
                          "Purpose.disease_whitespace^"+w_purpose,"description.disease_whitespace^"+w_des,
                          "Inclusion Criteria.disease_whitespace^"+w_ic,"official_title.disease_whitespace^"+w_ot,
                          "brief_title.disease_whitespace^"+w_bt,"Conditions.disease_whitespace^"+w_con]
    """

    """
    disease_multi_query_fields = ["Purpose.disease^" + wconf.w_purpose, "description.disease^" + wconf.w_des,
                                  "Inclusion Criteria.disease^" + wconf.w_ic,
                                  "official_title.disease^" + wconf.w_ot, "brief_title.disease^" + wconf.w_bt,
                                  "Conditions.disease^" + wconf.w_con,
                                  "Purpose.disease_whitespace^" + wconf.w_purpose,
                                  "description.disease_whitespace^" + wconf.w_des]

    gene_multi_query_fields = ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
                               "Conditions",
                               "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
                               "official_title.whitespace", "brief_title.whitespace", "Conditions.whitespace"] 
    """
    if myargs.slop is None:
        slop = config.slop
    else:
        slop = myargs.slop

    if myargs.disease is not None:
        search_factors.append("--disease")
        search_factors.append(myargs.disease)
        body["query"]["bool"]["must"].append({
            "multi_match":
                {
                    "query": myargs.disease,
                    "type": "phrase",
                    "boost": wconf.boost_must_value,
                    "fields": disease_multi_query_fields,
                    "slop": slop}})

        if wconf.use_should:
            print(wconf.use_should)
            body["query"]["bool"]["should"].append({
                "multi_match": {
                    "query": myargs.disease,
                    "boost": wconf.boost_should_value,
                    "fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
                }
            })

    if myargs.gene is not None:
        search_factors.append('--gene')
        search_factors.append(myargs.gene)
        body["query"]["bool"]["must"].append({
            "multi_match":
                {
                    "query": myargs.gene,
                    "boost": wconf.boost_must_value,
                    "fields": gene_multi_query_fields}})

        body["query"]["bool"]["should"].append({
            "multi_match": {
                "query": myargs.gene,
                "boost": 0.1,
                "fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
            }
        })

    age = ""
    if myargs.age is not None:
        search_factors.append('--age')
        search_factors.append(str(myargs.age))
        body["query"]["bool"]["must"].append({
            "range": {
                "maximumAge": {"gte": myargs.age * 365 * 24 * 60}}})
        body["query"]["bool"]["must"].append({
            "range": {
                "minimumAge": {"lte": myargs.age * 365 * 24 * 60}}})
        if myargs.age < 18:
            age = "&age=0"
        elif myargs.age >= 18 and myargs.age < 66:
            age = "&age=1"
        else:
            age = "&age=2"

    body["query"]["bool"]["must"].append({"bool": {}})
    body["query"]["bool"]["must"][-1]["bool"]["should"] = []
    gender = ""
    if myargs.gender is None:
        body["query"]["bool"]["must"][-1]["bool"]["should"].append({"match": {
            "gender": "Male"
        }})
        body["query"]["bool"]["must"][-1]["bool"]["should"].append({
            "match": {
                "gender": "Female"
            }})
        body["query"]["bool"]["must"][-1]["bool"]["should"].append({
            "match": {
                "gender": "Both"
            }})
    else:
        search_factors.append('--gender')
        search_factors.append(myargs.gender)
        body["query"]["bool"]["must"][-1]["bool"]["should"].append({
            "match": {
                "gender": myargs.gender
            }})
        body["query"]["bool"]["must"][-1]["bool"]["should"].append({
            "match": {
                "gender": "Both"
            }})
        gender = "&gndr=" + myargs.gender

    if myargs.results is not None:
        search_factors.append('--results')
        search_factors.append(str(myargs.results))
    else:
        search_factors.append('--results')
        search_factors.append(str(RES_NUM))

    if myargs.aas is not None:
        search_factors.append('--aas')
        search_factors.append(myargs.aas)
        body["query"]["bool"]["must"].append({
            "multi_match": {
                "query": myargs.aas,
                "boost": wconf.boost_must_value,
                "fields": gene_multi_query_fields}})

        if wconf.use_should:
            body["query"]["bool"]["should"].append({
                "multi_match": {
                    "query": myargs.aas,
                    "boost": wconf.boost_should_value,
                    "fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
                }
            })

    if myargs.stage is not None:
        search_factors.append('--stage')
        search_factors.append(myargs.stage)
        body["query"]["bool"]["must"].append({
            "match": {
                "stages": myargs.stage}})

    if myargs.grade is not None:
        search_factors.append('--grade')
        search_factors.append(myargs.grade)
        body["query"]["bool"]["must"].append({
            "match": {
                "grades": myargs.grade}})

    if myargs.start is not None:
        search_factors.append('--start')
        search_factors.append(myargs.start)
        body["query"]["bool"]["filter"].append({
            "range": {
                "update_date": {
                    'gte': myargs.start
                }
            }
        })
        if myargs.end is not None:
            search_factors.append('--end')
            search_factors.append(myargs.end)
            body["query"]["bool"]["filter"][-1]["range"]["update_date"]['lte'] = myargs.end
    else:
        if myargs.end is not None:
            search_factors.append('--end')
            search_factors.append(myargs.end)
            body["query"]["bool"]["filter"].append({
                "range": {
                    "update_date": {
                        'lte': myargs.end
                    }
                }
            })
    return body, age, gender, search_factors


def add_must_not(body, myargs, disease=None, aas=None):
    """
    when querying parent disease, the child diseases that's already queried have to be excluded.
    e.g., disease B is parent disease of A.
    we already get query results for A, and now is getting results for B.
    Now, we need to exclude documents that contain A from results of querying B.
    one way to do it is using elasticsearch's 'must_not' query.
    when querying for B, we are querying 'contains B and not contains A'.
    :param body:
    :param myargs:
    :param disease:
    :return:
    """
    """
    disease_multi_query_fields = ["Purpose.disease^" + wconf.w_purpose, "description.disease^" + wconf.w_des,
                                  "Inclusion Criteria.disease^" + wconf.w_ic,
                                  "official_title.disease^" + wconf.w_ot, "brief_title.disease^" + wconf.w_bt,
                                  "Conditions.disease^" + wconf.w_con,
                                  "Purpose.disease_whitespace^" + wconf.w_purpose,
                                  "description.disease_whitespace^" + wconf.w_des]
    """
    if myargs.slop is None:
        slop = config.slop
    else:
        slop = myargs.slop
    body['query']['bool']['must_not'].append({
        "multi_match":
            {
                "query": disease,
                "type": "phrase",
                "fields": disease_multi_query_fields,
                "slop": slop}
    })


def query_one_level(diseases, body, myargs, es, cur_level_res, aas_hier=False):
    level_count = 0
    cur_level_hits = []
    for disease in diseases:
        body["query"]["bool"]["must"][0]['multi_match']['query'] = disease
        body["query"]["bool"]["must"][0]['multi_match']['boost'] = wconf.boost_must_value
        if myargs.results is not None:
            response = es.queryES(body, myargs.results)
        else:
            response = es.queryES(body, RES_NUM)
        hits, new_count = get_hits(response, myargs.aas, aas_hier)
        cur_level_hits.extend(hits)
        level_count += new_count
        add_must_not(body, myargs, disease)
    cur_level_hits = sorted(cur_level_hits, key=itemgetter('score'), reverse=True)
    cur_level_res['hits'].extend(cur_level_hits)

    return level_count


def get_hits(response, aas, aas_hier=False):
    hits = []
    count = response['hits']['total']
    for hit in response['hits']['hits']:
        if aas_hier:
            hits.append({'id': hit['_id'], 'score': hit['_score'], 'context': hit['_source'], 'aas': aas})
        else:
            hits.append({'id': hit['_id'], 'score': hit['_score']})
    return hits, count


def dis_hier_old(myargs, es):
    """
    utilize disease ontology (parent disease) information, from tree_build_out module.
    First returns disease itself as level 1, with 1 as weight for scoring,
    then comes its first parent as level 2, with 1/5.0 as weight,
    then all other parents (before 'cancer') as level 3, with 1/25.0 as weight.
    :param myargs: dictionary. e.g., {"disease":"lung cancer", 'gene':'egfr', ....}.
    :param body: query body for elasticsearch
    :return:
    """
    # Query the ES index with the search body that we have created
    diseases = [myargs.disease]
    count = 0  # total number of results
    level = 1  # disease itself
    hit_ids = []
    res = []
    parents = tb.main(myargs.disease.lower())  # get parent diseases of given disease
    length = len(parents)
    body, age, gender, search_factors = query_body(myargs)
    while diseases:
        level_count = 0
        parent_diseases = []
        if length > 1:
            if level == 1:
                pd = list(parents[1].keys())[0]
                parent_diseases.append(pd)
            elif level == 2:
                if length > 2:
                    for i in range(2, length):
                        pd = list(parents[i].keys())[0]
                        if pd == 'cancer':
                            break
                        parent_diseases.append(pd)
        cur_level_res = {}
        cur_level_res['level'] = level
        cur_level_res['diseases'] = diseases
        cur_level_res['hits'] = []

        level_count = query_one_level(diseases, body, myargs, es, cur_level_res, hit_ids, count)

        cur_level_res['total_hits'] = level_count
        res.append(cur_level_res)
        diseases = parent_diseases
        wconf.boost_must_value = wconf.boost_must_value / 5.0
        level += 1
    return res, count


def dis_hier(myargs, es):
    """
    utilize disease ontology (parent disease) information, from tree_build_out module.
    First returns disease itself as level 1, with 1 as weight for scoring,
    then comes its first parent as level 2, with 1/5.0 as weight,
    then all other parents (before 'cancer') as level 3, with 1/25.0 as weight.
    :param myargs: dictionary. e.g., {"disease":"lung cancer", 'gene':'egfr', ....}.
    :param body: query body for elasticsearch
    :return:
    """
    # Query the ES index with the search body that we have created
    diseases = [myargs.disease]
    count = 0  # total number of results
    level = 1  # disease itself
    hit_ids = []
    res = []
    parents = tb.main(myargs.disease.lower())  # get parent diseases of given disease
    length = len(parents)
    body, age, gender, search_factors = query_body(myargs)
    while diseases:
        level_count = 0
        parent_diseases = []
        if length > 1:
            if level == 1:
                pd = list(parents[1].keys())[0]
                parent_diseases.append(pd)
            elif level == 2:
                if length > 2:
                    for i in range(2, length):
                        pd = list(parents[i].keys())[0]
                        if pd == 'cancer':
                            break
                        parent_diseases.append(pd)
        cur_level_res = {}
        cur_level_res['level'] = level
        cur_level_res['diseases'] = diseases
        cur_level_res['hits'] = []

        level_count = query_one_level(diseases, body, myargs, es, cur_level_res)
        count += level_count

        cur_level_res['total_hits'] = level_count
        res.append(cur_level_res)
        diseases = parent_diseases
        wconf.boost_must_value = wconf.boost_must_value / 5.0
        level += 1
    return res, count


def dis_hier_aas(myargs, es):
    """
    utilize disease ontology (parent disease) information, from tree_build_out module.
    First returns disease itself as level 1, with 1 as weight for scoring,
    then comes its first parent as level 2, with 1/5.0 as weight,
    then all other parents (before 'cancer') as level 3, with 1/25.0 as weight.
    :param myargs: dictionary. e.g., {"disease":"lung cancer", 'gene':'egfr', ....}.
    :param body: query body for elasticsearch
    :return:
    """
    # Query the ES index with the search body that we have created
    diseases = [myargs.disease]
    count = 0  # total number of results
    level = 1  # disease itself
    hit_ids = []
    res = []
    parents = tb.main(myargs.disease.lower())  # get parent diseases of given disease
    length = len(parents)
    body, age, gender, search_factors = query_body(myargs)
    body2 = {}
    if myargs.aas is not None and myargs.aas != '':
        aas = myargs.aas
        myargs.aas = None
        body2, age, gender, search_factors2 = query_body(myargs)
        body2['query']['bool']['must_not'].append({
            "multi_match":
                {
                    "query": aas,
                    "fields": gene_multi_query_fields
                }
        })
        myargs.aas = aas
    while diseases:
        level_count = 0
        parent_diseases = []
        if length > 1:
            if level == 1:
                pd = list(parents[1].keys())[0]
                parent_diseases.append(pd)
            elif level == 2:
                if length > 2:
                    for i in range(2, length):
                        pd = list(parents[i].keys())[0]
                        if pd == 'cancer':
                            break
                        parent_diseases.append(pd)
        cur_level_res = {}
        cur_level_res['level'] = level
        cur_level_res['diseases'] = diseases
        cur_level_res['hits'] = []

        level_count = query_one_level(diseases, body, myargs, es, cur_level_res, True)
        if myargs.aas is not None and myargs.aas != '':
            aas = myargs.aas
            myargs.aas = None
            level_count2 = query_one_level(diseases, body2, myargs, es, cur_level_res, True)
            level_count += level_count2
            myargs.aas = aas
        cur_level_res['total_hits'] = level_count
        count += level_count
        res.append(cur_level_res)
        diseases = parent_diseases
        wconf.boost_must_value = wconf.boost_must_value / 5.0
        level += 1
    return res, count


def normal(args,index):
    es = ESOperations(index)
    print(index)
    body, age, gender, search_factors = query_body(args)
    if args.results is not None:
        response = es.queryES(body, args.results)
    else:
        response = es.queryES(body, RES_NUM)
    print('Search Criteria:')
    print(search_factors)
    res = outff.tool_only(response)
    return res
    """
    if config.output_format == 1:
        outputs.tool_only(response)
    elif config.output_format == 2:
        outputs.tool_and_ctgov(response, myargs, gender, age)
    else:
        print('wrong output format setting in config.py. It must be 1 or 2')
    if config.output_details:
        outputs.output_details_in_json(response, search_factors)
    """

if __name__ == '__main__':
    #es = ESOperations('test_disease')
    argumentParser = argparse.ArgumentParser(description='Pass the input')
    argumentParser.add_argument('-d', '--disease', help='disease type', type=str)
    argumentParser.add_argument('-g', '--gene', help='gene mutation', type=str)
    argumentParser.add_argument('-a', '--age', help='age of the patient in years', type=int)
    argumentParser.add_argument('-s', '--gender', help='gender of the patient', type=str)
    argumentParser.add_argument('-n', '--results', help='number of results to display', type=int, default=RES_NUM)
    argumentParser.add_argument('-m', '--aas', help='amino acid substitution', type=str)
    argumentParser.add_argument('-k', '--stage', help='stage of the disease', type=str)
    argumentParser.add_argument('-l', '--grade', help='grade of the tumor', type=str)
    argumentParser.add_argument('-sd', '--start', help='last update date start from', type=str)
    argumentParser.add_argument('-ed', '--end', help='last update date end at', type=str)
    argumentParser.add_argument('-slop', '--slop', help='slop of disease terms', type=int)
    args = argumentParser.parse_args()
    #"""
    #res, count = dis_hier(args, es)
    #res, count = dis_hier_aas(args, es)
    #print(count)
    #for r in res:
    #    print('----------------')
    #    print(r)
        # normal(args)
    #"""
    print(normal(args,'test12'))
