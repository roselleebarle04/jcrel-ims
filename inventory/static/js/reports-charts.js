$.ajax({
    type: 'POST' ,
    url: '{% url "reports_data" %}',
    datatype: 'json' ,
    async: true,
    data:{
        csrfmiddlewaretoken: '{{ csrf_token }}',
        sentence: $('#word').val()
    },

    success: function(json) {
        console.log(json.message);
        $('#output').html(json.message);
    }
});

var ctx = document.getElementById("myChart").getContext("2d");

// Generate dataset for each product, containing stock quantities in all locations charted
// through monthly levels. 

var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July", "August"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
};

var myLineChart = new Chart(ctx).Line(data);