from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
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
from django.contrib import messages


from django.forms import formset_factory
from django.db import IntegrityError, transaction
from django.core import validators

from config import settings
from .models import *
from .forms import *


# @login_required
# def dashboard(request):
# 	print request.user.username
#     return render(request, 'dashboard/dashboard.html', {
#     'user' = request.user.username
#     })
@login_required
def dashboard(request):
	items_list = Item.objects.all()
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
		'items':items_list
		})

def signup(request):

	if request.method == 'POST':	
		form = UserCreationForm(request.POST or None)

		if form.is_valid():
			username = request.POST.get("username")
			email = request.POST.get("email")
			password1 = request.POST.get("password1")
			password2 = request.POST.get("password2")

			form.save()
			
			return HttpResponseRedirect('/login/')
	else:
		# form = AccountForm()
		form = UserCreationForm()

	return render(request, 'accounts/signup.html', {'form':form})

def change_password(request):
	items_list = Item.objects.all()
	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {'items':items_list})


@login_required
def notifications(request):
	items_list = Item.objects.all()
	itemLength = len(items_list)

	for i in items_list:
		print "%s %d" % (i.item_code, i.total_quantity)

	return render(request, 'notifications/notification_page.html', {
		'items':items_list,
		'itemLength': itemLength
		})


@login_required
def inventory_reports(request):
	items_list = Item.objects.all()
	filterby = request.GET.get('filter')
	items = Item.objects.all()
	itemsLen = len(items)
	return render(request, 'reports/inventory_reports.html', {
		'filterby': filterby,
		'items': items,
		'items_length': itemsLen,
		'items':items_list
	})

@login_required
def sales_reports(request):
	items_list = Item.objects.all()
	return render(request, 'reports/sales_reports.html', {'items':items_list})

def login(request):
	return render(request, 'dashboard/login.html', {})

def transfer_hist(request):
	items_list = Item.objects.all()
	transfer_list = Transfer_item.objects.all()
	transferLen = len(transfer_list)
	return render(request, 'transfer/transfer_hist.html', {
		'transfer': transfer_list,
		'transferLen': transferLen,
		'items':items_list
		})


def create_transfer(request):
	items_list = Item.objects.all()
	transferForm = TransferForm(request.POST or None)
	formset = formset_factory(Transfer_itemForm, formset=Transfer_itemFormset, extra = 1)
	transferFormset = formset(request.POST or None)

	if transferForm.is_valid() and transferFormset.is_valid():
		p = transferForm.save(commit=False)
		p.save()
		transfer_id = p
		new_items = []

		
		for form in transferFormset:
			item = form.cleaned_data.get('item')
			transfer = transfer_id
			quantity_to_transfer = form.cleaned_data.get('quantity_to_transfer')
			i = Transfer_item(item = item,quantity_to_transfer=quantity_to_transfer, trans=p)	
			i.save()
		
		return HttpResponseRedirect(reverse('transfer_hist'))

	return render(request, 'transfer/transfer_form.html', {
		'TransferForm' : transferForm, 
		'formset' : transferFormset, 
		'items':items_list
		})
#def create_transfer(request,template_name ='transfer/transfer_form.html'):
#	form = TransferForm(request.POST or None)
#	if form.is_valid():
#		form.save()
#		return redirect('transfer_hist')
#	return render(request,template_name,{'form':form})

def location(request):
	items_list = Item.objects.all()
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
		'items':items_list
		})


def transfer_delete(request, transfer_id):
	items_list = Item.objects.all()
	t_item = Transfer_item.objects.filter(pk=transfer_id)
	t_item.delete()
	return HttpResponseRedirect(reverse('transfer_hist'))

def location_delete(request, location_id):
	items_list = Item.objects.all()
	lo = Location.objects.get(pk=location_id)
	lo.delete()
	return HttpResponseRedirect(reverse('location'))


@login_required
def items(request):
	items_list = Item.objects.all().filter(status=True)
	itemLen = len(items_list)
	
	return render(request, 'items/items.html', {
		'items': items_list,
		'itemLen': itemLen,
		# 'items_list':items_list
		})

def add_item(request):
	items_list = Item.objects.all()
	form = AddItemForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'items/add_item.html' , {'form' : form, 'items':items_list})

def delete_item(request, item_id):
	items_list = Item.objects.all()
	item = Item.objects.get(pk = item_id)
	item.status = False
	item.save()
	return HttpResponseRedirect(reverse('items'))

def update_item(request, item_id):
	items_list = Item.objects.all()
	item = Item.objects.get(pk=item_id)

	if request.method == 'POST':
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

	return render(request, 'items/update_item.html', {'item' : item, 'items':items_list})


