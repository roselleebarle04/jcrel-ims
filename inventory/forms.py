from django import forms
<<<<<<< HEAD
from .models import Accounts,Transfer_item, AddArrival
=======
from .models import Accounts,Transfer_item,AddArrival, Item
>>>>>>> 328289c767f8210aa8b9eb7bfd97e0a923d7d121

class AccountsForm(forms.ModelForm):
	class Meta:
		widgets = {
		'password': forms.PasswordInput()
		}
<<<<<<< HEAD
=======

class Item(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['store_code', 'unit_cost', 'category','brand','item_model','supplier', 'supplier_code']
		

>>>>>>> 328289c767f8210aa8b9eb7bfd97e0a923d7d121
class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item_code', 'quantity_to_transfer', 'transfer_date']

