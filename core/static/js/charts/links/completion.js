$(document).ready(function () {
    datatables_link_delegate(this, '.completion_link', completion_link_handler);
});

function completion_link_handler(link) {
    var parent_row = $(link).parent('td').parent('tr');
    var assign_id = extract_id(parent_row.find(".assignment_id"));
    var topic = extract_text(parent_row.find(".assign_title"));

    if ($("#assignment_completion").length > 0) {
        prep_chart_popup('assignment_completion_chart');
        $.getJSON(CHART_ENDPOINT + "completion/" + assign_id, function (assignment_data) {
            var completion_data = [];
            for (var j = 0; j < assignment_data.length; j++) {
                var student_completion = assignment_data[j];
                completion_data.push([
                    student_completion.full_name,
                    student_completion.completion
                ]);
            }
            draw_assignment_completion(completion_data, topic);
        });
        $("#assignment_completion_popup").modal('show');
    }
}
