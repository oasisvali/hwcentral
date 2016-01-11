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
    $("select").not(".skip-chosen").not(".chosen-no-search").not('.chosen-smaller').chosen({width: "400px"});
    $("select.chosen-smaller").not('.chosen-no-search').chosen({width: "300px"});
    $("select.chosen-no-search").not('.chosen-smaller').chosen({disable_search: true, width: "400px"});
    $("select.chosen-no-search.chosen-smaller").chosen({disable_search: true, width: "300px"});

    // hack - make footer expand to over full width (problem is min-width on auth body forces wider overall page width,
    // but the container of auth_body, base-body does not grow with it, leaving the footer narrower)
    window.setInterval(refreshFooterWidth, 2000);
});

var BODY_WIDTH = null;
function refreshFooterWidth() {
    var body_width = Math.max($("#base_body").outerWidth(), $("#auth_body").outerWidth());
    if (body_width != BODY_WIDTH) {
        BODY_WIDTH = body_width;
        $("#footer").css("width", String(body_width).concat("px"));
    }
}
