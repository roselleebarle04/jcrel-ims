
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
from django.db import IntegrityError, transaction, models
from django.core import validators

from config import settings
from .models import *
from .forms import *
from .formsets import *
from .quantity import *


def landing_page(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('dashboard')

	return render(request, 'landing.html', {
		'not_in_account_page': True,
		})

@login_required
def dashboard(request): 
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()
	sales = Sale.objects.all()
	customers = Customer.objects.all()
	items_len = len(itemloc)
	sales_len = len(sales)

	below_min = check_minimum()
	print "below_min %d" % below_min

	return render(request, 'dashboard.html', {
		'user':request.user.username,
		'itemloc':itemloc,
		'sales': sales,
		'customers': customers, 
		'items_len' : items_len,
		'sales_len':sales_len,
		'items':items_list,
		'below_min':below_min,

	})

#############################################
##	Items 
#############################################
@login_required
def list_items(request):
	active_items = Item.objects.all().filter(is_active=True)
	itemLen = len(active_items)
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	return render(request, 'items/items.html', {
		'items': active_items,
		'itemLen': itemLen,
		'below_min':below_min,
		'itemloc':itemloc
	})

# def notifications(request):
# 	itemloc = ItemLocation.objects.all()
# 	itemLength = len(items)
# 	warning = WarningItems.objects.all()

# 	below_min = check_minimum()
# 	print "below_min %d" % below_min

# 	return render(request, 'notifications/notification_page.html', {
# 		'itemloc':itemloc,
# 		'itemLength': itemLength,
# 		'below_min':below_min
# 	})

@login_required
def add_item(request):
	"""
	In adding an item, we want to store where the item is located, and the quantity of that 
	item in that location.
	"""
	add_new_item_form = ItemForm(request.POST or None)
	locations = Location.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	

	
	if request.method == 'POST':
		if add_new_item_form.is_valid():
			item = add_new_item_form.save(commit=False)
			item.save()

			# Save supplier if new
			supplier_name = request.POST.get('supplier_name', '')
			supplier_address = request.POST.get('supplier_address', '')
			if supplier_name and supplier_address:
				Supplier.objects.create(name=supplier_name, address=supplier_address)
				
			# Now save the quantity of each item in each location
			for loc in locations:
				current_stock = request.POST.get('current_stock_%d' % (loc.id))
				re_order_point = request.POST.get('re_order_point_%d' % (loc.id))
				re_order_amount = request.POST.get('re_order_amount_%d' % (loc.id))
				
				i = ItemLocation(item=item, location=loc, current_stock=current_stock, re_order_point=re_order_point, re_order_amount=re_order_amount)
				i.save()
				print i.current_stock
			messages.success(request, 'Item has been successfully added.')
			return HttpResponseRedirect(reverse('add_item'))

	save_minimums()
	
	return render(request, 'items/add_item.html', {
		'form' : add_new_item_form, 
		'locations' : locations,
		'below_min':below_min,
		'itemloc':itemloc
	})

@login_required
def delete_item(request, item_id):
	items_list = Item.objects.all()
	item = Item.objects.get(pk = item_id)
	item.is_active = False
	item.save()
	return HttpResponseRedirect(reverse('list_items'))

@login_required
def update_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	update_item_form = ItemForm(request.POST or None, instance=item)
	locations = Location.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	if request.method == 'POST':
		if update_item_form.is_valid():
			update_item_form.save()

			# Now save the quantity of each item in each location
			for loc in locations:
				print loc
				current_stock = request.POST.get('current_stock_%d' % (loc.id))
				print current_stock
				re_order_point = request.POST.get('re_order_point_%d' % (loc.id))
				re_order_amount = request.POST.get('re_order_amount_%d' % (loc.id))
				
				i = ItemLocation(item=item, location=loc, current_stock=current_stock, re_order_point=re_order_point, re_order_amount=re_order_amount)
				i.save()
				print i.current_stock
			messages.success(request, 'Item has been successfully updated.')
			return HttpResponseRedirect(reverse('list_items'))

	return render(request, 'items/update_item.html', {'form':update_item_form, 'below_min':below_min, 'itemloc':itemloc})
	

#############################################
##	Transfers 
#############################################
@login_required
def create_transfer(request):
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()
	transferForm = TransferForm(request.POST or None)
	formset = formset_factory(ItemTransferForm, formset=ItemTransferFormset, extra = 1)
	transferFormset = formset(request.POST or None)

	below_min = check_minimum()

	if transferForm.is_valid() and transferFormset.is_valid():
		p = transferForm.save(commit=False)
		source = transferForm.cleaned_data['From']
		destination = transferForm.cleaned_data['To']
		p.user = request.user
		p.save()
		transfer_id = p

		try: 
		
			for form in transferFormset:
				transfer = transfer_id
				item = form.cleaned_data['item']
				quantity = form.cleaned_data['quantity']
				i = ItemTransfer(item = item, quantity=quantity, transfer=transfer)
				i.save()	

				for loc in itemloc:
					if loc.location == source and loc.item == item :
						quantity_current = loc.current_stock

						if quantity <quantity_current :

							decremented = quantity_current - quantity
							loc.current_stock = decremented
							loc.save()

							for loct in itemloc:
								if loct.location == destination and loct.item == item :
									quantity_current = loct.current_stock
									incremented = quantity_current + quantity
									loct.current_stock = incremented
									loct.save()
						else:
							raise ValidationError("Insufficient Stock")
				return HttpResponseRedirect(reverse('transfer_history'))

		except KeyError:
			messages.warning(request, 'Please fill in all input boxes before submitting ')
			pass

	return render(request, 'transfer/transfer_form.html', {
		'TransferForm' : transferForm, 
		'formset' : transferFormset,
		'all_items':items_list,
		'itemloc':itemloc,
		'below_min':below_min}) 

@login_required
def list_locations(request):
	""" We want to display all items and their respective locations """
	locations = Location.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	print 'hi'
	loc_len = len(locations)
	return render(request, 'transfer/location.html', {
		'locations' : locations,
		'itemloc' : itemloc,
		'itemlen' : len(itemloc),
		'below_min':below_min,
		'loc_len' : loc_len,
	})

@login_required
def add_location(request):
	location_list = Location.objects.all()
	form = LocationForm(request.POST or None)
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	if form.is_valid():
		form.save()
		return redirect('location')

	return render (request, 'transfer/add_location.html', {
		'form' : form,
		'itemloc' : itemloc, 
		'location':location_list,
		# 'items':items, 
		'below_min':below_min
		})

@login_required
def update_location(request, location_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	location_list = Location.objects.all()
	location = Location.objects.get(pk=location_id)
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	if request.method == 'POST':
		location.branch_name = request.POST.get('name')
		location.address = request.POST.get('address')
		location.save()
		return HttpResponseRedirect(reverse('location'))
	return render(request, 'transfer/update_location.html', {
		'location': location, 
		'all_items':items_list,
		'itemloc':itemloc, 
		# 'items':items, 
		'below_min':below_min
		})

@login_required
def delete_location(request, location_id):
	location = Location.objects.all()
	lo = Location.objects.get(pk=location_id)
	lo.delete()
	return HttpResponseRedirect(reverse('location'))


#############################################
##	Arrivals 
#############################################
@login_required
def arrival(request):
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min
	
	arrivalForm = ArrivalForm(request.POST or None)
	formset = formset_factory(ItemArrivalForm, formset=ItemArrivalFormset, extra = 1)
	arrivalFormset = formset(request.POST or None)

	if arrivalForm.is_valid() and arrivalFormset.is_valid():
		# first save arrival details
		# commit = False means that we can store the arrival instance to the value p
		p = arrivalForm.save(commit=False)

		#save the form
		p.save()
		arrival_id = p
		new_items = []
		
		# loop through all forms in the formset, and save each form - add the arrivalId to each form
		try:
			for form in arrivalFormset:
				# print form.cleaned_data
				item = form.cleaned_data.get('item')
				arrival = arrival_id
				quantity = form.cleaned_data.get('quantity')
				item_cost = form.cleaned_data.get('item_cost')
				i = ItemArrival(item=item, quantity=quantity, item_cost=item_cost, arrival=arrival)

				for loc in itemloc:
					destination = arrivalForm.cleaned_data['location']	
					if loc.location == destination and loc.item == item :
						quantity_current = loc.current_stock
						incremented = quantity_current + quantity
						loc.current_stock = incremented
						loc.save()
				i.save()
			messages.success(request, 'New Arrival has been added.')
			return HttpResponseRedirect(reverse('arrival_history'))
			
		except ValueError:
			messages.warning(request, 'Please fill in all input boxes before submitting ')
			pass

	return render(request, 'arrival/arrival.html', {
		'AddArrivalForm' : arrivalForm, 
		'formset' : arrivalFormset,
		'itemloc':itemloc,
		'all_items':items_list,
		'below_min':below_min
		})

@login_required
def arrival_delete(request, arrival_id):
	items_list = Item.objects.all()
	# items = AddItem.objects.all()
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
	item_locations = ItemLocation.objects.all()
	saleForm = SaleForm(request.POST or None)
	formset = formset_factory(ItemSaleForm, formset=ItemSaleFormset, extra = 1)
	saleFormset = formset(request.POST or None)

	below_min = check_minimum()
	print "below_min %d" % below_min

	if saleForm.is_valid() and saleFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		p = saleForm.save(commit=False)
		#save the form
		p.save()
		sale_id = p
		new_items = []
		location = saleForm.cleaned_data['location']

		# try:
			# loop through all forms in the formset, and save each form - add the purchaseId to each form
		for form in saleFormset:
			sale_item = form.cleaned_data['item']
			sale = sale_id
			quantity = form.cleaned_data['quantity']				
			i =  ItemSale(item=sale_item, sale=p, quantity=quantity)

			for item in item_locations:
				if item.item==sale_item and item.location==location:
					if item.current_stock >= quantity:
						curr_stock = item.current_stock
						update_stock = curr_stock - quantity
						item.current_stock = update_stock
						item.save()	
						i.save()					
					else:
						messages.warning(request,"Quantity exceeds the current quantity of items.")	
				elif item.item==sale_item and item.location!=location:
					messages.warning(request,"The item does not exit exist in the location.")	
			
		messages.success(request, 'Sale successfully added.')
		return HttpResponseRedirect(reverse('sales'))

		# except KeyError: 
			# messages.warning(request, 'Please fill in all input boxes before submitting.')
			# pass

	sales_save_minimums()

	return render(request, 'sales/add_sale.html', {
		'AddSaleForm' : saleForm, 
		'formset' : saleFormset,
		'items':item_locations,
		'all_items':items_list,
		'below_min':below_min
		})

#############################################
##	Supplier
#############################################
@login_required
def suppliers(request):
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()
	s_list = Supplier.objects.all()
	s_len = len(s_list)

	below_min = check_minimum()
	print "below_min %d" % below_min

	return render(request, 'supplier/suppliers.html', {
		'suppliers': s_list,
		's_len': s_len,
		'itemloc':itemloc,
		'all_items':items_list,
		'below_min':below_min
	})

@login_required
def add_supplier(request):
	redirect_to = request.REQUEST.get('next', '/suppliers/')
	itemloc = ItemLocation.objects.all()

	items_list = Item.objects.all()
	# items = AddItem.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	supplierForm = SupplierForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if  supplierForm.is_valid():
			supplierForm.save()
			return HttpResponseRedirect(redirect_to)

	return render(request, 'supplier/add_supplier.html', {
	 'form': supplierForm,
	  'all_items':items_list,
	  'next': redirect_to,
	  'itemloc':itemloc,
	  'below_min':below_min
	  })

@login_required
def update_supplier(request, supplier_id):
	supplier = Supplier.objects.get(pk=supplier_id)
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	if request.method == 'POST':
		supplier.avatar = request.FILES.get('avatar')
		supplier.name = request.POST.get('name')
		supplier.phone = request.POST.get('phone')
		supplier.address = request.POST.get('address')
		supplier.save()
		return HttpResponseRedirect(reverse('suppliers'))
	
	return render(request, 'supplier/update_supplier.html', {
		'supplier': supplier,
		'all_items':items_list,
		'itemloc':itemloc,
		'below_min':below_min
		})

@login_required
def delete_supplier(request, supplier_id):
	items_list = Item.objects.all()
	
	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))

