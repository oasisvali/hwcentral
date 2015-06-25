google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});


function draw_performance_report(arraydata) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Subject');
    data.addColumn('number', 'My Performance');
    data.addColumn('number', 'Class Average');


    data.addRows(arraydata);

    var options = {
        width: 1100,
        height: 400,
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

