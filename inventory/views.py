from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from .models import *
from .forms import *


@login_required
def dashboard(request):
    print request.user.username
    return render(request, 'dashboard/dashboard.html', {
        # 'user' = request.user.username
    })

def login(request):
	return render(request, 'dashboard/login.html', {})

def signup(request):
	if request.method == 'POST':	
		# form = AccountForm()	

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password_confirmation = request.POST.get('password_confirmation')

		new_user = User.objects.create_user(username=username, email=email, password=password1)
		new_user.save()
			
		return HttpResponseRedirect('/login/')
	else:
		form = AccountForm()

	return render(request, 'accounts/signup.html', {})

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
def arrival_list(request, template_name='arrival/arrival_list.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)


@login_required
def arrivals(request):
	alist = AddArrival.objects.all()
	a_len = len(a_list)
	return render(request, 'arrival/arrival_list.html', {
		'arrival_list': a_list,
		'a_len': a_len
	})

@login_required
def arrival_create(request, template_name='arrival/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('arrival_list')
    return render(request, template_name, {'form':form})


@login_required
def arrival_update(request, arrival_id):
	if request.method == 'POST':
		arrival = AddArrival.objects.get(pk=arrival_id)
		arrival.itemName = request.POST.get('itemName')
		arrival.qty = request.POST.get('qty')
		arrival.itemCost = request.POST.get('itemCost')
		arrival.save()
		return redirect('arrival_list')
# def arrival_update(request, pk, template_name='arrival/arrival_form.html'):
#     arrival = get_object_or_404(AddArrival, pk=pk)
#     form = ArrivalForm(request.POST or None, instance=arrival)
#     if form.is_valid():
#         form.save()
#         return redirect('arrival_list')
#     return render(request, template_name, {'form':form})

@login_required
def arrival_delete(request, arrival_id):
	a = AddArrival.objects.get(pk=arrival_id)
	a.delete()
	return HttpResponseRedirect(reverse('arrival_list'))


@login_required
def inventory_reports(request):
	filterby = request.GET.get('filter')
	# Create dummy data for the items
	items = [{ 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }, { 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }]
	return render(request, 'reports/inventory_reports.html', {
		'filterby': filterby,
		'items': items, 
	})

@login_required
def sales_reports(request):
	return render(request, 'reports/sales_reports.html', {})
def login(request):
	return render(request, 'dashboard/login.html', {})


def create_transfer(request,template_name ='transfer/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		d = form.cleaned_data['item']
		q_transfer = form.cleaned_data['quantity_to_transfer']
		w_qty = d.warehouse_quantity
		if  q_transfer > w_qty:
			raise forms.ValidationError("Quantity exceed the current quantity of the Item in the Warehouse")
		else:
			current_w = w_qty - q_transfer
			current_s = d.store_quantity + q_transfer
			d.warehouse_quantity = current_w
			d.store_quantity = current_s
			d.save()
		form.save()
		return redirect('transfer_hist')
	return render(request,template_name,{'form':form})

def transfer_hist(request,template_name = 'transfer/transfer_hist.html'):
	transfer = Transfer_item.objects.all()
	data = {}
	data['object_list'] = transfer
	return render(request,template_name,data)


def transfer_delete(request, transfer_id):
	t_item = Transfer_item.objects.filter(pk=transfer_id)
	t_item.delete()
	return HttpResponseRedirect(reverse('transfer_hist'))

@login_required
def items(request):
	items_list = Item.objects.all()
	itemLen = len(items_list)
	return render(request, 'items/items.html', {
		'items': items_list,
		'itemLen': itemLen
		})

def items_list(request):
	items = Item.objects.all()
	return HttpResponse({items})

@login_required
def add_item(request):
	form = AddItemForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'items/add_item.html', {'form':form})

def delete_item(request, item_id):
	item = Item.objects.get(pk = item_id)
	item.delete()
	return HttpResponseRedirect(reverse('items'))

def update_item(request, item_id):
	if request.method == 'POST':
		item = Item.objects.get(pk = item_id)
		item.types = request.POST.get('types')
		item.category = request.POST.get('category')
		item.brand = request.POST.get('brand')
		item.model = request.POST.get('model')
		item.supplier.name = request.POST.get('supplier')
		item.supplier_code = request.POST.get('supplier_code')
		item.store_code = request.POST.get('store_code')
		item.store_quantity= request.POST.get('store_qty')
		item.warehouse_quantity= request.POST.get('warehouse_quantity')
		item.unit_cost= request.POST.get('unit_cost')
		item.srp = request.POST.get('srp')
		item.save()
	return HttpResponseRedirect(reverse('items'))


@login_required
def sales(request):
	sales_list= Sale.objects.all()
	salesLen = len(sales_list)
	return render(request, 'sales/sales.html', {
		'sales_list':sales_list,
		'salesLen' : salesLen
		})

def add_sale(request):
	form = AddSaleForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('sales')
	return render(request, 'sales/add_sale.html', {'form':form})

def delete_sale(request, sale_id):
	sale = Sale.objects.get(pk = sale_id)
	sale.delete()
	return HttpResponseRedirect(reverse('sales'))

def update_sale(request, sale_id):
	if request.method == 'POST':
		sale = Sale.objects.get(pk = sale_id)
		sale.item.store_code = request.POST.get('item')
		sale.quantity =  request.POST.get('quantity')
		sale.date = request.POST.get('date')
		sale.save()
	return HttpResponseRedirect(reverse('sales')) 		

def suppliers(request):
	s_list = Supplier.objects.all()
	s_len = len(s_list)
	return render(request, 'supplier/suppliers.html', {
		'suppliers': s_list,
		's_len': s_len
	})

def list_suppliers(request):
	ls = Supplier.objects.all()
	return HttpResponse({ls})

def add_supplier(request):
	form = AddSupplierForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('suppliers')
	return render(request, 'supplier/add_supplier.html', {'form':form})

def update_supplier(request, supplier_id):
	if request.method == 'POST':
		supplier = Supplier.objects.get(pk=supplier_id)
		supplier.name = request.POST.get('name')
		supplier.phone = request.POST.get('phone')
		supplier.address = request.POST.get('address')
		supplier.save()

	return HttpResponseRedirect(reverse('suppliers'))
	
def delete_supplier(request, supplier_id):
	s = Supplier.objects.get(pk=supplier_id)
	s.delete()
	return HttpResponseRedirect(reverse('suppliers'))


# def arrivals(request):
# 	a_list = AddArrival.objects.all()
# 	a_len = len(a_list)
# 	return render(request, 'arrival/arrivals.html', {
# 		'arrivals': a_list,
# 		'a_len': a_len
# 	})

# def list_arrivals(request):
# 	ls = AddArrival.objects.all()
# 	return HttpResponse({ls})

# def add_arrival(request):
# 	form = ArrivalForm(request.POST or None)
# 	if  form.is_valid():
# 		form.save()
# 		return redirect('arrivals')
# 	return render(request, 'arrival/add_arrival.html', {'form':form})

# def delete_arrival(request, arrival_id):
# 	a = AddArrival.objects.get(pk=arrival_id)
# 	a.delete()
# 	return HttpResponseRedirect(reverse('arrivals'))
