$(document).ready(function() {
    var user_id = extract_id($("#user_id"));

    if($("#parent-home-body").length>0){ // check if user is parent
        $(".parent_child_id").each(function(){
            var child_id = extract_id($(this));
            if ($("#student_performance_" + child_id).length > 0) {
                $.getJSON(CHART_ENDPOINT+"student/"+child_id,function(student_data){
                    if ($("#student_performance_breakdown_" + child_id).length > 0) {
                        for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                            var subject = student_data.breakdown_listing[i].subject;
                            $("#subjectbar_"+child_id).append(
                                "<li class=sub_" + child_id + " target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li>");
                            $("#subject_performance_"+child_id).append(
                                "<div id='subject_performance_"+child_id + i + "' class='chart chart_" + child_id + "'></div>");
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
                            var subjectbar_id = $(this).parent('li').parent('ul.nav-tabs').attr('id');
                            $('#' + subjectbar_id + ' li.active').removeClass('active');
                            $(this).parent('li').addClass('active');
                        });

                        var subjectroomlist= student_data.breakdown_listing;
                        for (var i = 0; i < subjectroomlist.length; i++) {
                            var student_performance_breakdown_data = [
                                ['Topic', 'Student\'s Score', 'Class Average']
                            ];
                            var assignmentlist= subjectroomlist[i].listing;
                            if (assignmentlist.length == 0) {
                                $('#subject_performance_' + child_id + i).html(NO_DATA_IMG);
                                continue;
                            }
                            for (var j = 0; j < assignmentlist.length; j++) {
                                var student_assignment= subjectroomlist[i].listing[j];
                                student_performance_breakdown_data.push([student_assignment.topic, student_assignment.student_score, student_assignment.subjectroom_average]);
                            }
                            draw_parent_child_performance_breakdown(student_performance_breakdown_data, i, student_data, child_id);
                        }
                    }

                    if ($("#student_performance_report_" + child_id).length > 0) {
                        var student_performance_report_data = [];
                        var subjectlist = student_data.performance_report.listing;
                        if (subjectlist.length == 0) {
                            $('#student_performance_bargraph_' + child_id).html(NO_DATA_IMG);
                            return;
                        }

                        for (var i = 0; i < subjectlist.length; i++) {
                            student_performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
                        }
                        draw_parent_child_performance_report(student_performance_report_data, child_id);
                    }
                });
            }
        });
    }

    if ($("#student_performance").length > 0) {

        $.getJSON(CHART_ENDPOINT+"student/"+user_id,function(student_data){
            if ($("#student_performance_breakdown").length > 0) {
                for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                    var subject = student_data.breakdown_listing[i].subject;
                    $("#subjectbar").append(
                        "<li class=sub target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li> ");
                    $("#subject_performance").append(
                        "<div id='subject_performance" + i + "' class='student_chart chart'></div>");
                }
                $('.student_chart').hide();
                $('#student_performance_bargraph').show();
        
                $('#all').click(function(){
                    $('.student_chart').hide();
                    $('#student_performance_bargraph').show();
                });

                $('.sub').click(function() {
                    $('.student_chart').hide();
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
                        $('#subject_performance' + i).html(NO_DATA_IMG);
                        continue;
                    }

                    for (var j = 0; j < assignmentlist.length; j++) {
                        var student_assignment= subjectroomlist[i].listing[j];
                        student_performance_breakdown_data.push([student_assignment.topic, student_assignment.student_score, student_assignment.subjectroom_average]);
                    }
                    draw_student_performance_breakdown(student_performance_breakdown_data, i, student_data);
                }
            }

            if ($("#student_performance_report").length > 0) {
                var student_performance_report_data = [];
                var subjectlist = student_data.performance_report.listing;

                if (subjectlist.length == 0) {
                    $('#student_performance_bargraph').html(NO_DATA_IMG);
                    return;
                }

                for (var i = 0; i < subjectlist.length; i++) {
                    student_performance_report_data.push([subjectlist[i].subject, subjectlist[i].student_average, subjectlist[i].subjectroom_average]);
                }
                draw_student_performance_report(student_performance_report_data);
            }
        });
    }

    

    if ($("#subjectroom_performance_breakdown").length > 0) {
        $.getJSON(CHART_ENDPOINT+"subjectteacher/"+user_id,function(subjectteacher_data){
            for (var i = 0; i < subjectteacher_data.length; i++) {
                var subject_room = subjectteacher_data[i].subject_room;
                $("#subjectroombar").append(
                    "<li class=subjectroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
                $("#subjectroombargraph").append(
                    "<div id='subjectroom_bargraph" + i + "' class='subjectroom_chart chart'></div>");
            }
            $("[target='0']").addClass('active');   // make first tab active
            $('#subjectroombargraph > #chart-loader').remove();      // remove chart loader
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
                    $('#subjectroom_bargraph' + i).html(NO_DATA_IMG);
                    continue;
                }
                var subjectroom_performance_breakdown_data = [
                    ['Topic', 'Section Average', 'Standard Average'],
                ];
                for (var j = 0; j < subjectteacher_data[i].listing.length; j++) {
                    var subjectroom_assignment= subjectteacher_data[i].listing[j];
                    subjectroom_performance_breakdown_data.push([subjectroom_assignment.topic, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average]);
                }
                draw_subjectroom_performance_breakdown(subjectroom_performance_breakdown_data,i,subjectteacher_data);
            }
        });
    }
    if ($("#student_subjectroom_performance").length > 0) {

        var subjectroom_id = extract_id($("#subjectroom_id"));
        var student_id = null;

        if ($("#parent_child_id").length > 0) {
            // the current user is a parent, use the child id for the subsequent chart call
            student_id = extract_id($("#parent_child_id"));
        }
        else {
            // current user is a student, use the user id for the subsequent chart call
            student_id = user_id;
        }

        $.getJSON(CHART_ENDPOINT + "student/" + student_id + "/" + subjectroom_id, function (single_subjectroom_data) {
            if (single_subjectroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
                return;
            }

            var student_subjectroom_performance_data = [
                ['Topic', 'Student\'s Score', 'Class Average'],
            ];
            for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                var subjectroom_assignment = single_subjectroom_data.listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.student_score, subjectroom_assignment.subjectroom_average]);
            }
            draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, true, false);
        });
    }    
    if ($("#teacher_subjectroom_performance").length > 0) {

        var subjectroom_id = extract_id($("#subjectroom_id"));
        $.getJSON(CHART_ENDPOINT + "subjectroom/" + subjectroom_id, function (single_subjectroom_data) {
            if (single_subjectroom_data.listing.length == 0) {
                $('#single_subjectroom_bargraph').html(NO_DATA_IMG);
                return;
            }

            var student_subjectroom_performance_data = [
                ['Topic', 'Section Average', 'Standard Average']
            ];
            for (var j = 0; j < single_subjectroom_data.listing.length; j++) {
                var subjectroom_assignment = single_subjectroom_data.listing[j];
                student_subjectroom_performance_data.push([subjectroom_assignment.topic, subjectroom_assignment.subjectroom_average, subjectroom_assignment.standard_average]);
            }
            draw_single_subjectroom_performance(student_subjectroom_performance_data, single_subjectroom_data, false, false);
        });
    }

    if ($("#classroom_performance_breakdown").length > 0) {
        var classteacher_id = extract_id($("#classteacher_id"));
        var classroom_id = extract_id($("#classroom_id"));

        $.getJSON(CHART_ENDPOINT+"classteacher/"+classteacher_id+"/"+classroom_id,function(classteacher_data){
            for (var i = 0; i < classteacher_data.length; i++) {
                var subject_room = classteacher_data[i].subject_room;
                $("#classroombar").append(
                    "<li class=classroomtab target=" + i + "><a title='View the performance of subjectroom: " + subject_room + "'>" + subject_room + "</a></li> ");
                $("#classroombargraph").append(
                    "<div id='classroom_bargraph" + i + "' class='classroom_chart chart'></div>");
            }
            $("[target='0']").addClass('active');
            $('#classroombargraph > #chart-loader').remove();      // remove chart loader
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
                    $('#classroom_bargraph' + i).html(NO_DATA_IMG);
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

    $(".histogram_link").click(function(){
        var parent_row = $(this).parent('td').parent('tr');
        var assign_id = extract_id(parent_row.find(".assignment_id"));
        var topic = extract_text(parent_row.find(".assign_title"));

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