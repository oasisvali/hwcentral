$(document).ready(function () {
    var user_id = extract_id($("#user_id"));
    $.getJSON(CHART_ENDPOINT + "subjectteacher/" + user_id, function (subjectteacher_data) {
        for (var i = 0; i < subjectteacher_data.length; i++) {
            var subject_room = subjectteacher_data[i].subject_room;
            $("#subjectroombar").append(
                "<li class=subjectroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
            $("#subjectroombargraph").append(
                "<div id='subjectroom_bargraph" + i + "' class='subjectroom_chart chart'></div>");
        }
        $("[target='0']").addClass('active');   // make first tab active
        $('#subjectroombargraph > #chart-loader').remove();      // remove chart loader
        $('.subjectroom_chart').hide();
        $('#subjectroom_bargraph0').show();

        $('.subjectroomtab').click(function () {
            $('.subjectroom_chart').hide();
            $('#subjectroom_bargraph' + $(this).attr('target')).show();
        });

        $('ul.nav-tabs li a').click(function (e) {
            $('ul.nav-tabs li.active').removeClass('active');
            $(this).parent('li').addClass('active');
        });

        for (var i = 0; i < subjectteacher_data.length; i++) {
            if (subjectteacher_data[i].listing.length == 0) {
                $('#subjectroom_bargraph' + i).html(NO_DATA_IMG);
                continue;
            }
            var subjectroom_performance_breakdown_data = [];
            for (var j = 0; j < subjectteacher_data[i].listing.length; j++) {
                var subjectroom_assignment = subjectteacher_data[i].listing[j];
                subjectroom_performance_breakdown_data.push([
                    subjectroom_assignment.date,
                    subjectroom_assignment.subjectroom_average,
                    subjectroom_assignment.standard_average,
                    subjectroom_assignment.topic,
                    subjectroom_assignment.subjectroom_completion
                ]);
            }
            draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data, i, subjectteacher_data);
        }
    });
});