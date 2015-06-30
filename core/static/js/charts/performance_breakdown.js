function draw_performance_breakdown(arraydata,tab_index,subject,subject_teacher) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        title: ""+subject+": "+subject_teacher,
        legend: {
        position: 'right'
        },
        pointSize:5,
        width: 1100,
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
