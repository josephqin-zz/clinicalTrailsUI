from django import forms
from joseph.models import cases_validate
from django.forms.models import modelformset_factory


def createChoice(lists):
	foo = ()
	for str in lists:
		foo = foo + ((str, str),)
	return foo + (('', 'SELECT'),)

class thresholdForm (forms.Form):
	max = forms.FloatField (label='MAX',min_value=0.0, max_value=1.0)
	min = forms.FloatField (label='MIN',min_value=0.0, max_value=1.0)



class EvaluationForm(forms.ModelForm):
	class Meta:
		model = cases_validate
		fields = ['is_Misspelled',]

