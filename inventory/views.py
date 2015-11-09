from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, Supplier, Category, Brand, ItemModel


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})




