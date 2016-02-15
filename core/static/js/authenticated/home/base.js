$(document).ready(function () {
    // set up handler for tutorial click
    $("#tutorial-button").click(function () {
        $("#tutorial_modal").modal('show');
    });
    // hnadler to stop video on modal close
    $('#tutorial_modal').on('hidden.bs.modal', function () {
        var src = $("#tutorial_modal #modal-vid").attr("src");
        $("#tutorial_modal #modal-vid").attr("src", "");
        $("#tutorial_modal #modal-vid").attr("src", src);
    });
});