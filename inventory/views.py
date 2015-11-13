from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import Item, Supplier, Category, Brand, ItemModel, AddArrival
from .forms import *


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username,email_address,password)
        new_user.save()

        return HttpResponseRedirect('/login/')
    return render(request, 'accounts/signup.html', {})

@login_required
def dashboard(request):
    print request.user.username
    return render(request, 'dashboard/dashboard.html', {
        # 'user' = request.user.username
    })

@login_required
def add_arrival(request, template_name='arrival_templates/add_arrival.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)

@login_required
def arrival_create(request, template_name='arrival_templates/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

@login_required
def arrival_update(request, pk, template_name='arrival_templates/arrival_form.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)
    form = ArrivalForm(request.POST or None, instance=arrival)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

@login_required
def arrival_delete(request, pk, template_name='arrival_templates/arrival_confirm_delete.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)    
    if request.method=='POST':
        arrival.delete()
        return redirect('add_arrival')
    return render(request, template_name, {'object':arrival})

@login_required
def inventory_reports(request):
	filterby = request.GET.get('filter')
	# Create dummy data for the items
	items = [{ 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }, { 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }]
	return render(request, 'dashboard/inventory_reports.html', {
		'filterby': filterby,
		'items': items,
	})

@login_required
def sales_reports(request):
	return render(request, 'dashboard/sales_reports.html', {})

@login_required
def items(request):
	return render(request, 'dashboard/items.html', {})

@login_required
def transfer_form(request,template_name ='dashboard/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_form')
	return render(request,template_name,{'form':form})

