function PerformanceBreakdownElement(performance_breakdown_element){
	this.date=performance_breakdown_element.date;
	this.topic=performance_breakdown_element.topic;
	this.subjectroom_average=performance_breakdown_element.subjectroom_average;
	this.student_score=performance_breakdown_element.student_score;
}

function PerformanceBreakdown(performance_breakdown){
	this.subject=performance_breakdown.subject;
    this.subject_teacher=performance_breakdown.subject_teacher;
	this.listing=performance_breakdown.listing;
}

function PerformanceReportElement(performance_report_element){
    this.subject=performance_report_element.subject;
    this.student_average=performance_report_element.student_average;
    this.subjectroom_average=performance_report_element.subjectroom_average;
}

function PerformanceReport(performance_report){
    this.class_teacher=performance_report.class_teacher;
    this.listing=performance_report.listing;
    
}
 
function Performance(performance){
    this.performance_report=performance.performance_report;
    this.breakdown_listing=performance.breakdown_listing;
}

function SubjectroomPerformanceBreakdownElement(subjectroom_performance_breakdown_element){
    this.date=subjectroom_performance_breakdown_element.date;
    this.topic=subjectroom_performance_breakdown_element.topic;
    this.subjectroom_average= subjectroom_performance_breakdown_element.subjectroom_average;
    this.standard_average=subjectroom_performance_breakdown_element.standard_average;
}


function SubjectroomPerformanceBreakdown(subjectroom_performance_breakdown){
    this.subject_room= subjectroom_performance_breakdown.subject_room;
    this.subject_teacher=subjectroom_performance_breakdown.subject_teacher;
    this.listing=subjectroom_performance_breakdown.listing;
}

function AssignmentPerformanceElement(assignment_performance_element){
    this.full_name=assignment_performance_element.full_name;
    this.score=assignment_performance_element.score;
}

var mock_assignment1_performancedata1={
    full_name: "Sharang Pai",
    score: 91
}

var mock_assignment1_performancedata2={
    full_name: "Oasis Vali",
    score: 100
}

var mock_assignment1_performancedata3={
    full_name: "Sidhant Pai",
    score: 92
}

var mock_assignment1_performancedata4={
    full_name: "Pujan Parikh",
    score: 82
}

var mock_assignment1_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 77
}

var mock_assignment1_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 75
}

var mock_assignment1_performancedata7={
    full_name: "Arpit Mathur",
    score: 79
}
var mock_assignment1_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 83
}

var mock_assignment1_performancedata9={
    full_name: "Shlok Singh",
    score: 11
}

var mock_assignment1_performancedata10={
    full_name: "Kanye West",
    score: 32
}

var mock_assignment1_performancedata11={
    full_name: "Lorem Ipsum",
    score: 73
}

var mock_assignment2_performancedata1={
    full_name: "Sharang Pai",
    score: 91
}

var mock_assignment2_performancedata2={
    full_name: "Oasis Vali",
    score: 100
}

var mock_assignment2_performancedata3={
    full_name: "Sidhant Pai",
    score: 92
}

var mock_assignment2_performancedata4={
    full_name: "Pujan Parikh",
    score: 82
}

var mock_assignment2_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 77
}

var mock_assignment2_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 75
}

var mock_assignment2_performancedata7={
    full_name: "Arpit Mathur",
    score: 79
}
var mock_assignment2_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 83
}

var mock_assignment2_performancedata9={
    full_name: "Shlok Singh",
    score: 11
}

var mock_assignment2_performancedata10={
    full_name: "Kanye West",
    score: 32
}

var mock_assignment2_performancedata11={
    full_name: "Lorem Ipsum",
    score: 73
}

var mock_assignment2_performancedata1={
    full_name: "Sharang Pai",
    score: 82
}

var mock_assignment2_performancedata2={
    full_name: "Oasis Vali",
    score: 94
}

var mock_assignment2_performancedata3={
    full_name: "Sidhant Pai",
    score: 91
}

var mock_assignment2_performancedata4={
    full_name: "Pujan Parikh",
    score: 88
}

var mock_assignment2_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 72
}

var mock_assignment2_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 86
}

var mock_assignment2_performancedata7={
    full_name: "Arpit Mathur",
    score: 99
}
var mock_assignment2_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 94
}

var mock_assignment2_performancedata9={
    full_name: "Shlok Singh",
    score: 83
}

var mock_assignment2_performancedata10={
    full_name: "Kanye West",
    score: 95
}

