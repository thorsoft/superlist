import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

   # def test_can_start_a_list_and_retrieve_it_later(self):
    def test_can_start_a_list_for_one_user(self):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its home page
        self.browser.get(self.live_server_url)

    # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


    # She is invited to enter a new to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

    # She types "Buy peacock feathers" into a text box (Ediths hobby)
    # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates and now the page lists
    # "1: Buy peacock feathers" as an item on a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

#        self.fail('Finish the test')
    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect

    # She visits that URL - her to-do list is still there

    # Satisfied she goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #She notices that her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # A new user Francis comes along to the site

        ## We use a new browser session to make sure that no information
        ## of Ediths is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage. No sign of Ediths list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis starts a new list by entering a new item. He is less interesting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Ediths list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('1: Buy milk', page_text)

        #Satisfied they both go to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')