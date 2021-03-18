import os
import time

import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options	# For Google Chrome ¬_¬

options = Options()
#chrome_user_data_path_windows = r"C:\Users\poku.flacko\AppData\Local\Google\Chrome\User Data\Default"
options.add_argument(r"user-data-dir=C:\Users\poku.flacko\AppData\Local\Google\Chrome\User Data\Default")
chromedriver_executable_path = r"C:\Users\poku.flacko\Downloads\Applications\chromedriver_win32\chromedriver.exe"

class NewVisitorTest(LiveServerTestCase):
	"""
	Only functions that begin with "test_" will be run
	"""
	
	""" TODO: Clean up database after functional test """
	
	def setUp(self):
		self.browser = webdriver.Chrome(executable_path=chromedriver_executable_path, options=options)
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def check_for_row_in_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		""" Edith(?) has heard about a cool new online to-do app. She goes 
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
		time.sleep(3)
		self.check_for_row_in_table("1: Buy peacock feathers")
		
		""" There is still a text box inviting her to add another item. She 
			enters "Use peacock feathers to make a fly" (Edith is very 
			methodical) """
		input_box = self.browser.find_element_by_id('id_new_item')
		# Do we actually need to get the input box again?
		# I suppose the page reloads after we post the first list item so it might be necessary
		input_box.send_keys("Use peacock feathers to make a fly")
		input_box.send_keys(Keys.ENTER)
		time.sleep(3)
		
		""" The page updates again, and now shows both items on her list """
		self.check_for_row_in_table("1: Buy peacock feathers")
		self.check_for_row_in_table("2: Use peacock feathers to make a fly")		
		
		
		self.fail("FINISH THE TEST")
		
		""" Edit wonders whether the site will remember her list. 
			Then she sees... """
