from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

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
        
        


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The First (Ever) List Item"
        first_item.save()

        second_item = Item()
        second_item = "The Second Item"
        second_item.save()

        saved_objects = Items.objects.all()
        self.assertEqual(saved_object.count,2)

        first_saved_item = saved_objects[0]
        second_saved_item = saved_objects[1]

        self.assertEqual(first_saved_item,'The First (Ever) List Item')
        self.assertEqual(second_saved_item,'The Second Item')
