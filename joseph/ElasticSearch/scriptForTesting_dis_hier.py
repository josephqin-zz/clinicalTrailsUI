from __future__ import print_function

import argparse
import os
import sys
import json
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from esoperations_disease import ESOperations
import config as config
from weights_config import *

import tree_build_out as tb

es = ESOperations('test7')
argumentParser = argparse.ArgumentParser(description='Pass the input')
argumentParser.add_argument('-d','--disease', help='disease type', type = str )
argumentParser.add_argument('-g','--gene',help='gene mutation',type = str)
argumentParser.add_argument('-a','--age',help='age of the patient in years',type = int)
argumentParser.add_argument('-s','--gender',help='gender of the patient',type = str)
argumentParser.add_argument('-n','--results',help='number of results to display',type = int,default=50)
argumentParser.add_argument('-m','--aas',help='amino acid substitution',type = str)
argumentParser.add_argument('-k','--stage',help='stage of the disease',type = str)
argumentParser.add_argument('-l','--grade',help='grade of the tumor',type = str)
argumentParser.add_argument('-sd', '--start',help='last update date start from',type=str)
argumentParser.add_argument('-ed', '--end',help='last update date end at',type=str)
argumentParser.add_argument('-slop', '--slop',help='slop of disease terms',type=int)
args = argumentParser.parse_args()

print(type(args))


body = {}
body["query"] = {}
body["query"]["bool"] = {}
body["query"]["bool"]["filter"] = []
body["query"]["bool"]["must"] = []
body["query"]["bool"]["should"] = []
#body["query"]["range"]["update_date"] = {}


search_factors = []

if args.aas is not None:
    args.aas = args.aas.replace("/","//")
"""
disease_multi_query_fields = ["Purpose.disease^"+w_purpose,"description.disease^"+w_des,"Inclusion Criteria.disease^"+w_ic,
                      "official_title.disease^"+w_ot,"brief_title.disease^"+w_bt,"Conditions.disease^"+w_con,
                      "Purpose.disease_whitespace^"+w_purpose,"description.disease_whitespace^"+w_des,
                      "Inclusion Criteria.disease_whitespace^"+w_ic,"official_title.disease_whitespace^"+w_ot,
                      "brief_title.disease_whitespace^"+w_bt,"Conditions.disease_whitespace^"+w_con]
"""
disease_multi_query_fields = ["Purpose.disease^"+w_purpose,"description.disease^"+w_des,"Inclusion Criteria.disease^"+w_ic,
                      "official_title.disease^"+w_ot,"brief_title.disease^"+w_bt,"Conditions.disease^"+w_con,
                      "Purpose.disease_whitespace^"+w_purpose,"description.disease_whitespace^"+w_des]
#"""
if args.slop is None:
    slop = config.slop
else:
    slop = args.slop

if args.disease is not None:
    search_factors.append("--disease")
    search_factors.append(args.disease)
    body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": args.disease,
                            "type": "phrase",
                            "boost":boost_must_value,
                            "fields": disease_multi_query_fields,
                            "slop": slop}})
    
    if use_should:
        print(use_should) 
        body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : args.disease,
                  "boost" : boost_should_value,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }

        })
    

if args.gene is not None:
    search_factors.append('--gene')
    search_factors.append(args.gene)
    body["query"]["bool"]["must"].append({
                        "multi_match":
                        {
                            "query": args.gene,
                            "boost" :boost_must_value,
                            "fields": ["Purpose","description","Inclusion Criteria","official_title","brief_title","Conditions",
                                       "Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace","brief_title.whitespace","Conditions.whitespace"]}})


    body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : args.gene,
                  "boost" : 0.1,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }

        })
    
age = ""
if args.age is not None:
    search_factors.append('--age')
    search_factors.append(str(args.age))
    body["query"]["bool"]["must"].append({
                        "range":{
                            "maximumAge":{"gte":args.age * 365 * 24 * 60}}})
    body["query"]["bool"]["must"].append({
                        "range":{
                            "minimumAge":{"lte":args.age * 365 * 24 * 60}}})
    if args.age < 18:
        age = "&age=0"
    elif args.age >= 18 and args.age < 66:
        age = "&age=1"
    else:
        age = "&age=2"

