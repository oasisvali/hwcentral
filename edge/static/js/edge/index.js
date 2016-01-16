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

function reset() {
    $("#result-row").addClass('hidden');
    $("#positive-pane").empty();
    $("#negative-pane").empty();
    $("#img-holder").removeClass("hidden");
    $("#img-holder").html($("#chart_loader_holder").html());
}

function no_data() {
    $("#img-holder").html(NO_DATA_IMG);
}

function setup_student() {
    // put chart loader in the panes
    reset();
    // make ajax request
    var student_id = extract_id($("#user_id"));
    $.getJSON(EDGE_ENDPOINT + "student/" + student_id, function (student_data) {
        if (student_data.positive.length == 0 && student_data.negative.length == 0) {
            no_data();
        }
        else {
            // draw chart
            fill_categories(student_data.application, student_data.conceptual, student_data.critical);
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
            reset();
            $.getJSON(endpoint, function (chart_data) {
                if (chart_data.positive.length == 0 && chart_data.negative.length == 0) {
                    no_data();
                }
                else {
                    // draw chart
                    fill_categories(chart_data.application, chart_data.conceptual, chart_data.critical);
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
            reset();
            $.getJSON(endpoint, function (child_data) {
                if (child_data.positive.length == 0 && child_data.negative.length == 0) {
                    no_data();
                }
                else {
                    // draw chart
                    fill_categories(child_data.application, child_data.conceptual, child_data.critical);
                    draw_advanced_chart_p(child_data.positive);
                    draw_advanced_chart_n(child_data.negative);
                }
            });
        }
    });
}

function draw_advanced_chart_p(data) {
    draw_advanced_chart(data, 'positive-pane', 'lightgreen');
}

function draw_advanced_chart_n(data) {
    draw_advanced_chart(data, 'negative-pane', 'lightcoral');
}

function draw_advanced_chart(elems, targetId, color) {
    $("#img-holder").addClass('hidden');
    $("#result-row").removeClass('hidden');

    if (elems.length == 0) {
        $("#" + targetId).html("<div class='insufficient-data'><b>Insufficient Data</b><div>Check back after solving some more assignments</div></div>");
        return;
    }

    var arrayData = [['Concept', 'Score']];
    for (var i = 0; i < elems.length; i++) {
        arrayData.push([elems[i].title, elems[i].score]);
    }

    var data = new google.visualization.arrayToDataTable(arrayData);

    var options = {
        width: 375,
        height: 500,
        legend: {position: 'none'},
        bar: {groupWidth: '75%'},
        colors: [color],
        hAxis: {
            title: "Score",
            minValue: 0,
            maxValue: 99
        },
        chartArea: {left: '30%', width: '80%', height: '80%'}
    };

    var chart = new google.visualization.BarChart(document.getElementById(targetId));
    chart.draw(data, options);

    $("#title-row").removeClass('hidden');
}

function fill_categories(application, conceptual, critical) {
    $("#application-val").html(application);
    $("#conceptual-val").html(conceptual);
    $("#critical-val").html(critical);

    $("#application-score").removeClass();
    if (application == null) {
        $("#application-score").addClass("score btn-warning");
    }
    else if (parseInt(application) > 50) {
        $("#application-score").addClass("score btn-success");
    }
    else {
        $("#application-score").addClass("score btn-danger");
    }

    $("#conceptual-score").removeClass();
    if (conceptual == null) {
        $("#conceptual-score").addClass("score btn-warning");
    }
    else if (parseInt(conceptual) > 50) {
        $("#conceptual-score").addClass("score btn-success");
    }
    else {
        $("#conceptual-score").addClass("score btn-danger");
    }

    $("#critical-score").removeClass();
    if (critical == null) {
        $("#critical-score").addClass("score btn-warning");
    }
    else if (parseInt(critical) > 50) {
        $("#critical-score").addClass("score btn-success");
    }
    else {
        $("#critical-score").addClass("score btn-danger");
    }
}