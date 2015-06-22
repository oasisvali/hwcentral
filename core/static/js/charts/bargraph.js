// Code to Run Google Charts API

// Student Home Over View Chart
                google.load('visualization', '1', {packages: ['corechart', 'bar']});
                google.setOnLoadCallback(drawColColors);

function drawColColors() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Subject');
      data.addColumn('number', 'My Performance');
      data.addColumn('number', 'Class Average');

      data.addRows([
        ['Mathematics', 77, 72],
        ['Science', 83, 89],
        ['Social Science', 81, 79],
        ['English', 82, 91],
        ['Second Language', 85, 81],
        ['FIT', 99, 94],
      ]);

      var options = {
        title: 'Performance Report',
        colors: ['#0000FF', '#00FF00'],
        hAxis: {
          title: 'Subject',
        },
        vAxis: {
          title: 'Aggregate'
        }
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('bargraph'));
      chart.draw(data, options);
    }


