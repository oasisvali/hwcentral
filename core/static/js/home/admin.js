$(document).ready(function(){
    $('#classrooms_table .classrooms_table_classroom').click(function(){
        $(this).nextUntil('#classrooms_table .classrooms_table_classroom').slideToggle(500);
    });
});