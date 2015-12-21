if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert("Sorry ! Homework Central does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {

    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('.reportcard').dataTable();

    $('.assignment_table').dataTable();
});



