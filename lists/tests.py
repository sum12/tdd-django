from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item,List

class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_url_returns_correct_html(self):
        req = HttpRequest()
        req.method = 'POST'
        req.POST['item_text'] = 'A new list Item'
        res = home_page(req)
        expected_string = render_to_string(
                                    'home.html',
                                    {
                                        'new_item_text' : 'A new list Item'
                                    })

    def test_home_page_only_saves_item_when_necessary(self):
        req = HttpRequest()
        res = home_page(req)
        self.assertEqual(Item.objects.count(),0)



class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The First (Ever) List Item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "The Second Item"
        second_item.list = list_
        second_item.save()

        saved_objects = Item.objects.all()
        self.assertEqual(saved_objects.count(),2)
        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        first_saved_item = saved_objects[0]
        second_saved_item = saved_objects[1]

        self.assertEqual(first_saved_item.text,'The First (Ever) List Item')
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(second_saved_item.list,list_)
        self.assertEqual(second_saved_item.text,'The Second Item')

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        res = self.client.get(
                    '/lists/%d/'%(list_.id),
                )
        self.assertTemplateUsed(res,'list.html')

    def test_displays_only_items_for_that_list(self):
        list1_ = List.objects.create()
        i1 = Item.objects.create(text='this is 1.1', list = list1_)
        i2 = Item.objects.create(text='this is 1.2', list = list1_)

        
        list2_ = List.objects.create()
        i2 = Item.objects.create(text='this is 2.1', list = list2_)
        i2 = Item.objects.create(text='this is 2.2', list = list2_)


        res = self.client.get('/lists/%d/'%(list1_.id))

        self.assertContains(res, 'this is 1.1')
        self.assertContains(res, 'this is 1.2')
        self.assertNotContains(res, 'this is 2.1')
        self.assertNotContains(res, 'this is 2`.1')


    def test_displays_all_items(self):
        list_ = List.objects.create()
        i1 = Item.objects.create(text='item says 1', list=list_)
        i2 = Item.objects.create(text='item says 2', list=list_)

        res = self.client.get('/lists/%d/'%list_.id)

        self.assertContains(res,'item says 1')
        self.assertContains(res, 'item says 2')



class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
                '/lists/new',
                data = {'item_text' : 'A new list Item'}
                )
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list Item')
    
    def test_redirects_after_POST(self):
        res = self.client.post(
                '/lists/new',
                data = {'item_text' : 'A new list Item'}
                )
        list_ = List.objects.first()
        self.assertRedirects(res,'/lists/%d/'%list_.id)



class NewItemTest(TestCase):

    def test_can_save_an_item_to_an_existing_list(self):
        list2 = List.objects.create()
        list1 = List.objects.create()

        res = self.client.post(
                '/lists/%d/add_item'%(list1.id),
                data={'item_text' : "A new item for an existing list"}
                )

        self.assertEqual(Item.objects.count(),1)
        i1 = Item.objects.first()
        self.assertEqual(i1.list,list1)
        self.assertEqual(i1.text,"A new item for an existing list")

    def test_redirects_to_list_view(self):
        list2 = List.objects.create()
        list1 = List.objects.create()

        res = self.client.post(
                '/lists/%d/add_item'%(list1.id),
                data = {"item_text" : "A new item for an existing list"}
                )

        self.assertRedirects(res, '/lists/%d/'%(list1.id))
    
    def test_passes_correct_list_to_template(self):
        l1 = List.objects.create()
        l2 = List.objects.create()

        res = self.client.get(
                '/lists/%d/'%l1.id
                )
        
        self.assertEqual(res.context['list'],l1)

