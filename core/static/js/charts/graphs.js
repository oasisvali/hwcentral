$(document).ready(function() {
    var user_id= $("#user_id").text();
    user_id= user_id.trim();
    if(isNaN(user_id)){
        console.error("The proviced user id is not a number");
        return;
    }
    $('#printable_report').hide();
    $.getJSON(CHART_ENDPOINT+"student/"+user_id,function(student_data){
        if ($("#performance_breakdown").length > 0) {
            for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                $("#subjectbar").append(
                    "<li class=sub target=" + i + "><a>" + student_data.breakdown_listing[i].subject + "</a></li> ");
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

            var subjectroomlist= student_data.breakdown_listing;
            for (var i = 0; i < subjectroomlist.length; i++) {
                var performance_breakdown_data = [
                    ['Topic', 'Average', 'My Performance'],
                ];
                var assignmentlist= subjectroomlist[i].listing;
                for (var j = 0; j < assignmentlist.length; j++) {
                    var student_assignment= subjectroomlist[i].listing[j];
                    performance_breakdown_data.push([student_assignment.topic, student_assignment.subjectroom_average, student_assignment.student_score]);
                }
                draw_performance_breakdown(performance_breakdown_data,i,subjectroomlist[i].subject,subjectroomlist[i].subject_teacher,student_data);
            }
        }

        if ($("#performance_report").length > 0) {
            var performance_report_data=[];
            var subjectlist= student_data.performance_report.listing;
            for (var i = 0; i < subjectlist.length; i++) {
                performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
            }
            draw_performance_report(performance_report_data);
        }

        $("#print_performance").click(function(){
     
            $('#printable_report').show();
            if ($("#printable_performance_report").length > 0) {
                draw_printable_performance_report(performance_report_data);
            }

            
            if ($("#printable_performance_breakdown").length > 0) {
                var print_subjectroomlist= student_data.breakdown_listing;
                for (var i = 0; i < print_subjectroomlist.length; i++) {
                    var performance_breakdown_data = [
                        ['Topic', 'Average', 'My Performance'],
                    ];
                    var print_assignmentlist= print_subjectroomlist[i].listing;
                    for (var j = 0; j < print_assignmentlist.length; j++) {
                        var student_assignment= print_subjectroomlist[i].listing[j];
                        performance_breakdown_data.push([student_assignment.topic, student_assignment.subjectroom_average, student_assignment.student_score]);
                    }   
                    $("#printable_subject_performance").append(
                        "<div id='printable_subject_performance" + i + "' class='printablechart'></div>"
                    ); 
                    draw_printable_performance_breakdown(performance_breakdown_data,i,print_subjectroomlist[i].subject,print_subjectroomlist[i].subject_teacher);
                }
            }
            
            printDiv('printable_report');
            $('#printable_report').hide();
        });
    });


    

    if ($("#subjectroom_performance_breakdown").length > 0) {
        $.getJSON(CHART_ENDPOINT+"subjectteacher/"+user_id,function(subjectteacher_data){
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
                    ['Topic', 'Class Average','Section Average'],
                ];
                for (var j = 0; j < subjectteacher_data[i].listing.length; j++) {
                    var subjectroom_assignment= subjectteacher_data[i].listing[j];
                    subjectroom_performance_breakdown_data.push([subjectroom_assignment.topic, subjectroom_assignment.standard_average, subjectroom_assignment.subjectroom_average]);
                }
                draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectteacher_data[i].subject_room,subjectteacher_data[i].subject_teacher);
            }
        });
    }

     if ($("#single_subjectroom_performance_breakdown").length > 0) {
});      $.getJSON(CHART_ENDPOINT+"subjectteacher/"+user_id,function(single_subjectteacher_data){