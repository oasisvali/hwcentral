var CHART_ENDPOINT="http://localhost:8000/chart/";
$(document).ready(function () {
    $('#announcement_table').dataTable({
        "pagingType":"full_numbers"
    });
    $('#active_assignment_table').dataTable();
    $('#graded_assignment_table').dataTable();
    $(function(){
        $("#menu").accordion();
    });
});