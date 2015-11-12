from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

<<<<<<< HEAD
def add_arrival(request):
	return render(request, 'dashboard/add_arrival.html', {})
=======
def login(request):
	return render(request, 'dashboard/login.html', {})
>>>>>>> 1e19ddfa3d1634f334f07d53f068b12d6c2009ba
