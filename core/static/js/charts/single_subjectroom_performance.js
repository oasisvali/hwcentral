google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_student_single_subjectroom_performance(arraydata, subjectteacher_data, is_popup_chart) {
    var dataTable = new google.visualization.DataTable();
    dataTable = prep_columnchart_data(dataTable, "Student\'s Score", "Class Average", arraydata);

    draw_single_subjectroom_performance(dataTable, subjectteacher_data, true, is_popup_chart);
}

function draw_teacher_single_subjectroom_performance(arraydata, subjectteacher_data) {
    var dataTable = new google.visualization.DataTable();
    dataTable = prep_columnchart_data(dataTable, "Section Average", "Standard Average", arraydata);

    draw_single_subjectroom_performance(dataTable, subjectteacher_data, false, false);
}

function draw_single_subjectroom_performance(dataTable, subjectteacher_data, is_student_chart, is_popup_chart) {
    var vAxisTitle = 'Score';
    if (!is_student_chart) {
        vAxisTitle = 'Average ' + vAxisTitle;
    }

    var options = {
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: CHART_WIDTH,
        height: CHART_HEIGHT,
        chartArea: CHART_AREA,
        vAxis: {
            title: vAxisTitle,
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min: -1,
            },
            baseline:-1
        },
        hAxis: {
            slantedText: true,
            textStyle: {
                fontSize: 12
            }
        },
        tooltip: {isHtml: true}
    };

    var target = 'single_subjectroom_bargraph';
    if (is_popup_chart) {
        target += '_popup';
    }
    chart = new google.visualization.ColumnChart(document.getElementById(target));
    chart.draw(dataTable, options);

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
            else if (col == 3) {
                if ($("#subjectroom_assignment_performance").length > 0) {
                    $("#subjectroom_performance_popup").modal('hide');
                    var assignment_id= subjectteacher_data.listing[row].assignment_id.toString();
                    var topic= subjectteacher_data.listing[row].topic;
                    var student_score=subjectteacher_data.listing[row].student_score;
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
        }
        else {
            if (col==1){
                if ($("#subjectroom_assignment_performance").length > 0) {
                    var assignment_id=subjectteacher_data.listing[row].assignment_id.toString();
                    var topic=subjectteacher_data.listing[row].topic;
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

            else if (col == 3) {
                if ($("#standard_assignment_performance").length > 0) {
                    var assignment_id=subjectteacher_data.listing[row].assignment_id.toString();
                    var topic=subjectteacher_data.listing[row].topic;
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
        }
    });
}