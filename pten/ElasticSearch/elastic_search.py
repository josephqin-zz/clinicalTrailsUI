import json, requests
import urllib.request as ur
import xmltodict

def show_file(nct):

	xml_url = 'https://clinicaltrials.gov/show/' + nct + '?resultsxml=true'
	data = ur.urlopen (xml_url).read ()
	xmldict = xmltodict.parse (data)

	return xmldict

def ES_search(index,setting,size):
	disease = setting['disease']
	gene = setting['gene']
	age = setting['age']
	gender = setting['gender']
	aas = setting['aas']
	stage = setting['stage']
	grade = setting['grade']
	address = setting['address']
	ls=[]
	# added here but should be put in a config file
	use_should = False
	multi_match_type = 'cross_fields'
	multi_match_operator = 'and'
	boost_must_value = 3
	boost_should_value = 0.1

	body = {}
	body["query"] = {}
	body["query"]["bool"] = {}
	body["query"]["bool"]["must"] = []
	body["query"]["bool"]["should"] = []

	body["highlight"] = {}
	body["highlight"]["fields"] = {}
	body["highlight"]["fields"]["Purpose"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["official_title"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["brief_title"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["description"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Inclusion Criteria"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Conditions"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Exclusion Criteria"] = {"number_of_fragments": 0}
	body["highlight"]["pre_tags"] = ["<mark>"]
	body["highlight"]["post_tags"] = ["</mark>"]
	if disease:
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": disease,
					"type": multi_match_type,
					"boost": boost_must_value,
					"operator": multi_match_operator,
					"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
					           "Conditions",
					           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
					           "official_title.whitespace", "brief_title.whitespace",
					           "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": disease,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}

			})
	if gene:
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": gene,
					"boost": boost_must_value,
					"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
					           "Conditions",
					           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
					           "official_title.whitespace", "brief_title.whitespace",
					           "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": gene,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}
			})
	if age:
		body["query"]["bool"]["must"].append ({
			"range": {
				"maximumAge": {"gte": int (age) * 365 * 24 * 60}}})
		body["query"]["bool"]["must"].append ({
			"range": {
				"minimumAge": {"lte": int (age) * 365 * 24 * 60}}})
	body["query"]["bool"]["must"].append ({"bool": {}})
	body["query"]["bool"]["must"][-1]["bool"]["should"] = []

	if gender and gender != "Select":
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": gender
			}})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": "Both"
			}})
	if aas:
		body["query"]["bool"]["must"].append ({
			"multi_match": {
				"query": aas,
				"boost": boost_must_value,
				"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
				           "Conditions",
				           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
				           "official_title.whitespace", "brief_title.whitespace", "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": aas,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}
			})
	if stage != '':
		body["query"]["bool"]["must"].append ({
			"match": {
				"stages": stage.split (' ')[1]}})

	if grade != '':
		body["query"]["bool"]["must"].append ({
			"match": {
				"grades": grade.split (' ')[1]}})

	records = requests.post ('http://127.0.0.1:9200/'+index+'/mappedTrials/_search?size='+str(size), data=json.dumps (body))

	records = records.json ()["hits"]["hits"]

	for i in records:
		rec = {}
		for field in i:
			if field == "_source":
				rec["source"] = i[field]
			elif field == "_id":
				rec["id"] = i[field]
			else:
				rec[field] = i[field]

		ls.append (rec)

	return ls

def es(index,setting,size):
	disease = setting['disease']
	gene = setting['gene']
	age = setting['age']
	gender = setting['gender']
	aas = setting['aas']
	stage = setting['stage']
	grade = setting['grade']
	address = setting['address']
	ls=[]
	# added here but should be put in a config file
	use_should = False
	multi_match_type = 'cross_fields'
	multi_match_operator = 'and'
	boost_must_value = 3
	boost_should_value = 0.1

	body = {}
	body["query"] = {}
	body["query"]["bool"] = {}
	body["query"]["bool"]["must"] = []
	body["query"]["bool"]["should"] = []

	body["highlight"] = {}
	body["highlight"]["fields"] = {}
	body["highlight"]["fields"]["Purpose"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["official_title"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["brief_title"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["description"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Inclusion Criteria"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Conditions"] = {"number_of_fragments": 0}
	body["highlight"]["fields"]["Exclusion Criteria"] = {"number_of_fragments": 0}
	body["highlight"]["pre_tags"] = ["<mark>"]
	body["highlight"]["post_tags"] = ["</mark>"]
	if disease:
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": disease,
					"type": multi_match_type,
					"boost": boost_must_value,
					"operator": multi_match_operator,
					"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
					           "Conditions",
					           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
					           "official_title.whitespace", "brief_title.whitespace",
					           "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": disease,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}

			})
	if gene:
		body["query"]["bool"]["must"].append ({
			"multi_match":
				{
					"query": gene,
					"boost": boost_must_value,
					"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
					           "Conditions",
					           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
					           "official_title.whitespace", "brief_title.whitespace",
					           "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": gene,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}
			})
	if age:
		body["query"]["bool"]["must"].append ({
			"range": {
				"maximumAge": {"gte": int (age) * 365 * 24 * 60}}})
		body["query"]["bool"]["must"].append ({
			"range": {
				"minimumAge": {"lte": int (age) * 365 * 24 * 60}}})
	body["query"]["bool"]["must"].append ({"bool": {}})
	body["query"]["bool"]["must"][-1]["bool"]["should"] = []

	if gender and gender != "Select":
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": gender
			}})
		body["query"]["bool"]["must"][-1]["bool"]["should"].append ({
			"match": {
				"gender": "Both"
			}})
	if aas:
		body["query"]["bool"]["must"].append ({
			"multi_match": {
				"query": aas,
				"boost": boost_must_value,
				"fields": ["Purpose", "description", "Inclusion Criteria", "official_title", "brief_title",
				           "Conditions",
				           "Purpose.whitespace", "description.whitespace", "Inclusion Criteria.whitespace",
				           "official_title.whitespace", "brief_title.whitespace", "Conditions.whitespace"]}})
		if use_should:
			body["query"]["bool"]["should"].append ({
				"multi_match": {
					"query": aas,
					"boost": boost_should_value,
					"fields": ["Exclusion Criteria", "Exclusion Criteria.whitespace",
					           "Exclusion Criteria.normal"]
				}
			})
	if stage != '':
		body["query"]["bool"]["must"].append ({
			"match": {
				"stages": stage.split (' ')[1]}})

	if grade != '':
		body["query"]["bool"]["must"].append ({
			"match": {
				"grades": grade.split (' ')[1]}})

	records = requests.post ('http://127.0.0.1:9200/'+index+'/mappedTrials/_search?size='+str(size), data=json.dumps (body))

	records = records.json ()["hits"]["hits"]

	for i in records:
		rec = {}
		for field in i:
			if field == "_source":
				rec["source"] = i[field]
			elif field == "_id":
				rec["id"] = i[field]
			else:
				rec[field] = i[field]

		ls.append (rec)

	return ls