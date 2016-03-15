$(document).ready(function () {
    var user_id = extract_id($("#user_id"));
    var focusroom_id = extract_id($("#focusroom_id"));
    var student_id = null;

    if ($("#child_id").length > 0) {
        // the current user is a parent, use the child id for the subsequent chart call
        student_id = extract_id($("#child_id"));
    }
    else {
        // current user is a student, use the user id for the subsequent chart call
        student_id = user_id;
    }

    $.getJSON(CHART_ENDPOINT + "focus/" + student_id + "/" + focusroom_id, function (single_focusroom_data) {
        if (single_focusroom_data.listing.length == 0) {
            $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
            return;
        }

        var student_focusroom_performance_data = [];
        for (var j = 0; j < single_focusroom_data.listing.length; j++) {
            var focusroom_assignment = single_focusroom_data.listing[j];
            student_focusroom_performance_data.push([
                focusroom_assignment.date,
                focusroom_assignment.student_score,
                focusroom_assignment.subjectroom_average,
                focusroom_assignment.topic,
                focusroom_assignment.student_completion
            ]);
        }
        draw_student_single_subjectroom_performance(student_focusroom_performance_data, single_focusroom_data, false);
    });
});