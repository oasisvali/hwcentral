$(document).ready(function () {
    var focusroom_id = extract_id($("#focusroom_id"));
    $.getJSON(CHART_ENDPOINT + "focusroom/" + focusroom_id, function (single_focusroom_data) {
        if (single_focusroom_data.listing.length == 0) {
            $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
            return;
        }

        var student_focusroom_performance_data = [];
        for (var j = 0; j < single_focusroom_data.listing.length; j++) {
            var focusroom_assignment = single_focusroom_data.listing[j];
            student_focusroom_performance_data.push([
                focusroom_assignment.date,
                focusroom_assignment.subjectroom_average,
                focusroom_assignment.standard_average,
                focusroom_assignment.topic,
                focusroom_assignment.subjectroom_completion
            ]);
        }
        draw_teacher_single_subjectroom_performance(student_focusroom_performance_data, single_focusroom_data);
    });
});