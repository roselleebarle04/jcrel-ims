from django.forms.formsets import BaseFormSet


class ItemArrivalFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class ItemTransferFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class ItemSaleFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class ItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return
	