from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

def add_arrival(request):
	return render(request, 'arrival_templates/add_arrival.html', {})

def login(request):
	return render(request, 'dashboard/login.html', {})
