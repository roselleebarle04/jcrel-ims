
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
from django.views.decorators.http import *

from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction, models
from django.core import validators

from django.utils import timezone

from config import settings
from .models import *
from .forms import *
from .formsets import *

def check_minimum():
	itemloc = ItemLocation.objects.all()
	is_zero = 0
	below_min = is_zero

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			below_min = below_min + 1

	return below_min

def check_item_exists():
	itemloc = ItemLocation.objects.all()

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			return i

def check_date_exists():
	sale = Sale.objects.all().order_by('-date')

	for s in sale:
		return s.date

def check_date_transfer():
	transfer = Transfer.objects.all().order_by('-date')

	for t in transfer:
		return t.date

def get_notif_dates():
	notif = Notifications.objects.all()

	for n in notif:
		return n.below_min_date


def save_minimums():
	itemloc = ItemLocation.objects.all()
	item = Item.objects.all()
	sale = Sale.objects.all()
	transfer = Transfer.objects.all()
	notif = Notifications.objects.all()
	is_zero = 0
	below_min = is_zero

	date = datetime.datetime.now().date()

	print check_item_exists()
	print check_date_exists()
	print get_notif_dates()
	print date

	for i in itemloc:
		print Notifications.objects.filter(item_loc=i).exists()
		if i.current_stock < i.re_order_point:
			if Notifications.objects.filter(item_loc=i).exists():
				continue
			else:
				message = "%s is below the minimum required quantity stored." % (i)
				notifs = Notifications.objects.create(item_loc=i, message=message, below_min_date=date)
				notifs.save()

def sales_save_minimums():
	itemloc = ItemLocation.objects.all()
	item = Item.objects.all()
	sale = Sale.objects.all()
	transfer = Transfer.objects.all()
	notif = Notifications.objects.all()

	date = datetime.datetime.now().date()

	# print check_date_exists()

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			if Notifications.objects.filter(item_loc=i, below_min_date=check_date_exists).exists():
				continue
			# elif Notifications.objects.filter(item_loc=i, below_min_date=None).exists():
			# 	continue
			else:
				message = "%s is below the minimum required quantity stored." % (i)
				notifs = Notifications.objects.create(item_loc=i, message=message, below_min_date=check_date_exists())
				notifs.save()

def transfer_save_minimums():
	itemloc = ItemLocation.objects.all()
	item = Item.objects.all()
	sale = Sale.objects.all()
	transfer = Transfer.objects.all()
	notif = Notifications.objects.all()

	date = datetime.datetime.now().date()

	# print check_date_exists()

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			if Notifications.objects.filter(item_loc=i, below_min_date=check_date_transfer).exists():
				continue
			# elif Notifications.objects.filter(item_loc=i, below_min_date=None).exists():
			# 	continue
			else:
				message = "%s is below the minimum required quantity stored." % (i)
				notifs = Notifications.objects.create(item_loc=i, message=message, below_min_date=check_date_transfer())
				notifs.save()
