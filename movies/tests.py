from django.test import TestCase
from movies.forms import MovieForm


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

    def test_html_modal(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'id="modal-create')
        self.assertContains(self.response, 'type="submit"', 2)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="url"', 1)
        self.assertContains(self.response, 'type="number"', 1)
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'textarea', 2)

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

    def test_modals_html(self):
        self.assertContains(self.response, 'id="modal-edit-')


# class MoviePostTest(TestCase):

#     def setUp(self):
#         data = dict(
#             name = 'Fast & Furious',
#             url = 'http://www.filmposter-archiv.de/filmplakat/2001/fast-and-the-furious-the-3.jpg',
#             rating = '6',
#             notes = 'It is an OK start',
#         )
#         self.response = self.client.post('/create/', data)

#     def test_post(self):
#         self.assertEqual(302, self.response.status_code)
    