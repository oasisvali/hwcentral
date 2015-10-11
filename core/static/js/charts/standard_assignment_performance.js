function draw_standard_assignment_performance(arraydata) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Full Name');
        data.addColumn('number', 'Score');
        data.addRows(arraydata);
        
        var options = {
          height:400,
          width: 825,
          legend: { 
            position: 'none' 
          },
          hAxis:{
            title: "Percentage",
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 101,
                min: 0
            },
            ticks: [0,10,20,30,40,50,60,70,80,90,100] // to keep xaxis fixed
          },
          vAxis:{
            title:"Number of students",
            viewWindow: {
                min: 0
            }
          },
          histogram: { 
            bucketSize:10 
          },
          colors:["#0000FF"]
        };
    var chart = new google.visualization.Histogram(document.getElementById('standard_assignment_histogram'));
        chart.draw(data, options);
}
