function draw_subjectroom_performance_breakdown(arraydata,tab_index,subject_room,subject_teacher) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        title: ""+subject_room+": "+subject_teacher,
        legend: {
            position: 'right'
        },
        pointSize:5,
        width: 1100,
        height: 500,
        hAxis: {
            title: 'Topic',
        },
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
}