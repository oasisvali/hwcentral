
$(document).ready(function() {   
  function animateImages() {
    $('#img13').animate({'opacity':1.0},6000).animate({'opacity':0.0},3000, animateImages2); 
    $('#img22').animate({'opacity':1.0},6000).delay(2600).animate({'opacity':0.0},4000); 
    $('#img30').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},3000); 
    $('#img23').animate({'opacity':1.0},6000).delay(2900).animate({'opacity':0.0},4000); 
    $('#img28').animate({'opacity':1.0},6000).delay(600).animate({'opacity':0.0},3000); 
    $('#img6').animate({'opacity':1.0},6000).delay(2600).animate({'opacity':0.0},3000); 
    $('#img4').animate({'opacity':1.0},6000).delay(2100).animate({'opacity':0.0},3000); 
    $('#img16').animate({'opacity':1.0},6000).delay(600).animate({'opacity':0.0},3000); 
  }


function animateImages2() {
    $('#img31').animate({'opacity':1.0},6000).animate({'opacity':0.0},3000, animateImages3); 
    $('#img11').animate({'opacity':1.0},6000).delay(1000).animate({'opacity':0.0},4000); 
    $('#img32').animate({'opacity':1.0},6000).delay(1600).animate({'opacity':0.0},4000); 
    $('#img18').animate({'opacity':1.0},6000).delay(400).animate({'opacity':0.0},3000); 
    $('#img3').animate({'opacity':1.0},6000).delay(300).animate({'opacity':0.0},3000);
    $('#img25').animate({'opacity':1.0},6000).delay(300).animate({'opacity':0.0},3000); 
    $('#img2').animate({'opacity':1.0},6000).delay(1600).animate({'opacity':0.0},3000);
    $('#img12').animate({'opacity':1.0},6000).delay(800).animate({'opacity':0.0},3000); 
    $('#img7').animate({'opacity':1.0},6000).delay(700).animate({'opacity':0.0},3000); 
  }

  function animateImages3() {
    $('#img14').animate({'opacity':1.0},6000).animate({'opacity':0.0},3000, animateImages); 
    $('#img17').animate({'opacity':1.0},6000).delay(700).animate({'opacity':0.0},3000); 
    $('#img21').animate({'opacity':1.0},6000).delay(400).animate({'opacity':0.0},3000); 
    $('#img5').animate({'opacity':1.0},6000).delay(1100).animate({'opacity':0.0},3000);
    $('#img9').animate({'opacity':1.0},6000).delay(100).animate({'opacity':0.0},3000);
    $('#img27').animate({'opacity':1.0},6000).delay(1600).animate({'opacity':0.0},4000);
    $('#img26').animate({'opacity':1.0},6000).delay(300).animate({'opacity':0.0},3000);
    $('#img20').animate({'opacity':1.0},6000).delay(100).animate({'opacity':0.0},3000);
  }

  animateImages();

});

        $(function() {
          $('a[href*=#]:not([href=#])').click(function() {
            if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
                || location.hostname == this.hostname) {

              var target = $(this.hash);
              target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
              if (target.length) {
                $('html,body').animate({
                  scrollTop: target.offset().top
                }, 1000);
                return false;
              }
            }
          });
        });