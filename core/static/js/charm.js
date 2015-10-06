$(document).ready(function () {
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

$(window).scroll(function(){
    var $footer = $('#footer');
    var $charm = $('.charm');
    var footerTopPos = $footer.offset().top;
    var footerHeight = $footer.outerHeight();
    var charmBottomPos = $charm.offset().top + $charm.outerHeight();

    var footerCharmGap = footerTopPos - charmBottomPos;

    var jumpThreshold = 15;

    if (footerCharmGap < jumpThreshold) {
        $('.charm').css('bottom', (footerHeight + (jumpThreshold * 2) - 1) + 'px');
    }
    if (footerCharmGap > (footerHeight + (jumpThreshold * 2))) {
        $('.charm').css('bottom', 25 + 'px');
    }
});
