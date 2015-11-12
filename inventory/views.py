from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

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

def add_arrival(request):
	return render(request, 'dashboard/add_arrival.html', {})

def login(request):
	return render(request, 'dashboard/login.html', {})
