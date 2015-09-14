
$(document).ready(function() {   
  function animateImages() {
    $('#img13').animate({'opacity':1.0},6000).animate({'opacity':0.0},6000, animateImages2); 
    $('#img22').animate({'opacity':1.0},6000).delay(5200).animate({'opacity':0.0},7000); 
    $('#img30').animate({'opacity':1.0},6000).delay(2500).animate({'opacity':0.0},6000); 
    $('#img23').animate({'opacity':1.0},6000).delay(5900).animate({'opacity':0.0},7000); 
    $('#img28').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},6000); 
    $('#img6').animate({'opacity':1.0},6000).delay(5200).animate({'opacity':0.0},6000); 
    $('#img4').animate({'opacity':1.0},6000).delay(4200).animate({'opacity':0.0},6000); 
    $('#img16').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},6000); 
  }


function animateImages2() {
    $('#img31').animate({'opacity':1.0},6000).animate({'opacity':0.0},6000, animateImages3); 
    $('#img11').animate({'opacity':1.0},6000).delay(5900).animate({'opacity':0.0},8000); 
    $('#img32').animate({'opacity':1.0},6000).delay(6500).animate({'opacity':0.0},8000); 
    $('#img18').animate({'opacity':1.0},6000).delay(1900).animate({'opacity':0.0},6000); 
    $('#img3').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},6000);
    $('#img25').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},6000); 
    $('#img2').animate({'opacity':1.0},6000).delay(5200).animate({'opacity':0.0},6000);
    $('#img12').animate({'opacity':1.0},6000).delay(3200).animate({'opacity':0.0},6000); 
    $('#img7').animate({'opacity':1.0},6000).delay(3000).animate({'opacity':0.0},6000); 
  }

  function animateImages3() {
    $('#img14').animate({'opacity':1.0},6000).animate({'opacity':0.0},6000, animateImages); 
    $('#img17').animate({'opacity':1.0},6000).delay(1500).animate({'opacity':0.0},6000); 
    $('#img21').animate({'opacity':1.0},6000).delay(3900).animate({'opacity':0.0},6000); 
    $('#img5').animate({'opacity':1.0},6000).delay(5200).animate({'opacity':0.0},6000);
    $('#img9').animate({'opacity':1.0},6000).delay(200).animate({'opacity':0.0},6000);
    $('#img27').animate({'opacity':1.0},6000).delay(6200).animate({'opacity':0.0},8000);
    $('#img26').animate({'opacity':1.0},6000).delay(1200).animate({'opacity':0.0},6000);
    $('#img20').animate({'opacity':1.0},6000).delay(3200).animate({'opacity':0.0},6000);
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