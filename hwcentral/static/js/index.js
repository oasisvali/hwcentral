var SHOW = {'opacity': 0.85};
var HIDE = {'opacity': 0.0};

var FADE_IN_MS = 6000;
var FADE_OUT_L_MS = 4000;   //long fade
var FADE_OUT_S_MS = 3000;   // short

function animateImages() {
    $('#img1').animate(SHOW, FADE_IN_MS).animate(HIDE, FADE_OUT_S_MS, animateImages2);
    $('#img2').animate(SHOW, FADE_IN_MS).delay(2600).animate(HIDE, FADE_OUT_L_MS);
    $('#img3').animate(SHOW, FADE_IN_MS).delay(1200).animate(HIDE, FADE_OUT_S_MS);
    $('#img4').animate(SHOW, FADE_IN_MS).delay(2900).animate(HIDE, FADE_OUT_L_MS);
    $('#img5').animate(SHOW, FADE_IN_MS).delay(600).animate(HIDE, FADE_OUT_S_MS);
    $('#img6').animate(SHOW, FADE_IN_MS).delay(2600).animate(HIDE, FADE_OUT_S_MS);
    $('#img7').animate(SHOW, FADE_IN_MS).delay(2100).animate(HIDE, FADE_OUT_S_MS);
    $('#img8').animate(SHOW, FADE_IN_MS).delay(600).animate(HIDE, FADE_OUT_S_MS);
}

function animateImages2() {
    $('#img9').animate(SHOW, FADE_IN_MS).animate(HIDE, FADE_OUT_S_MS, animateImages3);
    $('#img10').animate(SHOW, FADE_IN_MS).delay(1000).animate(HIDE, FADE_OUT_L_MS);
    $('#img11').animate(SHOW, FADE_IN_MS).delay(1600).animate(HIDE, FADE_OUT_L_MS);
    $('#img12').animate(SHOW, FADE_IN_MS).delay(400).animate(HIDE, FADE_OUT_S_MS);
    $('#img13').animate(SHOW, FADE_IN_MS).delay(300).animate(HIDE, FADE_OUT_S_MS);
    $('#img14').animate(SHOW, FADE_IN_MS).delay(300).animate(HIDE, FADE_OUT_S_MS);
    $('#img15').animate(SHOW, FADE_IN_MS).delay(1600).animate(HIDE, FADE_OUT_S_MS);
    $('#img16').animate(SHOW, FADE_IN_MS).delay(800).animate(HIDE, FADE_OUT_S_MS);
    $('#img17').animate(SHOW, FADE_IN_MS).delay(700).animate(HIDE, FADE_OUT_S_MS);
}

function animateImages3() {
    $('#img18').animate(SHOW, FADE_IN_MS).animate(HIDE, FADE_OUT_S_MS, animateImages);
    $('#img19').animate(SHOW, FADE_IN_MS).delay(700).animate(HIDE, FADE_OUT_S_MS);
    $('#img20').animate(SHOW, FADE_IN_MS).delay(400).animate(HIDE, FADE_OUT_S_MS);
    $('#img21').animate(SHOW, FADE_IN_MS).delay(1100).animate(HIDE, FADE_OUT_S_MS);
    $('#img22').animate(SHOW, FADE_IN_MS).delay(100).animate(HIDE, FADE_OUT_S_MS);
    $('#img23').animate(SHOW, FADE_IN_MS).delay(1600).animate(HIDE, FADE_OUT_L_MS);
    $('#img24').animate(SHOW, FADE_IN_MS).delay(300).animate(HIDE, FADE_OUT_S_MS);
    $('#img25').animate(SHOW, FADE_IN_MS).delay(100).animate(HIDE, FADE_OUT_S_MS);
}

$(document).ready(function() {


    animateImages();

    $('#learnmorebutton_link').on('click', function (event) {
        event.preventDefault();
        $('body,html').animate({
                scrollTop: $( $.attr(this, 'href') ).offset().top
            }, 700
        );
    });

});