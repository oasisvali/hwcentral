 google.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Assignment Date', 'Average', 'My Performance'],
          ['11/07/15',  80,      70],
          ['12/07/15',  40,      57],
          ['17/07/15',  77,      91],
          ['18/07/15',  83,      72]
        ]);

        var options = {
          title: 'Assignment Performance',
          legend: { position: 'right' },
          width: 1000,
          height: 600 
        };

        var chart = new google.visualization.LineChart(document.getElementById('linegraph1'));

        chart.draw(data, options);
      }