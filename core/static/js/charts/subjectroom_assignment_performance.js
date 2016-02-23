function draw_subjectroom_assignment_performance(arraydata, topic, assignment_data) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Full Name');
        data.addColumn('number', 'Score');
        data.addRows(arraydata);
        
        var options = {
          title: topic,
          height:CHART_HEIGHT,
          width: CHART_WIDTH,
          legend: { 
            position: 'none' 
          },
          hAxis:{
              title: "Score"
          },
          vAxis:{
            title:"Number of students",
          },
          histogram: { 
            bucketSize:10 
          },
          colors:["#e7711c"]
        };
    var chart = new google.visualization.Histogram(document.getElementById('subjectroom_assignment_histogram'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
            // grab a few details before redirecting
  
          var selection = chart.getSelection();
          chart.setSelection(); // to remove the selection from the chart element
          var row = selection[0].row;
          var col = selection[0].column;
         
      
          if (col==1){
              var submission_id = assignment_data[row].submission_id;
              if (submission_id) {    // only redirect for non-anonymized histogram elements
                  window.open("/submission/" + submission_id, '_blank');
              }
          }
        });
}


  
