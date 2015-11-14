from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Item, Supplier, Category, Brand, ItemModel, AddArrival
from .forms import *
from django.core.urlresolvers import reverse


# Dashboard
def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

# Accounts
def login(request):
	return render(request, 'dashboard/login.html', {})

# Accounts
def signup(request):

	if request.method == 'POST':		

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password_confirmation = request.POST.get('password_confirmation')

		print "%s %s %s %s" % (first_name, last_name, username, password1)

		new_user = User.objects.create_user(username=username, email=email, password=password1)
		new_user.set_password('password1')
		new_user.save()
			
		return HttpResponseRedirect('/login/')
	else:
		form = AccountForm()

	return render(request, 'dashboard/signup.html', {})

# Arrivals
def add_arrival(request, template_name='arrival_templates/add_arrival.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)

def arrival_create(request, template_name='arrival_templates/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

def arrival_update(request, pk, template_name='arrival_templates/arrival_form.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)
    form = ArrivalForm(request.POST or None, instance=arrival)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

def arrival_delete(request, pk, template_name='arrival_templates/arrival_confirm_delete.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)    
    if request.method=='POST':
        arrival.delete()
        return redirect('add_arrival')
    return render(request, template_name, {'object':arrival})

# Reports
def inventory_reports(request):
	filterby = request.GET.get('filter')
	# Create dummy data for the items
	items = [{ 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }, { 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }]
	return render(request, 'dashboard/inventory_reports.html', {
		'filterby': filterby,
		'items': items,
	})

def sales_reports(request):
	return render(request, 'dashboard/sales_reports.html', {})

# Items
def items(request):
	return render(request, 'dashboard/items.html', {})

def add_item(request):
	form = ItemForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'dashboard/add_item.html', {'form':form})
	
def reports(request):
	return render(request, 'dashboard/reports.html', {})

def add_arrival(request):
	return render(request, 'arrival_templates/add_arrival.html', {})

def login(request):
	return render(request, 'dashboard/login.html', {})

# Transfers
def create_transfer(request,template_name ='transfer/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_form')
	return render(request,template_name,{'form':form})

def transfer_hist(request,template_name = 'transfer/transfer_hist.html'):
	transfer = Transfer_item.objects.all()
	data = {}
	data['object_list'] = transfer
	return render(request,template_name,data)
