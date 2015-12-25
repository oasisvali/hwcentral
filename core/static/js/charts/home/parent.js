$(document).ready(function () {
    $(".parent_child_id").each(function () {
        var child_id = extract_id($(this));
        if ($("#student_performance_" + child_id).length > 0) {
            $.getJSON(CHART_ENDPOINT + "student/" + child_id, function (student_data) {
                if ($("#student_performance_breakdown_" + child_id).length > 0) {
                    for (var i = 0; i < student_data.breakdown_listing.length; i++) {
                        var subject = student_data.breakdown_listing[i].subject;
                        $("#subjectbar_" + child_id).append(
                            "<li class=sub_" + child_id + " target=" + i + "><a title='View the student&#39;s performance in " + subject + "'>" + subject + "</a></li>");
                        $("#subject_performance_" + child_id).append(
                            "<div id='subject_performance_" + child_id + i + "' class='chart chart_" + child_id + "'></div>");
                    }

                    $('.chart_' + child_id).hide();
                    $('#student_performance_bargraph_' + child_id).show();

                    $('#all_' + child_id).click(function () {
                        $('.chart_' + child_id).hide();
                        $('#student_performance_bargraph_' + child_id).show();
                    });

                    $('.sub_' + child_id).click(function () {
                        $('.chart_' + child_id).hide();
                        $('#subject_performance_' + child_id + $(this).attr('target')).show();
                    });


                    $('ul.nav-tabs li a').click(function (e) {
                        var subjectbar_id = $(this).parent('li').parent('ul.nav-tabs').attr('id');
                        $('#' + subjectbar_id + ' li.active').removeClass('active');
                        $(this).parent('li').addClass('active');
                    });

                    var subjectroomlist = student_data.breakdown_listing;
                    for (var i = 0; i < subjectroomlist.length; i++) {
                        var student_performance_breakdown_data = [];
                        var assignmentlist = subjectroomlist[i].listing;
                        if (assignmentlist.length == 0) {
                            $('#subject_performance_' + child_id + i).html(NO_DATA_IMG);
                            continue;
                        }
                        for (var j = 0; j < assignmentlist.length; j++) {
                            var student_assignment = subjectroomlist[i].listing[j];
                            student_performance_breakdown_data.push([student_assignment.date, student_assignment.student_score, student_assignment.subjectroom_average, student_assignment.topic]);
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
});