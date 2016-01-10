// check if we are within ap context
if (typeof HWCentralAppContext !== 'undefined') {
    // do app-specific setup
}
else {
    if (screen.width <= MIN_DIMENSION || screen.height <= MIN_DIMENSION) {
        var alerted = localStorage.getItem('screen_size_alerted') || '';
        if (alerted != 'yes') {
            alert("It appears you are using Homework Central on a mobile device. If you are on an android device, we recommend downloading the Homework Central app available on the Play Store. For an optimal experience, please use Homework Central on a desktop or laptop.");
            localStorage.setItem('screen_size_alerted', 'yes');
        }
    }
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



