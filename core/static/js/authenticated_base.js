var CHARTPOPUP=true;
var DATATABLES_DEBUG=false;
var CHART_ENDPOINT="/chart/";
var MIN_DIMENSION=600;
if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert ("Sorry ! HWCentral does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}




$(document).ready(function () {

    $('.disable_clipboard').bind("cut copy paste",function(e) {
      e.preventDefault();
    });
 
    $.fn.dataTable.moment('hh:mm A, D MMM YYYY');

    $('#announcement_table').dataTable({
        "pagingType":"full_numbers"
    });
    
    $('.reportcard').dataTable({
        "orderCellsTop":true
    });
    
    $('.classroom_header').click(function(){
        $(this).nextUntil('tr.classroom_header').slideToggle(50);
    });
    
    $('.assignment_table').dataTable();
    
    $(".student_subjectroom_performance_link").click(function(){
        var stud_id=$(this).parent().parent().find(".stud_id").text();
        var subjectroom_id= $("#subjectroom_id").text();
        if ($("#student_subjectroom_popup").length > 0) {
            CHARTHANDLER=true;
            var chart_width=800;
            var chart_height=400;
            CHARTPOPUP=false;
            $.getJSON(CHART_ENDPOINT+ "student/"+stud_id+"/"+subjectroom_id,function(single_subjectteacher_data){
                var student_subjectroom_performance_data = [
                    ['Topic', 'My Performance','Section Average'],
                ];
                for (var j = 0; j <single_subjectteacher_data.listing.length; j++) {
                    var subjectroom_assignment= single_subjectteacher_data.listing[j];
                    student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
                }
            draw_single_subjectroom_performance(student_subjectroom_performance_data,single_subjectteacher_data.subject,single_subjectteacher_data.subject_teacher,single_subjectteacher_data,CHARTHANDLER,chart_width,chart_height);
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
                    $("#subjectroombar").append(
                        "<li class=subjectroomtab target=" + i + "><a>" + subjectteacher_data[i].subject_room + "</a></li> ");
                    $("#subjectroombargraph").append(
                        "<div id='subjectroom_bargraph" + i + "' class='subjectroom_chart scroll'></div>");
                }

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
                    var subjectroom_performance_breakdown_data = [
                        ['Topic','Section Average', 'Class Average'],
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
        var stud_id=$(this).parent().parent().find(".stud_id").text();
        if ($("#student_performance_breakdown_popup").length > 0) {
            var chart_width=800;
            var chart_height=400;
            $.getJSON(CHART_ENDPOINT+"student/"+stud_id,function(student_data){
                if ($("#performance_breakdown_popup").length > 0) {
                    $("#subjectbar").html("<li id='all'><a>Overall</a></li>");
                    for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                        $("#subjectbar").append(
                            "<li class=sub target=" + i + "><a>" + student_data.breakdown_listing[i].subject + "</a></li> ");
                        $("#subject_performance").append(
                            "<div id='subject_performance" + i + "' class='popup_chart'></div>");
                    }
                    $('.popup_chart').hide();
                    $('#performance_bargraph').show();
            
                    $('#all').click(function(){
                        $('.popup_chart').hide();
                        $('#performance_bargraph').show();
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
                        var performance_breakdown_data = [
                            ['Topic','My Performance','Class Average'],
                        ];
                        var assignmentlist= subjectroomlist[i].listing;
                        for (var j = 0; j < assignmentlist.length; j++) {
                            var student_assignment= subjectroomlist[i].listing[j];
                            performance_breakdown_data.push([student_assignment.topic,student_assignment.student_score,student_assignment.subjectroom_average]);
                        }
                        draw_performance_breakdown(performance_breakdown_data,i,subjectroomlist[i].subject,subjectroomlist[i].subject_teacher,student_data,chart_width,chart_height);
                    }
                }

                if ($("#performance_report").length > 0) {
                    var performance_report_data=[];
                    var subjectlist= student_data.performance_report.listing;
                    for (var i = 0; i < subjectlist.length; i++) {
                        performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
                    }
                    draw_performance_report(performance_report_data,chart_width,chart_height);
                }
            });
            $("#student_performance_breakdown_popup").modal('show');
        }
    });

    $(".histogram_link").click(function(){
        var assign_id=$(this).parent().parent().find(".assignment_id").text();
        var topic= $(this).parent().parent().find(".assign_title").text();
        if ($("#section_assignment_performance").length > 0){
                $.getJSON(CHART_ENDPOINT+"assignment/"+assign_id,function(assignment_data){
                    var assignment_performance_data=[];
                    for(var j=0;j<assignment_data.length;j++){
                        var student_assignment=assignment_data[j];
                        assignment_performance_data.push([student_assignment.full_name,student_assignment.score]);
                    }
                    draw_section_assignment_performance(assignment_performance_data,topic,assignment_data);
                });   
            $("#section_chart_popup").modal('show');
        }
    });

    // Script to change sidebar height based on length of doc
    
        var refreshDocHeight = function(){
            var h = $("#auth_body").height();
            var s = String(h).concat("px");
            $("#sidebar").css("height",s);
        };

        window.setInterval(refreshDocHeight, 1000);
    

})




