from django.urls import path, re_path
import lists.views

urlpatterns = [
	path('new', lists.views.new_list, name='new_list'),
	re_path(r'^(\d+)/$', lists.views.view_list, name='view_list'),
	path('<int:list_id>/add_item', lists.views.add_item, name='add_item'),
]
