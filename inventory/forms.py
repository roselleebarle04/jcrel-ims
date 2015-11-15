from django import forms
<<<<<<< HEAD
from .models import Account,Transfer_item,AddArrival, Item
=======
>>>>>>> ca151792ce6434e674bfcaff048cf68ea27fbada
from .models import *


class AccountForm(forms.ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ['first_name', 'last_name']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['store_code', 'unit_cost', 'category','brand','model','supplier', 'supplier_code']

class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item', 'quantity_to_transfer', 'transfer_date']
