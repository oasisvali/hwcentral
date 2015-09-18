google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_subjectroom_performance_breakdown(arraydata,tab_index,subject_room,subject_teacher,subjectteacher_data) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: 1000,
        height: 400,
        chartArea: {'width': '65%', 'height': '80%'},
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:0,
            }
        }
    };


    var chart = new google.visualization.ColumnChart(document.getElementById('subjectroom_bargraph' + tab_index));
    chart.draw(data, options);


    google.visualization.events.addListener(chart, 'select', function() {
          // grab a few details before redirecting
        var selection = chart.getSelection();
        var row = selection[0].row;
        var col = selection[0].column;

        if (col==1){
            if ($("#section_assignment_performance").length > 0) {
                var assignment_id=subjectteacher_data[tab_index].listing[row].assignment_id.toString();
                var topic=subjectteacher_data[tab_index].listing[row].topic;
                $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_section_assignment_performance(assignment_performance_data,topic);
                });
            }   
            $("#section_chart_popup").modal('show');
        }        
        
        if (col==2){
            if ($("#standard_assignment_performance").length > 0) {
                var assignment_id=subjectteacher_data[tab_index].listing[row].assignment_id.toString();
                var topic=subjectteacher_data[tab_index].listing[row].topic;
                $.getJSON(CHART_ENDPOINT + "standard-assignment/" + assignment_id, function (assignment_data) {
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_standard_assignment_performance(assignment_performance_data,topic);
                });
            }   
            $("#standard_chart_popup").modal('show');
        }
        
    });
}








