from django.shortcuts import *
from django.http import JsonResponse
from validation.models import *
from validation.forms import *
from pten.views import get_args
# Create your views here.
from pten.ElasticSearch import dis_hier,dis_hier_aas,normal
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import json
def resTrimer(res,query):
	rs = []
	for r in res:
		if 'hits' in r:
			if r['hits']:
				for h in r['hits']:
					ct = {}
					ct['id'] = h['id']
					ct['disease'] = r['diseases']
					ct['level'] = r['level']
					if 'aas' in h:
						ct['aas'] = h['aas']
					else:
						ct['aas'] = query.aas
					rs.append (ct)

		else:
			ct = {}
			ct['id'] = r['id']
			ct['disease']=query.disease
			ct['aas']=query.aas
			ct['level'] = None
			rs.append(ct)
	return rs

def ElasticSearch(query,option):
	index_file = option['index']
	if option['ontology'] :
		res,count = dis_hier(query,index_file.index_name)

	elif option['withoutAAS'] :
		res,count = dis_hier_aas (query, index_file.index_name)

	else:
		res,count = normal(query,index_file.index_name)

	return resTrimer(res,query), count


from django.core.exceptions import ObjectDoesNotExist
def getQueryID(queryDetial):
	query={}
	for k,v in queryDetial.items():
		if v:
			if k in ['disease','gene','aas']:
				query[k]=v.lower()
			else:
				query[k]=v

	try:
		q  = Query.objects.get(**query)
	except ObjectDoesNotExist:
		q = Query(**query)
		q.save()
	return q

def getScenarioID(scenario):
	try:
		q  = Scenario.objects.get(**scenario)
	except ObjectDoesNotExist:
		q = Scenario(**scenario)
		q.save()
	return q

def addNewQuery(queryDetial,ScenarioDetial):

	q = getQueryID (queryDetial)
	query_args = get_args (queryDetial)
	s = getScenarioID (ScenarioDetial)

	clist, total = ElasticSearch (query_args,ScenarioDetial)
	for rs in clist:
		trial = {}
		trial['query'] = q
		trial['scenario'] = s
		trial['nct'] = rs['id']
		trial['disease'] = json.dumps (rs['disease'])
		trial['aas'] = rs['aas']
		trial['gene'] = query_args.gene
		try:
			t = Trial.objects.get (**trial)
		except ObjectDoesNotExist:
			t = Trial (**trial)
			t.save ()
	return q,s,total

def QueryDetials(query,scenario):
	try:
		trials = Trial.objects.filter(scenario=scenario,query=query)
	except:
		trials = []
	return trials

def ScenarioDetials(scenario):
	queryIDs=Trial.objects.filter(scenario=scenario).values("query").distinct()
	querys = []
	for q in queryIDs:
		qs={}
		query = Query.objects.get(id=q['query'])
		trials = queryTrialDetial(query,scenario)
		qs={"query":query,"trials":trials}
		querys.append(qs)
	return querys



from django.forms import model_to_dict
def queryLists(requests,queryID):
	try:
		query = model_to_dict(Query.objects.get(id=queryID))
	except:
		query = {}
	return JsonResponse(query)

def trialDetials(trials):
	finished = Answer.objects.filter (trial__in=trials)
	eligible = finished.filter (eligibility=True)
	noneligible = finished.filter (eligibility=False)
	unfinished = set(trials)-set(a.trial for a in finished)
	return {'total':trials,'finished':finished,'eligible':eligible,'noneligible':noneligible,'unfinished':unfinished}


def scenarioTrialDetial(scenario):
	total = Trial.objects.filter(scenario=scenario)
	return trialDetials(total)

def queryTrialDetial(query,scenario):
	total = Trial.objects.filter (scenario=scenario,query=query)
	return trialDetials(total)

def summaries(request):
	scenarios = Scenario.objects.all ()
	rs = {s:scenarioTrialDetial(s) for s in scenarios}

	return render (request,'summary.html',{'rs':rs})

def querySummaries(request,scenarioID):
	scenario = Scenario.objects.get(id=scenarioID)
	querys = [Query.objects.get(id=q['query']) for q in Trial.objects.filter(scenario=scenario).values('query').distinct()]

	rs = {q:queryTrialDetial(q,scenario) for q in querys}
	return render (request, 'query_summary.html', {'rs': rs})

from elasticsearch import Elasticsearch

def TrialContent(trial):
	es = Elasticsearch()
	try:
		rec = es.get(index=trial.scenario.index.index_name, doc_type="mappedTrials",id=trial.nct)
		rec = dict ((k.replace ('_', ''), v) for k, v in rec.items ())
	except :
		rec = {}

	return rec
from joseph.views import str2bool
def TrialValidation(request,trialID):
	trial = Trial.objects.get(id=trialID)
	rec = TrialContent(trial)
	form = questionForm()
	try:
		aws = Answer.objects.get(trial=trial)
	except ObjectDoesNotExist:
		aws = {}

	if request.method == 'POST':
		sections = request.POST.getlist ('section')
		print (request.POST['eligibility'])
		aws = Answer (trial=trial,eligibility=str2bool (request.POST['eligibility']),
		              sentence=request.POST['sentence'], author=request.POST['author'], timer=request.POST['timer'])

		aws.save ()
		for sec in sections:
			aws.section.add (sec)

		return HttpResponseRedirect(reverse('query_validation',kwargs={'scenarioID':trial.scenario.id}))
	else:
		return render (request,'trialvalidation.html',{'rec':rec,'form':form,'aws':aws})

def admin(request):


	if request.method == 'POST':
		queryform = QueryForm (request.POST)
		scenarioform = ScenarioForm (request.POST)
		selectionform = QuerySelectionForm ()
		if queryform.is_valid() and scenarioform.is_valid():
			q,s,total = addNewQuery(queryform.cleaned_data,scenarioform.cleaned_data)
			selectionform.fields['query'].initial = q

	else:
		queryform = QueryForm ()
		scenarioform = ScenarioForm ()
		selectionform = QuerySelectionForm()


	scenarios = Scenario.objects.all ()
	scenario_dict = {s: ScenarioDetials(s) for s in scenarios}

	return render (request,'admin.html',{'queryform':queryform,'scenarioform':scenarioform,'selectionform':selectionform,'scenario':scenario_dict})

