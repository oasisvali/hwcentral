$(document).ready(function () {
    datatables_link_delegate(this, '.student_subjectroom_performance_link', student_focusroom_performance_link_handler);
});

function student_focusroom_performance_link_handler(link) {
    var student_id = $(link).parent('td').parent('tr').find(".student_id").text();
    var focusroom_id = $("#focusroom_id").text();
    if ($("#student_subjectroom_popup").length > 0) {
        prep_chart_popup('single_subjectroom_bargraph_popup');
        $.getJSON(CHART_ENDPOINT + "focus/" + student_id + "/" + focusroom_id, function (single_focusroom_data) {
            if (single_focusroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph_popup').html(NO_DATA_IMG);
            }
            else {
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
                draw_student_single_subjectroom_performance(student_focusroom_performance_data, single_focusroom_data, true);
            }
        });
        $("#subjectroom_performance_popup").modal('show');
    }
}