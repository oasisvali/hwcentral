function draw_performance_breakdown(arraydata,tab_index,subject,subject_teacher) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        title: ""+subject+": "+subject_teacher,
        legend: {
        position: 'right'
        },
        pointSize:5,
        width: 1000,
        height: 400,
        hAxis: {
            title: 'Topic',
        },
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:0
            }
        }
    };


    var chart = new google.visualization.ColumnChart(document.getElementById('subject_performance' + tab_index));
    chart.draw(data, options);

    google.visualization.events.addListener(chart, 'select', function() {
          // grab a few details before redirecting
        var selection = chart.getSelection();
        var row = selection[0].row;
        var col = selection[0].column;
        if (col==1){
            if ($("#assignment_performance").length > 0) {
                var subjectroomlist= studentdata.breakdown_listing;
                var topic=subjectroomlist[tab_index].listing[row].topic;
                var assignment_performance_data=[
                        ['Fullname','Score']
                    ];
                for(var j=0;j<assignmentarray[row].length;j++){
                    var student_assignment=assignmentarray[row][j];
                    assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                }
                draw_assignment_performance(assignment_performance_data,topic);
            }
        $("#chart_popup").modal('show');
        }    
    });
}


function draw_printable_performance_breakdown(arraydata,tab_index,subject,subject_teacher) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        title: ""+subject+": "+subject_teacher,
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: 825,
        height: 360,
        hAxis: {
            title: 'Topic',
        },
        vAxis: {
            title: 'Aggregate',
            viewWindowMode: 'Explicit',
            viewWindow: {
                max: 100,
                min:0
            }
        }
    };


    var chart = new google.visualization.ColumnChart(document.getElementById('printable_subject_performance' + tab_index));
    chart.draw(data, options);
}
