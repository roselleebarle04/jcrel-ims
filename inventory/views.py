from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm

from .models import *
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    print request.user.username
    return render(request, 'dashboard/dashboard.html', {
        # 'user' = request.user.username
    })

def login(request):
	return render(request, 'dashboard/login.html', {})

def reset(request):
    # Wrap the built-in password reset view and pass it the arguments
    # like the template name, email template name, subject template name
    # and the url to redirect after the password reset is initiated.
    return password_reset(request, template_name='accounts/reset.html',
        email_template_name='accounts/reset_email.html',
        subject_template_name='accounts/reset_subject.txt',
        post_reset_redirect=reverse('success'))
    
# This view handles password reset confirmation links. See urls.py file for the mapping.
# This view is not used here because the password reset emails with confirmation links
# cannot be sent from this application.
def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='accounts/reset_confirm.html',
        uidb36=uidb36, token=token, post_reset_redirect=reverse('success'))

# This view renders a page with success message.
def success(request):
  return render(request, "accounts/success.html")


def signup(request):
	if request.method == 'POST':		

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password_confirmation = request.POST.get('password_confirmation')

		new_user = User.objects.create_user(username=username, email=email, password=password1)
		new_user.save()
			
		return HttpResponseRedirect('/login/')
	else:
		form = AccountForm()

	return render(request, 'accounts/signup.html', {})

@login_required
def add_arrival(request, template_name='arrival/add_arrival.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)

@login_required
def arrival_create(request, template_name='arrival/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

@login_required
def arrival_update(request, pk, template_name='arrival/arrival_form.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)
    form = ArrivalForm(request.POST or None, instance=arrival)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

@login_required
def arrival_delete(request, pk, template_name='arrival/arrival_confirm_delete.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)    
    if request.method=='POST':
        arrival.delete()
        return redirect('add_arrival')
    return render(request, template_name, {'object':arrival})

@login_required
def inventory_reports(request):
	filterby = request.GET.get('filter')
	# Create dummy data for the items
	items = [{ 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }, { 'name': 'Fernando', 'location': 'Store', 'supplier_code': 'ABD-DFS', 'qty': '5' }]
	return render(request, 'dashboard/inventory_reports.html', {
		'filterby': filterby,
		'items': items,
	})

@login_required
def sales_reports(request):
	return render(request, 'dashboard/sales_reports.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

def add_arrival(request):
	return render(request, 'arrival/add_arrival.html', {})

def create_transfer(request,template_name ='dashboard/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_form')
	return render(request,template_name,{'form':form})

def transfer_hist(request,template_name = 'transfer/transfer_hist.html'):
	transfer = Transfer_item.objects.all()
	data = {}
	data['object_list'] = transfer
	return render(request,template_name,data)

@login_required
def items(request):
	items = Item.objects.all()
	list_item = {}
	list_item['items'] = items
	return render(request, 'items/items.html', list_item)

@login_required
def add_item(request):
	form = AddItemForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('items')
	return render(request, 'items/add_item.html', {'form':form})

@login_required
def sales(request):
	sales = Sale.objects.all()
	data = {}
	data['sales'] = sales
	return render(request, 'sales/sales.html', data)

def add_sale(request):
	form = AddSaleForm(request.POST or None)
	if  form.is_valid():
		form.save()
		return redirect('sales')
	return render(request, 'sales/add_sale.html', {'form':form})
