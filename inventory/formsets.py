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

class ItemLocationFormset(BaseFormSet):
	""" The intermediary between the item and location. We want to store the quantity of each item in a location """
	def clean(self):
		if any(self.errors):
			return

class ItemTransferFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

		# for form in self.forms:
		# 	quantity = form.cleaned_data['quantity']
		# 	item = form.cleaned_data['item']
		# 	itemloc = ItemLocation.objects.all()

			# for loc in itemloc:
			# 	if loc.location == source and loc.item == item :
			# 		quantity_current = loc.current_stock
			# 		decremented = quantity_current - quantity
			# 		loc.current_stock = decremented
			# 		loc.save()

			# 	if loct.location == destination and loct.item == item :
			# 		quantity_current = loc.current_stock
			# 		incremented = quantity_current + quantity
			# 		loc.current_stock = incremented
			# 		loc.save()
		

