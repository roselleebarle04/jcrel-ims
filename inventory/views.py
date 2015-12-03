from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.template.context import RequestContext

from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.core import validators

from config import settings
from .models import *
from .forms import *
from .formsets import *


@login_required
def dashboard(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	sales = Sale.objects.all()
	items_len = len(items)
	sales_len = len(sales)
	is_zero = 0
	below_min = is_zero
	

	for i in items:

		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)



	return render(request, 'dashboard.html', {
		'user':request.user.username,
		'items' : items,
		'sales': sales,
		'items_len' : items_len,
		'sales_len':sales_len,
		'items':items_list,
		'warning':warning,
		'below_min':below_min
		})

def landing_page(request):
	return render(request, 'landing_page.html')

def signup(request):
	if request.method == 'POST':	
		form = UserCreationForm(request.POST or None)

		if form.is_valid():
			username = request.POST.get("username")
			email = request.POST.get("email")
			password1 = request.POST.get("password1")
			password2 = request.POST.get("password2")

			# form = User.objects.create_user(username, email, password1)
			# # form.save()
			# new_user = form.save(commit=False)
			# new_user.save()

			
			new_user = User.objects.create_user(username, email, password1)
			new_user.save()

			avatar = request.FILES.get("avatar")

			# We need to create an account for the user created.
			new_account = Account(user=new_user, avatar=avatar)
			new_account.save()


			return HttpResponseRedirect('/login/')
	else:
		# form = AccountForm()
		form = UserCreationForm()

	return render(request, 'accounts/signup.html', {'form':form})

def change_password(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	

	for i in items_list:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {
		'all_items':items_list,
		# 'items':items,
		'warning':warning,
		# 'below_min':below_min
		})

@login_required
def notifications(request):
	items = ItemLocation.objects.all()
	itemLength = len(items)
	warning = WarningItems.objects.all()
	# is_zero = 0
	# below_min = is_zero
	

	# for i in items:

	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'notifications/notification_page.html', {
		'items':items,
		'itemLength': itemLength,
		'warning':warning,
		# 'below_min':below_min
		})

@login_required
def transfer_hist(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	transfer_list = Transfer_item.objects.all()
	transferLen = len(transfer_list)
	warning = WarningItems.objects.all()

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'transfer/transfer_hist.html', {
		'transfer': transfer_list,
		'transferLen': transferLen,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
		})

@login_required
def create_transfer(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	transferForm = TransferForm(request.POST or None)
	formset = formset_factory(Transfer_itemForm, formset=Transfer_itemFormset, extra = 1)
	transferFormset = formset(request.POST or None)

	if transferForm.is_valid() and transferFormset.is_valid():
		p = transferForm.save(commit=False)
		p.save()
		transfer_id = p
		
		for form in transferFormset:
			transfer = transfer_id
			item = form.cleaned_data['item']
			quantity_to_transfer = form.cleaned_data['quantity_to_transfer']
			i = Transfer_item(item = item, quantity_to_transfer=quantity_to_transfer, trans=p)	
			i.save()

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)
		
	return render(request, 'transfer/transfer_form.html', {
		'TransferForm' : transferForm, 
		'formset' : transferFormset,
		'all_items':items_list,
		'items':items,
		'warning':warning,
		# 'below_min':below_min
		}) 

def additemwlocation(request):
	addnewitemForm = AddNewItemForm(request.POST or None)
	formset = formset_factory(ItemLocationForm, formset=ItemLocationFormset, extra = 1)
	addnewitemFormset = formset(request.POST or None)
	
	if addnewitemForm.is_valid() and addnewitemFormset.is_valid():
		p = addnewitemForm.save(commit=False)
		p.save()
		add_id = p
		
		try:
			for form in addnewitemFormset:
				add = add_id
				dest = form.cleaned_data['destination']
				quantity = form.cleaned_data['quantity']
				i = ItemLocation(destination = dest, quantity=quantity, item = p)	
				i.save()
			
			messages.success(request, 'Item successfully added.')

			return HttpResponseRedirect(reverse('additemwlocation'))
		except KeyError:
			messages.warning(request, 'Please fill in all input boxes before submitting.')
			pass



	return render(request, 'items/itemwLocation.html', {
		'AddNewItemForm' : addnewitemForm, 
		'formset' : addnewitemFormset, 
		})



