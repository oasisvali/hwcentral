google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_parent_child_performance_report(arraydata,chart_width,chart_height,child_id) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Subject');
    data.addColumn('number', 'Student\'s Performance');
    data.addColumn('number', 'Class Average');

    data.addRows(arraydata);

    var options = {
        width:chart_width,
        height:chart_height,
        chartArea: {'width': '65%', 'height': '80%'},
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

    var chart = new google.visualization.ColumnChart(document.getElementById('student_performance_bargraph_' + child_id));
    chart.draw(data, options);
}

//function draw_parent_child_printable_performance_report(arraydata,child_id) {
//    var data = new google.visualization.DataTable();
//    data.addColumn('string', 'Subject');
//    data.addColumn('number', 'Student\'s Performance');
//    data.addColumn('number', 'Class Average');
//
//
//    data.addRows(arraydata);
//
//    var options = {
//        width:825,
//        height:500,
//        title: 'Performance Report',
//        hAxis: {
//            title: 'Subject',
//        },
//        vAxis: {
//            title: 'Aggregate',
//            viewWindowMode: 'Explicit',
//            viewWindow: {
//                max: 100,
//                min:0
//            }
//        },
//
//    };
//
//    var chart = new google.visualization.ColumnChart(document.getElementById('printable_performance_bargraph_'+child_id));
//    chart.draw(data, options);
//}