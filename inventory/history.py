from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
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
from django.db import IntegrityError, transaction
from django.core import validators

from config import settings
from .models import *
from .forms import *
from .quantity import *
from .formsets import *


@login_required
def transfer_history(request):
	transfers = TransferRecord.objects.all()
	transferLen = len(transfers)

	return render(request, 'transfer/transfer_history.html', {
		'transfers': transfers,
		'transferLen': transferLen,
	})

def sales_history(request):
	items = ItemLocation.objects.all()
	sales_list = ItemSale.objects.filter(is_active=True)
	salesLen = len(sales_list)
	items_list = Item.objects.all()

	# for i in items:
	# 	below_min = 0
	# 	if i.quantity < 10:
	# 		below_min = below_min + 1
	# 		print "below_min %d" % (below_min)

	return render(request, 'sales/sales_history.html', {
		'sales_list':sales_list,
		'salesLen' : salesLen,
		'items':items,
		'all_items':items_list,
		# 'below_min': below_min
		})

def arrival_history(request):
	items =ItemLocation.objects.all()
	arr = Arrival.objects.all()
	arrivalLen = len(arr)
	suppliers = Supplier.objects.all()
	items_list = Item.objects.all()

	if request.method == 'POST': 
		date_from = request.POST.get('from') 
		date_to = request.POST.get('to')
		supplier = request.POST.get('supplier')

		filtered_arr = Arrival.apply_filter(date_from, date_to, supplier)
		
		arrivalLen = len(filtered_arr)
		return render(request, 'arrival/arrival_history.html', {
			'arrival': filtered_arr,
			'arrivalLen': arrivalLen,
			'suppliers': suppliers,
			'items':items,
			'all_items':items_list,
		})

	return render(request, 'arrival/arrival_history.html', {
		'arrival': arr,
		'arrivalLen': arrivalLen,
		'suppliers' : suppliers,
		'items':items,
		'all_items':items_list,
	})