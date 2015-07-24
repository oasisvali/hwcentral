var CHART_ENDPOINT="http://localhost:8000/chart/";
var MIN_DIMENSION=600;
console.log(screen.width);
console.log(screen.height);
if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert ("Sorry ! HWCentral does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {
    $(document).tooltip();
    $('#announcement_table').dataTable({
        "pagingType":"full_numbers"
    });
    $('#active_assignment_table').dataTable();
    $('#graded_assignment_table').dataTable();
    $('#teacher_listing').dataTable();
    $(function(){
        $("#menu").accordion();
    });
})
