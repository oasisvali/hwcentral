var COLUMN_HEIGHT = null;

$(document).ready(function () {
    // Script to change left column height based on height of right column
    window.setInterval(refreshColumnHeight, 2000);
});


// TODO: this code is similar to sidebar height refresh
function refreshColumnHeight() {
    var column_height = $("#horizontaldiv3 #drivercolumn").outerHeight();
    if (column_height != COLUMN_HEIGHT) {
        COLUMN_HEIGHT = column_height;
        $("#horizontaldiv3 #drivencolumn").css("min-height", String(column_height).concat("px")); //setting min-height instead of height since the driven can have content longer than driver column
    }
};