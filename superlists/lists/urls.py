from django.urls import path, re_path
import lists.views

# https://docs.djangoproject.com/en/3.1/topics/http/urls/

urlpatterns = [
	path('new', lists.views.new_list, name='new_list'),
	# Equivalent to above: re_path(r'^new$', lists.views.new_list, name='new_list')
	# Equivalent to below: ('<int:list_id>/', lists.views.view_list, name='view_list')
	re_path(r'^(\d+)/$', lists.views.view_list, name='view_list'),
	path('<int:list_id>/add_item', lists.views.add_item, name='add_item'),
	# Equivalent to above: re_path(r'^(\d+)/add_item$', lists.views.view_list, name='add_item')
]
