import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
chrome_user_data_path_windows = r"C:\Users\poku.flacko\AppData\Local\Google\Chrome\User Data\Default"
options.add_argument(r"user-data-dir=C:\Users\poku.flacko\AppData\Local\Google\Chrome\User Data\Default")

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Chrome(executable_path="C:\\Users\\poku.flacko\\Downloads\\Applications\\chromedriver_win32\\chromedriver.exe", options=options)
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	"""TODO: finish the "user story" comments"""
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get("http://localhost:8000")
		
		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		#"Browser title was {}".format(self.browser.title)
		self.fail("Finish the test")
		
		# She is invited to enter a to-do item straight away

if __name__ == "__main__":
	unittest.main(warnings="ignore")
