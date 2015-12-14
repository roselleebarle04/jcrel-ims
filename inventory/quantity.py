
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

import datetime

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

def check_if_exists():
		itemloc = ItemLocation.objects.all()
		item = Item.objects.all()
		sale = Sale.objects.all()
		transfer = Transfer.objects.all()

		for i in itemloc:
			if i.current_stock < i.re_order_point:
				if Notifications.objects.filter(item_loc=i).exists():
					for s in sale:
						if Notifications.objects.filter(below_min_date=s.date).exists():
							return True
						else: 
							return False

def check_item_exists():
	itemloc = ItemLocation.objects.all()

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			return i

def check_date_exists():
	sale = Sale.objects.all()

	for s in sale:
		return s.date

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

	# print check_item_exists()
	print check_date_exists()
	print get_notif_dates()
	# print Notifications.objects.filter(item_loc=check_item_exists()).exists()
	# print Notifications.objects.filter(below_min_date=check_date_exists()).exists()
	# print Notifications.objects.filter(item_loc=check_item_exists(), below_min_date=check_date_exists()).exists()

	for i in itemloc:
		if i.current_stock < i.re_order_point:
			if Notifications.objects.filter(item_loc=check_item_exists(), below_min_date=check_date_exists()).exists():
				print "Wow"
				continue
			else:
				print "Why"
				message = "%s is below the minimum required quantity stored." % (i)
				notifs = Notifications.objects.create(item_loc=i, message=message)
				notifs.save()

	# for i in itemloc:
	# 	print Notifications.objects.filter(item_loc=i).exists()
	# 	if i.current_stock < i.re_order_point:
	# 		if Notifications.objects.filter(item_loc=i).exists():
	# 			continue
	# 		else:
	# 			message = "%s is below the minimum required quantity stored." % (i)
	# 			notifs = Notifications.objects.create(item_loc=i, message=message)
	# 			notifs.save()

	# for i in itemloc:
	# 	for s in sale:
	# 		print Notifications.objects.filter(item_loc=i).exists()
	# 		print Notifications.objects.filter(below_min_date=s.date).exists()
	# 		if i.current_stock < i.re_order_point:
	# 			print Notifications.objects.filter(item_loc=i).exists()
	# 			print Notifications.objects.filter(below_min_date=s.date).exists()		
	# 			if Notifications.objects.filter(item_loc=i).exists() and Notifications.objects.filter(below_min_date=s.date).exists():
	# 				print "True"
	# 				continue
	# 			else:
	# 				print "None"
	# 				message = "%s is below the minimum required quantity stored." % (i)
	# 				notifs = Notifications.objects.create(item_loc=i, message=message)
	# 				notifs.save()
