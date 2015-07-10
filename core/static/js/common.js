$(document).ready(function () {
    $('#announcement_table').dataTable({
        'order':[[2]]
    });
    $('#active_assignment_table').dataTable();
    $('#graded_assignment_table').dataTable();
});