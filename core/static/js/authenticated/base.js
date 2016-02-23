$(document).ready(function () {

    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('.reportcard').dataTable({
        "orderCellsTop": true
    });

    $('.assignment_table').dataTable({
        "order": []
    });

    // set up handler for help click
    $("#help-button").click(function () {
        $("#help_modal").modal('show');
    });

    // handler to stop video on modal close
    $('.video-modal').on('hidden.bs.modal', function () {
        var $vid = $($(this).find("#modal-vid")[0]);
        var src = $vid.attr("src");
        $vid.attr("src", "");
        $vid.attr("src", src);
    });
});



