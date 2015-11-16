


from django import forms
from .models import Account,Transfer_item,AddArrival, Item, Sale, Supplier
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class AccountForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch'
			)
		self.instance.username = self.cleaned_data.get('username')
		password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
		return password2

	# def clean_password2(self):
 #        password1 = self.cleaned_data.get("password1")
 #        password2 = self.cleaned_data.get("password2")
 #        if password1 and password2 and password1 != password2:
 #            raise forms.ValidationError(
 #                self.error_messages['password_mismatch'],
 #                code='password_mismatch',
 #            )
 #        self.instance.username = self.cleaned_data.get('username')
 #        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
 #        return password2


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['types', 'category', 'brand', 'model', 'supplier','supplier_code', 'store_code','store_quantity', 'warehouse_quantity','unit_cost', 'srp']

class AddSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['item', 'quantity', 'date']

'''class AddSupplierForm(forms.ModelForm):
	class Meta:
		model = Supplier
        fields = ['name', 'address', 'phone']'''
        
class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item', 'quantity_to_transfer', 'transfer_date']
