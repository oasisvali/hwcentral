$(document).ready(function () {
    if ($('#skip-global-chosen').length === 0) {
        $("select").not(".hidden").addClass("chosen-select");
    }
    $(".chosen-select").chosen({width: "400px"});
});
