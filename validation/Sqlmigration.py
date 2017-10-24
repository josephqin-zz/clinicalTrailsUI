import joseph.models as old
import validation.models as new
from django.forms.models import model_to_dict
from validation.views import getScenarioID,getQueryID,addNewQuery

def addIndex(index):
	try:
		i = new.Index.objects.get(index_name=index['index_name'])
	except:
		i = new.Index(**index)
		i.save()
	return i

def QueryMigration_dier(query):
	new_q = model_to_dict(query,[],['resultNUM','es_index','id'])
	new_i = addIndex(model_to_dict(query.es_index,['index_name','update_date']))
	new_s = {'index':new_i,'ontology':query.es_index.disease_hier,'withoutAAS':False}
	q,s,total = addNewQuery(new_q,new_s)
	old_awss = old.Answer.objects.filter(query=query)
	for a in old_awss:
		sections  = new.Section.objects.filter(id__in=[s.id for s in a.section.all()])
		a_dict = model_to_dict(a,[],['queryID','query','clinicalTrial','section','id'])
		new_a = new.Answer(**a_dict)
		new_a.trial = new.Trial.objects.get(query=q,scenario=s,nct=a.clinicalTrial)
		new_a.save()
		new_a.section.set (sections)
	return q,s,total

def QueryMigration(query):
	new_q = model_to_dict(query,[],['resultNUM','es_index','id'])
	new_i = addIndex(model_to_dict(query.es_index,['index_name','update_date']))
	new_s = {'index':new_i,'ontology':query.es_index.disease_hier,'withoutAAS':False}
	q = getQueryID(new_q)
	s = getScenarioID(new_s)
	total = query.resultNUM
	old_awss = old.Answer.objects.filter(query=query)
	for a in old_awss:
		sections  = new.Section.objects.filter(id__in=[s.id for s in a.section.all()])
		a_dict = model_to_dict(a,[],['queryID','query','clinicalTrial','section','id'])
		new_a = new.Answer(**a_dict)
		trial = new.Trial(query=q,scenario=s,nct=a.clinicalTrial,disease=q.disease,gene=q.gene,aas=q.aas)
		trial.save()
		new_a.trial = trial
		new_a.save()
		new_a.section.set (sections)
	return q,s,total