$(document).ready(function() {
    $('#printable_report').hide();
    if ($("#performance_breakdown").length > 0) {
        var subjectroomlist= studentdata.breakdown_listing;
        for (var i = 0; i < subjectroomlist.length; i++) {
            var performance_breakdown_data = [
                ['Topic', 'Average', 'My Performance'],
            ];
            var assignmentlist= subjectroomlist[i].listing;
            for (var j = 0; j < assignmentlist.length; j++) {
                var student_assignment= subjectroomlist[i].listing[j];
                performance_breakdown_data.push([student_assignment.topic, student_assignment.subjectroom_average, student_assignment.student_score]);
            }
            draw_performance_breakdown(performance_breakdown_data,i,subjectroomlist[i].subject,subjectroomlist[i].subject_teacher);
        }
    }

    if ($("#performance_report").length > 0) {
        var performance_report_data=[];
        var subjectlist= studentdata.performance_report.listing;
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
            var subjectroomlist= studentdata.breakdown_listing;
            for (var i = 0; i < subjectroomlist.length; i++) {
                $("#printable_subject_performance").append(
                    "<div id='printable_subject_performance" + i + "' class='printablechart'></div>"
                ); 
                draw_printable_performance_breakdown(performance_breakdown_data,i,subjectroomlist[i].subject,subjectroomlist[i].subject_teacher);
            }
        }
        
        printDiv('printable_report');
        $('#printable_report').hide();
    });

    if ($("#subjectroom_performance_breakdown").length > 0) {
        for (var i = 0; i < subjectroomarray.length; i++) {
            var subjectroom_performance_breakdown_data = [
                ['Topic', 'Class Average','Section Average'],
            ];
            for (var j = 0; j < subjectroomarray[i].listing.length; j++) {
                var subjectroom_assignment= subjectroomarray[i].listing[j];
                subjectroom_performance_breakdown_data.push([subjectroom_assignment.topic, subjectroom_assignment.class_average, subjectroom_assignment.subjectroom_average]);
            }
            draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectroomarray[i].subject_room,subjectroomarray[i].subject_teacher);
        }
    }
});