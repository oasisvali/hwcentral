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