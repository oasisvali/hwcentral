google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_student_performance_breakdown(arraydata, tab_index, student_data) {
    arraydata.splice(0, 0, ['Topic', 'Student\'s Score', 'Class Average']);
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        legend: {
        position: 'right'
        },
        pointSize:5,
        width: CHART_WIDTH,
        height: CHART_HEIGHT,
        chartArea: CHART_AREA,
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:-1
            },
            baseline:-1,
        }
    };


    var chart = new google.visualization.ColumnChart(document.getElementById('subject_performance' + tab_index));
    chart.draw(data, options);

    google.visualization.events.addListener(chart, 'select', function() {
          // grab a few details before redirecting
        var selection = chart.getSelection();
        chart.setSelection(); // to remove the selection from the chart element
        var row = selection[0].row;
        var col = selection[0].column;
        var counter=0;
        var colorarray=[];
        if(col==1){
            var submission_id= student_data.breakdown_listing[tab_index].listing[row].submission_id.toString(); 
            window.location.href="/submission/"+submission_id;
            alert("Redirecting Page to Assignment Submission");
        }
        if (col==2){
            if ($("#subjectroom_assignment_performance").length > 0) {
                $("#student_performance_breakdown_popup").modal('hide');
                var assignment_id=student_data.breakdown_listing[tab_index].listing[row].assignment_id.toString();
                var topic=student_data.breakdown_listing[tab_index].listing[row].topic;
                var student_score=student_data.breakdown_listing[tab_index].listing[row].student_score;
                $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    if (assignment_data[0].submission_id==undefined){
                        assignment_data=null; // differentiate between unanonymized and anonymized histrogram
                    }
                    draw_subjectroom_assignment_performance(assignment_performance_data, topic, assignment_data);
                });
            }
            $("#subjectroom_assignment_chart_popup").modal('show');
        }   
    });
}

