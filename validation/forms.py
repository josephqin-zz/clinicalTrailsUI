from django import forms
from validation.models import *

class QueryForm (forms.ModelForm):
	class Meta:
		model = Query
		fields = ['disease', 'age', 'gender', 'gene', 'aas', 'stage', 'grade', 'address']
		labels = {
			'disease': 'Disease Name',
			'aas':'Amino Acid Substitution',
		}

class ScenarioForm (forms.ModelForm):
	class Meta:
		model = Scenario
		fields = ['index', 'ontology', 'withoutAAS']

from validation.models import Query
class QuerySelectionForm (forms.Form):
	query = forms.ModelChoiceField(queryset=Query.objects.all(),required=False)


class questionForm (forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['eligibility', 'section', 'sentence', 'author', 'timer']
		labels = {
			'eligibility': 'Is the patient eligible for this trial',
			'section': 'What section(s) of the clinical trial document allowed you to render this decision',
			'sentence': 'What sentence(s) of these section(s) allowed you to render this decision',
			'author': 'Signature',
			'timer': ''
		}
		widgets = {'timer': forms.TextInput (attrs={'class': 'hideme'})}