#############################################
##	Customer
#############################################
@login_required
def customers(request):
	itemloc = ItemLocation.objects.all()
	items_list = Item.objects.all()
	c_list = Customer.objects.all()
	c_len = len(c_list)
	

	below_min = check_minimum()
	print "below_min %d" % below_min

	return render(request, 'customer/customers.html', {
		'customers': c_list,
		'c_len': c_len,
		'all_items':items_list,
		'itemloc':itemloc,
		'below_min':below_min
	})

@login_required
def add_customer(request):
	items_list = Item.objects.all()
	customerForm = CustomerForm(request.POST or None, request.FILES)
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	if  customerForm.is_valid():
		customerForm.save()
		return HttpResponseRedirect(reverse('customers'))

	return render(request, 'customer/add_customer.html', {
		'form': customerForm,
		'itemloc':itemloc,
		'below_min':below_min
	})

@login_required
def update_customer(request, customer_id):
	items_list = Item.objects.all()
	customer = Customer.objects.get(pk=customer_id)
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min
	

	if request.method == 'POST':
		customer.avatar = request.FILES.get('avatar')
		customer.name = request.POST.get('name')
		customer.phone = request.POST.get('phone')
		customer.address = request.POST.get('address')
		customer.save()
		return HttpResponseRedirect(reverse('customers'))

	return render(request, 'customer/update_customer.html', {
		'customer': customer,
		'all_items':items_list,
		'itemloc':itemloc,
		'below_min':below_min
 	})

@login_required
def delete_customer(request, customer_id):
	items_list = Item.objects.all()
	s = Customer.objects.get(pk=customer_id)
	s.delete()

	return HttpResponseRedirect(reverse('customers'))
