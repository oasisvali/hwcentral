$(document).ready(function () {
    datatables_link_delegate(this, '.histogram_link', histogram_link_handler);
});

function histogram_link_handler(link) {
    var parent_row = $(link).parent('td').parent('tr');
    var assign_id = extract_id(parent_row.find(".assignment_id"));
    var topic = extract_text(parent_row.find(".assign_title"));

    if ($("#subjectroom_assignment_performance").length > 0) {
        prep_chart_popup('subjectroom_assignment_histogram');
        $.getJSON(CHART_ENDPOINT + "assignment/" + assign_id, function (assignment_data) {
            var assignment_performance_data = [];
            for (var j = 0; j < assignment_data.length; j++) {
                var student_assignment = assignment_data[j];
                assignment_performance_data.push([
                    student_assignment.full_name,
                    student_assignment.score
                ]);
            }
            draw_subjectroom_assignment_performance(assignment_performance_data, topic, assignment_data);
        });
        $("#subjectroom_assignment_chart_popup").modal('show');
    }
}