from django.forms.formsets import BaseFormSet


class ItemArrivalFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

<<<<<<< HEAD
class ItemTransferFormset(BaseFormSet):
=======
class TransferRecordFormset(BaseFormSet):
>>>>>>> fee39a11981730017b369b40a18a276a1382a4e8
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
