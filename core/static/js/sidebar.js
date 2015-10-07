$(document).ready(function () {
    // Script to change sidebar height based on length of doc

    var refreshDocHeight = function () {
        var body_height = $("#auth_body").outerHeight();

        $("#sidebar").css("min-height", String(body_height).concat("px")); //setting min-height instead of height since the sidebar can have content longer than body
    };

    window.setInterval(refreshDocHeight, 500);
});