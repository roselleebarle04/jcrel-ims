from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from .models import Item, Supplier, Category, Brand, ItemModel, AddArrival


def add_arrival(request, template_name='arrival_templates/add_arrival.html'):
    arrivals = AddArrival.objects.all()
    data = {}
    data['object_list'] = arrivals
    return render(request, template_name, data)

<<<<<<< HEAD
def arrival_create(request, template_name='arrival_templates/arrival_form.html'):
    form = ArrivalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

def arrival_update(request, pk, template_name='arrival_templates/arrival_form.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)
    form = ArrivalForm(request.POST or None, instance=arrival)
    if form.is_valid():
        form.save()
        return redirect('add_arrival')
    return render(request, template_name, {'form':form})

def arrival_delete(request, pk, template_name='arrival_templates/arrival_confirm_delete.html'):
    arrival = get_object_or_404(AddArrival, pk=pk)    
    if request.method=='POST':
        arrival.delete()
        return redirect('add_arrival')
    return render(request, template_name, {'object':arrival})
=======
from .models import Item, Supplier, Category, Brand, ItemModel
from .forms import *
>>>>>>> efdba7f6c78b42bb77fe83ed40151ef10e501a50


def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})

def reports(request):
	return render(request, 'dashboard/reports.html', {})

<<<<<<< HEAD
# def signup(request):

=======
def add_arrival(request):
	return render(request, 'arrival_templates/add_arrival.html', {})
	return render(request, 'dashboard/add_arrival.html', {})
>>>>>>> efdba7f6c78b42bb77fe83ed40151ef10e501a50

def login(request):
	return render(request, 'dashboard/login.html', {})

<<<<<<< HEAD
=======
def transfer_form(request,template_name ='dashboard/transfer_form.html'):
	form = TransferForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('transfer_form')
	return render(request,template_name,{'form':form})
>>>>>>> efdba7f6c78b42bb77fe83ed40151ef10e501a50
