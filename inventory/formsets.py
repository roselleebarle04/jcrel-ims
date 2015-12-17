from django.forms.formsets import BaseFormSet
from .models import *


class ItemArrivalFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class ItemSaleFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

	def __init__(self, *args, **kwargs):
		super(ItemSaleFormset, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False

class ItemLocationFormset(BaseFormSet):
	""" The intermediary between the item and location. We want to store the quantity of each item in a location """
	def clean(self):
		if any(self.errors):
			return

class ItemTransferFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return