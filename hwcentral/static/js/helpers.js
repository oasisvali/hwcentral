function extract_id(dom_obj) {
    var id = dom_obj.text().trim();
    if (isNaN(id)) {
        console.error("The extracted id is not a number! HOLDER ->");
        console.error(dom_obj);
        return null;
    }
    return id;
}

function extract_text(dom_obj) {
    var text = dom_obj.text().trim();
    if (text) {
        return text;
    }
    console.error("The extracted text is empty! HOLDER ->");
    console.error(dom_obj);
    return null;
}

// Usage - highlight_effect($("#description-holder"), "#62C2C2");
function highlight_effect(dom_obj, highlight_color) {
    $("<div/>")
        .width(dom_obj.outerWidth())
        .height(dom_obj.outerHeight())
        .css({
            "position": "absolute",
            "left": dom_obj.offset().left,
            "top": dom_obj.offset().top,
            "background-color": highlight_color,
            "opacity": ".7",
            "z-index": "9999999"
        })
        .appendTo('body')
        .fadeOut(1500)
        .queue(function () {
            $(this).remove();
        });
}

function datatables_link_delegate(container_selector, link_selector, handler) {
    /*

     NOTE: Cannot just use .click() as delegate for entire document is required rather than binding to existing elements
     only. This is because datatables paging and search remove and add elements to page dynamically which requires
     handler to be rebound by a delegate.

     */
    $(container_selector).on('click', link_selector, function () {
        handler(this);
    });
}

function make_nonbreaking(string) {
    return string.replace(/ /g, '\u00a0');
}

function render_columnchart_tooltip1(date, topic, completion, label, value) {
    return "<div class='columnchart-tooltip'><div><b>" + make_nonbreaking(topic) + '</b></div><div>' + make_nonbreaking(date) + '</div><div>' + make_nonbreaking(label) + ':&nbsp;<b>' + value + '</b></div><div>Completion:&nbsp;<b>' + completion + '&#37;</b></div></div>';
}

function render_columnchart_tooltip2(topic, label, value) {
    return "<div class='columnchart-tooltip'><div><b>" + make_nonbreaking(topic) + '</b></div><div>' + '</div><div>' + make_nonbreaking(label) + ':&nbsp;<b>' + value + '</b></div></div>';
}

function prep_chart_popup(target) {
    // make sure the target is flushed and loader is shown
    var target_obj = $('#' + target);
    $(target_obj).empty();
    $(target_obj).html($("#chart_loader_holder").html());
}

function capitalize_first_letter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function abbreviate_title(title) {
    var title_words = title.split(" ");
    if (title_words[title_words.length - 1][0] === '(') {
        title_words.pop();
    }

    var number = title_words.pop();
    var dash = title_words.pop();

    for (var i = 0; i < title_words.length; i++) {
        title_words[i] = capitalize_first_letter(title_words[i]);
    }

    var squashed = title_words.join("");
    return squashed.substring(0, 5) + dash + number;
}

function prep_columnchart_data(dataTable, label1, label2, arraydata) {
    dataTable.addColumn('string', 'Topic');
    dataTable.addColumn('number', label1);
    // A column for topic tooltip content
    dataTable.addColumn({type: 'string', role: 'tooltip', p: {html: true}});
    dataTable.addColumn('number', label2);
    // A column for topic tooltip content
    dataTable.addColumn({type: 'string', role: 'tooltip', p: {html: true}});

    var chartRows = [];
    for (var i = 0; i < arraydata.length; i++) {
        var topic = arraydata[i][3];
        var date = arraydata[i][0];
        var completion = arraydata[i][4];

        var tooltip1 = render_columnchart_tooltip1(date, topic, completion, label1, arraydata[i][1]);
        var tooltip2 = render_columnchart_tooltip2(topic, label2, arraydata[i][2]);

        chartRows.push([abbreviate_title(topic), arraydata[i][1], tooltip1, arraydata[i][2], tooltip2]);
    }

    dataTable.addRows(chartRows);
    return dataTable;
}

function full_page_overlay() {  //used by android app for better loading visual
    document.body.innerHTML += "<div class='dim'></div>";
}