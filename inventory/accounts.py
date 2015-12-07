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
from .formsets import *

def check_minimum():
	items = ItemLocation.objects.all()
	is_zero = 0
	below_min = is_zero

	for i in items:
		if i.current_stock < i.re_order_point:
			below_min = below_min + 1

	return below_min


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
	# items = AddItem.objects.all()
	

	for i in items_list:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	if request.method == 'POST':

		username = request.POST.get('username')
		new_password = request.POST.get('new_password')

		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()

		return HttpResponseRedirect('/login/')

	return render(request, 'accounts/change_password.html', {
		'all_items':items_list,
		# 'items':items,
		# 'below_min':below_min
		})

@login_required
def notifications(request):
	items_list = Item.objects.all()
	itemLength = len(items_list)
	items = ItemLocation.objects.all()
	itemLength = len(items)

	for i in items:
		below_min = 0
		if i.quantity < 10:
			below_min = below_min + 1
			print "below_min %d" % (below_min)

	return render(request, 'notifications/notification_page.html', {
		'items':items,
		'itemLength': itemLength,
		})



def settings(request):
	# items = AddItem.objects.all()
	items_list = Item.objects.all()

	below_min = check_minimum()
	print "below_min %d" % below_min
	

	try:
		account = Account.objects.filter(user=request.user.id)[0]
	except:
		account = ''

	return render(request, 'settings/settings.html', {
		'account':account,
		# 'items':items,
		'all_items':items_list,
		'below_min':below_min
		})

def update_settings(request):
	# If the account is already created for the user, just update the avatar, 
	# but not that the original user might not hava an account, yet - TODO

	items_list = Item.objects.all()
	# items = AddItem.objects.all()
	below_min = check_minimum()
	print "below_min %d" % below_min

	user = request.user
	try:
		account = Account.objects.filter(user=user.id)[0]
	except: 
		account = ''
	if request.method == 'POST':
		new_avatar = request.FILES.get('avatar')
		
		if account:
			account.avatar = new_avatar
			account.save()
		else:
			new_account = Account(user=user, avatar=new_avatar)
			new_account.save()
		return HttpResponseRedirect(reverse('settings'))

	return render(request, 'settings/update_settings.html', {
		'account': account,
		'all_items':items_list,
		'below_min':below_min,
		# 'items':items
		})
