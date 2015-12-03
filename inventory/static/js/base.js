<script type="text/javascript" src="static/js/jquery2.min.js"></script>
<script type="text/javascript">
$(document).ready(function()
{
$("#notificationLink").click(function()
{
$("#notificationContainer").fadeIn(300);
$("#notification_count").fadeOut("slow");
//return false;
e.stopPropagation();
});

//Document Click hiding the popup 
$(document).click(function()
{
$("#notificationContainer").hide();
});

//Popup on click
$("#notificationContainer").click(function()
{
//return false;
e.stopPropagation();
});

});
</script>