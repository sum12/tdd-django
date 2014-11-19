from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_url_returns_correct_html(self):
        req = HttpRequest()
        req.method = 'POST'
        req.POST['item_text'] = 'A new list Item'
        res = home_page(req)
        self.assertIn('A new list Item',res.content.decode())
        expected_string = render_to_string(
                                    'home.html',
                                    {
                                        'new_item_text' : 'A new list Item'
                                    })
        self.assertEqual(res.content.decode(), expected_string)
        
        


