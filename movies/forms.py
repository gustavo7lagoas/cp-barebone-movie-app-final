from django import forms


class MovieForm(forms.Form):
    name = forms.CharField(label="Name", initial='')
    url = forms.URLField(label='Image Url', initial='')
    rating = forms.IntegerField(label="Rating", initial='')
    notes = forms.CharField(label="Notes", widget=forms.Textarea, initial='')

    name.widget.attrs.update({'class': 'form-control'})
    url.widget.attrs.update({'class': 'form-control'})
    rating.widget.attrs.update({'class': 'form-control'})
    notes.widget.attrs.update({'class': 'form-control'})