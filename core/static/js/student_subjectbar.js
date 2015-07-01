$('#printable_report').hide();
$(document).ready(function() {

    for (var i = 0; i < studentdata.breakdown_listing.length; i++) {
        $("#subjectbar").append(
            "<li class=sub target=" + i + "><a>" + studentdata.breakdown_listing[i].subject + "</a></li> ");
        $("#subject_performance").append(
            "<div id='subject_performance" + i + "' class='chart scroll'></div>");
    }
    
    
    $('.chart').hide();
    $('#performance_bargraph').show();
    
    $('#all').click(function(){
        $('.chart').hide();
        $('#performance_bargraph').show();
    });

    $('.sub').click(function() {
        $('.chart').hide();
        $('#subject_performance' + $(this).attr('target')).show();
    });
    

    $('ul.nav-tabs li a').click(function(e) {
        $('ul.nav-tabs li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });
});