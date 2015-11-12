from django import forms
from .models import Accounts,Transfer_item

class AccountsForm(forms.ModelForm):
	class Meta:
		widgets = {
		'password': forms.PasswordInput()
		}

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item_code', 'quantity_to_transfer', 'transfer_date']