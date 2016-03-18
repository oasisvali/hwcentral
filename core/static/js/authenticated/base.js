// check if we are within app context
if (typeof HWCentralAppContext !== 'undefined') {
    // do app-specific setup
}
else {
    // if android device, show message and hard redirect to play store
    if (/Android/i.test(navigator.userAgent)) {
        alert("It appears you are using an android device! Press OK to download the Homework Central app from the Play Store.");
        window.location = "https://play.google.com/store/apps/details?id=com.smartsourcer.hwcentral.homeworkcentral&hl=en";
    }
    // else if mobile device show message (only once)
    else if (screen.width <= MIN_DIMENSION || screen.height <= MIN_DIMENSION) {
        var alerted = localStorage.getItem('screen_size_alerted') || '';
        if (alerted != 'yes') {
            alert("It appears you are using a mobile device! If you are on an android device, we recommend downloading the Homework Central app available on the Play Store. For the best user experience, please use Homework Central on a desktop or laptop.");
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



