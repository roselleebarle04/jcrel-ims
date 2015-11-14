from django import forms
<<<<<<< HEAD
from .models import Accounts,Transfer_item, AddArrival
=======
>>>>>>> 31e3e06bd3da449572cab0c4e2701e0badc74845
from .models import Accounts,Transfer_item,AddArrival, Item

class AccountsForm(forms.ModelForm):
	class Meta:
		fields = ['first_name', 'last_name', 'email', 'password']
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
