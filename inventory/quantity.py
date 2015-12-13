
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
from datetime import date

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
			# message = "%s is below the minimum required quantity stored." % (i)
			below_min = below_min + 1
			# notifs = Notifications.objects.create(item_loc=i, message=message)
			# notifs.save()

	return below_min


def save_minimums():
	itemloc = ItemLocation.objects.all()
	is_zero = 0
	below_min = is_zero

	notif = Notifications.objects.all()

	for i in itemloc:
		print "i is %s" % i
		print i
		print notif
		print i.item
		if i.current_stock < i.re_order_point:
			if Notifications.objects.filter(item_loc=i).exists():
				print "True"
				continue
			else:
				print "False"
				message = "%s is below the minimum required quantity stored." % (i)
				notifs = Notifications.objects.create(item_loc=i, message=message)
				notifs.save()
