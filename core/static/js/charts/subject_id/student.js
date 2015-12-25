$(document).ready(function () {
    var user_id = extract_id($("#user_id"));
    var subjectroom_id = extract_id($("#subjectroom_id"));
    var student_id = null;

    if ($("#parent_child_id").length > 0) {
        // the current user is a parent, use the child id for the subsequent chart call
        student_id = extract_id($("#parent_child_id"));
    }
    else {
        // current user is a student, use the user id for the subsequent chart call
        student_id = user_id;
    }

    $.getJSON(CHART_ENDPOINT + "student/" + student_id + "/" + subjectroom_id, function (single_subjectroom_data) {
        if (single_subjectroom_data.listing.length == 0) {
            $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
            return;
        }

        var student_subjectroom_performance_data = [];
        for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
            var subjectroom_assignment = single_subjectroom_data.listing[j];
            student_subjectroom_performance_data.push([subjectroom_assignment.date, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average, subjectroom_assignment.topic]);
        }
        draw_student_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, false);
    });
});