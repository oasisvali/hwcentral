$(document).ready(function () {
    var classteacher_id = extract_id($("#classteacher_id"));
    var classroom_id = extract_id($("#classroom_id"));

    $.getJSON(CHART_ENDPOINT + "classteacher/" + classteacher_id + "/" + classroom_id, function (classteacher_data) {
        for (var i = 0; i < classteacher_data.length; i++) {
            var subject_room = classteacher_data[i].subject_room;
            $("#classroombar").append(
                "<li class=classroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
            $("#classroombargraph").append(
                "<div id='classroom_bargraph" + i + "' class='classroom_chart chart'></div>");
        }
        $("[target='0']").addClass('active');
        $('#classroombargraph > #chart-loader').remove();      // remove chart loader
        $('.classroom_chart').hide();
        $('#classroom_bargraph0').show();

        $('.classroomtab').click(function () {
            $('.classroom_chart').hide();
            $('#classroom_bargraph' + $(this).attr('target')).show();
        });

        $('ul.nav-tabs li a').click(function (e) {
            $('ul.nav-tabs li.active').removeClass('active');
            $(this).parent('li').addClass('active');
        });

        for (var i = 0; i < classteacher_data.length; i++) {
            if (classteacher_data[i].listing.length == 0) {
                $('#classroom_bargraph' + i).html(NO_DATA_IMG);
                continue;
            }

            var classroom_performance_breakdown_data = [];
            for (var j = 0; j < classteacher_data[i].listing.length; j++) {
                var classroom_assignment = classteacher_data[i].listing[j];
                classroom_performance_breakdown_data.push([
                    classroom_assignment.date,
                    classroom_assignment.subjectroom_average,
                    classroom_assignment.standard_average,
                    classroom_assignment.topic,
                    classroom_assignment.subjectroom_completion
                ]);
            }
            draw_classroom_performance_breakdown(classroom_performance_breakdown_data, i, classteacher_data);
        }
    });
});