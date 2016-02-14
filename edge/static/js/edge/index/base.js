var EDGE_ENDPOINT = '/edge/'

function render_disabled_select_in_holder(select_holder_id) {
    $("#" + select_holder_id).html($("#disabled-select")[0].outerHTML);
    $("#" + select_holder_id + " > select").chosen({
        disable_search: true,
        width: "300px"
    });
}

function initialize_concepts_table() {
    $("#table-row").html("<table class='reportcard table table-condensed table-striped' id='concepts-table'><thead><tr><th>Concept</th><th>Score</th></tr></thead><tbody></tbody></table>");
}

function reset() {
    $("#result-row").addClass('hidden');
    $("#loader-row").addClass('hidden');

    $('#badge-row .tag-badge').each(function () {
        var $holder = $($(this).children('div')[0]);
        $($holder.children(".title-holder")[0]).empty();
        $($holder.children(".badge-val")[0]).empty();

        $holder.removeClass();
        $holder.prop('title', '');
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
    if (title.length > 25) {
        return $.trim(title.substring(0, 22)) + "...";
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
    $($("#application").children(".title-holder")[0]).text(application.title);
    $($("#conceptual").children(".title-holder")[0]).text(conceptual.title);
    $($("#critical").children(".title-holder")[0]).text(critical.title);

    $($("#application").children(".badge-val")[0]).text(application.score);
    $($("#conceptual").children(".badge-val")[0]).text(conceptual.score);
    $($("#critical").children(".badge-val")[0]).text(critical.score);

    $("#badge-row .tag-badge").each(function () {
        var $holder = $($(this).children("div")[0]);
        var val = $($holder.children(".badge-val")[0]).text();
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
            if (val >= 80) {
                $holder.addClass("success");
            }
            else if (val > 40) {
                $holder.addClass("warning");
            }
            else {
                $holder.addClass("danger");
            }
        }
    });
}