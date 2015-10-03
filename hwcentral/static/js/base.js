$(document).ready(function () {
    $("select").addClass("chosen-select");
    if ($('#skip-global-chosen').length === 0) {
        $(".chosen-select").chosen({width: "400px"});
    }
});
