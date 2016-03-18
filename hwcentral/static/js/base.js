
$(document).ready(function () {
    $("select.chosen-select").chosen({width: "400px"});
    $("select.chosen-smaller").not('.chosen-no-search').chosen({width: "300px"});
    $("select.chosen-no-search").not('.chosen-smaller').chosen({disable_search: true, width: "400px"});
    $("select.chosen-no-search.chosen-smaller").chosen({disable_search: true, width: "300px"});

    // hack - make footer expand to over full width (problem is min-width on auth body forces wider overall page width,
    // but the container of auth_body, base-body does not grow with it, leaving the footer narrower)
    window.setInterval(refreshFooterWidth, 2000);
});

var BODY_WIDTH = null;
function refreshFooterWidth() {
    var body_width = Math.max($("#base_body").outerWidth(), $("#auth_body").outerWidth());
    if (body_width != BODY_WIDTH) {
        BODY_WIDTH = body_width;
        $("#footer").css("width", String(body_width).concat("px"));
    }
}
