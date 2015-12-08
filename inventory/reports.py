from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

from .models import *
from .quantity import *

def reports_data(request):
	if request.method == 'POST' and request.is_ajax():
		items = Item.objects.all()
		# response_data={}
		# response_data['title']='NO'
		# response_data['message']='NO'
		data = serializers.serialize("json", Item.objects.all())
		return HttpResponse(json.dumps(data),content_type="application/json")
	return HttpResponse({})

@login_required
def inventory_reports(request):
	items_list = Item.objects.all()
	supplier_list = Supplier.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

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
		'below_min':below_min
	})

@login_required
def sales_reports(request):
	items_list = Item.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min

	return render(request, 'reports/sales_reports.html', {'items':items_list, 'below_min':below_min})
