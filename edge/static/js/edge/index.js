var EDGE_ENDPOINT = '/edge/'

$(document).ready(function () {
    // call the appropriate function based on the kind of page this is
    if ($('#child-select').length > 0) {
        setup_parent();
    }
    else if ($('#subjectroom-select').length > 0) {
        setup_teacher();
    }
    else {
        setup_student();
    }
});

function reset_panes() {
    $("#positive-pane").empty();
    $("#negative-pane").empty();
    $("#positive-pane").html($("#chart_loader_holder").html());
}

function no_data_panes() {
    $("#positive-pane").empty();
    $("#negative-pane").empty();
    $("#positive-pane").html(NO_DATA_IMG);
}

function setup_student() {
    // put chart loader in the panes
    reset_panes();
    // make ajax request
    var student_id = extract_id($("#user_id"));
    $.getJSON(EDGE_ENDPOINT + "student/" + student_id, function (student_data) {
        if (student_data.length == 0) {
            no_data_panes();
        }
        else {
            // draw chart
            draw_advanced_chart(student_data.positive, "positive-pane");
            draw_advanced_chart(student_data.negative, "negative-pane");
        }
    });
}

function setup_teacher() {
    // enable-disable go button based on subjectroom select state
    $('#subjectroom-select').on('change', function () {
        $("#student-select-holder").empty();
        var subjectroom_pk = parseInt($("#subjectroom-select").val());
        if (subjectroom_pk > 0) {
            $("#student-select-holder").html($("#student-select-" + subjectroom_pk)[0].outerHTML);
            $("#student-select-holder > select").chosen({width: '300px'});
            $("#go-button").removeClass("disabled_action_button");
        }
        else {
            $("#go-button").addClass("disabled_action_button");
        }
    });
    // on go button click make ajax request
    $("#go-button").on('click', function () {
        var subjectroom_pk = parseInt($("#subjectroom-select").val());
        if (subjectroom_pk > 0) {
            var endpoint = EDGE_ENDPOINT;
            if (parseInt($("#student-select-holder > select").val()) === 0) {
                endpoint += 'subject/' + $("#subjectroom-select").val();
            }
            else {
                endpoint += 'student/' + $("#student-select-holder > select").val();
            }
            reset_panes();
            $.getJSON(endpoint, function (chart_data) {
                if (chart_data.length === 0) {
                    no_data_panes();
                }
                else {
                    // draw chart
                    draw_advanced_chart(chart_data.positive, "positive-pane");
                    draw_advanced_chart(chart_data.negative, "negative-pane");
                }
            });
        }
    });
}

function setup_parent() {
    // enable-disable go button based on child select state
    $('#child-select').on('change', function () {
        var child_pk = parseInt($("#child-select").val());
        if (child_pk > 0) {
            $("#go-button").removeClass("disabled_action_button");
        }
        else {
            $("#go-button").addClass("disabled_action_button");
        }
    });
    // on go button click make ajax request
    $("#go-button").on('click', function () {
        var child_pk = parseInt($("#child-select").val());
        if (child_pk > 0) {
            var endpoint = EDGE_ENDPOINT + 'student/' + child_pk;
            reset_panes();
            $.getJSON(endpoint, function (child_data) {
                if (child_data.length === 0) {
                    no_data_panes();
                }
                else {
                    // draw chart
                    draw_advanced_chart(child_data.positive, "positive-pane");
                    draw_advanced_chart(child_data.negative, "negative-pane");
                }
            });
        }
    });
}