$(document).ready(function () {
    //duration of the top scrolling animation (in ms)
    scroll_top_duration = 700,
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
  var footerTopPos = $('#footer').offset().top;
  var savebuttonBottomPos = $('.charm').offset().top + $('.charm').outerHeight();

  if(savebuttonBottomPos >= footerTopPos) {
    $('.charm').css('position', 'absolute');
  }

  else{
    $('.charm').css ('position','fixed');
  }
});
