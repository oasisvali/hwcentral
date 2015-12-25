$(document).ready(function () {
    var subjectroom_id = extract_id($("#subjectroom_id"));
    $.getJSON(CHART_ENDPOINT + "subjectroom/" + subjectroom_id, function (single_subjectroom_data) {
        if (single_subjectroom_data.listing.length == 0) {
            $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
            return;
        }

        var student_subjectroom_performance_data = [];
        for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
            var subjectroom_assignment = single_subjectroom_data.listing[j];
            student_subjectroom_performance_data.push([subjectroom_assignment.date, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average, subjectroom_assignment.topic]);
        }
        draw_teacher_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data);
    });
});