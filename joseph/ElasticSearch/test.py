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

from esoperations_disease_test import ESOperations
import config as config
import weights_config as ws

import tree_build_out_test as tb

def update_print(print_content, response, hit_ids):

	count = 0
	if not hit_ids:
		for hit in response['hits']['hits']:
			cnt = {}
			hit_ids.append (hit['_id'])
			cnt['id'] = hit['_id']
			cnt['score'] = hit['_score']

			print_content.append (cnt)
			print (hit_ids)
			print("test"+cnt['id'])
	else:
		for hit in response['hits']['hits']:
			print('repeat')

			if hit['_id'] not in hit_ids:
				hit_ids.append (hit['_id'])
				cnt = {}
				count += 1
				cnt['id'] = hit['_id']
				cnt['score'] = hit['_score']

				print_content.append (cnt)

				print("tt"+cnt['id'])
			else:
				print('not in ')
				print(hit['_id'])
	return count
def es_DiseaseOntology():
	es = ESOperations ('test_disease')

	p_disease='Rhabdoid tumor'
	p_gene='INI1'
	p_aas = None
	p_end = None
	p_start = None
	p_slop = None
	p_age = None
	p_results = 50
	p_gender = None
	p_stage = None
	p_grade = None



	body = {}
	body["query"] = {}
	body["query"]["bool"] = {}
	body["query"]["bool"]["filter"] = []
	body["query"]["bool"]["must"] = []
	body["query"]["bool"]["should"] = []
	# body["query"]["range"]["update_date"] = {}


	search_factors = []

	if p_aas is not None:
		p_aas = p_aas.replace ("/", "//")
	"""
	disease_multi_query_fields = ["Purpose.disease^"+w_purpose,"description.disease^"+w_des,"Inclusion Criteria.disease^"+w_ic,
	                      "official_title.disease^"+w_ot,"brief_title.disease^"+w_bt,"Conditions.disease^"+w_con,
	                      "Purpose.disease_whitespace^"+w_purpose,"description.disease_whitespace^"+w_des,
	                      "Inclusion Criteria.disease_whitespace^"+w_ic,"official_title.disease_whitespace^"+w_ot,
	                      "brief_title.disease_whitespace^"+w_bt,"Conditions.disease_whitespace^"+w_con]
	"""
	disease_multi_query_fields = ["Purpose.disease^" + ws.w_purpose, "description.disease^" + ws.w_des,
	                              "Inclusion Criteria.disease^" + ws.w_ic,
	                              "official_title.disease^" + ws.w_ot, "brief_title.disease^" + ws.w_bt,
	                              "Conditions.disease^" + ws.w_con,
	                              "Purpose.disease_whitespace^" + ws.w_purpose, "description.disease_whitespace^" + ws.w_des]
	# """
	if p_slop is None:
		slop = config.slop
	else:
		slop = p_slop

	if p_disease is not None:
		search_factors.append ("--disease")
		search_factors.append (p_disease)
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": p_disease,
					"type": "phrase",
					"boost": ws.boost_must_value,
					"fields": disease_multi_query_fields,
					"slop": slop}})

		if ws.use_should:

			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": p_disease,
					"boost": ws.boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
				}

			})

	if p_gene is not None:
		search_factors.append ('--gene')
		search_factors.append (p_gene)
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": p_gene,
					"boost": ws.boost_must_value,
					"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
					           "Conditions",
					           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
					           "official_title.whitespace", "brief_title.whitespace", "Conditions.whitespace"]}})

		body["query"]["bool"]["should"].append ({
			"multi_match": {
				"query": p_gene,
				"boost": 0.1,
				"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
			}

		})

	age = ""
	if p_age is not None:
		search_factors.append ('--age')
		search_factors.append (str (p_age))
		body["query"]["bool"]["must"].append ({
			"range": {
				"maximumAge": {"gte": p_age * 365 * 24 * 60}}})
		body["query"]["bool"]["must"].append ({
			"range": {
				"minimumAge": {"lte": p_age * 365 * 24 * 60}}})
		if p_age < 18:
			age = "&age=0"
		elif p_age >= 18 and p_age < 66:
			age = "&age=1"
		else:
			age = "&age=2"

	body["query"]["bool"]["must"].append ({"bool": {}})
	body["query"]["bool"]["must"][-1]["bool"]["should"] = []
	gender = ""
	if p_gender is None:
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({"match": {
			"gender": "Male"
		}})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": "Female"
			}})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": "Both"
			}})
	else:
		search_factors.append ('--gender')
		search_factors.append (p_gender)
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": p_gender
			}})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": "Both"
			}})
		gender = "&gndr=" + p_gender

	if p_results is not None:
		search_factors.append ('--results')
		search_factors.append (str (p_results))

	if p_aas is not None:
		search_factors.append ('--aas')
		search_factors.append (p_aas)
		body["query"]["bool"]["must"].append ({
			"multi_match": {
				"query": p_aas,
				"boost": ws.boost_must_value,
				"fields": disease_multi_query_fields}})

		if ws.use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": p_aas,
					"boost": ws.boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace", "Exclusion Criteria.normal"]
				}

			})

	if p_stage is not None:
		search_factors.append ('--stage')
		search_factors.append (p_stage)
		body["query"]["bool"]["must"].append ({
			"match": {
				"stages": p_stage}})

	if p_grade is not None:
		search_factors.append ('--grade')
		search_factors.append (p_grade)
		body["query"]["bool"]["must"].append ({
			"match": {
				"grades": p_grade}})

	if p_start is not None:
		search_factors.append ('--start')
		search_factors.append (p_start)
		body["query"]["bool"]["filter"].append ({
			"range": {
				"update_date": {
					'gte': p_start
				}
			}
		})
		if p_end is not None:
			search_factors.append ('--end')
			search_factors.append (p_end)
			body["query"]["bool"]["filter"][-1]["range"]["update_date"]['lte'] = p_end
	else:
		if p_end is not None:
			search_factors.append ('--end')
			search_factors.append (p_end)
			body["query"]["bool"]["filter"].append ({
				"range": {
					"update_date": {
						'lte': p_end
					}
				}
			})





	# Query the ES index with the search body that we have created
	diseases = [p_disease]

	count = 0  # total number of results
	level = 1  # disease itself
	hit_ids = []
	print_content = []
	rs = {}
	rs['levels'] = []
	parents = tb.main (p_disease.lower ())  # get parent diseases of given disease
	length = len (parents)
	while diseases:
		l = {}
		level_count = 0
		parent_diseases = []
		if length > 1:
			if level == 1:
				pd = list (parents[1].keys ())[0]
				parent_diseases.append (pd)
			elif level == 2:
				if length > 2:
					for i in range (2, length):
						pd = list (parents[i].keys ())[0]
						if pd == 'cancer':
							break
						parent_diseases.append (pd)
		l['level'] = level
		l['diseases'] = ','.join (diseases)

		ctlist = []
		for disease in diseases:
			body["query"]["bool"]["must"][0]['multi_match']['query'] = disease
			body["query"]["bool"]["must"][0]['multi_match']['boost'] = ws.boost_must_value
			# print(body["query"]["bool"]["must"][0])

			response = es.queryES (body, p_results)
			if level == 1:
				count += response['hits']['total']
				level_count += response['hits']['total']
				update_print (ctlist, response, hit_ids)

			else:
				new_count = update_print (ctlist, response, hit_ids)

				count += new_count
				level_count += new_count
			# parent_diseases.extend(get_parents(disease))
		l['nct'] = ctlist

		l['count'] = level_count
		rs['levels'].append (l)
		diseases = parent_diseases
		boost_must_value = ws.boost_must_value / 5.0
		level += 1

	rs['total_number'] = count
	return rs

print(es_DiseaseOntology())