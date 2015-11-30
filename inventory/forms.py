from django import forms
from django.forms import fields, models, formsets, widgets
from django.forms import BaseFormSet, formset_factory, BaseInlineFormSet
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core import validators
from django.contrib import messages


class AccountForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ['avatar']

class AddItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['types', 'category', 'brand', 'model', 'supplier', 'location', 'item_code','quantity', 'srp']

	def __init__(self, *args, **kwargs):
		super(AddItemForm,self).__init__(*args, **kwargs)
		self.fields['supplier'].widget.attrs['class'] = 'form-control'
		self.fields['location'].widget.attrs['class'] = 'form-control'
		self.fields['types'].error_messages['required'] = 'Enter item\'s type.'
		self.fields['category'].error_messages['required'] = 'Enter item\'s category'
		self.fields['brand'].error_messages['required'] = 'Enter item\'s brand'
		self.fields['model'].error_messages['required'] = 'Enter item\'s model'
		self.fields['supplier'].error_messages['required'] = 'Choose supplier.'	
		self.fields['location'].error_messages['required'] = 'Choose location.'		
		self.fields['item_code'].error_messages['required'] = 'Enter item\'s item code'
		self.fields['quantity'].error_messages['required'] = 'Enter item\'s quantity'
		self.fields['srp'].error_messages['required'] = 'Enter item\'s srp'
        	
class AddSaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ['date']

	def __init__(self, *args, **kwargs):
		super(AddSaleForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'

class AddSoldItemForm(forms.ModelForm):
	class Meta:
		model = SoldItem
		fields = ['item', 'quantity']

	def __init__(self, *args, **kwargs):
		super(AddSoldItemForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['item'].queryset = Item.objects.filter(status=True)
		# self.fields['item_cost'] = self.fields['item'].srp

	def clean_quantity(self):
		item = self.cleaned_data['item']
		qty_sale = self.cleaned_data['quantity']
		curr_qty = item.quantity
		update_qty = curr_qty - qty_sale
		
		if qty_sale <= curr_qty:
			item.quantity = update_qty
			item.save()
		else:
			raise ValidationError("Quantity exceeds the current quantity of items in the store")
		
		return self.cleaned_data['quantity']

class AddSoldItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return
			
class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer
		fields = ['location', 'transfer_date']

	def __init__(self, *args, **kwargs):
		super(TransferForm, self).__init__(*args, **kwargs)
		self.fields['location'].widget.attrs['class'] = 'form-control'
		self.fields['transfer_date'].widget.attrs['class'] = 'form-control'	

class Transfer_itemForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item', 'quantity_to_transfer']
		
	
	def clean(self):
		data = self.cleaned_data['item']
		q_transfer = self.cleaned_data['quantity_to_transfer']
		w_qty = data.warehouse_quantity
		if q_transfer> w_qty:
			raise forms.ValidationError("Quantity Exceed current quantity of the Item in the Warehouse")
		else:
			current_w = w_qty - q_transfer
			current_s = data.store_quantity + q_transfer
			data.warehouse_quantity = current_w
			data.store_quantity = current_s
			data.save()

	def __init__(self, *args, **kwargs):
		super(Transfer_itemForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity_to_transfer'].widget.attrs['class'] = 'form-control'
		
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
		self.fields['name'].widget.attrs['class'] = 'form-control'
		self.fields['address'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['class'] = 'form-control'

class AddArrivalForm(forms.ModelForm): 
	class Meta: 
		model = Arrival
		fields = ['date', 'supplier', 'delivery_receipt_no', 'tracking_no']

	def __init__(self, *args, **kwargs):
		super(AddArrivalForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'
		self.fields['delivery_receipt_no'].widget.attrs['class'] = 'form-control'
		self.fields['tracking_no'].widget.attrs['class'] = 'form-control'
		

class AddArrivedItemForm(forms.ModelForm): 
	class Meta: 
		model = ArrivedItem
		fields = ['item', 'quantity', 'item_cost']

	def __init__(self, *args, **kwargs):
		super(AddArrivedItemForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['item_cost'].widget.attrs['class'] = 'form-control'

class AddCustomerForm(forms.ModelForm):
	class Meta: 
		model = Customer
		fields = ['avatar', 'name', 'address', 'phone']

	# Override the django default fields
	def __init__(self, *args, **kwargs):
		super(AddCustomerForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'

