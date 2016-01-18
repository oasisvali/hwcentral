function draw_assignment_completion(arraydata, topic) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Full Name');
    data.addColumn('number', 'Completion');
    data.addRows(arraydata);

    var options = {
        title: topic,
        height: (CHART_HEIGHT * (arraydata.length / 20.0)),
        width: CHART_WIDTH,
        legend: {
            position: 'none'
        },
        hAxis: {
            title: "Completion",
            minValue: 0,
            maxValue: 99
        },
        colors: ["red"],
        chartArea: {left: '25%', width: '70%', height: '80%'}
    };
    var chart = new google.visualization.BarChart(document.getElementById('assignment_completion_chart'));
    chart.draw(data, options);
}