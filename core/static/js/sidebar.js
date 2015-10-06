$(document).ready(function () {
    // Script to change sidebar height based on length of doc

    var refreshDocHeight = function () {
        var h = $("#auth_body").outerHeight();
        var s = String(h).concat("px");
        $("#sidebar").css("min-height", s);
    };

    window.setInterval(refreshDocHeight, 500);
});