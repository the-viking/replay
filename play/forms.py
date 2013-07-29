from django import forms

class AddForm(forms.Form):
	name = forms.CharField()
	desc = forms.CharField(widget=forms.Textarea)	
	url = forms.FileField(
        label='Select an image',
        help_text='max. 3 megabytes'
    )
