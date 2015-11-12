from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

# def signup(request):
	

def login(request):
	return render(request, 'dashboard/login.html', {})