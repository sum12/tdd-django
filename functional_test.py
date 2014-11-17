from selenium import webdriver
from selenium.webdriver.common.keys  import  Keys

import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('localhost:8888')
        self.assertIn('To-Do',self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(headerText,'To-Do')

        input_box = self.browser.find_element_id('id_new_item')
        self.assertEqual(
                    input_box.get_attribute('placeholder'),
                    'Enter a new To-Do Item'
                )
        input_box.sendkeys('Buy Peacock Feathers')
        input_box.sendkeys(Keys.Enter)

        table = self.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
                    any(row == '1: Buy Peacock Feathers' for row in rows)
                )
        self.fail('Finish the test')


if __name__== '__main__':
    unittest.main() 
