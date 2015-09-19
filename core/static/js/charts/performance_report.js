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
        width:1000,
        height:400,
        chartArea: {'width': '65%', 'height': '80%'},
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:0
            }
        },
        
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('performance_bargraph'));
    chart.draw(data, options);
}

function draw_printable_performance_report(arraydata) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Subject');
    data.addColumn('number', 'My Performance');
    data.addColumn('number', 'Class Average');


    data.addRows(arraydata);

    var options = {
        width:825,
        height:500,
        title: 'Performance Report',
        hAxis: {
            title: 'Subject',
        },
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:0
            }
        },
        
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('printable_performance_bargraph'));
    chart.draw(data, options);
}
