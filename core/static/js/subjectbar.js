$(document).ready(function () {
	$('ul.nav-tabs li a').click(function (e) {
  		$('ul.nav-tabs li.active').removeClass('active')
  		$(this).parent('li').addClass('active')
})
$('.chart').hide();
$('#linegraph1').show();
 $('.sub').click(function(){
              $('.chart').hide();
              $('#linegraph'+$(this).attr('target')).show();
        });
})