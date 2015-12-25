dynamic-formset.js (https://gist.github.com/jteso/2130643)
function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('.dynamic-form:first').clone(true).get(0);
    $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
    $(row).children().not(':last').children().each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
    });
    $(row).find('.delete-row').click(function() {
        deleteForm(this, prefix);
    });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix) {
    var forms = $('.dynamic-form');
    if (!(forms.length <= 1))
        $(btn).parents('.dynamic-form').remove();
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i=0, formCount=forms.length; i<formCount; i++) {
        $(forms.get(i)).children().not(':last').children().each(function() {
            updateElementIndex(this, prefix, i);
        });
    }
    return false;
}

HOWTO
1. Declare Your Models
models.py
lass Arrival(models.Model):
	"""	This model refers to the arrival of the store owner from its suppliers """
	date = models.DateField(default=timezone.now)
	delivery_receipt_no = models.CharField(max_length=100, null=True, blank=True)
	tracking_no = models.CharField(max_length=100, null=True, blank=True)
	items = models.ManyToManyField(Item, through='ArrivedItem')
	supplier = models.ForeignKey(Supplier)

	def __unicode__(self):
		return self.tracking_no

def items_list(self):
	return ', '.join([a.item for i in self.items.all()])

class ArrivedItem(models.Model):
	item = models.ForeignKey(Item)
	arrival = models.ForeignKey(Arrival)
	quantity = models.IntegerField(default=0)
	item_cost = models.FloatField(null=True, blank=True)

	#source_location = models.ForeignKey(Location)
	#destination = models.ForeignKey(Location)
	def __unicode__(self):
		return self.item.item_code


2. Create Forms for the models
class AddArrivalForm(forms.ModelForm): 
	class Meta: 
		model = Arrival
		fields = ['date', 'delivery_receipt_no', 'tracking_no', 'supplier']

	def __init__(self, *args, **kwargs):
		super(AddArrivalForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs['class'] = 'form-control'
		self.fields['delivery_receipt_no'].widget.attrs['class'] = 'form-control'
		self.fields['tracking_no'].widget.attrs['class'] = 'form-control'
		self.fields['supplier'].widget.attrs['class'] = 'form-control'

class AddArrivedItemForm(forms.ModelForm): 
	class Meta: 
		model = ArrivedItem
		fields = ['item', 'quantity', 'item_cost']

	def __init__(self, *args, **kwargs):
		super(AddArrivedItemForm, self).__init__(*args, **kwargs)
		self.fields['item'].widget.attrs['class'] = 'form-control'
		self.fields['quantity'].widget.attrs['class'] = 'form-control'
		self.fields['item_cost'].widget.attrs['class'] = 'form-control'

3. Create formset for the intermediary model (arriveditemform) 
class AddArrivedItemFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return

4. Update views
def arrival(request):
	items_list = Item.objects.all()
	arrivalForm = AddArrivalForm(request.POST or None)
	formset = formset_factory(AddArrivedItemForm, formset=AddArrivedItemFormset, extra = 1)
	arrivalFormset = formset(request.POST or None)

	if arrivalForm.is_valid() and arrivalFormset.is_valid():
		# first save arrival details
		# commit = False means that we can store the arrival instance to the value p
		p = arrivalForm.save(commit=False)

		#save the form
		p.save()
		arrival_id = p
		new_items = []

		# loop through all forms in the formset, and save each form - add the arrivalId to each form
		for form in arrivalFormset:
			print form.cleaned_data
			item = form.cleaned_data.get('item')
			arrival = arrival_id
			quantity = form.cleaned_data.get('quantity')
			item_cost = form.cleaned_data.get('item_cost')
			i = ArrivedItem(item=item, arrival=p, quantity=quantity, item_cost=item_cost)	
			i.save()
		
		return HttpResponseRedirect(reverse('arrival'))

	return render(request, 'arrival/arrival.html', {
		'AddArrivalForm' : arrivalForm, 
		'formset' : arrivalFormset,
		'items':items_list 
		})

5. Render in your templates


5.1 Add styles
<style type="text/css">
    .add-row {
        margin-top: 10px;
        width: 150px;
    }

    .delete-row {
        width: 80%;
        margin-left: 10%;
    }

</style>


5.2 Add scripts
<script type="text/javascript" src="/static/js/jquery.formset.js"></script>
<script type="text/javascript">
    <!--
    $(function () {
        $('.add-row').click(function() {
            return addForm(this, 'form');
        });
        $('.delete-row').click(function() {
            return deleteForm(this, 'form');
        })
    })
    //-->
    </script>

5.3 Add form
<form class="form" method="POST">
            {% csrf_token %}
            {{ AddArrivalForm.as_p }}
            
            <h2>Arrived Items</h2>
            <table id="id_orders_table" width="100%" border="0" cellpadding="50" cellspacing="1500">
                <thead>
                    <tr>
                        <th scope="col">Item</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Item Cost</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    {% for form in formset.forms %}
                    <tr id="{{ form.prefix }}-row" class="dynamic-form">
                        <td>{{ form.item }}</td>
                        <td>{{form.quantity}}</td>
                        <td>{{form.item_cost}}</td>
                        <td><a id="remove-{{ form.prefix }}-row" href="javascript:void(0)" class="delete-row btn btn-danger">Remove</a></td>
                    </tr>
                    {% endfor %}
                </tbody>

            </table>
            <a href="javascript:void(0)" class="add-row btn btn-info">Add More</a>
            {{ formset.management_form }}
            <br><br>
            <div class="form-group">
                <input type="submit" class="form-control btn btn-primary" name="name" value="Submit" />
            </div>
        </form>



