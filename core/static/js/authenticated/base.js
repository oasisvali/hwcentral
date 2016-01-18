$(document).ready(function () {

    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('.reportcard').dataTable({
        "orderCellsTop": true
    });

    $('.assignment_table').dataTable({
        "order": []
    });

    $('.do-datatable').dataTable({
        "order": []
    });
});



