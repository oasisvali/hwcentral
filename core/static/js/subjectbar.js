$(document).ready(function () {
	$('.chart').hide();
    $('#linegraph1').show();
    $('.sub').click(function(){
        $('.chart').hide();
        $('#linegraph'+$(this).attr('target')).show();
    });
    for (var i=0;i<test.breakdown_listing.length;i++){
        $("#subjectbar").append(
            "<li class=sub> <a>"+test.breakdown_listing[i].subject+"</a></li> ");
        }
    $('ul.nav-tabs li a').click(function (e) {
        $('ul.nav-tabs li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    }); 
});