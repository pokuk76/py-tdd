import os
import time

import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options	# For Google Chrome ¬_¬
from selenium.common.exceptions import WebDriverException

OPTIONS = Options()
OPTIONS.add_argument(r"user-data-dir=C:\Users\poku.flacko\AppData\Local\Google\Chrome\User Data\Default")
CHROMEDRIVER_EXECUTABLE_PATH = r"C:\Users\poku.flacko\Downloads\Applications\chromedriver_win32\chromedriver.exe"

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	"""
	Only functions that begin with "test_" will be run
	"""
	
	""" TODO: Find out if there is a way to have multiline comment that 
		do not become docstrings """
	
	def setUp(self):
		self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_EXECUTABLE_PATH, options=OPTIONS)
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def wait_for_row_in_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if (time.time() - start_time) > MAX_WAIT:
					raise e
				time.sleep(0.5)

				
	def test_can_start_a_persistent_list_for_one_user(self):
		""" Edith has heard about a cool new online to-do app. She goes 
			to check out its homepage """
		self.browser.get(self.live_server_url)
		
		""" She notices the page title and header mention to-do lists """
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text # I'm assuming this finds the first such element
		self.assertIn('To-Do', header_text)
		
		""" She is invited to enter a to-do item straight away """
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		""" She types "Buy peacock feathers" into a text box (Edith's hobby is
			tying fly-fishing lures) """
		input_box.send_keys("Buy peacock feathers")
		
		""" When she hits enter, the page updates, and now the page lists
			"1: Buy peacock feathers" as an item in a to-do list table """
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_table("1: Buy peacock feathers")
		
		""" There is still a text box inviting her to add another item. She 
			enters "Use peacock feathers to make a fly" (Edith is very 
			methodical) """
		input_box = self.browser.find_element_by_id('id_new_item')
		# Do we actually need to get the input box again?
		# I suppose the page reloads after we post the first list item so it might be necessary
		input_box.send_keys("Use peacock feathers to make a fly")
		input_box.send_keys(Keys.ENTER)
		
		""" The page updates again, and now shows both items on her list """
		self.wait_for_row_in_table("1: Buy peacock feathers")
		self.wait_for_row_in_table("2: Use peacock feathers to make a fly")		
		
		
		""" Satisfied, she goes back to sleep """
		
	def test_multiple_users_can_start_lists_at_different_urls(self):
		""" Edith starts a new to-do list """
		self.browser.get(self.live_server_url)
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: Buy peacock feathers')
		
		""" She notices that her list has a unique URL """
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		
		""" Now a new user, Francis, comes along to the site """
		
		# We use a new browser session to make sure that no information of 
		# Edith's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_EXECUTABLE_PATH, options=OPTIONS)
		
		""" Francis visits the home page. There is no sign of Edith's list """
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		
		""" Francis starts a new list by entering a new item. He is less 
			interesting than Edith... """
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: Buy milk')
		
		""" Francis gets his own unique URL """
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		
		""" Again, there is no trace of Edith's list """
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
		
		""" Satisfied, they both go back to sleep """

	def test_layout_and_styling(self):
		''' Someone goes to the home page '''
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		''' They notice the input box is centered '''
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2, 
			512, 
			delta=10
		)

		''' They start a new list and see the input is centered there as well '''
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2, 
			512, 
			delta=10
		)
