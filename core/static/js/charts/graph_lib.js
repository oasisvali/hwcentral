$(document).ready(function() {
    var user_id= $("#user_id").text();
    user_id= user_id.trim();
    if(isNaN(user_id)){
        console.error("The provided user id is not a number");
        return;
    }
    //$('.print_content').hide();
    if ($("#child_id").length>0){ // for parent subjectroom page
        user_id= $("#child_id").text();
    }
    if($("#parent_content").length>0){ // check if user is parent
        $(".parent_child_id").each(function(){
            user_id= $(this).text();
            if ($("#student_performance_" + user_id).length > 0) {
                var chart_width=1000;
                var chart_height=400;
                var child_id=user_id; // variable to make sure value doesnt change during call
                $.getJSON(CHART_ENDPOINT+"student/"+child_id,function(student_data){
                    if ($("#student_performance_breakdown_" + child_id).length > 0) {
                        for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                            var subject = student_data.breakdown_listing[i].subject;
                            $("#subjectbar_"+child_id).append(
                                "<li class=sub_" + child_id + " target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li>");
                            $("#subject_performance_"+child_id).append(
                                "<div id='subject_performance_"+child_id + i + "' class='chart_"+child_id+" scroll no-border'></div>");
                        }
                        
                        $('.chart_'+child_id).hide();
                        $('#student_performance_bargraph_' + child_id).show();
                
                        $('#all_'+child_id).click(function(){
                            $('.chart_'+child_id).hide();
                            $('#student_performance_bargraph_' + child_id).show();
                        });

                        $('.sub_'+child_id).click(function() {
                            $('.chart_'+child_id).hide();
                            $('#subject_performance_'+child_id+$(this).attr('target')).show();
                        });
                        

                        $('ul.nav-tabs li a').click(function(e) {
                            $('ul.nav-tabs li.active').removeClass('active');
                            $(this).parent('li').addClass('active');
                        });

                        var subjectroomlist= student_data.breakdown_listing;
                        for (var i = 0; i < subjectroomlist.length; i++) {
                            var student_performance_breakdown_data = [
                                ['Topic', 'Student\'s Score', 'Class Average']
                            ];
                            var assignmentlist= subjectroomlist[i].listing;
                            if (assignmentlist.length == 0) {
                                $('#subject_performance_' + child_id + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                                continue;
                            }
                            for (var j = 0; j < assignmentlist.length; j++) {
                                var student_assignment= subjectroomlist[i].listing[j];
                                student_performance_breakdown_data.push([student_assignment.topic, student_assignment.student_score, student_assignment.subjectroom_average]);
                            }
                            draw_parent_child_performance_breakdown(student_performance_breakdown_data, i, subjectroomlist[i].subject, subjectroomlist[i].subject_teacher, student_data, chart_width, chart_height, child_id);
                        }
                    }

                    if ($("#student_performance_report_" + child_id).length > 0) {
                        var student_performance_report_data = [];
                        var subjectlist= student_data.performance_report.listing;
                        console.log(subjectlist);
                        if (subjectlist.length == 0) {
                            $('#student_performance_bargraph_' + child_id).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                            return;
                        }

                        for (var i = 0; i < subjectlist.length; i++) {
                            student_performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
                        }
                        draw_parent_child_performance_report(student_performance_report_data, chart_width, chart_height, child_id);
                    }

                    //$("#print_performance_"+child_id).click(function(){
                    //
                    //    $('#printable_report_'+child_id).show();
                    //    if ($("#printable_performance_report_"+child_id).length > 0) {
                    //        draw_parent_child_printable_performance_report(student_performance_report_data,child_id);
                    //    }
                    //
                    //
                    //
                    //    if ($("#printable_performance_breakdown_"+child_id).length > 0) {
                    //        var print_subjectroomlist= student_data.breakdown_listing;
                    //        for (var i = 0; i < print_subjectroomlist.length; i++) {
                    //            var performance_breakdown_data = [
                    //                ['Topic', 'Student\'s Score','Class Average'],
                    //            ];
                    //            var print_assignmentlist= print_subjectroomlist[i].listing;
                    //            for (var j = 0; j < print_assignmentlist.length; j++) {
                    //                var student_assignment= print_subjectroomlist[i].listing[j];
                    //                performance_breakdown_data.push([student_assignment.topic, student_assignment.student_score, student_assignment.subjectroom_average]);
                    //            }
                    //            $("#printable_subject_performance_"+child_id).append(
                    //                "<div id='printable_subject_performance_"+child_id+ i + "' class='printablechart'></div>"
                    //            );
                    //            draw_parent_child_printable_performance_breakdown(performance_breakdown_data,i,print_subjectroomlist[i].subject,print_subjectroomlist[i].subject_teacher,child_id);
                    //        }
                    //    }
                    //    printDiv('printable_report_'+child_id);
                    //    $('.print_content').hide();
                    //    window.setTimeout('location.reload()',1500);
                    //});
                });
            }
        });
    }

    if ($("#student_performance").length > 0) {
        var chart_width=1000;
        var chart_height=400;
        $.getJSON(CHART_ENDPOINT+"student/"+user_id,function(student_data){
            if ($("#student_performance_breakdown").length > 0) {
                for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                    var subject = student_data.breakdown_listing[i].subject;
                    $("#subjectbar").append(
                        "<li class=sub target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li> ");
                    $("#subject_performance").append(
                        "<div id='subject_performance" + i + "' class='chart scroll no-border'></div>");
                }
                $('.chart').hide();
                $('#student_performance_bargraph').show();
        
                $('#all').click(function(){
                    $('.chart').hide();
                    $('#student_performance_bargraph').show();
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
                    var student_performance_breakdown_data = [];
                    var assignmentlist= subjectroomlist[i].listing;

                    if (assignmentlist.length == 0) {
                        $('#subject_performance' + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                        continue;
                    }

                    for (var j = 0; j < assignmentlist.length; j++) {
                        var student_assignment= subjectroomlist[i].listing[j];
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
            //$("#print_performance").click(function(){
            //
            //    $('#printable_report').show();
            //    if ($("#printable_performance_report").length > 0) {
            //        draw_printable_performance_report(student_performance_report_data);
            //    }
            //
            //
            //
            //    if ($("#printable_performance_breakdown").length > 0) {
            //        var print_subjectroomlist= student_data.breakdown_listing;
            //        for (var i = 0; i < print_subjectroomlist.length; i++) {
            //            var student_performance_breakdown_data = [
            //                ['Topic', 'Student\'s Score', 'Class Average'],
            //            ];
            //            var print_assignmentlist= print_subjectroomlist[i].listing;
            //            for (var j = 0; j < print_assignmentlist.length; j++) {
            //                var student_assignment= print_subjectroomlist[i].listing[j];
            //                student_performance_breakdown_data.push([student_assignment.topic, student_assignment.subjectroom_average, student_assignment.student_score]);
            //            }
            //            $("#printable_subject_performance").append(
            //                "<div id='printable_subject_performance" + i + "' class='printablechart'></div>"
            //            );
            //            draw_printable_performance_breakdown(student_performance_breakdown_data,i,print_subjectroomlist[i].subject,print_subjectroomlist[i].subject_teacher);
            //        }
            //    }
            //    printDiv('printable_report');
            //    $('.print_content').hide();
            //    window.setTimeout('location.reload()',1500);
            //});
        });
    }

    

    if ($("#subjectroom_performance_breakdown").length > 0) {
        $.getJSON(CHART_ENDPOINT+"subjectteacher/"+user_id,function(subjectteacher_data){
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
            var chart_width=1000;
            var chart_height=500;
            for (var i = 0; i < subjectteacher_data.length; i++) {
                if (subjectteacher_data[i].listing.length == 0) {
                    $('#subjectroom_bargraph' + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                    continue;
                }
                var subjectroom_performance_breakdown_data = [
                    ['Topic', 'Section Average', 'Standard Average'],
                ];
                for (var j = 0; j < subjectteacher_data[i].listing.length; j++) {
                    var subjectroom_assignment= subjectteacher_data[i].listing[j];
                    subjectroom_performance_breakdown_data.push([subjectroom_assignment.topic, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average]);
                }
                draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectteacher_data[i].subject_room,subjectteacher_data[i].subject_teacher,subjectteacher_data,chart_width,chart_height);
            }
        });
    }
    if ($("#student_subjectroom_performance").length > 0) {
        var chart_width=1000;
        var chart_height=400;
        var subjectroom_id= $("#subjectroom_id").text();
        subjectroom_id=subjectroom_id.trim();
        if(isNaN(subjectroom_id)){
            console.error("The provided subjectroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT + "student/" + user_id + "/" + subjectroom_id, function (single_subjectroom_data) {
            if (single_subjectroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph').html("<img class='no-data-img' src='/static/img/no-data.png'>");
                return;
            }

            var student_subjectroom_performance_data = [
                ['Topic', 'Student\'s Score', 'Class Average'],
            ];
            for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                var subjectroom_assignment = single_subjectroom_data.listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
            }
            draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, true, false, chart_width, chart_height);
        });
    }    
    if ($("#teacher_subjectroom_performance").length > 0) {
        var chart_width=1000;
        var chart_height=400;
        var subjectroom_id= $("#subjectroom_id").text();
        subjectroom_id=subjectroom_id.trim();
        if(isNaN(subjectroom_id)){
            console.error("The provided subjectroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT + "subjectroom/" + subjectroom_id, function (single_subjectroom_data) {
            if (single_subjectroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph').html("<img class='no-data-img' src='/static/img/no-data.png'>");
                return;
            }

            var student_subjectroom_performance_data = [
                ['Topic', 'Section Average', 'Standard Average']
            ];
            for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                var subjectroom_assignment = single_subjectroom_data.listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average]);
            }
            draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, false, false, chart_width, chart_height);
        });
    }

    if ($("#classroom_performance_breakdown").length > 0) {
        var classteacher_id= $("#classteacher_id").text();
        var classroom_id= $("#classroom_id").text();
        classteacher_id=classteacher_id.trim();
        if(isNaN(classteacher_id)){
            console.error("The provided classteacher id is not a number");
            return;
        }
        classroom_id=classroom_id.trim();
        if(isNaN(classroom_id)){
            console.error("The provided classroom id is not a number");
            return;
        }
        $.getJSON(CHART_ENDPOINT+"classteacher/"+classteacher_id+"/"+classroom_id,function(classteacher_data){
            for (var i = 0; i < classteacher_data.length; i++) {
                var subject_room = classteacher_data[i].subject_room;
                $("#classroombar").append(
                    "<li class=classroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
                $("#classroombargraph").append(
                    "<div id='classroom_bargraph" + i + "' class='classroom_chart scroll'></div>");
            }
            $("[target='0']").addClass('active');
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
                if (classteacher_data[i].listing.length == 0) {
                    $('#classroom_bargraph' + i).html("<img class='no-data-img' src='/static/img/no-data.png'>");
                    continue;
                }

                var classroom_performance_breakdown_data = [
                    ['Topic', 'Section Average', 'Standard Average'],
                ];
                for (var j = 0; j < classteacher_data[i].listing.length; j++) {
                    var classroom_assignment= classteacher_data[i].listing[j];
                    classroom_performance_breakdown_data.push([classroom_assignment.topic, classroom_assignment.subjectroom_average, classroom_assignment.standard_average]);
                }
                draw_classroom_performance_breakdown(classroom_performance_breakdown_data, i, classteacher_data);
            }
        });
    }
});