from django.shortcuts import *

# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse
from django.template import Context, loader, RequestContext
from joseph.models import words
from joseph.forms import thresholdForm, EvaluationForm
from joseph.models import potential_gene, cases, gene_in_CT,cases_validate

import json, requests
from django.contrib.auth.decorators import login_required
from joseph.beacon import beacon_import_data

def str2bool(v):
	return v.lower () in ("yes", "true", "t", "1")


def msp_demo(request):
	if request.method == 'POST':
		form = thresholdForm (request.POST)
		max = float (request.POST['max'])
		min = float (request.POST['min'])
		obj = potential_gene.objects.filter (score__gte=min, score__lte=max)
	else:
		obj = {}
		form = thresholdForm ()
	return render (request, 'msq_demo.html', {'obj': obj, 'form': form})


def msp_cases(request, wordID='1', geneID='1'):
	word = words.objects.get (id=wordID)
	obj = cases.objects.filter (word=word)
	obj2 = cases_validate.objects.all().select_related()
	gene = gene_in_CT.objects.get (id=geneID)

	return render (request, 'msq_cases.html', {'obj': obj, 'word': word, 'gene': gene})


def msp_file(request, wordID='1', geneID='1', caseID='1'):
	word = words.objects.get (id=wordID)
	case = cases.objects.get (id=caseID)
	gene = gene_in_CT.objects.get (id=geneID)
	value = str (case.file_num)[:-4]


	path = 'http://127.0.0.1:9200/test13/mappedTrials/' + value
	record = requests.get (path)
	record = record.json ()
	rec = {}
	rec["source"] = {}
	rec["source"]["IC"] = {}
	rec["source"]["EC"] = {}
	msg = ""
	for field in record:
		if field == "_source":
			rec["source"] = record[field]
			if "maximumAge" in record[field]:
				rec["source"]["maximumAge"] = int (record[field]["maximumAge"]) / 525600
			if "minimumAge" in record[field]:
				rec["source"]["minimumAge"] = int (record[field]["minimumAge"]) / 525600
			if "Inclusion Criteria" in record[field]:
				rec["source"]["IC"] = record[field]["Inclusion Criteria"]
			if "Exclusion Criteria" in record[field]:
				rec["source"]["EC"] = record[field]["Exclusion Criteria"]
		elif field == "_id":
			rec["id"] = record[field]
		else:
			rec[field] = record[field]
	if request.method == 'POST':
		form = ""
		aws = cases_validate(case=case,is_Misspelled=str2bool(request.POST['is_Misspelled']),gene="")
		aws.save()
		msg = "Thanks for evaluation"
	else:
		try:
			ev_result = cases_validate.objects.get (case=case)
			form = ""
			if ev_result.is_Misspelled:
				msg = "This case has been evaluated as Positive Case"
			else:
				msg = "This case has been evaluated as Negative Case"
		except :
			form = EvaluationForm ()
	return render (request, 'msq_file.html', {'rec': rec, 'word': word, 'gene': gene,'form':form,'msg':msg})

import random
def random_sum(n,total):
	dividers = sorted (random.sample (range (1, total), n - 1))
	return [a - b for a, b in zip (dividers + [total], [0] + dividers)]

def words_landscape(request):
	list = random_sum(2000,186794)
	return render(request,'word_landscape.html',{'random':list})

