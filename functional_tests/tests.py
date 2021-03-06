from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import unittest
from django.test import LiveServerTestCase
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        self.browser.get('http://localhost:8081/lists/the-only-list-in-the-world')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
#        self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        self.assertIn('Start A New list',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start A New list', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
       ## self.assertRegex(edith_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        ##Enter之后需要重新找元素
        inputbox = self.browser.find_element_by_id('id_new_item')
 
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        ##我们使用一个新浏览器会话,确保伊迪斯的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('Finish the test!')
#if __name__ == '__main__':
#    unittest.main()
