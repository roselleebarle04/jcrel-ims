from django import forms
from .models import Account,Transfer_item, AddArrival
from .models import Account,Transfer_item,AddArrival, Item

class AccountForm(forms.ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ['first_name', 'last_name']

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't math")
		return password2


	# def clean_username(self):
	# 	username = self.cleaned_data['username']
	# 	if not re.search(r'^\w+$', username):
 #  		raise forms.ValidationError(u'Username can only contain '
 #    		'alphanumeric characters and the underscore.')
	# 	try:
 #  			User.objects.get(username=username)
	# 	except User.DoesNotExist:
 #  		return username
	# 	raise forms.ValidationError(u'Username is already taken.')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['store_code', 'unit_cost', 'category','brand','item_model','supplier', 'supplier_code']

class ArrivalForm(forms.ModelForm):
    class Meta:
        model = AddArrival
        fields = ['itemName', 'qty', 'itemCost']

class TransferForm(forms.ModelForm):
	class Meta:
		model = Transfer_item
		fields = ['item_code', 'quantity_to_transfer', 'transfer_date']