@login_required
def location(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	location_list = Location.objects.all()
	warning = WarningItems.objects.all()
	locationLen = len(location_list)
	form = LocationForm(request.POST or None)
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	if form.is_valid():
		form.save()
		return redirect('location')

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'transfer/location.html', {
		'location': location_list,
		'locationLen': locationLen,
		'form' : form,
		'all_items':items_list,
		'items':items,
		'warning':warning,
		# 'below_min':below_min
		})

@login_required
def transfer_delete(request, transfer_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	t_item = Transfer_item.objects.filter(pk=transfer_id)
	t_item.delete()
	

	for i in items_list:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('transfer_hist'))

@login_required
def arrival_delete(request, arrival_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	a_item = ArrivedItem.objects.get(item=arrival_id)
	a_item.is_active = False
	a_item.save()
	

	for i in items_list:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('arrival_history'))

@login_required
def add_location(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	location_list = Location.objects.all()
	form = LocationForm(request.POST or None)
	

	# for i in items_list:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if form.is_valid():
		form.save()
		return redirect('location')

	return render (request, 'transfer/add_location.html', {
		'form' : form, 
		'location':location_list,
		'all_items':items_list, 
		'warning':warning, 
		# 'items':items, 
		# 'below_min':below_min
		})


def update_location(request, location_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	location_list = Location.objects.all()
	location = Location.objects.get(pk=location_id)
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if request.method == 'POST':
		location.branch_name = request.POST.get('branch_name')
		location.address = request.POST.get('address')
		location.save()
		return HttpResponseRedirect(reverse('location'))
	return render(request, 'transfer/update_location.html', {
		'location': location, 
		'all_items':items_list, 
		'warning':warning,
		# 'items':items, 
		# 'below_min':below_min
		})

@login_required
def location_delete(request, location_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	lo = Location.objects.get(pk=location_id)
	lo.delete()
	return HttpResponseRedirect(reverse('location'))




@login_required
def items(request):
	items_list = Item.objects.all().filter(status=True)
	items = ItemLocation.objects.all()
	itemLen = len(items_list)
	warning = WarningItems.objects.all()
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)
	
	return render(request, 'items/items.html', {
		'all_items': items_list,
		'items':items,
		'itemLen': itemLen,
		'warning':warning,
		# 'below_min':below_min
		})

def add_item(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	form = AddItemForm(request.POST or None)
	

	form = AddNewItemForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('items')

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'items/add_item.html' , {
		'form' : form,
		'all_items':items_list, 
		'warning':warning,
		# 'items':items, 
	 # 'below_min':below_min
	 })

def delete_item(request, item_id):
	# items_list = Item.objects.filter(status=True,)
	warning = WarningItems.objects.all()
	item = ItemLocation.objects.get(pk = item_id)
	# item.status = False
	item.delete()
	# item.save()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('items'))

def update_item(request, item_id):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	item = Item.objects.get(pk=item_id)
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if request.method == 'POST':
		item.types = request.POST.get('types')
		item.category = request.POST.get('category')
		item.brand = request.POST.get('brand')
		item.model = request.POST.get('model')
		item.supplier.name = request.POST.get('supplier')
		item.location = request.POST.get('location')
		item.item_code = request.POST.get('item_code')
		items.quantity= request.POST.get('quantity')
		item.srp = request.POST.get('srp')
		item.save()
		return HttpResponseRedirect(reverse('items'))

	return render(request, 'items/update_item.html', {
		'item' : item,
		'all_items':items_list,
		'items':items,
		'warning':warning, 
		# 'below_min':below_min
		})


#add Sale
@login_required
def sales(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	saleForm = AddSaleForm(request.POST or None)
	formset = formset_factory(AddSoldItemForm, formset=AddSoldItemFormset, extra = 1)
	saleFormset = formset(request.POST or None)
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	if saleForm.is_valid() and saleFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		p = saleForm.save(commit=False)

		#save the form
		p.save()
		sale_id = p
		new_items = []

		try:
			# loop through all forms in the formset, and save each form - add the purchaseId to each form
			for form in saleFormset:
				item = form.cleaned_data.get('item')
				sale = sale_id
				quantity = form.cleaned_data.get('quantity')
				i = SoldItem(item=item, sale=p, quantity=quantity)	
				i.save()
			messages.success(request, 'Sale successfully added.')
			return HttpResponseRedirect(reverse('sales'))
		except ValueError:
			messages.warning(request, 'Please fill in all input boxes before submitting.')
			pass

	return render(request, 'sales/add_sale.html', {
		'AddSaleForm' : saleForm, 
		'formset' : saleFormset,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
		})

def sales_history(request):
	items = ItemLocation.objects.all()
	sales_list = SoldItem.objects.filter(is_active=True)
	warning = WarningItems.objects.all()
	salesLen = len(sales_list)
	items_list = Item.objects.all()
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'sales/sales_history.html', {
		'sales_list':sales_list,
		'salesLen' : salesLen,
		'items':items,
		'all_items':items_list,
		'warning':warning, 
		# 'below_min': below_min
		})


# def arrival_history(request):
# 	arr = Arrival.objects.all()
# 	arrivalLen = len(arr)
# 	suppliers = Supplier.objects.all()

# 	if request.method == 'POST': 
# 		date_from = request.POST.get('from') 
# 		date_to = request.POST.get('to')
# 		supplier = request.POST.get('supplier')

# 		filtered_arr = Arrival.apply_filter(date_from, date_to, supplier)
		
# 		arrivalLen = len(filtered_arr)
# 		return render(request, 'arrival/arrival_history.html', {
# 			'arrival': filtered_arr,
# 			'arrivalLen': arrivalLen,
# 			'suppliers': suppliers,
# 		})

# 	return render(request, 'arrival/arrival_history.html', {
# 		'arrival': arr,
# 		'arrivalLen': arrivalLen,
# 		'suppliers' : suppliers,
# 	})

def delete_sale(request, sale_id):
	warning = WarningItems.objects.all()
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	sale = SoldItem.objects.get(pk = sale_id)
	sale.is_active = False
	sale.save()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('history'))

def suppliers(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	s_list = Supplier.objects.all()
	s_len = len(s_list)
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'supplier/suppliers.html', {
		'suppliers': s_list,
		's_len': s_len,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
	})

def add_supplier(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	supplierForm = AddSupplierForm(request.POST or None, request.FILES or None)
	

	# for i in items_:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if  supplierForm.is_valid():
		supplierForm.save()
		return HttpResponseRedirect(reverse('suppliers'))

	return render(request, 'supplier/add_supplier.html', {
	 'form': supplierForm,
	  'all_items':items_list,
	  # 'items':items,
	  'warning':warning,
	  # 'below_min':below_min 
	  })

	# return render(request, 'supplier/add_supplier.html', { 'form': supplierForm, 'below_min':below_min })

	# return HttpResponseRedirect(reverse('suppliers'))

def add_supplier_arrival(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	supplierForm = AddSupplierForm(request.POST or None, request.FILES or None)
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if  supplierForm.is_valid():
		supplierForm.save()
		return HttpResponseRedirect(reverse('arrival'))

	return render(request, 'supplier/add_supplier.html', {
	 'form': supplierForm,
	  'all_items':items_list,
	  # 'items':items,
	  'warning':warning,
	  # 'below_min':below_min 
	  })

def update_supplier(request, supplier_id):
	# items = AddItem.objects.all()
	supplier = Supplier.objects.get(pk=supplier_id)
	warning = WarningItems.objects.all()
	items_list = Item.objects.all()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	if request.method == 'POST':
		supplier.avatar = request.FILES.get('avatar')
		supplier.name = request.POST.get('name')
		supplier.phone = request.POST.get('phone')
		supplier.address = request.POST.get('address')
		supplier.save()
		return HttpResponseRedirect(reverse('suppliers'))
	return render(request, 'supplier/update_supplier.html', {
		'supplier': supplier,
		# 'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
		})

def delete_supplier(request, supplier_id):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))


def arrival(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	arrivalForm = AddArrivalForm(request.POST or None)
	formset = formset_factory(AddArrivedItemForm, formset=AddArrivedItemFormset, extra = 1)
	arrivalFormset = formset(request.POST or None)
	


	if arrivalForm.is_valid() and arrivalFormset.is_valid():
		# first save arrival details
		# commit = False means that we can store the arrival instance to the value p
		p = arrivalForm.save(commit=False)
		p.save()

		#save the form
		
		arrival_id = p
		new_items = []
		p.save()
		
		# loop through all forms in the formset, and save each form - add the arrivalId to each form
		try:
			for form in arrivalFormset:
				# print form.cleaned_data
				item = form.cleaned_data.get('item')
				arrival = arrival_id
				quantity = form.cleaned_data.get('quantity')
				item_cost = form.cleaned_data.get('item_cost')
				i = ArrivedItem(item=item, arrival=p, quantity=quantity, item_cost=item_cost)	
				i.save()
				messages.success(request, 'New Arrival has been added.')
			return HttpResponseRedirect(reverse('arrival'))
			
		except ValueError:
			messages.warning(request, 'Please fill in all input boxes before submitting ')
			pass

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'arrival/arrival.html', {
		'AddArrivalForm' : arrivalForm, 
		'formset' : arrivalFormset,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min 
		})

def register_arrived_item(request):
	item_list = RegisterArrivedItem.objects.all()
	warning = WarningItems.objects.all()

	registerForm = RegisterArrivedItemForm(request.POST or None, request.FILES)

	if  registerForm.is_valid():
		registerForm.save()
		return HttpResponseRedirect(reverse('arrival'))

	return render(request, 'arrival/register_arrived_item.html', {
		'form': registerForm,
		'all_items':item_list,
	})

def arrival_history(request):
	items =ItemLocation.objects.all()
	arr = Arrival.objects.all()
	warning = WarningItems.objects.all()
	arrivalLen = len(arr)
	suppliers = Supplier.objects.all()
	items_list = Item.objects.all()
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	if request.method == 'POST': 
		date_from = request.POST.get('from') 
		date_to = request.POST.get('to')
		supplier = request.POST.get('supplier')

		filtered_arr = Arrival.apply_filter(date_from, date_to, supplier)
		
		arrivalLen = len(filtered_arr)
		return render(request, 'arrival/arrival_history.html', {
			'arrival': filtered_arr,
			'arrivalLen': arrivalLen,
			'suppliers': suppliers,
			'items':items,
			'all_items':items_list,
			'warning':warning,
			# 'below_min':below_min
		})


	return render(request, 'arrival/arrival_history.html', {
		'arrival': arr,
		'arrivalLen': arrivalLen,
		'suppliers' : suppliers,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
	})

def arrival_delete(request, arrival_id):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	a_item = ArrivedItem.objects.get(pk=arrival_id)
	a_item.is_active = False
	a_item.save()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('arrival_history'))


