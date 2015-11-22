from django import forms
# from django.forms import fields, models, formsets, widgets
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator



class AccountForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

		def save(self, commit=True):
			user = super(AccountForm, self).save(commit=False)
			user.email = self.cleaned_data["email"]
			if commit:
				user.save()
			return user

		def clean_password2(self):
			password1 = self.cleaned_data.get("password1")
			password2 = self.cleaned_data.get("password2")

			if not password2:
				raise forms.ValidationError(self.error_messages['Must input Password Confirmation'],
					code='Password_Confirmation_empty')
			if password1 != password2:
				raise forms.ValidationError(self.error_messages['Passwords do not match.'],
					code='password_mismatch')

			# if password1 and password2 and password1 != password2:
				# raise forms.ValidationError("Password mismatch")
			# self.instance.username = self.cleaned_data.get('username')
			# password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
			return password2

# def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         self.instance.username = self.cleaned_data.get('username')
#         password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
#         return password2

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


class AddArrivalForm(forms.ModelForm): 
	class Meta: 
		model = Arrival
		fields = ['date', 'dr', 'trckng_no', 'supp']

	def __init__(self, *args, **kwargs):
		super(AddArrivalForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'
		self.fields['dr'].widget.attrs['class'] = 'form-control'
		self.fields['trckng_no'].widget.attrs['class'] = 'form-control'
		self.fields['supp'].widget.attrs['class'] = 'form-control'


class AddArrivedItemForm(forms.ModelForm): 
	class Meta: 
		model = ArrivedItem
		fields = ['arrived_item', 'arrived_quantity', 'itemCost']

	def __init__(self, *args, **kwargs):
		super(AddArrivedItemForm, self).__init__(*args, **kwargs)
		self.fields['arrived_item'].widget.attrs['class'] = 'form-control'
		self.fields['arrived_quantity'].widget.attrs['class'] = 'form-control'
		self.fields['itemCost'].widget.attrs['class'] = 'form-control'


class AddArrivedItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

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

class AddCustomerForm(forms.ModelForm):
	class Meta: 
		model = Supplier
		fields = ['avatar', 'name', 'address', 'phone']

	# Override the django default fields
	def __init__(self, *args, **kwargs):
		super(AddCustomerForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'

