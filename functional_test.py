from selenium import webdriver
from selenium.webdriver.common.keys  import  Keys

import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_taag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('localhost:8000')
        self.assertIn('To-Do',self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',headerText)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                    input_box.get_attribute('placeholder'),
                    'Enter a new To-Do Item'
                )
        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use Peacock Feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy Peacock Feathers')
        self.check_for_row_in_list_table('2: Use Peacock Feather to make a fly')

        self.fail('Finish the test')


if __name__== '__main__':
    unittest.main() 
