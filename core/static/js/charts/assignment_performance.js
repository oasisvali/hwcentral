function draw_assignment_performance(arraydata,topic) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Full Name');
        data.addColumn('number', 'Score');
        //data.addColumn('string', {role:'annotation'});
        data.addRows(arraydata);
        console.log(arraydata);
        
        var options = {
          title: ""+topic,
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
          }
        };
        console.log(data);
        var chart = new google.visualization.Histogram(document.getElementById('histogram'));
        chart.draw(data, options);
}


  
