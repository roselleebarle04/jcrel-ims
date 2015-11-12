from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Item, Supplier, Category, Brand, ItemModel
from .forms import *


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

def add_arrival(request):
	return render(request, 'arrival_templates/add_arrival.html', {})
	return render(request, 'dashboard/add_arrival.html', {})

def login(request):
	return render(request, 'dashboard/login.html', {})

def transfer_form(request,template_name ='dashboard/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_form')
	return render(request,template_name,{'form':form})