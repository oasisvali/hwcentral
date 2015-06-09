$(document).ready(function(){

  $('.landingimagebox').hover(
  function(){
      $(this).fadeTo(300,'1.0','swing');
   },
   function(){
      $(this).fadeTo(300,'0.5','swing');
   }
);

});