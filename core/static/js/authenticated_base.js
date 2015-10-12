var DATATABLES_DEBUG=false;
var CHART_ENDPOINT="/chart/";
var MIN_DIMENSION=600;

if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert("Sorry ! Homework Central does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {

    $('.disable_clipboard').bind("cut copy paste",function(e) {
      e.preventDefault();
    });
 
    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('#announcement_table').dataTable({
        "pagingType":"full_numbers",
        "sDom":"ltipr" // to disable global search on datatables
    });
    
    $('.reportcard').dataTable({
        "orderCellsTop":true
    });

    // TODO: move to specific classroom js file
    $('.classroom_header').click(function(){
        $(this).nextUntil('tr.classroom_header').slideToggle(50);
    });
    
    $('.assignment_table').dataTable();

    // TODO: move these chart popups to a seperate file
    $(".student_subjectroom_performance_link").click(function(){
        var student_id = $(this).parent().parent().find(".student_id").text();
        var subjectroom_id= $("#subjectroom_id").text();
        if ($("#student_subjectroom_popup").length > 0) {
            var chart_width=800;
            var chart_height=400;
            $.getJSON(CHART_ENDPOINT + "student/" + student_id + "/" + subjectroom_id, function (single_subjectroom_data) {
                if (single_subjectroom_data.listing.length == 0) {
                    $('#single_subjectroom_bargraph_popup').html("<img class='no-data-img' src='/static/img/no-data.png'>");
                    return;
                }

                var student_subjectroom_performance_data = [
                    ['Topic', 'Student\'s Score', 'Class Average']
                ];
                for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                    var subjectroom_assignment = single_subjectroom_data.listing[j];
                    student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
                }
                draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, true, true, chart_width, chart_height);
            });
            $("#subjectroom_performance_popup").modal('show');
        }    
    });


    $(".subjectroom_performance_breakdown_link").click(function(){
        var subjectteacher_id=$(this).parent().parent().find(".subjectteacher_id").text();
        if ($("#subjectroom_performance_breakdown_popup").length > 0) {
            $("#subjectroombar").html("");
            var chart_width=810;
            var chart_height=400;
            $.getJSON(CHART_ENDPOINT+"subjectteacher/"+subjectteacher_id,function(subjectteacher_data){

                for (var i = 0; i < subjectteacher_data.length; i++) {
                    var subject_room = subjectteacher_data[i].subject_room;
                    $("#subjectroombar").append(
                        "<li class=subjectroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
                    $("#subjectroombargraph").append(
                        "<div id='subjectroom_bargraph" + i + "' class='subjectroom_chart scroll'></div>");
                }
                $("[target='0']").addClass('active');
                $('.subjectroom_chart').hide();
                $('#subjectroom_bargraph0').show();

                $('.subjectroomtab').click(function() {
                    $('.subjectroom_chart').hide();
                    $('#subjectroom_bargraph' + $(this).attr('target')).show();
                });

                $('ul.nav-tabs li a').click(function(e) {
                    $('ul.nav-tabs li.active').removeClass('active');
                    $(this).parent('li').addClass('active');
                });
                
                for (var i = 0; i < subjectteacher_data.length; i++) {
                    if (subjectteacher_data[i].listing.length == 0) {
                        $('#subjectroom_bargraph' + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                        continue;
                    }

                    var subjectroom_performance_breakdown_data = [
                        ['Topic', 'Section Average', 'Standard Average']
                    ];
                    for (var j = 0; j < subjectteacher_data[i].listing.length; j++) {
                        var subjectroom_assignment= subjectteacher_data[i].listing[j];
                        subjectroom_performance_breakdown_data.push([subjectroom_assignment.topic, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average]);
                    }
                    draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectteacher_data[i].subject_room,subjectteacher_data[i].subject_teacher,subjectteacher_data,chart_width,chart_height);
                }
            });
            $("#teacher_performance_breakdown_popup").modal('show');
        }
    });

    $(".student_performance_breakdown_link").click(function(){
        var student_id = $(this).parent().parent().find(".student_id").text();
        if ($("#student_performance_breakdown_popup").length > 0) {
            var chart_width=800;
            var chart_height=400;
            $.getJSON(CHART_ENDPOINT + "student/" + student_id, function (student_data) {
                if ($("#student_performance_breakdown_popup").length > 0) {
                    $("#subjectbar").html("<li id='all' class='active'><a title='View overall performance across all subjects'>Overall</a></li>");                 
                    for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                        var subject = student_data.breakdown_listing[i].subject;
                        $("#subjectbar").append(
                            "<li class=sub target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li>");
                        $("#subject_performance").append(
                            "<div id='subject_performance" + i + "' class='popup_chart'></div>");
                    }
                    $('.popup_chart').hide();
                    $('#student_performance_bargraph').show();
            
                    $('#all').click(function(){
                        $('.popup_chart').hide();
                        $('#student_performance_bargraph').show();
                    });

                    $('.sub').click(function() {
                        $('.popup_chart').hide();
                        $('#subject_performance' + $(this).attr('target')).show();
                    });
                    

                    $('ul.nav-tabs li a').click(function(e) {
                        $('ul.nav-tabs li.active').removeClass('active');
                        $(this).parent('li').addClass('active');
                    });

                    var subjectroomlist= student_data.breakdown_listing;
                    for (var i = 0; i < subjectroomlist.length; i++) {
                        var student_performance_breakdown_data = [];
                        var assignmentlist= subjectroomlist[i].listing;
                        if (assignmentlist.length == 0) {
                            $('#subject_performance' + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                            continue;
                        }

                        for (var j = 0; j < assignmentlist.length; j++) {
                            var student_assignment = assignmentlist[j];
                            student_performance_breakdown_data.push([student_assignment.topic, student_assignment.student_score, student_assignment.subjectroom_average]);
                        }
                        draw_student_performance_breakdown(student_performance_breakdown_data, i, student_data, chart_width, chart_height);
                    }
                }

                if ($("#student_performance_report").length > 0) {
                    var student_performance_report_data = [];
                    var subjectlist= student_data.performance_report.listing;
                    if (subjectlist.length == 0) {
                        $('#student_performance_bargraph').html("<img class='no-data-img' src='/static/img/no-data.png'>");
                        return;
                    }
                    for (var i = 0; i < subjectlist.length; i++) {
                        student_performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
                    }
                    draw_student_performance_report(student_performance_report_data, chart_width, chart_height);
                }
            });
            $("#student_performance_breakdown_popup").modal('show');
        }
    });

    $(".histogram_link").click(function(){
        var assign_id = $(this).parent().parent().find(".assignment_id").text();
        var topic = $(this).parent().parent().find(".assign_title").text();
        if ($("#subjectroom_assignment_performance").length > 0) {
                $.getJSON(CHART_ENDPOINT+"assignment/"+assign_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_subjectroom_assignment_performance(assignment_performance_data, topic, assignment_data);
                });
            $("#subjectroom_assignment_chart_popup").modal('show');
        }
    });


});




