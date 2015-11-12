from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

<<<<<<< HEAD
# def signup(request):
	
=======
def add_arrival(request):
	return render(request, 'dashboard/add_arrival.html', {})
>>>>>>> 6ce6f04972a3a0e83c7007bc35322ea1d817165f

def login(request):
	return render(request, 'dashboard/login.html', {})
