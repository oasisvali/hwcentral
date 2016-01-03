if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert("We have detected that you are using Homework Central on a mobile device. If you are on an android device, we recommend downloading our application Homework Central from the play store. For an optimal experience, please use Homework Central on a computer or laptop.");
}

$(document).ready(function () {

    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('.reportcard').dataTable({
        "orderCellsTop": true
    });

    $('.assignment_table').dataTable({
        "order": []
    });
});



