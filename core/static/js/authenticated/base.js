if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert("Sorry ! Homework Central does not support this device (Height: " + screen.height + " Width: " + screen.width + "). To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {

    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('.reportcard').dataTable({
        "orderCellsTop": true
    });

    $('.assignment_table').dataTable();
});



