from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
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

from threading import Thread

from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.core import validators


from config import settings
from .models import *
from .forms import *
from .formsets import *
from .quantity import *


def signup(request):
	if request.method == 'POST':	
		form = UserCreationForm(request.POST or None)

		if form.is_valid():
			username = request.POST.get("username")
			email = request.POST.get("email")
			password1 = request.POST.get("password1")
			password2 = request.POST.get("password2")

			# form = User.objects.create_user(username, email, password1)
			# # form.save()
			# new_user = form.save(commit=False)
			# new_user.save()

			
			new_user = User.objects.create_user(username, email, password1)
			new_user.save()

			avatar = request.FILES.get("avatar")

			# We need to create an account for the user created.
			new_account = Account(user=new_user, avatar=avatar)
			new_account.save()


			return HttpResponseRedirect('/login/')
	else:
		# form = AccountForm()
		form = UserCreationForm()

	return render(request, 'accounts/signup.html', {'form':form})

def change_password(request):
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()
	# items = AddItem.objects.all()
	

	below_min = check_minimum()
	print "below_min %d" % below_min

	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {
		'all_items':items_list,
		'itemloc':itemloc,
		'below_min':below_min
		})

@login_required
def notifications(request):
	items_list = Item.objects.all()
	itemLength = len(items_list)
	itemloc = ItemLocation.objects.all()
	itemLength = len(itemloc)
	notifs = Notifications.objects.all().order_by('-below_min_date')

	# print datetime.datetime.now().date()
	# save_minimums()

	below_min = check_minimum()
	# print "below_min %d" % below_min
	# print "notifs %s" % notifs
	# print "items %s" % itemloc

	return render(request, 'notifications/notification_page.html', {
		'itemloc':itemloc,
		'itemLength': itemLength,
		'below_min':below_min,
		'notifs':notifs
		})



def settings(request):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min
	

	try:
		account = Account.objects.filter(user=request.user.id)[0]
	except:
		account = ''

	return render(request, 'settings/settings.html', {
		'account':account,
		'itemloc':itemloc,
		'all_items':items_list,
		'below_min':below_min
		})

def update_settings(request):
	# If the account is already created for the user, just update the avatar, 
	# but not that the original user might not hava an account, yet - TODO

	items_list = Item.objects.all()
	itemloc = ItemLocation.objects.all()
	# items = AddItem.objects.all()
	below_min = check_minimum()
	print "below_min %d" % below_min

	user = request.user
	try:
		account = Account.objects.filter(user=user.id)[0]
	except: 
		account = ''
	if request.method == 'POST':
		new_avatar = request.FILES.get('avatar', '')
		new_password = request.POST.get('new_password')
		if account:
			if not new_avatar == '':
				account.avatar = new_avatar
				account.save()
		# else:
		# 	new_account = Account(user=user, avatar=new_avatar)
		# 	new_account.save()
		user.set_password(new_password)
		user.save()
		update_session_auth_hash(request, request.user)
		return HttpResponseRedirect(reverse('settings'))

	return render(request, 'settings/update_settings.html', {
		'account': account,
		'all_items':items_list,
		'below_min':below_min,
		'itemloc':itemloc
		})
