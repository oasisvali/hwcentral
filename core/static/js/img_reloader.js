$(document).ready(function () {
    MAX_TRIES = 3;

    // set the callback for all images that fail
    $('img').error(function () {
        $img = $(this);

    });

    //duration of the top scrolling animation (in ms)
    var scroll_top_duration = 700,
    //grab the "back to top" link
        $back_to_top = $('#charm-top');

    //smooth scroll to top
    $back_to_top.on('click', function (event) {
        event.preventDefault();
        $('body,html').animate({
                scrollTop: 0
            }, scroll_top_duration
        );
    });
});