from django import forms
from validation.models import Query



def createChoice(lists):
	foo = ()
	for str in lists:
		foo = foo + ((str, str),)
	return foo + (('', 'SELECT'),)

class QueryForm (forms.ModelForm):
	class Meta:
		model = Query
		fields = ['disease', 'gene', 'age', 'aas', 'gender', 'stage', 'grade', 'address', 'include_keywords', 'exclude_keywords']
		widgets = {
			'disease': forms.TextInput(attrs={'placeholder': 'Enter the patients disease'}),
			'gene': forms.TextInput (attrs={'placeholder': 'Enter the gene mutation'}),
		}



from validation.models import Index as ES_Index
class OptionsForm(forms.Form):
	ElasticSearch = forms.ModelChoiceField(queryset=ES_Index.objects.all())
	Ontology = forms.BooleanField(initial=False,required=False)
	aas_on = forms.BooleanField(initial=False,required=False)

	def __init__(self, *args, **kwargs):
		super (OptionsForm, self).__init__ (*args, **kwargs)
		self.fields['ElasticSearch'].label = 'Elastic Search Version'
		self.fields['Ontology'].label = 'Enable Disease Ontology'
		self.fields['aas_on'].label = 'Results without AAS'

