$(document).ready(function () {
    setup_student();
});

function extract_subjectroom_pk() {
    return parseInt($("#subject-select").val());
}

function setup_student() {
    var student_id = extract_id($("#user_id"));

    // enable-disable go button based on subject select state
    $('#subject-select').on('change', function () {
        var subjectroom_pk = extract_subjectroom_pk();
        if (subjectroom_pk > 0) {
            $("#go-button").removeClass("disabled_action_button");
        }
        else {
            $("#go-button").addClass("disabled_action_button");
        }
    });

    // on go button click make ajax request
    $("#go-button").on('click', function () {
        if ($(this).hasClass('disabled_action_button')) {
            return;
        }

        var subjectroom_pk = extract_subjectroom_pk();
        var endpoint = EDGE_ENDPOINT + 'student/' + student_id + '/' + subjectroom_pk;

        reset();
        loading();

        $.getJSON(endpoint, function (data) {
            show_data(data);
        });
    });
}