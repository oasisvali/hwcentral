var BODY_HEIGHT = null;

$(document).ready(function () {
    // Script to change sidebar height based on length of doc
    window.setInterval(refreshSidebarHeight, 500);
});

function refreshSidebarHeight() {
    var body_height = $("#auth_body").outerHeight();
    if (body_height != BODY_HEIGHT) {
        BODY_HEIGHT = body_height;
        $("#sidebar").css("min-height", String(body_height).concat("px")); //setting min-height instead of height since the sidebar can have content longer than body
    }
};