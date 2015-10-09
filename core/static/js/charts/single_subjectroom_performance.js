google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_single_subjectroom_performance(arraydata, subjectteacher_data, is_student_chart, is_popup_chart, chart_width, chart_height) {
    var data = google.visualization.arrayToDataTable(arraydata);
    var options = {
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: chart_width,
        height: chart_height,
        chartArea: {'width': '65%', 'height': '70%'},
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min: -1,
            },
            baseline:-1
        }
    };

    var chart = null;
    if (is_popup_chart) {
        chart = new google.visualization.ColumnChart(document.getElementById('single_subjectroom_bargraph_popup'));
    }
    else {
        chart = new google.visualization.ColumnChart(document.getElementById('single_subjectroom_bargraph'));
    }
    chart.draw(data, options);

    google.visualization.events.addListener(chart, 'select', function() {
          // grab a few details before redirecting
        var selection = chart.getSelection();
        chart.setSelection(); // to remove the selection from the chart element
        var row = selection[0].row;
        var col = selection[0].column;
        var counter=0;
        var colorarray=[];
        if (is_student_chart == true) {
            if(col==1){
                var submission_id= subjectteacher_data.listing[row].submission_id.toString();
                window.location.href="/submission/"+submission_id;
                alert("Redirecting Page to Assignment Submission");
            }
            else if (col == 2) {
                if ($("#subjectroom_assignment_performance").length > 0) {
                    $("#subjectroom_performance_popup").modal('hide');
                    var assignment_id= subjectteacher_data.listing[row].assignment_id.toString();
                    var topic= subjectteacher_data.listing[row].topic;
                    var student_score=subjectteacher_data.listing[row].student_score;
                    $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                        var assignment_performance_data=[];
                        for(var j=0;j<assignment_data.length;j++){
                            var student_assignment=assignment_data[j];
                            assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                        }
                        draw_subjectroom_assignment_performance(assignment_performance_data, topic, null);
                    });
                }
                $("#subjectroom_assignment_chart_popup").modal('show');
            }    
        }
        else {
            if (col==1){
                if ($("#subjectroom_assignment_performance").length > 0) {
                    var assignment_id=subjectteacher_data.listing[row].assignment_id.toString();
                    var topic=subjectteacher_data.listing[row].topic;
                    $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                        var assignment_performance_data=[];
                        for(var j=0;j<assignment_data.length;j++){
                            var student_assignment=assignment_data[j];
                            assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                        }
                        draw_subjectroom_assignment_performance(assignment_performance_data, topic, assignment_data);
                    });
                }
                $("#subjectroom_assignment_chart_popup").modal('show');
            }

            else if (col == 2) {
                if ($("#standard_assignment_performance").length > 0) {
                    var assignment_id=subjectteacher_data.listing[row].assignment_id.toString();
                    var topic=subjectteacher_data.listing[row].topic;
                    $.getJSON(CHART_ENDPOINT + "standard-assignment/" + assignment_id, function (assignment_data) {
                        var assignment_performance_data=[];
                        for(var j=0;j<assignment_data.length;j++){
                            var student_assignment=assignment_data[j];
                            assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                        }
                        draw_standard_assignment_performance(assignment_performance_data);
                    });
                }
                $("#standard_assignment_chart_popup").modal('show');
            }
        }
    });
}