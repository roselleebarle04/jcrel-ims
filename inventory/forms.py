from django import forms
from .models import Account,Transfer_item, AddArrival, Item, Sale, Supplier
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory



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
		fields = ['types', 'category', 'brand', 'model', 'supplier','supplier_code', 'store_code','store_quantity', 'warehouse_quantity','unit_cost', 'srp']

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
		
	
	def clean(self):
		cleaned_data = super(TransferForm,self).clean()
		d = cleaned_data.get('item')
		q_transfer =cleaned_data.get('quantity_to_transfer')
		w_qty = d.warehouse_quantity
		if  q_transfer > w_qty:
			msg = "Quantity exceed the current quantity of the Item in the Warehouse"
			self.add_error('quantity_to_transfer',msg)
		else:
			current_w = w_qty - q_transfer
			current_s = d.store_quantity + q_transfer
			d.warehouse_quantity = current_w
			d.store_quantity = current_s
			d.save()


	def __init__(self, *args, **kwargs):
		super(TransferForm,self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'


class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ['branch_name', 'address']


class AddSupplierForm(forms.ModelForm):
	class Meta: 
		model = Supplier
		fields = ['avatar', 'name', 'address', 'phone']

	# Override the django default fields
	def __init__(self, *args, **kwargs):
		super(AddSupplierForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'
