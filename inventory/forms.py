from django import forms
from django.forms import fields, models, formsets, widgets, inlineformset_factory, BaseInlineFormSet
# from django.forms.formsets import BaseInlineFormSet
from .models import *
from django.conf import settings
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
        model = Arrival
        fields = ['date', 'dr', 'tracking_no','supplier']

    def __init__(self, *args, **kwargs):
		super(ArrivalForm,self).__init__(*args, **kwargs)
		self.fields['supplier'].widget.attrs['class'] = 'form-control'

class ArrivedItemForm(forms.ModelForm):
	class Meta(object):
		model = ArrivedItem
		fields = ['itemName', 'qty', 'itemCost']

	def __init__(self, arg):
		super(ArrivedItemForm, self).__init__(*args, **kwargs)
		self.fields['itemName'].widget.attrs['class'] = 'form-control'
		
class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['date', 'dr', 'tracking_no','supplier', 'itemName', 'qty', 'itemCost']
	def __init__(self, *args, **kwargs):
		super(ArrivalForm,self).__init__(*args, **kwargs)
		self.fields['itemName'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'

def get_arriveditem_formset(form, formset=BaseInlineFormSet, **kwargs):
    return inlineformset_factory(Arrival, ArrivedItem, form, formset, **kwargs)


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
