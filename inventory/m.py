def sale(request):
	saleForm = AddSaleForm(request.POST or None)
	formset = formset_factory(AddSoldItemForm, formset=AddArrivedItemFormset, extra = 1)
	formset = formset_factory(AddSoldItemForm, formset=AddArrivedItemFormset, extra=3)
	saleFormset = formset(request.POST or None)

	if saleForm.is_valid() and saleFormset.is_valid():
		# first save purchase details
		# commit = False means that we can store the purchase instance to the value p
		p = saleForm.save(commit=False)

		#save the form
		p.save()
		sale_id = p
		new_items = []

		# loop through all forms in the formset, and save each form - add the purchaseId to each form
		for form in saleFormset:
			item = form.cleaned_data.get('item')
			sale = sale_id
			quantity = form.cleaned_data.get('quantity')
			item_cost = form.cleaned_data.get('item_cost')
			new_item = ArrivedItem(item=item, sale=p, quantity=quantity, item_cost=item_cost)	
			new_item.save()
		
		return HttpResponseRedirect(reverse('sale'))

	return render(request, 'sale/sale.html', {
		'AddsaleForm' : saleForm, 
		'formset' : saleFormset, 
		})