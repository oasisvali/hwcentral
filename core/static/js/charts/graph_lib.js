$(document).ready(function() {
    var user_id= $("#user_id").text();
    user_id= user_id.trim();
    if(isNaN(user_id)){
        console.error("The proviced user id is not a number");
        return;
    }
    $('.printable_report').hide();
    if ($("#stud_performance").length>0){
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
                        ['Topic','My Performance','Class Average'],
                    ];
                    var assignmentlist= subjectroomlist[i].listing;
                    for (var j = 0; j < assignmentlist.length; j++) {
                        var student_assignment= subjectroomlist[i].listing[j];
                        performance_breakdown_data.push([student_assignment.topic,student_assignment.student_score,student_assignment.subjectroom_average]);
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
        
                $('.printable_report').show();
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
                
                printDiv('.printable_report');
                $('.printable_report').hide();
            });
        });
    }

    

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
                draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectteacher_data[i].subject_room,subjectteacher_data[i].subject_teacher,subjectteacher_data);
            }
        });
    }
    if ($("#student_subjectroom_performance").length > 0) {
        var subjectroom_id= $("#subjectroom_id").text();
        subjectroom_id=subjectroom_id.trim();
        if(isNaN(subjectroom_id)){
            console.error("The proviced subjectroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT+ "student/"+user_id+"/"+subjectroom_id,function(single_subjectteacher_data){
            var student_subjectroom_performance_data = [
                ['Topic', 'My Performance','Section Average'],
            ];
            for (var j = 0; j <single_subjectteacher_data.listing.length; j++) {
                var subjectroom_assignment= single_subjectteacher_data.listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
            }
        draw_single_subjectroom_performance(student_subjectroom_performance_data,single_subjectteacher_data.subject,single_subjectteacher_data.subject_teacher);
        });
    }    
    if ($("#teacher_subjectroom_performance").length > 0) {
        var subjectroom_id= $("#subjectroom_id").text();
        subjectroom_id=subjectroom_id.trim();
        if(isNaN(subjectroom_id)){
            console.error("The provided subjectroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT+ "subjectroom/"+subjectroom_id,function(single_subjectteacher_data){
            var student_subjectroom_performance_data = [
                ['Topic', 'Class Average','Section Average'],
            ];
            for (var j = 0; j <single_subjectteacher_data[0].listing.length; j++) {
                var subjectroom_assignment= single_subjectteacher_data[0].listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.standard_average, subjectroom_assignment.subjectroom_average]);
            }
        draw_single_subjectroom_performance(student_subjectroom_performance_data,single_subjectteacher_data[0].subject_room,single_subjectteacher_data[0].subject_teacher);
        });
    }  

    if ($("#classroom_performance_breakdown").length > 0) {
        var classroom_id= $("#classroom_id").text();
        classroom_id=classroom_id.trim();
        if(isNaN(classroom_id)){
            console.error("The provided classroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT+"classteacher/"+user_id+"/"+classroom_id,function(classteacher_data){
            for (var i = 0; i < classteacher_data.length; i++) {
                $("#classroombar").append(
                    "<li class=classroomtab target=" + i + "><a>" + classteacher_data[i].subject_room + "</a></li> ");
                $("#classroombargraph").append(
                    "<div id='classroom_bargraph" + i + "' class='classroom_chart scroll'></div>");
            }

            $('.classroom_chart').hide();
            $('#classroom_bargraph0').show();

            $('.classroomtab').click(function() {
                $('.classroom_chart').hide();
                $('#classroom_bargraph' + $(this).attr('target')).show();
            });

            $('ul.nav-tabs li a').click(function(e) {
                $('ul.nav-tabs li.active').removeClass('active');
                $(this).parent('li').addClass('active');
            });
            
            for (var i = 0; i < classteacher_data.length; i++) {
                var classroom_performance_breakdown_data = [
                    ['Topic', 'Class Average','Section Average'],
                ];
                for (var j = 0; j < classteacher_data[i].listing.length; j++) {
                    var classroom_assignment= classteacher_data[i].listing[j];
                    classroom_performance_breakdown_data.push([classroom_assignment.topic, classroom_assignment.standard_average, classroom_assignment.subjectroom_average]);
                }
                draw_classroom_performance_breakdown(classroom_performance_breakdown_data,i,classteacher_data[i].subject_room,classteacher_data[i].subject_teacher);
            }
        });
    }
});