var mock_assignment2_performancedata11={
    full_name: "Lorem Ipsum",
    score: 54
}

var mock_assignment3_performancedata1={
    full_name: "Sharang Pai",
    score: 33
}

var mock_assignment3_performancedata2={
    full_name: "Oasis Vali",
    score: 25
}

var mock_assignment3_performancedata3={
    full_name: "Sidhant Pai",
    score: 98
}

var mock_assignment3_performancedata4={
    full_name: "Pujan Parikh",
    score: 38
}

var mock_assignment3_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 54
}

var mock_assignment3_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 44
}

var mock_assignment3_performancedata7={
    full_name: "Arpit Mathur",
    score: 53
}
var mock_assignment3_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 88
}

var mock_assignment3_performancedata9={
    full_name: "Shlok Singh",
    score: 100
}

var mock_assignment3_performancedata10={
    full_name: "Kanye West",
    score: 57
}

var mock_assignment3_performancedata11={
    full_name: "Lorem Ipsum",
    score: 52
}

var mock_assignment4_performancedata1={
    full_name: "Sharang Pai",
    score: 88
}

var mock_assignment4_performancedata2={
    full_name: "Oasis Vali",
    score: 76
}

var mock_assignment4_performancedata3={
    full_name: "Sidhant Pai",
    score: 77
}

var mock_assignment4_performancedata4={
    full_name: "Pujan Parikh",
    score: 91
}

var mock_assignment4_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 77
}

var mock_assignment4_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 25
}

var mock_assignment4_performancedata7={
    full_name: "Arpit Mathur",
    score: 33
}
var mock_assignment4_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 67
}

var mock_assignment4_performancedata9={
    full_name: "Shlok Singh",
    score: 8
}

var mock_assignment4_performancedata10={
    full_name: "Kanye West",
    score: 65
}

var mock_assignment4_performancedata11={
    full_name: "Lorem Ipsum",
    score: 81
}

var mock_assignment5_performancedata1={
    full_name: "Sharang Pai",
    score: 90
}

var mock_assignment5_performancedata2={
    full_name: "Oasis Vali",
    score: 84
}

var mock_assignment5_performancedata3={
    full_name: "Sidhant Pai",
    score: 36
}

var mock_assignment5_performancedata4={
    full_name: "Pujan Parikh",
    score: 32
}

var mock_assignment5_performancedata5={
    full_name: "Hrishikesh Rao",
    score: 39
}

var mock_assignment5_performancedata6={
    full_name: "Abizer Lokhandwala",
    score: 47
}

var mock_assignment5_performancedata7={
    full_name: "Arpit Mathur",
    score: 49
}
var mock_assignment5_performancedata8={
    full_name: "Rutwik Dhongde",
    score: 76
}

var mock_assignment5_performancedata9={
    full_name: "Shlok Singh",
    score: 90
}

var mock_assignment5_performancedata10={
    full_name: "Kanye West",
    score: 94
}

var mock_assignment5_performancedata11={
    full_name: "Lorem Ipsum",
    score: 65

}

var mock_subjectroomdata1={
    subject_room: "8-A Mathematics",
    subject_teacher: "Anjali Lal",
    listing:[
        {
            date: "July 20",
            topic: "Mensuration",
            subjectroom_average: 85,
            standard_average:83
        },
        {
            date: "July 22",
            topic: "Triangles",
            subjectroom_average: 88,
            standard_average:81
        },
        {
            date: "July 23",
            topic: "Basics of Geometry",
            subjectroom_average: 81,
            standard_average:90
        },
        {
            date: "July 24",
            topic: "Linear equations",
            subjectroom_average: 91,
            standard_average:84
        },
        {
            date: "July 29",
            topic: "Quadratic equations",
            subjectroom_average: 83,
            standard_average:86
        }
    ]
}
var mock_subjectroomdata2={
    subject_room: "8-B Mathematics",
    subject_teacher: "Pujan Parikh",
    listing:[
        {
            date: "July 20",
            topic: "Mensuration",
            subjectroom_average: 95,
            standard_average:83
        },
        {
            date: "July 22",
            topic: "Triangles",
            subjectroom_average: 84,
            standard_average:81
        },
        {
            date: "July 23",
            topic: "Basics of Geometry",
            subjectroom_average: 88,
            standard_average:90
        },
        {
            date: "July 24",
            topic: "Linear equations",
            subjectroom_average: 90,
            standard_average:84
        },
        {
            date: "July 29",
            topic: "Quadratic equations",
            subjectroom_average: 87,
            standard_average:86
        }
    ]
}
var mock_subjectroomdata3={
    subject_room: "8-C Mathematics",
    subject_teacher: "Hrishikesh Rao",
    listing:[
        {
            date: "July 20",
            topic: "Mensuration",
            subjectroom_average: 99,
            standard_average:83
        },
        {
            date: "July 22",
            topic: "Triangles",
            subjectroom_average: 98,
            standard_average:81
        },
        {
            date: "July 23",
            topic: "Basics of Geometry",
            subjectroom_average: 94,
            standard_average:90
        },
        {
            date: "July 24",
            topic: "Linear equations",
            subjectroom_average: 98,
            standard_average:84
        },
        {
            date: "July 29",
            topic: "Quadratic equations",
            subjectroom_average: 100,
            standard_average:86
        }
    ]
}
var mock_subjectroomdata4={
    subject_room: "8-D Mathematics",
    subject_teacher: "Oasis Vali",
    listing:[
        {
            date: "July 20",
            topic: "Mensuration",
            subjectroom_average: 78,
            standard_average:83
        },
        {
            date: "July 22",
            topic: "Triangles",
            subjectroom_average: 86,
            standard_average:81
        },
        {
            date: "July 23",
            topic: "Basics of Geometry",
            subjectroom_average: 89,
            standard_average:90
        },
        {
            date: "July 24",
            topic: "Linear equations",
            subjectroom_average: 75,
            standard_average:84
        },
        {
            date: "July 29",
            topic: "Quadratic equations",
            subjectroom_average: 100,
            standard_average:86
        }
    ]
}

var mock_studentdata={
    performance_report:{    
        class_teacher: "Oasis Vali",
        listing: [ 
            { 
                subject:"Mathematics",
                student_average: 56,
                subjectroom_average:83
            },
            {
                subject:"Science",
                student_average:82,
                subjectroom_average:77,
            },
            {
                subject:"Social Studies",
                student_average:88,
                subjectroom_average:81,
            },
            {
                subject:"English",
                student_average:91,
                subjectroom_average:88,
            },
            {
                subject:"Second Language",
                student_average:95,
                subjectroom_average:97,
            },
            {
                subject:"FIT",
                student_average:84,
                subjectroom_average:89,
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
                    subjectroom_average: 81,
                    student_score: 88
                },
                {
                    date: "July 19",
                    topic: "Series and Sequences",
                    subjectroom_average: 84,
                    student_score: 86
                },
                {
                    date: "July 20",
                    topic: "Integration",
                    subjectroom_average: 94,
                    student_score: 96
                },
                {
                    date: "July 21",
                    topic: "3D Geometry",
                    subjectroom_average: 95,
                    student_score: 91
                },
                {
                    date: "July 23",
                    topic: "Probability",
                    subjectroom_average: 77,
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
                    subjectroom_average: 89,
                    student_score: 83
                },
                {
                    date: "July 19",
                    topic: "Atoms and Molecules",
                    subjectroom_average: 83,
                    student_score: 28
                },
                {
                    date: "July 21",
                    topic: "Redox Reactions",
                    subjectroom_average: 74,
                    student_score: 91
                },
                {
                    date: "July 22",
                    topic: "Nuclear Chemistry",
                    subjectroom_average: 87,
                    student_score: 99
                },
                {
                    date: "July 24",
                    topic: "Environmental Chemistry",
                    subjectroom_average: 81,
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
                    subjectroom_average: 89,
                    student_score: 82
                },
                {
                    date: "July 19",
                    topic: "Pre-independent India",
                    subjectroom_average: 70,
                    student_score: 88
                },
                {
                    date: "July 20",
                    topic: "Politics in India",
                    subjectroom_average: 83,
                    student_score: 95
                },
                {
                    date: "July 20",
                    topic: "Natural Resources",
                    subjectroom_average: 92,
                    student_score: 97
                },
                {
                    date: "July 23",
                    topic: "Books of the Past",
                    subjectroom_average: 84,
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
                    subjectroom_average: 87,
                    student_score: 91
                },
                {
                    date: "July 18",
                    topic: "Tale of Two cities",
                    subjectroom_average: 82,
                    student_score: 88
                },
                {
                    date: "July 19",
                    topic: "Ranga's Marriage",
                    subjectroom_average: 94,
                    student_score: 96
                },
                {
                    date: "July 21",
                    topic: "Wolf Grey",
                    subjectroom_average: 89,
                    student_score: 100
                },
                {
                    date: "July 23",
                    topic: "Lorum Ipsum",
                    subjectroom_average: 71,
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
                    subjectroom_average: 74,
                    student_score: 99
                },
                {
                    date: "July 19",
                    topic: "Vedas",
                    subjectroom_average: 84,
                    student_score: 80
                },
                {
                    date: "July 20",
                    topic: "Yajurveda",
                    subjectroom_average: 87,
                    student_score: 92
                },
                {
                    date: "July 20",
                    topic: "Atharvaveda",
                    subjectroom_average: 93,
                    student_score: 90
                },
                {
                    date: "July 25",
                    topic: "Sandhi",
                    subjectroom_average: 92,
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
                    subjectroom_average: 95,
                    student_score: 99
                },
                {
                    date: "July 19",
                    topic: "Basics of HTML",
                    subjectroom_average: 10,
                    student_score: 100
                },
                {
                    date: "July 20",
                    topic: "Basics of XML",
                    subjectroom_average: 73,
                    student_score: 82
                },
                {
                    date: "July 21",
                    topic: "JSON introduction",
                    subjectroom_average: 87,
                    student_score: 76
                },
                {
                    date: "July 25",
                    topic: "Concepts of Javascript",
                    subjectroom_average: 82,
                    student_score: 77
                }
            ]
        }
    ]
}
var studentdata=new Performance(mock_studentdata);

var subjectroomdata1 = new SubjectroomPerformanceBreakdown(mock_subjectroomdata1);
var subjectroomdata2 = new SubjectroomPerformanceBreakdown(mock_subjectroomdata2);
var subjectroomdata3 = new SubjectroomPerformanceBreakdown(mock_subjectroomdata3);
var subjectroomdata4 = new SubjectroomPerformanceBreakdown(mock_subjectroomdata4);

var subjectroomarray=[subjectroomdata1,subjectroomdata2,subjectroomdata3,subjectroomdata4];

var assignment1_student1= new AssignmentPerformanceElement(mock_assignment1_performancedata1);
var assignment1_student2= new AssignmentPerformanceElement(mock_assignment1_performancedata2);
var assignment1_student3= new AssignmentPerformanceElement(mock_assignment1_performancedata3);
var assignment1_student4= new AssignmentPerformanceElement(mock_assignment1_performancedata4);
var assignment1_student5= new AssignmentPerformanceElement(mock_assignment1_performancedata5);
var assignment1_student6= new AssignmentPerformanceElement(mock_assignment1_performancedata6);
var assignment1_student7= new AssignmentPerformanceElement(mock_assignment1_performancedata7);
var assignment1_student8= new AssignmentPerformanceElement(mock_assignment1_performancedata8);
var assignment1_student9= new AssignmentPerformanceElement(mock_assignment1_performancedata9);
var assignment1_student10= new AssignmentPerformanceElement(mock_assignment1_performancedata10);
var assignment1_student11= new AssignmentPerformanceElement(mock_assignment1_performancedata11);

var assignment2_student1= new AssignmentPerformanceElement(mock_assignment2_performancedata1);
var assignment2_student2= new AssignmentPerformanceElement(mock_assignment2_performancedata2);
var assignment2_student3= new AssignmentPerformanceElement(mock_assignment2_performancedata3);
var assignment2_student4= new AssignmentPerformanceElement(mock_assignment2_performancedata4);
var assignment2_student5= new AssignmentPerformanceElement(mock_assignment2_performancedata5);
var assignment2_student6= new AssignmentPerformanceElement(mock_assignment2_performancedata6);
var assignment2_student7= new AssignmentPerformanceElement(mock_assignment2_performancedata7);
var assignment2_student8= new AssignmentPerformanceElement(mock_assignment2_performancedata8);
var assignment2_student9= new AssignmentPerformanceElement(mock_assignment2_performancedata9);
var assignment2_student10= new AssignmentPerformanceElement(mock_assignment2_performancedata10);
var assignment2_student11= new AssignmentPerformanceElement(mock_assignment2_performancedata11);

