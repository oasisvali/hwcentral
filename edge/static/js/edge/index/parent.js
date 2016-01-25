$(document).ready(function () {
    setup_parent();
});

function extract_student_id() {
    return parseInt($("#child-select").val());
}

function extract_subjectroom_pk() {
    return parseInt($("#subject-select-holder > select").val());
}

function setup_parent() {
    // enable-disable go button based on subjectroom select state
    $('#child-select').on('change', function () {
        $("#subject-select-holder").empty();
        var student_id = extract_student_id();
        if (student_id > 0) {
            $("#subject-select-holder").html($("#subject-select-" + student_id)[0].outerHTML);
            $("#subject-select-holder > select").chosen({disable_search: true, width: "300px"});
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
        var student_id = extract_student_id();
        var endpoint = EDGE_ENDPOINT + 'student/' + student_id + '/' + subjectroom_pk;

        reset();
        loading();

        $.getJSON(endpoint, function (data) {
            show_data(data);
        });

    });
}