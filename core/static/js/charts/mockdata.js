function PerformanceBreakdownElement(performance_breakdown_element){
	this.date=performance_breakdown_element.date;
	this.topic=performance_breakdown_element.topic;
	this.class_average=performance_breakdown_element.class_average;
	this.student_score=performance_breakdown_element.student_score;
}

function PerformanceBreakdown(performance_breakdown){
	this.subject=performance_breakdown.subject;
    this.subject_teacher=performance_breakdown.subjectteacher;
	this.listing=performance_breakdown.listing;
}

function PerformanceReportElement(performance_report_element){
    this.subject=performance_report_element.subject;
    this.student_average=performance_report_element.student_average;
    this.class_average=performance_report_element.class_average;
}

function PerformanceReport(performance_report){
    this.class_teacher=performance_report.class_teacher;
    this.listing=performance_report.listing;
    
}
 
function Performance(performance){
    this.performance_report=performance.performance_report;
    this.breakdown_listing=performance.breakdown_listing;
}

var mock={
    performance_report:{    
        class_teacher: "Oasis Vali",
        listing: [ 
            { 
                subject:"Mathematics",
                student_average: 72,
                class_average:83
            },
            {
                subject:"Science",
                student_average:82,
                class_average:77,
            }
            {
                subject:"Social Studies",
                student_average:88,
                class_average:81,
            }
            {
                subject:"English",
                student_average:91,
                class_average:88,
            }
            {
                subject:"Second Language",
                student_average:95,
                class_average:97,
            }
            {
                subject:"FIT",
                student_average:84,
                class_average:89,
            }
        ]   
    }

    breakdown_listing:[
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Science",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }
        {
            subject:"Mathematics",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                }
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                }
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                }
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                }
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
                
        }



        





}
var test=new Performance(mock);

