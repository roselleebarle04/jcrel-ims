from django.forms.formsets import BaseFormSet


class AddArrivedItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class ItemTransferFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

class AddSoldItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return
			
class ItemLocationFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return