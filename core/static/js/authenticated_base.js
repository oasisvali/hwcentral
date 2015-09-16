var DATATABLES_DEBUG=false;
var CHART_ENDPOINT="/chart/";
var MIN_DIMENSION=600;
if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert ("Sorry ! HWCentral does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {

    $('.disable_clipboard').bind("cut copy paste",function(e) {
      e.preventDefault();
    });

    if($("#toast").length){
      $("#success_modal").modal('show');
    }
 
    $('#announcement_table').dataTable({
        "pagingType":"full_numbers"
    });
    $('.reportcard').dataTable();
    $('.assignment_table').dataTable();
    $('#teachers_table').dataTable();
    $(function(){
        $("#menu").accordion();
    });
})


