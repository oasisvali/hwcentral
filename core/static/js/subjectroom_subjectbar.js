$(document).ready(function() {


    for (var i = 0; i < subjectroomarray.length; i++) {
        $("#subjectroombar").append(
            "<li class=sub target=" + i + "><a>" + subjectroomarray[i].subject_room + "</a></li> ");
        $("#subjectroombargraph").append(
            "<div id='subjectroom_bargraph" + i + "' class='chart scroll'></div>");
    }

    $('.chart').hide();
    $('#subjectroom_bargraph0').show();

     $('.sub').click(function() {
        $('.chart').hide();
        $('#subjectroom_bargraph' + $(this).attr('target')).show();
    });

    $('ul.nav-tabs li a').click(function(e) {
        $('ul.nav-tabs li.active').removeClass('active');
        $(this).parent('li').addClass('active');
    });
});