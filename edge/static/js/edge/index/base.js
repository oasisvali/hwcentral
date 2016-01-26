var EDGE_ENDPOINT = '/edge/'

function initialize_concepts_table() {
    $("#table-row").html("<table class='reportcard table table-condensed table-striped' id='concepts-table'><thead><tr><th>Concept</th><th>Score</th></tr></thead><tbody></tbody></table>");
}

function reset() {
    $("#result-row").addClass('hidden');
    $("#loader-row").addClass('hidden');

    $('.tag-badge').each(function () {
        var $holder = $($(this).children('div')[0]);
        $($holder.children("span.title-holder")[0]).empty();
        $($holder.children("span.badge-val")[0]).empty();

        $holder.removeClass();
        $holder.prop('title', '');
        $($holder.children('span')[0]).removeClass();
    });

    $("#visualization-row .pane").empty();

    $("#questions-row").empty();
    $("#questions-holder").addClass('hidden');

    $("#table-row").empty();
}

function loading() {
    $('#loader-row').removeClass('hidden');
}

function show_data(data) {

    render_special_tags(data.application, data.conceptual, data.critical);
    draw_panes(data.positive, data.negative);
    fill_concepts_table(data.tablerows);

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

function draw_panes(positive, negative) {

    draw_pane(positive, "#positive-col > .pane", "success", "thumbs-up");
    draw_pane(negative, "#negative-col > .pane", "danger", "thumbs-down");
}

function truncate_concept(title) {
    if (title.length > 30) {
        return $.trim(title.substring(0, 27)) + "...";
    }
    return title;
}

function render_badge(title, score, className, glyphicon) {
    return "<div class='tag-badge'><div title='" + title + "' class='" + className + "'><span class='glyphicon glyphicon-" + glyphicon + "'></span><span class='title-holder'>" + truncate_concept(title) + "</span><span class='badge-val'>" + score + "</span></div></div>";
}

function draw_pane(elems, targetId, className, glyphicon) {
    var $target = $(targetId);
    if (elems.length == 0) {
        $target.html("<div class='insufficient-data'><b>Insufficient Data</b><div>Check back after solving some more assignments</div></div>");
        return;
    }

    for (var i = 0; i < elems.length; i++) {
        $target.append(render_badge(elems[i].title, elems[i].score, className, glyphicon));
    }
}

function render_special_tags(application, conceptual, critical) {
    $($("#application").children("span.title-holder")[0]).text(application.title);
    $($("#conceptual").children("span.title-holder")[0]).text(conceptual.title);
    $($("#critical").children("span.title-holder")[0]).text(critical.title);

    $($("#application").children("span.badge-val")[0]).text(application.score);
    $($("#conceptual").children("span.badge-val")[0]).text(conceptual.score);
    $($("#critical").children("span.badge-val")[0]).text(critical.score);

    $(".tag-badge").each(function () {
        var $holder = $($(this).children("div")[0]);
        var val = $($holder.children("span.badge-val")[0]).text();
        if (val === "---") {
            val = NaN;
        }
        else {
            val = parseInt(val.substring(0, (val.length) - 1));
        }

        if (isNaN(val)) {
            $holder.addClass("unknown");
            $holder.prop('title', 'Insufficient Data! Solve more assignments');
        }
        else {
            $glyphicon = $($holder.children('span')[0]);
            if (val >= 80) {
                $holder.addClass("success");
                $glyphicon.addClass('glyphicon glyphicon-thumbs-up');
            }
            else if (val > 40) {
                $holder.addClass("warning");
                $glyphicon.addClass('glyphicon glyphicon-record');
            }
            else {
                $holder.addClass("danger");
                $glyphicon.addClass('glyphicon glyphicon-thumbs-down');
            }
        }
    });
}