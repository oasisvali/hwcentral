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
