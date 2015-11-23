from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,render_to_response, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.forms import formset_factory
from django.db import IntegrityError, transaction
from django.core import validators
from django.template.context import RequestContext


from config import settings
from .models import *
from .forms import *


# @login_required
# def dashboard(request):
# 	print request.user.username
#     return render(request, 'dashboard/dashboard.html', {
#     'user' = request.user.username
#     })

def display_data(request, data, **kwargs):
    return render_to_response('arrival/arrival_history.html', dict(data=data, **kwargs),
        context_instance=RequestContext(request))

@login_required
def dashboard(request):
	items = Item.objects.all()
	sales = Sale.objects.all()
	items_len = len(items)
	sales_len = len(sales)
	return render(request, 'dashboard.html', {
		'user':request.user.username,
		'items' : items,
		'sales': sales,
		'items_len' : items_len,
		'sales_len':sales_len,
		})

def login(request):
	return render(request, 'accounts/login.html', {})

def signup(request):

	if request.method == 'POST':	
		form = AccountForm(request.POST)	
		# form = UserCreationForm(request.POST)
		if form.is_valid:
			username = request.POST.get("username")
			email = request.POST.get("email")
			password1 = request.POST.get("password1")
			password2 = request.POST.get("password2")

			form.clean_password2
			form.save(True)
			


		# first_name = request.POST.get('first_name')
		# last_name = request.POST.get('last_name')
		# email = request.POST.get('email')
		# username = request.POST.get('username')
		# password1 = request.POST.get('password1')
		# password_confirmation = request.POST.get('password_confirmation')
		# form.clean_password2

		# new_user = User.objects.create_user(username=username, email=email, password=password1)
		# new_user.save()
			
		return HttpResponseRedirect('/login/')
	else:
		form = AccountForm()
		# form = UserCreationForm()

	return render(request, 'accounts/signup.html', {'form':form})

def change_password(request):
	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {})


@login_required
def notifications(request):
	items_list = Item.objects.all()
	itemLen = len(items_list)

	for i in items_list:
		print "%s %d" % (i.item_code, i.total_quantity)

	return render(request, 'notifications/notification_page.html', {
		'items_list':items_list,
		'itemLen': itemLen
		})


@login_required
def inventory_reports(request):
	filterby = request.GET.get('filter')
	items = Item.objects.all()
	itemsLen = len(items)
	return render(request, 'reports/inventory_reports.html', {
		'filterby': filterby,
		'items': items,
		'items_length': itemsLen,
	})

@login_required
def sales_reports(request):
	return render(request, 'reports/sales_reports.html', {})
def login(request):
	return render(request, 'dashboard/login.html', {})

def transfer_hist(request):
	transfer_list = Transfer_item.objects.all()
	transferLen = len(transfer_list)
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_hist')
	return render(request, 'transfer/transfer_hist.html', {
		'transfer': transfer_list,
		'transferLen': transferLen,
		'form' : form,
		})

def location(request):
	location_list = Location.objects.all()
	locationLen = len(location_list)
	form = LocationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('location')
	return render(request, 'transfer/location.html', {
		'location': location_list,
		'locationLen': locationLen,
		'form' : form,
		})


def transfer_delete(request, transfer_id):
	t_item = Transfer_item.objects.filter(pk=transfer_id)
	t_item.delete()
	return HttpResponseRedirect(reverse('transfer_hist'))

def location_delete(request, location_id):
	lo = Location.objects.get(pk=location_id)
	lo.delete()
	return HttpResponseRedirect(reverse('location'))


@login_required
def items(request):
	items_list = Item.objects.all().filter(status=True)
	itemLen = len(items_list)
	form = AddItemForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'items/items.html', {
		'items': items_list,
		'itemLen': itemLen,
		'form' : form,
		})

def delete_item(request, item_id):
	item = Item.objects.get(pk = item_id)
	item.status = False
	item.drop()
	return HttpResponseRedirect(reverse('items'))

def update_item(request, item_id):
	if request.method == 'POST':
		item = Item.objects.get(pk = item_id)
		item.types = request.POST.get('types')
		item.category = request.POST.get('category')
		item.brand = request.POST.get('brand')
		item.model = request.POST.get('model')
		item.supplier.name = request.POST.get('supplier')
		item.item_code = request.POST.get('item_code')
		item.store_quantity= request.POST.get('store_quantity')
		item.warehouse_quantity= request.POST.get('warehouse_quantity')
		item.srp = request.POST.get('srp')
		item.save()
	return HttpResponseRedirect(reverse('items'))


