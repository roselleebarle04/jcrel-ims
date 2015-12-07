from django import forms
from django.forms import fields, models, formsets, widgets
from django.forms import BaseFormSet, formset_factory, BaseInlineFormSet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core import validators
from django.contrib import messages

from .models import *

class AccountForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ['avatar']

class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ['name', 'address']

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name', 'description', 'category', 'brand', 'model', 'item_code', 'unit_cost', 'supplier']

	def __init__(self, *args, **kwargs):
		super(ItemForm,self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['class'] = 'form-control'
		self.fields['category'].widget.attrs['class'] = 'form-control'
		self.fields['brand'].widget.attrs['class'] = 'form-control'
		self.fields['model'].widget.attrs['class'] = 'form-control'
		self.fields['item_code'].widget.attrs['class'] = 'form-control'
		self.fields['unit_cost'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'

		self.fields['name'].error_messages['required'] = 'Enter item\'s name.'
		self.fields['description'].error_messages['required'] = 'Enter item\'s description.'
		self.fields['category'].error_messages['required'] = 'Enter item\'s category'
		self.fields['brand'].error_messages['required'] = 'Enter item\'s brand'
		self.fields['model'].error_messages['required'] = 'Enter item\'s model'
		self.fields['item_code'].error_messages['required'] = 'Enter item\'s item code'
		self.fields['unit_cost'].error_messages['required'] = 'Enter item\'s unit cost'
		self.fields['supplier'].error_messages['required'] = 'Choose supplier.'	

class ItemLocationForm(forms.ModelForm):
	class Meta:
		model = ItemLocation
		fields = ['current_stock', 're_order_point', 're_order_amount']

	def __init__(self, *args, **kwargs):
		super(ItemLocationForm,self).__init__(*args, **kwargs)
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['current_stock'].widget.attrs['class'] = 'form-control'
		self.fields['re_order_point'].widget.attrs['class'] = 'form-control'
		self.fields['re_order_amount'].widget.attrs['class'] = 'form-control'
		
class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ['date', 'location','customer']

	def __init__(self, *args, **kwargs):
		super(SaleForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'
		self.fields['location'].widget.attrs['class'] = 'form-control'
		self.fields['customer'].widget.attrs['class'] = 'form-control'

class ItemSaleForm(forms.ModelForm):
	class Meta:
		model = ItemSale
		fields = ['item', 'quantity']

	def __init__(self, *args, **kwargs):
		super(ItemSaleForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['item'].queryset = Item.objects.filter(status=True)
		# self.fields['item_cost'] = self.fields['item'].srp

	# def clean_quantity(self):
	# 	item = self.cleaned_data['item']
	# 	qty_sale = self.cleaned_data['quantity']
	# 	curr_qty = item.location.quantity
	# 	update_qty = curr_qty - qty_sale
		
	# 	if qty_sale <= curr_qty:
	# 		item.location.itemlocation.quantity = update_qty
	# 		item.save()
	# 	else:
	# 		raise ValidationError("Quantity exceeds the current quantity of the item.")
		
	# 	return self.cleaned_data['quantity']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer
		fields = ['From', 'To']

	def __init__(self, *args, **kwargs):
		super(TransferForm, self).__init__(*args, **kwargs)
		self.fields['From'].widget.attrs['class'] = 'form-control'
		self.fields['To'].widget.attrs['class'] = 'form-control'

class ItemTransferForm(forms.ModelForm):
	class Meta:
		model = ItemTransfer
		fields = ['item', 'quantity']

	def __init__(self, *args, **kwargs):
		super(ItemTransferForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		
	
	# def clean(self):
	# 	data = self.cleaned_data['item']
	# 	q_transfer = self.cleaned_data['quantity_to_transfer']
	# 	w_qty = data.warehouse_quantity
	# 	if q_transfer> w_qty:
	# 		raise forms.ValidationError("Quantity Exceed current quantity of the Item in the Warehouse")
	# 	else:
	# 		current_w = w_qty - q_transfer
	# 		current_s = data.store_quantity + q_transfer
	# 		data.warehouse_quantity = current_w
	# 		data.store_quantity = current_s
	# 		data.save()

	

class SupplierForm(forms.ModelForm):
	class Meta: 
		model = Supplier
		fields = ['avatar', 'name', 'address', 'phone']

	def __init__(self, *args, **kwargs):
		super(SupplierForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'
		self.fields['name'].widget.attrs['class'] = 'form-control'
		self.fields['address'].widget.attrs['class'] = 'form-control'
		self.fields['phone'].widget.attrs['class'] = 'form-control'

class CustomerForm(forms.ModelForm):
	class Meta: 
		model = Customer
		fields = ['avatar', 'name', 'address', 'phone']

	# Override the django default fields
	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].widget.attrs['class'] = 'form-control'

class ArrivalForm(forms.ModelForm):
	class Meta: 
		model = Arrival
		fields = ['date', 'supplier', 'delivery_receipt_no', 'tracking_no', 'location']

	def __init__(self, *args, **kwargs):
		super(ArrivalForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'
		self.fields['delivery_receipt_no'].widget.attrs['class'] = 'form-control'
		self.fields['tracking_no'].widget.attrs['class'] = 'form-control'
		self.fields['location'].widget.attrs['class'] = 'form-control'

class ItemArrivalForm(forms.ModelForm):
	class Meta: 
		model = ItemArrival
		fields = ['item', 'quantity', 'item_cost']

	def __init__(self, *args, **kwargs):
		super(ItemArrivalForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['item_cost'].widget.attrs['class'] = 'form-control'

