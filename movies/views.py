from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
    for movie in search_result:
        movie['form'] = MovieForm(initial={
            'name': movie['fields']['Name'],
            'url': movie['fields']['Pictures'][0]['url'],
            'rating': movie['fields']['Rating'],
            'notes': movie['fields']['Notes']}
        )
    return render(request, 'movies/movies_stuff.html', context)


def create(request):
    if(request.method == 'POST'):
        form = MovieForm(request.POST)
        if form.is_valid():
            data = {
                'Name': form.cleaned_data['name'],
                'Pictures': [{'url': form.cleaned_data['url']}],
                'Rating': form.cleaned_data['rating'],
                'Notes': form.cleaned_data['notes']
            }
            AT.insert(data)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse()



def edit(request, movie_id):
    print('haha')
    if(request.method == 'POST'):
        form = MovieForm(request.POST)
        if(form.is_valid()):
            data = {
                'Name': form.cleaned_data['name'],
                'Pictures': [{'url': form.cleaned_data['url']}],
                'Rating': form.cleaned_data['rating'],
                'Notes': form.cleaned_data['notes']
            }
            AT.update(movie_id, data)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse()