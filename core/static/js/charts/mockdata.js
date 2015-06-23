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
            },
            {
                subject:"Social Studies",
                student_average:88,
                class_average:81,
            },
            {
                subject:"English",
                student_average:91,
                class_average:88,
            },
            {
                subject:"Second Language",
                student_average:95,
                class_average:97,
            },
            {
                subject:"FIT",
                student_average:84,
                class_average:89,
            }
        ]   
    },

    breakdown_listing:[
        {
            subject:"Mathematics",
            subject_teacher:"Anjali Lal",
            listing:[
                {
                    date: "July 18",
                    topic: "Complex Numbers",
                    class_average: 81,
                    student_score: 85
                },
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    class_average: 84,
                    student_score: 86
                },
                {
                    date: "July 20",
                    topic: "Integration",
                    class_average: 94,
                    student_score: 96
                },
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    class_average: 95,
                    student_score: 91
                },
                {
                    date: "July 23",
                    topic: "Probability",
                    class_average: 77,
                    student_score: 82
                }
            ]    
        },
        {
            subject:"Science",
            subject_teacher:"Amita Singh",
            listing:[
                {
                    date: "July 18",
                    topic: "Organic Chemistry",
                    class_average: 89,
                    student_score: 83
                },
                {
                    date: "July 19",
                    topic: "Atoms and Molecules",
                    class_average: 83,
                    student_score: 28
                },
                {
                    date: "July 21",
                    topic: "Redox Reactions",
                    class_average: 74,
                    student_score: 91
                },
                {
                    date: "July 22",
                    topic: "Nuclear Chemistry",
                    class_average: 87,
                    student_score: 99
                },
                {
                    date: "July 24",
                    topic: "Environmental Chemistry",
                    class_average: 81,
                    student_score: 77
                }
            ]    
        },
        {
            subject:"Social Studies",
            subject_teacher:"Rama Kumar",
            listing:[
                {
                    date: "July 17",
                    topic: "India Geography",
                    class_average: 89,
                    student_score: 82
                },
                {
                    date: "July 19",
                    topic: "Pre-independent India",
                    class_average: 70,
                    student_score: 88
                },
                {
                    date: "July 20",
                    topic: "Politics in India",
                    class_average: 83,
                    student_score: 95
                },
                {
                    date: "July 20",
                    topic: "Natural Resources",
                    class_average: 92,
                    student_score: 97
                },
                {
                    date: "July 23",
                    topic: "Books of the Past",
                    class_average: 84,
                    student_score: 94
                }
            ]   
        },
        {
            subject:"English",
            subject_teacher:"Shivani Lal",
            listing:[
                {
                    date: "July 16",
                    topic: "Ghost of Canterville",
                    class_average: 87,
                    student_score: 91
                },
                {
                    date: "July 18",
                    topic: "Tale of Two cities",
                    class_average: 82,
                    student_score: 88
                },
                {
                    date: "July 19",
                    topic: "Ranga's Marriage",
                    class_average: 94,
                    student_score: 96
                },
                {
                    date: "July 21",
                    topic: "Wolf Grey",
                    class_average: 89,
                    student_score: 100
                },
                {
                    date: "July 23",
                    topic: "Lorum Ipsum",
                    class_average: 71,
                    student_score: 72
                }
            ]    
        },
        {
            subject:"Second Language",
            subject_teacher:"Swagata Rudra",
            listing:[
                {
                    date: "July 18",
                    topic: "Shlokas",
                    class_average: 74,
                    student_score: 99
                },
                {
                    date: "July 19",
                    topic: "Vedas",
                    class_average: 84,
                    student_score: 80
                },
                {
                    date: "July 20",
                    topic: "Yajurveda",
                    class_average: 87,
                    student_score: 92
                },
                {
                    date: "July 20",
                    topic: "Atharvaveda",
                    class_average: 93,
                    student_score: 90
                },
                {
                    date: "July 25",
                    topic: "Sandhi",
                    class_average: 92,
                    student_score: 96
                }
            ]   
        },
        {
            subject:"FIT",
            subject_teacher:"Sandeep Raut",
            listing:[
                {
                    date: "July 17",
                    topic: "Binary Representation",
                    class_average: 95,
                    student_score: 99
                },
                {
                    date: "July 19",
                    topic: "Basics of HTML",
                    class_average: 10,
                    student_score: 100
                },
                {
                    date: "July 20",
                    topic: "Basics of XML",
                    class_average: 73,
                    student_score: 82
                },
                {
                    date: "July 21",
                    topic: "JSON introduction",
                    class_average: 87,
                    student_score: 76
                },
                {
                    date: "July 25",
                    topic: "Concepts of Javascript",
                    class_average: 82,
                    student_score: 77
                }
            ]
        }
    ]
}
var test=new Performance(mock);

