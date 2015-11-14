from django import forms
from .models import Accounts,Transfer_item,AddArrival, Item

class AccountsForm(forms.ModelForm):
	class Meta:
		widgets = {
		'password': forms.PasswordInput()
		}

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['store_code', 'unit_cost', 'category','brand','item_model','supplier', 'supplier_code']

class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item_code', 'quantity_to_transfer', 'transfer_date']
