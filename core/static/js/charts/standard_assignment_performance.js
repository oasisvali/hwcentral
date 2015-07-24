function draw_standard_assignment_performance(arraydata,topic) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Full Name');
        data.addColumn('number', 'Score');
        data.addRows(arraydata);
        
        var options = {
          title: topic.toString(),
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
            }
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
        var chart = new google.visualization.Histogram(document.getElementById('standard_histogram'));
        chart.draw(data, options);
}
