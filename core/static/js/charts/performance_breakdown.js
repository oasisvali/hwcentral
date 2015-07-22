google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_performance_breakdown(arraydata,tab_index,subject,subject_teacher,student_data) {
        
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
        var counter=0;
        var colorarray=[];
        if (col==1){
            if ($("#assignment_performance").length > 0) {
                var assignment_id=student_data.breakdown_listing[tab_index].listing[row].assignment_id.toString();
                var topic=student_data.breakdown_listing[tab_index].listing[row].topic;
                var student_score=student_data.breakdown_listing[tab_index].listing[row].student_score;
                $.getJSON(CHART_ENDPOINT+"assignment/"+assignment_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_assignment_performance(assignment_performance_data,topic);
                });
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

