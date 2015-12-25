google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_subjectroom_performance_breakdown(arraydata,tab_index,subjectteacher_data) {
    var dataTable = new google.visualization.DataTable();
    dataTable = prep_columnchart_data(dataTable, "Section Average", "Standard Average", arraydata);

    var options = {
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: CHART_WIDTH,
        height: CHART_HEIGHT,
        chartArea: CHART_AREA,
        vAxis: {
            title: 'Average Score',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:-1
            },
            baseline:-1,
        },
        tooltip: {isHtml: true}
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('subjectroom_bargraph' + tab_index));
    chart.draw(dataTable, options);

    google.visualization.events.addListener(chart, 'select', function() {
          // grab a few details before redirecting
        var selection = chart.getSelection();
        chart.setSelection(); // to remove the selection from the chart element
        var row = selection[0].row;
        var col = selection[0].column;

        if (col==1){
            if ($("#subjectroom_assignment_performance").length > 0) {
                $("#teacher_performance_breakdown_popup").modal('hide');
                var assignment_id=subjectteacher_data[tab_index].listing[row].assignment_id.toString();
                var topic=subjectteacher_data[tab_index].listing[row].topic;
                prep_chart_popup('subjectroom_assignment_histogram');
                $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_subjectroom_assignment_performance(assignment_performance_data, topic, assignment_data);
                });
                $("#subjectroom_assignment_chart_popup").modal('show');
            }
        }

        if (col == 3) {
            if ($("#standard_assignment_performance").length > 0) {
                $("#teacher_performance_breakdown_popup").modal('hide');
                var topic=subjectteacher_data[tab_index].listing[row].topic;
                var assignment_id=subjectteacher_data[tab_index].listing[row].assignment_id.toString();
                prep_chart_popup('standard_assignment_histogram');
                $.getJSON(CHART_ENDPOINT + "standard-assignment/" + assignment_id, function (assignment_data) {
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_standard_assignment_performance(assignment_performance_data, topic, assignment_data);
                });
                $("#standard_assignment_chart_popup").modal('show');
            }
        }
    });
}








