$(document).ready(function () {
    // load the announcements data into the container
    $.getJSON(AJAX_ENDPOINT + "announcements/", function (announcements_data) {
        var formatted_announcements = "<li>No Recent Announcements...</li>";
        if (announcements_data.length > 0) {
            formatted_announcements = "";
            for(var i = 0; i<announcements_data.length; i++) {
                var announcement_row = announcements_data[i];
                formatted_announcements += "<li><div><span class='announcement_source'>" + announcement_row.source + "</span><span class='announcement_timestamp'>" + announcement_row.timestamp + "</span></div><div class='announcement_message'>" + announcement_row.message + "</div></li>";
            }
        }
        $("#announcements_container").html(formatted_announcements);
    });
});