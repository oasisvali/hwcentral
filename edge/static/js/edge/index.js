var EDGE_ENDPOINT = '/edge/'

google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

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
    $("#note").addClass('.hidden');
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
        if (student_data.positive.length == 0 && student_data.negative.length == 0) {
            no_data_panes();
        }
        else {
            // draw chart
            draw_advanced_chart_p(student_data.positive);
            draw_advanced_chart_n(student_data.negative);
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
                if (chart_data.positive.length == 0 && chart_data.negative.length == 0) {
                    no_data_panes();
                }
                else {
                    // draw chart
                    draw_advanced_chart_p(chart_data.positive);
                    draw_advanced_chart_n(chart_data.negative);
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
                if (child_data.positive.length == 0 && child_data.negative.length == 0) {
                    no_data_panes();
                }
                else {
                    // draw chart
                    draw_advanced_chart_p(child_data.positive);
                    draw_advanced_chart_n(child_data.negative);
                }
            });
        }
    });
}

function draw_advanced_chart_p(data) {
    draw_advanced_chart(data, 'positive-pane', 'Strengths');
}

function draw_advanced_chart_n(data) {
    draw_advanced_chart(data, 'negative-pane', 'Weaknesses');
}

function draw_advanced_chart(elems, targetId, title) {
    if (elems.length == 0) {
        $("#" + targetId).html('<b>No ' + title + ' found</b><div>Check back after solving some more assignments</div>');
        return;
    }

    var arrayData = [['ScoreType', 'Absolute Score', 'Relative Score', {role: 'annotation'}]];
    for (var i = 0; i < elems.length; i++) {
        arrayData.push([elems[i].title, elems[i].basic, elems[i].relative, '']);
    }

    var data = new google.visualization.arrayToDataTable(arrayData);

    var options = {
        title: title,
        width: 400,
        height: 600,
        legend: {position: 'top', maxLines: 2},
        bar: {groupWidth: '75%'},
        colors: ['#f1ca3a', '#1c91c0'],
        isStacked: true
    };

    var chart = new google.visualization.BarChart(document.getElementById(targetId));
    chart.draw(data, options);

    $("#note").removeClass('hidden');
}