var EDGE_ENDPOINT = '/edge/'

google.load('visualization', '1', {
    packages: ['corechart', 'bar']
});

function initialize_concepts_table() {
    $("#table-row").html("<table class='reportcard table table-condensed table-striped' id='concepts-table'><thead><tr><th>Concept</th><th>Score</th></tr></thead><tbody></tbody></table>");
}

function reset() {
    $("#result-row").addClass('hidden');
    $("#loader-row").addClass('hidden');

    $(".badge-val").empty();

    $("#positive-pane").empty();
    $("#negative-pane").empty();

    $("#questions-row").empty();

    $("#table-row").empty();
}

function loading() {
    $('#loader-row').removeClass('hidden');
}

function show_data(data) {

    render_special_tags(data.application, data.conceptual, data.critical);
    draw_chart(data.positive, data.negative);
    fill_concepts_table(data.tablerows);

    if (data.questions) {
        render_questions(data.questions);
    }

    $('#loader-row').addClass('hidden');
    $("#result-row").removeClass('hidden');
}

function fill_concepts_table(tablerows) {
    initialize_concepts_table();
    $tbody = $("#concepts-table > tbody");
    if (tablerows.length == 0) {
        $tbody.html("<tr><td>No Data Available</td></tr>");
    }
    else {
        for (var i = 0; i < tablerows.length; i++) {
            $tbody.append("<tr><td>" + tablerows[i].title + "</td><td>" + tablerows[i].score + "</td></tr>")
        }
    }
    $('#concepts-table').dataTable({
        "order": []
    });
}

function draw_chart(positive, negative) {

    draw_pane(positive, "positive-pane", "lightgreen");
    draw_pane(negative, "negative-pane", "lightcoral");
}

function draw_pane(elems, targetId, color) {
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
}

function render_special_tags(application, conceptual, critical) {
    $("#application > .badge-val").html(application + "%");
    $("#conceptual > .badge-val").html(conceptual + "%");
    $("#critical > .badge-val").html(critical + "%");

    $(".tag-badge").each(function () {
        var $holder = $($(this).children("div")[0]);
        $holder.removeClass();
        $holder.prop('title', '');
        var val = parseInt($($holder.children("span")[0]).html());

        if (isNaN(val)) {
            $holder.addClass("unknown");
            $holder.prop('title', 'Insufficient Data! Solve more assignments');
        }
        else {
            if (val >= 70) {
                $holder.addClass("success");
            }
            else if (val > 30) {
                $holder.addClass("warning");
            }
            else {
                $holder.addClass("danger");
            }
        }
    });
}