@login_required
def sales(request):

	sales_list = Sale.objects.all()
	salesLen = len(sales_list)
	form = AddSaleForm(request.POST or None)
	
	if form.is_valid():
		item = form.cleaned_data['item']
		q_sale = form.cleaned_data['quantity']
		store_qty = item.store_quantity
		update_qty = store_qty - q_sale

		if update_qty < 0 :
			form.clean_message()			
			return render (request, 'sales/modals.html', {'error' : True})
		else:
			item.store_quantity = update_qty
			item.save()
			
		form.save()			
		return redirect('sales')

	return render(request, 'sales/sales.html', {
		'sales_list':sales_list,
		'salesLen' : salesLen,
		'form' : form,
		})

def delete_sale(request, sale_id):
	sale = Sale.objects.get(pk = sale_id)
	sale.delete()
	return HttpResponseRedirect(reverse('sales'))

def update_sale(request, sale_id):
	if request.method == 'POST':
		sale = Sale.objects.get(pk = sale_id)
		sale.item.item_code = request.POST.get('item')
		sale.quantity =  request.POST.get('quantity')
		sale.date = request.POST.get('date')
		sale.save()
	return HttpResponseRedirect(reverse('sales')) 		

def suppliers(request):
	s_list = Supplier.objects.all()
	s_len = len(s_list)

	# Add Supplier Pop-up Form - Handling
	# NOTE: Remove add_supplier view since it's already integrated here.
	supplierForm = AddSupplierForm(request.POST or None, request.FILES)
	if  supplierForm.is_valid():
		supplierForm.save()
		return HttpResponseRedirect(reverse('suppliers'))

	return render(request, 'supplier/suppliers.html', {
		'suppliers': s_list,
		's_len': s_len,
		'supplierForm': supplierForm
	})

def update_supplier(request, supplier_id):
	if request.method == 'POST':
		supplier = Supplier.objects.get(pk=supplier_id)
		supplier.avatar = request.FILES.get('avatar')
		supplier.name = request.POST.get('name')
		supplier.phone = request.POST.get('phone')
		supplier.address = request.POST.get('address')
		supplier.save()
	return HttpResponseRedirect(reverse('suppliers'))

def delete_supplier(request, supplier_id):
	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))


def arrival(request):
	arrivalForm = AddArrivalForm(request.POST or None)
	formset = formset_factory(AddArrivedItemForm, formset=AddArrivedItemFormset, extra = 1)
	arrivalFormset = formset(request.POST or None)

	if arrivalForm.is_valid() and arrivalFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		a = arrivalForm.save(commit=False)

		#save the form
		a.save()
		arrival_id = a
		new_items = []

		# loop through all forms in the formset, and save each form - add the arrivalid to each form
		for form in arrivalFormset:
			item = form.cleaned_data.get('item')
			arrival = arrival_id
			quantity = form.cleaned_data.get('quantity')
			item_cost = form.cleaned_data.get('item_cost')
			i = ArrivedItem(item=item, arrival=a, quantity=quantity, item_cost=item_cost)	
			i.save()

		return HttpResponseRedirect(reverse('arrival'))

	return render(request, 'arrival/arrival.html', {
		'AddArrivalForm' : arrivalForm, 
		'formset' : arrivalFormset, 
		})
def customers(request):
	c_list = Customer.objects.all()
	c_len = len(c_list)

	# Add Supplier Pop-up Form - Handling
	# NOTE: Remove add_supplier view since it's already integrated here.
	customerForm = AddCustomerForm(request.POST or None, request.FILES)
	if  customerForm.is_valid():
		customerForm.save()
		return HttpResponseRedirect(reverse('customers'))

	return render(request, 'customers.html', {
		'customers': c_list,
		'c_len': c_len,
		'customerForm': customerForm
	})

def update_customer(request, supplier_id):
	if request.method == 'POST':
		customer = Supplier.objects.get(pk=supplier_id)
		customer.avatar = request.FILES.get('avatar')
		customer.name = request.POST.get('name')
		customer.phone = request.POST.get('phone')
		customer.address = request.POST.get('address')
		customer.save()
	return HttpResponseRedirect(reverse('customers'))

def delete_customer(request, customer_id):
	s = Customer.objects.get(pk=customer_id)
	s.delete()
	return HttpResponseRedirect(reverse('customers'))


