$(document).ready(function(){
    $('#classrooms_table .classrooms_table_classroom').click(function(){
        $(this).nextUntil('#classrooms_table .classrooms_table_classroom').slideToggle(500);
        $(this).toggleClass("expanded");
        // if any classroom rows are open, mark the entire table as open
        if ($("#classrooms_table .classrooms_table_classroom.expanded").length > 0) {
            $("#classrooms_table").addClass("open");
        }
        else {
            $("#classrooms_table").removeClass("open");
        }
    });
});