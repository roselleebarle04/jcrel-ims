from django.forms.formsets import BaseFormSet


class ItemArrivalFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class TransferRecordFormset(BaseFormSet):
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
