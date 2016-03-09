$(document).ready(function () {

    $('.smooth-scroll-link').on('click', function (event) {
        event.preventDefault();
        $('body,html').animate({
                scrollTop: $($.attr(this, 'href')).offset().top
            }, 700
        );
    });
});