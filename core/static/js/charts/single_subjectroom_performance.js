google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function draw_single_subjectroom_performance(arraydata,subject_room,subject_teacher) {
        
    var data = google.visualization.arrayToDataTable(arraydata);

    var options = {
        title: subject_room.toString();+":"+subject_teacher.toString();,
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


    var chart = new google.visualization.ColumnChart(document.getElementById('single_subjectroom_bargraph'));
    chart.draw(data, options);
}