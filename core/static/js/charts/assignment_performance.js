function draw_assignment_performance(arraydata,topic) {
        var data = google.visualization.arrayToDataTable(arraydata);
        var options = {
          title: ""+topic,
          height:400,
          width: 825,
          legend: { 
            position: 'none' 
          },
          colors: ['#e7711c'],
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
          }
        };

        var chart = new google.visualization.Histogram(document.getElementById('histogram'));
        chart.draw(data, options);
}


  