@login_required
<<<<<<< HEAD
=======
def sale(request):
	items_list = Item.objects.all()
	saleForm = AddSaleForm(request.POST or None)
	formset = formset_factory(AddSoldItemForm, formset=AddSoldItemFormset, extra = 1)
	saleFormset = formset(request.POST or None)

	if saleForm.is_valid() and saleFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		p = saleForm.save(commit=False)

		#save the form
		p.save()
		sale_id = p
		new_items = []

		# loop through all forms in the formset, and save each form - add the purchaseId to each form
		for form in saleFormset:
			item = form.cleaned_data.get('item')
			sale = sale_id
			quantity = form.cleaned_data.get('quantity')
			item_cost = form.cleaned_data.get('item_cost')
			new_item = SoldItem(item=item, sale=p, quantity=quantity, item_cost=item_cost)	
			new_item.save()
		
		return HttpResponseRedirect(reverse('sale'))

	return render(request, 'sales/sale.html', {
		'AddSaleForm' : saleForm, 
		'formset' : saleFormset, 
		'items':items_list
		})
>>>>>>> 4d1d763965d60295a7c4ff69c3c09d92682b3eb0
def sales(request):
	items_list = Item.objects.all()
	sales_list = Sale.objects.all()
	salesLen = len(sales_list)

	return render(request, 'sales/sales.html', {
		'sales_list':sales_list,
		'salesLen' : salesLen,
		'items':items_list
		})

def add_sale(request):
	items_list = Item.objects.all()
	form = AddSaleForm(request.POST or None)
	if form.is_valid():
		form.clean_quantity()
		form.save()
		return redirect('sales')
	return render(request, 'sales/add_sale.html', {'form' : form, 'items':items_list})


def delete_sale(request, sale_id):
	items_list = Item.objects.all()
	sale = Sale.objects.get(pk = sale_id)
	sale.delete()
	return HttpResponseRedirect(reverse('sales'))

def update_sale(request, sale_id):
	items_list = Item.objects.all()
	sale = Sale.objects.get(pk = sale_id)
	if request.method == 'POST':
		sale = Sale.objects.get(pk = sale_id)
		sale.item.item_code = request.POST.get('item')
		sale.quantity =  request.POST.get('quantity')
		sale.date = request.POST.get('date')
		sale.save()
		return HttpResponseRedirect(reverse('sales')) 

	return render(request, 'sales/update_sale.html', {'sale' : sale, 'items':items_list})	

def suppliers(request):
	items_list = Item.objects.all()
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
		'supplierForm': supplierForm,
		'items':items_list
	})

def update_supplier(request, supplier_id):
	items_list = Item.objects.all()
	if request.method == 'POST':
		supplier = Supplier.objects.get(pk=supplier_id)
		supplier.avatar = request.FILES.get('avatar')
		supplier.name = request.POST.get('name')
		supplier.phone = request.POST.get('phone')
		supplier.address = request.POST.get('address')
		supplier.save()
	return HttpResponseRedirect(reverse('suppliers'))

def delete_supplier(request, supplier_id):
	items_list = Item.objects.all()
	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))


def arrival(request):
	items_list = Item.objects.all()
	arrivalForm = AddArrivalForm(request.POST or None)
	formset = formset_factory(AddArrivedItemForm, formset=AddArrivedItemFormset, extra = 1)
	arrivalFormset = formset(request.POST or None)

	if arrivalForm.is_valid() and arrivalFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		p = arrivalForm.save(commit=False)

		#save the form
		p.save()
		arrival_id = p
		new_items = []

		# loop through all forms in the formset, and save each form - add the purchaseId to each form
		for form in arrivalFormset:
			item = form.cleaned_data.get('item')
			arrival = arrival_id
			quantity = form.cleaned_data.get('quantity')
			item_cost = form.cleaned_data.get('item_cost')
			i = ArrivedItem(item=item, arrival=p, quantity=quantity, item_cost=item_cost)	
			i.save()
		
		return HttpResponseRedirect(reverse('arrival'))

	return render(request, 'arrival/arrival.html', {
		'AddArrivalForm' : arrivalForm, 
		'formset' : arrivalFormset,
		'items':items_list 
		})

def arrival_history(request):
	arrival_list = ArrivedItem.objects.all()
	arrivalLen = len(arrival_list)
	return render(request, 'arrival/arrival_history.html', {
		'arrival': arrival_list,
		'arrivalLen': arrivalLen
		})


def customers(request):
	items_list = Item.objects.all()
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
		'customerForm': customerForm,
		'items':items_list
	})

def update_customer(request, supplier_id):
	items_list = Item.objects.all()
	if request.method == 'POST':
		customer = Supplier.objects.get(pk=supplier_id)
		customer.avatar = request.FILES.get('avatar')
		customer.name = request.POST.get('name')
		customer.phone = request.POST.get('phone')
		customer.address = request.POST.get('address')
		customer.save()
	return HttpResponseRedirect(reverse('customers'))

def delete_customer(request, customer_id):
	items_list = Item.objects.all()
	s = Customer.objects.get(pk=customer_id)
	s.delete()
	return HttpResponseRedirect(reverse('customers'))


def settings(request):
	items_list = Item.objects.all()
	users = User.objects.all()
	account_form = AccountForm()
	return render(request, 'settings/settings.html', {'account_form':account_form,
<<<<<<< HEAD
		'users':users})
=======
		'users':users, 'items':items_list})
>>>>>>> 4d1d763965d60295a7c4ff69c3c09d92682b3eb0
