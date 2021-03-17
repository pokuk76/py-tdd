from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()	# Assuming that the default value for request method is GET
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		# NB: this fails because the actual value of the csrf token template tag
		# is NOT in the expected_html
		
	def test_home_page_handles_POST_request(self):
		request = HttpRequest()
		request.method = "POST"
		request.POST['item_text'] = "A new list item"
		
		response = home_page(request)
		self.assertIn('A new list item', response.content.decode())
		
		# The render_to_string function takes, as its second parameter, 
		# a mapping of variable names to values
		expected_html = render_to_string(
			'home.html', {'new_item_text': 'A new list item'}
		)
		
		self.assertEqual(response.content.decode(), expected_html)
		# Again, this will fail