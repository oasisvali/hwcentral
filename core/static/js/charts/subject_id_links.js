$(document).ready(function(){
    $(".student_subjectroom_performance_link").click(function(){
        var student_id = $(this).parent('td').parent('tr').find(".student_id").text();
        var subjectroom_id= $("#subjectroom_id").text();
        if ($("#student_subjectroom_popup").length > 0) {
            $.getJSON(CHART_ENDPOINT + "student/" + student_id + "/" + subjectroom_id, function (single_subjectroom_data) {
                if (single_subjectroom_data.listing.length == 0) {
                    $('#single_subjectroom_bargraph_popup').html(NO_DATA_IMG);
                    return;
                }

                var student_subjectroom_performance_data = [
                    ['Topic', 'Student\'s Score', 'Class Average']
                ];
                for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                    var subjectroom_assignment = single_subjectroom_data.listing[j];
                    student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
                }
                draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, true, true);
            });
            $("#subjectroom_performance_popup").modal('show');
        }
    });
});