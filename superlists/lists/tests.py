from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
	
	# def test_root_url_resolves_to_home_page_view(self):
		# found = resolve('/')
		# self.assertEqual(found.func, home_page)
		
	# def test_home_page_returns_correct_html(self):
		# # request = HttpRequest()	# Assuming that the default value for request method is GET
		# # response = home_page(request)
		# # expected_html = render_to_string('home.html')
		# # self.assertEqual(response.content.decode(), expected_html)
		# # NB: this fails because the actual value of the csrf token template tag
		# # is NOT in the expected_html
		
		# response = self.client.get('/')
		
		# html = response.content.decode('utf8')
		# self.assertTrue(html.startswith('<html>'))
		# self.assertIn('<title>To-Do lists</title>', html)
		# self.assertTrue(html.strip().endswith('</html>'))
		
		# self.assertTemplateUsed(response, 'home.html')
		
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		
	def test_can_handle_POST_request(self):
		""" TODO: POST test getting too long? """
		response = self.client.post('/', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first() #equivalent to Item.objects.all()[0]
		self.assertEqual(new_item.text, "A new list item")
		
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')
		
class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.save()
		
		second_item = Item()
		second_item.text = "Item the second"
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, "The first (ever) list item")
		self.assertEqual(second_saved_item.text, "Item the second")
		