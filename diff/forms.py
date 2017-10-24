from django import forms



class diffForm(forms.Form):
	before = forms.FileField (label='Before')
	after = forms.FileField (label='After')


class diffForm_txt(forms.Form):
	before = forms.CharField( widget = forms.Textarea )
	after = forms.CharField( widget = forms.Textarea )
from diff.models import Diff_case
class diffCaseForm(forms.Form):
	case = forms.ModelChoiceField(queryset=Diff_case.objects.all(),required=False)