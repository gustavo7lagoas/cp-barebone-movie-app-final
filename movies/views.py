from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
    'Movies',
    api_key=os.environ.get('AIRTABLE_API_KEY'))

def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    context_dictionary = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', context_dictionary)

def create(request):
    print('Super Django')
    return redirect('/')