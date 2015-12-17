import datetime
from django.core.urlresolvers import reverse
# from django.core.exceptions import DoesNotExist
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

from .models import *
from .quantity import *

def build_items_per_location(location):
	out = []
	items = Item.objects.all()
	for item in items:
		try: 
			i = item.itemlocation_set.get(location=location)
			out.append(i)
		except:
			pass
	return out

def build_sales_data(request):
	""" Build Sales Reports """
	"""
	[{item: item, item_code: item_code, date: date, revenue: revenue, gross_profit: gross_profit}]
	"""
	out = []
	items = Item.objects.all()

	# Now calculate sales per item
	for item in items:
		sales = ItemSale.objects.filter(item=item)
		
		revenue = 0
		gross_profit_php = 0
		gross_profit_per = 0
		total_quantity_sold = 0

		for sale in sales:
			revenue = revenue + (sale.quantity * sale.item.unit_cost)
			total_quantity_sold = total_quantity_sold + sale.quantity
			print total_quantity_sold

		entry = {}
		entry['item_name'] = item.category + ' ' + item.brand + ' ' + item.model
		entry['total_quantity_sold'] = total_quantity_sold
		entry['unit_cost'] = item.unit_cost
		entry['revenue'] = revenue
		entry['gross_profit_php'] = gross_profit_php
		entry['gross_profit_per'] = gross_profit_per
		out.append(entry)
	return out

def build_data(request):
	"""Build inventory reports"""
	"""
	[{
		location: 'location1',
		item: [{name: name, item_code: code, date_created: date, current_stock: 15, ...}]
	}]
	"""
	out = []

	locations = Location.objects.all()
	for location in locations:
		"""Build item list for each location"""
		entry = {}

		entry['location'] = location.name
		entry['items'] = []
		print location
		items_in_location = build_items_per_location(location)
		for i in items_in_location:
			a = {}
			a['item_name'] = i.item
			a['item_code'] = i.item.item_code
			a['date_created'] = i.item.date
			a['current_stock'] = i.current_stock
			a['stock_value'] = i.current_stock * i.item.unit_cost
			a['unit_cost'] = i.item.unit_cost
			a['reorder_point'] = i.re_order_point
			a['reorder_amount'] = i.re_order_amount
			entry['items'].append(a)
		out.append(entry)
	print out
	return out

def charts(request):
	return render(request, 'reports/charts.html', {})

@login_required
def reports_data(request):
	if request.method == 'POST' and request.is_ajax():
		items = Item.objects.all()
		data = serializers.serialize("json", Item.objects.all())
		return HttpResponse(json.dumps(data),content_type="application/json")
	return HttpResponse({})

@login_required
def inventory_reports(request):
	below_min = check_minimum()

	data = build_data(request)
	total_current_stock = Item.get_total_current_stock
	total_stock_value = Item.get_total_stock_value

	summary = { 
		'total_current_stock': total_current_stock, 
		'total_stock_value': total_stock_value
	}

	return render(request, 'reports/inventory_reports.html', {
		'data': data,
		'summary': summary,
	})

@login_required
def sales_reports(request):
	below_min = check_minimum()

	data = build_sales_data(request)
	return render(request, 'reports/sales_reports.html', {
		'data': data, 
	})
