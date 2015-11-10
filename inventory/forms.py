from django import forms
from .models import Accounts

class AccountsForm(forms.ModelForm):
	class Meta:
		widgets = {
		'password': forms.PasswordInput()
		}