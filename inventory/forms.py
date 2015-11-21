from django import forms
from .models import Account,Transfer_item, AddArrival, Item, Sale, Supplier
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

class AddItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['types', 'category', 'brand', 'model', 'supplier', 'item_code','store_quantity', 'warehouse_quantity', 'srp']

	def __init__(self, *args, **kwargs):
		super(AddItemForm,self).__init__(*args, **kwargs)
		self.fields['supplier'].widget.attrs['class'] = 'form-control'
        	
class AddSaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ['item', 'quantity', 'date']

	def __init__(self, *args, **kwargs):
		super(AddSaleForm,self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'

	def clean_message(self):
		item = form.cleaned_data['item']
		qty_sale = form.cleaned_data['quantity']
		store_qty = item.store_quantity
		update_qty = store_qty - q_sale

		if update_qty < 0 :
			raise forms.ValidationError("Quantity exceeds the current quantity of items in the store.")

class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['date', 'dr', 'tracking_no','supplier', 'itemName', 'qty', 'itemCost']

    def __init__(self, *args, **kwargs):
		super(ArrivalForm,self).__init__(*args, **kwargs)
		self.fields['itemName'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item', 'quantity_to_transfer']

	def __init__(self, *args, **kwargs):
		super(TransferForm,self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'

class AddSupplierForm(forms.ModelForm):
	class Meta: 
		model = Supplier
		fields = ['avatar', 'name', 'address', 'phone']

	# Override the django default fields
	def __init__(self, *args, **kwargs):
		super(AddSupplierForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'
