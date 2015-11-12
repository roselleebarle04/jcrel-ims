from django import forms
from .models import Accounts,Transfer_item

class AccountsForm(forms.ModelForm):
	class Meta:
		widgets = {
		'password': forms.PasswordInput()
		}

<<<<<<< HEAD
class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']
=======
class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item_code', 'quantity_to_transfer', 'transfer_date']
>>>>>>> efdba7f6c78b42bb77fe83ed40151ef10e501a50
