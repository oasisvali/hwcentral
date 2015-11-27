$(document).ready(function () {
    //duration of the top scrolling animation (in ms)
    var scroll_top_duration = 700,
        //grab the "back to top" link
        $back_to_top = $('#charm-gotop');

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
    var $charm = $('.charm-bottom');
    var footerTopPos = $footer.offset().top;
    var footerHeight = $footer.outerHeight();
    var charmBottomPos = $charm.offset().top + $charm.outerHeight();

    var footerCharmGap = footerTopPos - charmBottomPos;

    var jumpThreshold = 15;

    if (footerCharmGap < jumpThreshold) {
        $('.charm-bottom').css('bottom', (footerHeight + (jumpThreshold * 2) - 1) + 'px');
        $('.charm-above-bottom').css('bottom', (footerHeight + (jumpThreshold * 2) - 1 + 60) + 'px');
    }
    if (footerCharmGap > (footerHeight + (jumpThreshold * 2))) {
        $('.charm-bottom').css('bottom', 25 + 'px');
        $('.charm-above-bottom').css('bottom', (25 + 60) + 'px');
    }
});
