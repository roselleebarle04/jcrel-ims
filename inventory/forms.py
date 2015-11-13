from django import forms
<<<<<<< HEAD
from .models import Accounts,Transfer_item, AddArrival
=======
from .models import Accounts,Transfer_item,AddArrival, Item
>>>>>>> 639c149debdfa6fe5059448aacc8faf7e1fcc8ab

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
<<<<<<< HEAD
=======

>>>>>>> 639c149debdfa6fe5059448aacc8faf7e1fcc8ab
