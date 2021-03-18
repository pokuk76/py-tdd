from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

# The convention that we're using is that URLs w/out trailing slash are 
# "action" URLs which modify the database

class HomePageTest(TestCase):
	""" So TestCase creates a test database for unit tests (this explain why 
		see "Destroying test database for alias 'default'..." at the end of 
		unit tests 
		
		The same does not seem to be true for the unittest.TestCase class used 
		in our functional tests	
	"""
		
	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		
		
class ListAndItemModelsTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List() # Using "list_" to avoid conflict with built-in list
		list_.save()
		
		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = "Item the second"
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, "The first (ever) list item")
		self.assertEqual(first_saved_item.list, list_)
		""" Comparing list objects: behind the scenes, Django is comparing 
			their primary keys """
		self.assertEqual(second_saved_item.text, "Item the second")
		self.assertEqual(second_saved_item.list, list_)
		
class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get("/lists/the-only-list-in-the-world/")
		self.assertTemplateUsed(response, "list.html")
	
	def test_displays_all_items(self):
		# Set up test
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')
		
		# Invoke code/unit under test 
		response = self.client.get('/lists/the-only-list-in-the-world/')
		
		# Assertion(s)
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		
class NewListTest(TestCase):
	
	def test_can_save_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first() #equivalent to Item.objects.all()[0]
		self.assertEqual(new_item.text, "A new list item")
		
	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': "A new list item"})
		
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')