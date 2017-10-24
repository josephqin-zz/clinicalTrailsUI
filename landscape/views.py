from django.shortcuts import render

# Create your views here.
from django.shortcuts import *
from landscape.forms import LandscapeForm
from landscape.landscape_v2 import wordcount
import json
import string
punctuation = list(string.punctuation)
punctuation.append(' ')

def trim_rs(var):
	var = dict((key.split('.')[0],value) for key,value in var.items() )

	rs={}
	if 'official_title' in var.keys() :
		ot = var['official_title']
	else:
		ot = 0
	if 'brief_title'in var.keys() :
		bt = var['brief_title']
	else:
		bt = 0
	rs['Title'] = ot+bt
	if 'Exclusion Criteria' in var.keys() :
		rs['Exclusion'] = var['Exclusion Criteria']
	else:
		rs['Exclusion'] = 0
	if 'Inclusion Criteria' in var.keys():
		rs['Inclusion'] = var['Inclusion Criteria']
	else:
		rs['Inclusion'] = 0
	if 'Purpose' in var.keys():
		rs['Purpose'] = var['Purpose']
	else:
		rs['Purpose'] = 0
	if 'description' in var.keys():
		rs['description'] = var['description']
	else:
		rs['description'] = 0
	return rs

def ls(request):

	if request.method == 'POST':
		form = LandscapeForm(request.POST)
		rs=[]

		for term in request.POST['reg'].split('\r\n'):

			if term:
				if term.endswith('#'):
					case_sensitive=True
					term = term[:-1]
				else:
					case_sensitive=False


				if any ((p in term) for p in punctuation):
					res = wordcount.ls_phrase(term)
				else:
					res = wordcount.LandScape(term, case_sensitive)
				if res:
					t = trim_rs(res['total_word_count_each_field'])
					t['label'] = term
					t['doc'] = res['doc_count']
					t['total'] = res['total_word_count']
					t['word_count_each_doc'] = res['word_count_each_doc']
					t['case_sensitive'] = case_sensitive
					rs.append(t)
				else :
					t={}
					t['label'] = term
					t['total'] = 0
					rs.append (t)
	else:
		form = LandscapeForm()
		rs=[]

	return render (request, 'landscape.html', {'form': form,'rs':rs,'data':json.dumps(rs)})