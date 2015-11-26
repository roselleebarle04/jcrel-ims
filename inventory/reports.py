from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json

from .models import *


def reports_data(request):
	if request.method == 'POST' and request.is_ajax():
		response_data={}
		response_data['title']='NO'
		response_data['message']='NO'
		return HttpResponse(json.dumps(response_data),content_type="application/json")
	return HttpResponse({})

@login_required
def inventory_reports(request):
	items_list = Item.objects.all()
	supplier_list = Supplier.objects.all()

	# To be rendered in filter form
	item_options = Item.objects.all() 

	if request.method == 'POST':
		item_pk = request.POST.get('item')
		items_list = Item.objects.filter(pk=item_pk)
		
	itemsLen = len(items_list)
	return render(request, 'reports/inventory_reports.html', {
		'items':items_list,
		'item_options': item_options,
		'items_length': itemsLen,
	})

@login_required
def sales_reports(request):
	items_list = Item.objects.all()
	return render(request, 'reports/sales_reports.html', {'items':items_list})
