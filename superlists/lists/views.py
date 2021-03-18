from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

def home_page(request):
	if request.method == "POST": 
		# Assuming POST request comes as JSON, transformed into a Python dictionary
		Item.objects.create(text=request.POST['item_text'])
		
		# objects.create is a shorthand for the following 3 lines:
		# item = Item()
		# item.text = request.POST.get("item_text", '')
		# item.save()
		return redirect('/lists/the-only-list-in-the-world/')
	
	items = Item.objects.all()
	return render(request, 'home.html', {'items': items})
	
def view_list(request):
	items = Item.objects.all()
	return render(request, 'home.html', {'items': items})