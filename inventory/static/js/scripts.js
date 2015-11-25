function confirmDelete(supplier_id){
  console.log(supplier_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/suppliers/delete/' + supplier_id + '/'; 
  else 
    window.location = '/suppliers/';
}

function confirmItemDelete(item_id){
  console.log(item_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/items/delete/' + item_id + '/'; 
  else 
    window.location = '/items/';
}

function confirmSaleDelete(sale_id){
  console.log(sale_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/sales/delete/' + sale_id + '/'; 
  else 
    window.location = '/sales/';
}

function confirmTransferDelete(transfer_id){
  console.log(transfer_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/transfer/delete/' + transfer_id + '/'; 
  else 
    window.location = '/transfer_hist/';
}

 function confirmLocationDelete(location_id){
  console.log(location_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/location/delete/' + location_id + '/'; 
  else 
    window.location = '/location/';
}

function confirmArrivalDelete(arrival_id){
  console.log(arrival_id);
  var r = confirm('Are you sure?'); 
  if (r==true) 
    window.location = '/arrivals/delete/' + arrival_id + '/'; 
  else 
    window.location = '/arrivals/';
}
    
$(document).ready(function(){
    $('#suppliers').DataTable();
    $('#items').DataTable(); 
    $('#sales').DataTable(); 
});