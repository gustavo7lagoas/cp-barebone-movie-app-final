from django import forms


class MovieForm(forms.Form):
    name = forms.CharField(label="Name")
    url = forms.URLField(label='Image Url')
    rating = forms.IntegerField(label="Rating")
    notes = forms.CharField(label="Notes", widget=forms.Textarea)

    name.widget.attrs.update({'class': 'form-control'})
    url.widget.attrs.update({'class': 'form-control'})
    rating.widget.attrs.update({'class': 'form-control'})
    notes.widget.attrs.update({'class': 'form-control'})