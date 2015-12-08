
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
from django.db import IntegrityError, transaction, models
from django.core import validators

from config import settings
from .models import *
from .forms import *
from .formsets import *

def check_minimum():
	items = ItemLocation.objects.all()
	is_zero = 0
	below_min = is_zero

	for i in items:
		if i.current_stock < i.re_order_point:
			below_min = below_min + 1

	return below_min