from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm

from config import settings
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

def change_password(request):
	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {})

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

@login_required
def arrival_list(request, template_name='arrival/arrival_list.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)

@login_required
def arrival_create(request, template_name='arrival/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('arrival_list')
    return render(request, template_name, {'form':form})

@login_required
def arrival_update(request, pk, template_name='arrival/arrival_form.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)
    form = ArrivalForm(request.POST or None, instance=arrival)
    if form.is_valid():
        form.save()
        return redirect('arrival_list')
    return render(request, template_name, {'form':form})

@login_required
def arrival_delete(request, pk, template_name='arrival/arrival_confirm_delete.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)    
    if request.method=='POST':
        arrival.delete()
        return redirect('arrival_list')
    return render(request, template_name, {'objects':arrival})

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

def add_arrival(request):
	return render(request, 'arrival/add_arrival.html', {})

def create_transfer(request,template_name ='transfer/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_hist')
	return render(request,template_name,{'form':form})

def transfer_hist(request,template_name = 'transfer/transfer_hist.html'):
	transfer = Transfer_item.objects.all()
	data = {}
	data['object_list'] = transfer
	return render(request,template_name,data)


def transfer_delete(request,pk, template_name= 'transfer/transfer_confirm_delete.html'):
	transfer = get_object_or_404(Transfer_item, pk=pk)
	if request.method == 'POST':
		transfer.delete()
		return redirect('transfer_hist')
	return render(request, template_name, {'object':transfer})

@login_required
def items(request):
	items = Item.objects.all()
	list_item = {}
	list_item['items'] = items
	return render(request, 'items/items.html', list_item)

@login_required
def add_item(request):
	form = AddItemForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'items/add_item.html', {'form':form})

@login_required
def sales(request):
	sales = Sale.objects.all()
	data = {}
	data['sales'] = sales
	return render(request, 'sales/sales.html', data)

def add_sale(request):
	form = AddSaleForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('sales')
	return render(request, 'sales/add_sale.html', {'form':form})

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

