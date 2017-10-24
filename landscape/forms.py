from django import forms






class LandscapeForm( forms.Form):
	reg = forms.CharField( widget = forms.Textarea )

