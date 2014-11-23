from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys  import  Keys

import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(5)
        self.assertIn('To-Do',self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',headerText)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                    input_box.get_attribute('placeholder'),
                    'Enter a new To-Do Item'
                )
        self.assertAlmostEqual(
                input_box.location['x'] + input_box.size['width'] / 2,
                512,
                delta=5
                )
        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)

        url1 = self.browser.current_url
        self.assertRegexpMatches(url1,'/lists/.+')
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use Peacock Feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy Peacock Feathers')
        self.check_for_row_in_list_table('2: Use Peacock Feathers to make a fly')

        ## test to check that browser is not servering list from cookies

        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        body_text =  self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feather',body_text)
        self.assertNotIn('Buy Milk',body_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy Milk')
        input_box.send_keys(Keys.ENTER)

        url2 = self.browser.current_url

        self.assertNotEqual(url1,url2)
        self.assertRegexpMatches(url2,'/lists/.+')

        body_text =  self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feather',body_text)
        self.assertIn('Buy Milk',body_text)


