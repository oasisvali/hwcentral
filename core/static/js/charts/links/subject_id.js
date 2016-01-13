$(document).ready(function () {
    datatables_link_delegate(this, '.student_subjectroom_performance_link', student_subjectroom_performance_link_handler);
});

function student_subjectroom_performance_link_handler(link) {
    var student_id = $(link).parent('td').parent('tr').find(".student_id").text();
    var subjectroom_id = $("#subjectroom_id").text();
    if ($("#student_subjectroom_popup").length > 0) {
        prep_chart_popup('single_subjectroom_bargraph_popup');
        $.getJSON(CHART_ENDPOINT + "student/" + student_id + "/" + subjectroom_id, function (single_subjectroom_data) {
            if (single_subjectroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph_popup').html(NO_DATA_IMG);
            }
            else {
                var student_subjectroom_performance_data = [];
                for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                    var subjectroom_assignment = single_subjectroom_data.listing[j];
                    student_subjectroom_performance_data.push([
                        subjectroom_assignment.date,
                        subjectroom_assignment.student_score,
                        subjectroom_assignment.subjectroom_average,
                        subjectroom_assignment.topic,
                        subjectroom_assignment.student_completion
                    ]);
                }
                draw_student_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, true);
            }
        });
        $("#subjectroom_performance_popup").modal('show');
    }
}