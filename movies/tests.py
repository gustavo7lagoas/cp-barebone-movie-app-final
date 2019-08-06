from django.test import TestCase


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

    def test_html_modal(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'modal')
        self.assertContains(self.response, 'type="submit"', 2)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="number"', 1)
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'textarea', 2)
        
    def test_csrf_token(self):
        """ HTML must contain csrf token """
        self.assertContains(self.response, 'csrfmiddlewaretoken')