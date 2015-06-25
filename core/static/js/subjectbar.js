$(document).ready(function() {

    for (var i = 0; i < studentdata.breakdown_listing.length; i++) {
        $("#subjectbar").append(
            "<li class=sub target=" + i + "><a>" + studentdata.breakdown_listing[i].subject + "</a></li> ");
        $("#linegraph").append(
            "<div id='linegraph" + i + "' class='chart scroll'></div>");
    }

    $('.chart').hide();
    $('#linegraph0').show();

    $('.sub').click(function() {
        $('.chart').hide();
        $('#linegraph' + $(this).attr('target')).show();
    });

    $('ul.nav-tabs li a').click(function(e) {
        $('ul.nav-tabs li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });
});