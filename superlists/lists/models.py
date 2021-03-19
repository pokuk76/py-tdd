from django.db import models

""" TODO: Support more than one list """
class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default="")
	list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
