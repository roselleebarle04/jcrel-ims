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

	return render(request, 'dashboard.html', {
		'user':request.user.username,
		'items' : items,
		'sales': sales,
		'items_len' : items_len,
		'sales_len':sales_len,
		'items':items_list,
		'warning':warning,
		})

#############################################
##	Items 
#############################################
@login_required
def list_items(request):
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
	"""
	In adding an item, we want to store where the item is located, and the quantity of that 
	item in that location. 

	In choosing a location: 
	- If location already exists, then choose simply save a new instance of an ItemLocation in db
	- If location is not yet registered, then just save the new location immediately. (TODO)
	"""
	add_new_item_form = ItemForm(request.POST or None)
	locations = Location.objects.all()
	
	if request.method == 'POST':
		if add_new_item_form.is_valid():
			# Save the primary item details (category, brand, etc.)
			item = add_new_item_form.save(commit=False)
			item.save()

			# Then save the item in the location provided
			location_id = request.POST.get('current_location')
			current_location = Location.objects.get(id=location_id)
			quantity = request.POST.get('stock_in_location')
			if current_location:
				# The item is registered in a location... Let's record the item and its quantity in a location
				i = ItemLocation(item=item, location=current_location, quantity=quantity)
				i.save()
			return HttpResponseRedirect(reverse('list_items'))

	return render(request, 'items/add_item.html', {
		'form' : add_new_item_form, 
		'locations' : locations,
	})

def delete_item(request, item_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	item = Item.objects.get(pk = item_id)
	item.status = False
	item.save()
	return HttpResponseRedirect(reverse('items'))

def update_item(request, item_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	item = Item.objects.get(pk=item_id)
	if request.method == 'POST':
		item.types = request.POST.get('types')
		item.category = request.POST.get('category')
		item.brand = request.POST.get('brand')
		item.model = request.POST.get('model')
		item.supplier.name = request.POST.get('supplier')
		item.location = request.POST.get('location')
		item.item_code = request.POST.get('item_code')
		item.quantity= request.POST.get('quantity')
		item.srp = request.POST.get('srp')
		item.save()
		return HttpResponseRedirect(reverse('items'))

	return render(request, 'items/update_item.html', {
		'item' : item,
		'all_items':items_list,
		# 'items':items,
		'warning':warning, 
		# 'below_min':below_min
		})

#############################################
##	Transfers 
#############################################

@login_required
def create_transfer(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	transferForm = TransferForm(request.POST or None)
	formset = formset_factory(ItemTransferForm, formset=ItemTransferFormset, extra = 1)
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
		
		return HttpResponseRedirect(reverse('transfer_hist'))

	return render(request, 'transfer/transfer_form.html', {
		'TransferForm' : transferForm, 
		'formset' : transferFormset,
		'all_items':items_list,
		'items':items,
		'warning':warning,
		# 'below_min':below_min
		})

@login_required
def delete_transfer(request, transfer_id):
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

#############################################
##	Locations 
#############################################

@login_required
def list_locations(request):
	""" We want to display all items and their respective locations """
	items = Item.objects.all()
	locations = Location.objects.all()
	item_locations = ItemLocation.objects.all()
	print 'hi'
	return render(request, 'transfer/location.html', {
		'items' : items,
		'locations' : locations,
		'item_locations' : item_locations,
	})

@login_required
def add_location(request):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	location_list = Location.objects.all()
	form = LocationForm(request.POST or None)
	
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
def delete_location(request, location_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	warning = WarningItems.objects.all()
	
	lo = Location.objects.get(pk=location_id)
	lo.delete()
	return HttpResponseRedirect(reverse('location'))

#############################################
##	Arrivals 
#############################################
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

#############################################
##	Sales
#############################################
@login_required
def sales(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	saleForm = SaleForm(request.POST or None)
	formset = formset_factory(ItemSaleForm, formset=ItemSaleFormset, extra = 1)
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
			
			return HttpResponseRedirect(reverse('sales'))
		except ValueError:
			messages.warning(request, 'Please fill in all input boxes before submitting ')
			pass

	return render(request, 'sales/add_sale.html', {
		'AddSaleForm' : saleForm, 
		'formset' : saleFormset,
		'items':items,
		'all_items':items_list,
		'warning':warning,
		# 'below_min':below_min
		})

def delete_sale(request, sale_id):
	warning = WarningItems.objects.all()
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	sale = SoldItem.objects.get(pk = sale_id)
	sale.is_active = False
	sale.save()

	return HttpResponseRedirect(reverse('history'))

#############################################
##	Supplier
#############################################
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

	if  supplierForm.is_valid():
		supplierForm.save()
		return HttpResponseRedirect(reverse('suppliers'))

	return render(request, 'supplier/add_supplier.html', {
	 'form': supplierForm,
	  'all_items':items_list,
	  'warning':warning,
	  })

def update_supplier(request, supplier_id):
	# items = AddItem.objects.all()
	supplier = Supplier.objects.get(pk=supplier_id)
	warning = WarningItems.objects.all()
	items_list = Item.objects.all()

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
	
	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))

#############################################
##	Arrivals
#############################################
def arrival(request):
	items_list = Item.objects.all()
	items = ItemLocation.objects.all()
	warning = WarningItems.objects.all()
	arrivalForm = ArrivalForm(request.POST or None)
	formset = formset_factory(ItemArrivalForm, formset=ItemArrivalFormset, extra = 1)
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


def delete_arrival(request, arrival_id):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	warning = WarningItems.objects.all()
	a_item = ArrivedItem.objects.get(pk=arrival_id)
	a_item.is_active = False
	a_item.save()
	
	return HttpResponseRedirect(reverse('arrival_history'))


#############################################
##	Customer
#############################################
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

	return HttpResponseRedirect(reverse('customers'))
