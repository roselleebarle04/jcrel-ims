from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import *


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
