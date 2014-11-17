from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_url_returns_correct_html(self):
        req = HttpRequest()
        res = home_page(req)
        self.assertTrue(res.content.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>',res.content)
        self.assertTrue(res.content.endswith('</html>'))




