$(document).ready(function() {
    if ($("#performance_breakdown").length > 0) {
        for (var i = 0; i < studentdata.breakdown_listing.length; i++) {
            var performance_breakdown_data = [
                ['Topic', 'Average', 'My Performance'],
            ];
            for (var j = 0; j < (studentdata.breakdown_listing[i]).listing.length; j++) {
                performance_breakdown_data.push([studentdata.breakdown_listing[i].listing[j].topic, studentdata.breakdown_listing[i].listing[j].class_average, studentdata.breakdown_listing[i].listing[j].student_score]);
            }
            draw_performance_breakdown(performance_breakdown_data,i);
        }
    }

    if ($("#performance_report").length > 0) {
        var performance_report_data=[];
        for (var i = 0; i < studentdata.performance_report.listing.length; i++) {
            performance_report_data.push([studentdata.performance_report.listing[i].subject, studentdata.performance_report.listing[i].student_average, studentdata.performance_report.listing[i].class_average]);
        }
        draw_performance_report(performance_report_data);
    }

    if ($("#subjectroom_performance_breakdown").length > 0) {
        for (var i = 0; i < studentdata.breakdown_listing.length; i++) {
            var performance_breakdown_data = [
                ['Topic', 'Average', 'My Performance'],
            ];
            for (var j = 0; j < (studentdata.breakdown_listing[i]).listing.length; j++) {
                performance_breakdown_data.push([studentdata.breakdown_listing[i].listing[j].topic, studentdata.breakdown_listing[i].listing[j].class_average, studentdata.breakdown_listing[i].listing[j].student_score]);
            }
            draw_performance_breakdown(performance_breakdown_data,i);
        }
    }
});