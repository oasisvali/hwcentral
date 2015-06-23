var test=new Performance(mock);
for (var i=0;i<test.breakdown_listing.length;i++){

 google.setOnLoadCallback(drawChart);

      function drawChart() {
        var arraydata=[
          ['Topic', 'Average', 'My Performance'],
        ];
        for (var j=0;j<test.breakdown_listing[i].listing.length;j++){
          arraydata.push([test.breakdown_listing[i].listing[j].topic,test.breakdown_listing[i].listing[j].class_average,test.breakdown_listing[i].listing[j].student_score]);
        }

        var data = google.visualization.arrayToDataTable(arraydata);

        var options = {
          title: 'Assignment Performance',
          legend: { position: 'right' },
          width: 1000,
          height: 600 
        };

        var chart = new google.visualization.LineChart(document.getElementById('linegraph'+i));

        chart.draw(data, options);
      }
}