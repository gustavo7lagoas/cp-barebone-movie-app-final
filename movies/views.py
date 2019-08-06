from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os
from movies.forms import MovieForm

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
    'Movies',
    api_key=os.environ.get('AIRTABLE_API_KEY'))

def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    context = {'search_result': search_result}
    context['form'] = MovieForm()
    return render(request, 'movies/movies_stuff.html', context)

def create(request):
    if(request.method == 'POST'):
        form = MovieForm(request.POST)
        form.full_clean()
        data = {
            'Name': form.cleaned_data['name'],
            'Pictures': [{'url': form.cleaned_data['url']}],
            'Rating': form.cleaned_data['rating'],
            'Notes': form.cleaned_data['notes']
        }
        AT.insert(data)
    return redirect('/')
    