body["query"]["bool"]["must"].append({"bool": {}})
body["query"]["bool"]["must"][-1]["bool"]["should"] = []
gender = ""
if args.gender is None:
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
    search_factors.append(args.gender)
    body["query"]["bool"]["must"][-1]["bool"]["should"].append({
                                "match": {
                                    "gender": args.gender
                                }})
    body["query"]["bool"]["must"][-1]["bool"]["should"].append({
                                "match": {
                                    "gender": "Both"
                                }})
    gender = "&gndr=" + args.gender

if args.results is not None:
    search_factors.append('--results')
    search_factors.append(str(args.results))

if args.aas is not None :
    search_factors.append('--aas')
    search_factors.append(args.aas)
    body["query"]["bool"]["must"].append({
          "multi_match": {
            "query": args.aas,
            "boost" :boost_must_value,
            "fields": disease_multi_query_fields}})


    if use_should:
        body["query"]["bool"]["should"].append({
          "multi_match": {
                  "query" : args.aas,
                  "boost" : boost_should_value,
                  "fields" : ["Exclusion Criteria","Exclusion Criteria.whitespace","Exclusion Criteria.normal"]
                }

        })
    

if args.stage is not None:
    search_factors.append('--stage')
    search_factors.append(args.stage)
    body["query"]["bool"]["must"].append({
          "match": {
            "stages": args.stage }})


if args.grade is not None:
    search_factors.append('--grade')
    search_factors.append(args.grade)
    body["query"]["bool"]["must"].append({
          "match": {
            "grades": args.grade }})


if args.start is not None:
    search_factors.append('--start')
    search_factors.append(args.start)
    body["query"]["bool"]["filter"].append({
        "range":{
            "update_date":{
                'gte': args.start
            }
        }
    })
    if args.end is not None:
        search_factors.append('--end')
        search_factors.append(args.end)
        body["query"]["bool"]["filter"][-1]["range"]["update_date"]['lte'] = args.end
else:
    if args.end is not None:
        search_factors.append('--end')
        search_factors.append(args.end)
        body["query"]["bool"]["filter"].append({
            "range":{
                "update_date":{
                    'lte': args.end
                }
            }
        })   

def update_print(print_content, response, hit_ids):
    count = 0
    if not hit_ids:
        for hit in response['hits']['hits']:
            hit_ids.append(hit['_id'])
            print_content.append(str(hit['_id']) + ", score: " + str(hit['_score']))
    else:
        for hit in response['hits']['hits']:
            if hit not in hit_ids:
                hit_ids.append(hit['_id'])
                count += 1
                print_content.append(str(hit['_id']) + ", score: " + str(hit['_score']))
    return count

#Query the ES index with the search body that we have created
diseases = [args.disease]
print(diseases)
count = 0  # total number of results
level = 1  # disease itself
hit_ids = []
print_content = []
parents = tb.main(args.disease.lower())  # get parent diseases of given disease
length = len(parents)
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
    print_content.append('------------------')
    print_content.append('level: {0}'.format(level))
    print_content.append(', '.join(diseases))
    print_content.append('------------------')
    for disease in diseases:
        body["query"]["bool"]["must"][0]['multi_match']['query'] = disease
        body["query"]["bool"]["must"][0]['multi_match']['boost'] = boost_must_value
        #print(body["query"]["bool"]["must"][0])
        print(args.results)
        response = es.queryES(body,args.results)
        if level == 1:
            count += response['hits']['total']
            level_count += response['hits']['total']
            update_print(print_content, response, hit_ids)
        else:
            new_count = update_print(print_content, response, hit_ids)
            count += new_count
            level_count += new_count
        #parent_diseases.extend(get_parents(disease))
    print_content.append('level {0} total number of hits: {1}'.format(level, level_count))
    diseases = parent_diseases
    boost_must_value = boost_must_value / 5.0
    level += 1

print_content.insert(0, 'Total number of results: {0}'.format(count))
print('\n'.join(print_content))
    
"""
        response = es.queryES(body,args.results)
print('Search Criteria:')
print(search_factors)

if config.output_format == 1:
    outputs.tool_only(response)
elif config.output_format == 2:
    outputs.tool_and_ctgov(response, args, gender, age)
else:
    print('wrong output format setting in config.py. It must be 1 or 2')
if config.output_details:
    outputs.output_details_in_json(response, search_factors)
"""
