from django.test import TestCase, tag
from movies.forms import MovieForm
from bs4 import BeautifulSoup
import re

class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """ GET / must return 200 """
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        """ Must use movies_stuff.html template """
        self.assertTemplateUsed(self.response, 'movies/movies_stuff.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="submit"')
        self.assertContains(self.response, '<img')


class CreateMovieTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/')
        soup = BeautifulSoup(self.response.content, 'html.parser')
        modal = str(soup.find_all(id='modal-create')[0])
        self.modal = BeautifulSoup(modal, 'html.parser')

    def test_html_modal(self):
        contents = [
            { 'element': 'form', 'count': 1},
            { 'element': 'input', 'count': 4 },
            { 'element': 'textarea', 'count': 1 },
            { 'element': 'button', 'count': 1, 'type': 'submit' },
            { 'element': 'input', 'count': 1,  'type': 'text' },
            { 'element': 'input', 'count': 1, 'type': 'number' },
            { 'element': 'input', 'count': 1, 'type': 'url' },
        ]
        for content in contents:
            with self.subTest():
                if('type' in content):
                    self.assertEqual(len(self.modal(content['element'], type=content['type'])), content['count'])
                else:
                    self.assertEqual(len(self.modal(content['element'])), content['count'])

    def test_csrf_token(self):
        """ HTML must contain csrf token """
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, MovieForm)

    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'url', 'rating', 'notes'], list(form.fields))


class MovieViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_modals_html(self):
        self.assertContains(self.response, 'id="modal-view-')


class MovieEditTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/')
        soup = BeautifulSoup(self.response.content, 'html.parser')
        modal = str(soup.find_all(id=re.compile('modal-edit-'))[0])
        self.modal = BeautifulSoup(modal, 'html.parser')

    def test_modals_html(self):
        contents = [
            { 'element': 'form', 'count': 1},
            { 'element': 'input', 'count': 4 },
            { 'element': 'textarea', 'count': 1 },
            { 'element': 'button', 'count': 1, 'type': 'submit' },
            { 'element': 'input', 'count': 1,  'type': 'text' },
            { 'element': 'input', 'count': 1, 'type': 'number' },
            { 'element': 'input', 'count': 1, 'type': 'url' },
        ]
        for content in contents:
            with self.subTest():
                if('type' in content):
                    self.assertEqual(len(self.modal(content['element'], type=content['type'])), content['count'])
                else:
                    self.assertEqual(len(self.modal(content['element'])), content['count'])

    def test_has_form(self):
        form = self.response.context['search_result'][0]['form']
        self.assertIsInstance(form, MovieForm)


@tag('database')
class MovieEditPostTest(TestCase):

    def test_post(self):
        """ Valid POST should redirect to / """
        data = dict(
            name = "The Pursuit of Happyness",
            url = "https://en.wikipedia.org/wiki/The_Pursuit_of_Happyness#/media/File:Poster-pursuithappyness.jpg",
            rating = 10,
            notes = "Very compelling movie."
        )
        response = self.client.post('/edit/123', data)
        self.assertEqual(302, response.status_code)


class MovieEditPostInvalidTest(TestCase):

    def test_post(self):
        response = self.client.post('/edit/123', {})
        self.assertEqual(200, response.status_code)


@tag('database')
class MoviePostTest(TestCase):

    def setUp(self):
        data = dict(
            name = 'Fast & Furious',
            url = 'http://www.filmposter-archiv.de/filmplakat/2001/fast-and-the-furious-the-3.jpg',
            rating = '6',
            notes = 'It is an OK start',
        )
        self.response = self.client.post('/create/', data)

    def test_post(self):
        """ Valid POST should redirect to / """
        self.assertEqual(302, self.response.status_code)


class MoviePostInvalidTest(TestCase):

    def test_post(self):
        """ Invalid POST should not redirect """
        response = self.client.post('/create/', {})
        self.assertEqual(200, response.status_code)
    