var assignment3_student1= new AssignmentPerformanceElement(mock_assignment3_performancedata1);
var assignment3_student2= new AssignmentPerformanceElement(mock_assignment3_performancedata2);
var assignment3_student3= new AssignmentPerformanceElement(mock_assignment3_performancedata3);
var assignment3_student4= new AssignmentPerformanceElement(mock_assignment3_performancedata4);
var assignment3_student5= new AssignmentPerformanceElement(mock_assignment3_performancedata5);
var assignment3_student6= new AssignmentPerformanceElement(mock_assignment3_performancedata6);
var assignment3_student7= new AssignmentPerformanceElement(mock_assignment3_performancedata7);
var assignment3_student8= new AssignmentPerformanceElement(mock_assignment3_performancedata8);
var assignment3_student9= new AssignmentPerformanceElement(mock_assignment3_performancedata9);
var assignment3_student10= new AssignmentPerformanceElement(mock_assignment3_performancedata10);
var assignment3_student11= new AssignmentPerformanceElement(mock_assignment3_performancedata11);

var assignment4_student1= new AssignmentPerformanceElement(mock_assignment4_performancedata1);
var assignment4_student2= new AssignmentPerformanceElement(mock_assignment4_performancedata2);
var assignment4_student3= new AssignmentPerformanceElement(mock_assignment4_performancedata3);
var assignment4_student4= new AssignmentPerformanceElement(mock_assignment4_performancedata4);
var assignment4_student5= new AssignmentPerformanceElement(mock_assignment4_performancedata5);
var assignment4_student6= new AssignmentPerformanceElement(mock_assignment4_performancedata6);
var assignment4_student7= new AssignmentPerformanceElement(mock_assignment4_performancedata7);
var assignment4_student8= new AssignmentPerformanceElement(mock_assignment4_performancedata8);
var assignment4_student9= new AssignmentPerformanceElement(mock_assignment4_performancedata9);
var assignment4_student10= new AssignmentPerformanceElement(mock_assignment4_performancedata10);
var assignment4_student11= new AssignmentPerformanceElement(mock_assignment4_performancedata11);

var assignment5_student1= new AssignmentPerformanceElement(mock_assignment5_performancedata1);
var assignment5_student2= new AssignmentPerformanceElement(mock_assignment5_performancedata2);
var assignment5_student3= new AssignmentPerformanceElement(mock_assignment5_performancedata3);
var assignment5_student4= new AssignmentPerformanceElement(mock_assignment5_performancedata4);
var assignment5_student5= new AssignmentPerformanceElement(mock_assignment5_performancedata5);
var assignment5_student6= new AssignmentPerformanceElement(mock_assignment5_performancedata6);
var assignment5_student7= new AssignmentPerformanceElement(mock_assignment5_performancedata7);
var assignment5_student8= new AssignmentPerformanceElement(mock_assignment5_performancedata8);
var assignment5_student9= new AssignmentPerformanceElement(mock_assignment5_performancedata9);
var assignment5_student10= new AssignmentPerformanceElement(mock_assignment5_performancedata10);
var assignment5_student11= new AssignmentPerformanceElement(mock_assignment5_performancedata11);

var assignmentarray =[
    [
        assignment1_student1,
        assignment1_student2,
        assignment1_student3,
        assignment1_student4,
        assignment1_student5,
        assignment1_student6,
        assignment1_student7,
        assignment1_student8,
        assignment1_student9,
        assignment1_student10,
        assignment1_student11
    ],
    [
        assignment2_student1,
        assignment2_student2,
        assignment2_student3,
        assignment2_student4,
        assignment2_student5,
        assignment2_student6,
        assignment2_student7,
        assignment2_student8,
        assignment2_student9,
        assignment2_student10,
        assignment2_student11
    ],
    [
        assignment3_student1,
        assignment3_student2,
        assignment3_student3,
        assignment3_student4,
        assignment3_student5,
        assignment3_student6,
        assignment3_student7,
        assignment3_student8,
        assignment3_student9,
        assignment3_student10,
        assignment3_student11
    ],
    [
        assignment4_student1,
        assignment4_student2,
        assignment4_student3,
        assignment4_student4,
        assignment4_student5,
        assignment4_student6,
        assignment4_student7,
        assignment4_student8,
        assignment4_student9,
        assignment4_student10,
        assignment4_student11
    ],
    [   
        assignment5_student1,
        assignment5_student2,
        assignment5_student3,
        assignment5_student4,
        assignment5_student5,
        assignment5_student6,
        assignment5_student7,
        assignment5_student8,
        assignment5_student9,
        assignment5_student10,
        assignment5_student11
    ]

];