def customers(request):
	items = ItemLocation.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	c_list = Customer.objects.all()
	c_len = len(c_list)
	

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'customer/customers.html', {
		'customers': c_list,
		'c_len': c_len,
		'all_items':items_list,
		'items':items,
		'warning':warning,
		# 'below_min':below_min
	})

def add_customer(request):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	
	print 'hi'
	customerForm = AddCustomerForm(request.POST or None, request.FILES)

	if  customerForm.is_valid():
		customerForm.save()
		return HttpResponseRedirect(reverse('customers'))

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'customer/add_customer.html', {
		'form': customerForm,
		'all_items':items_list,
		# 'below_min':below_min,
		# 'items':items
	})

def update_customer(request, customer_id):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	customer = Customer.objects.get(pk=customer_id)
	

	if request.method == 'POST':
		customer.avatar = request.FILES.get('avatar')
		customer.name = request.POST.get('name')
		customer.phone = request.POST.get('phone')
		customer.address = request.POST.get('address')
		customer.save()
		return HttpResponseRedirect(reverse('customers'))

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'customer/update_customer.html', {
		'customer': customer,
		# 'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
 	})

def delete_customer(request, customer_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	s = Customer.objects.get(pk=customer_id)
	s.delete()
	

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return HttpResponseRedirect(reverse('customers'))


def settings(request):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	

	try:
		account = Account.objects.filter(user=request.user.id)[0]
	except:
		account = ''

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'settings/settings.html', {
		'account':account,
		# 'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
		})

def update_settings(request):
	# If the account is already created for the user, just update the avatar, 
	# but not that the original user might not hava an account, yet - TODO

	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	# items = AddItem.objects.all()
	

	user = request.user
	try:
		account = Account.objects.filter(user=user.id)[0]
	except: 
		account = ''
	if request.method == 'POST':
		new_avatar = request.FILES.get('avatar')
		
		if account:
			account.avatar = new_avatar
			account.save()
		else:
			new_account = Account(user=user, avatar=new_avatar)
			new_account.save()
		return HttpResponseRedirect(reverse('settings'))

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'settings/update_settings.html', {
		'account': account,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min,
		# 'items':items
		})
