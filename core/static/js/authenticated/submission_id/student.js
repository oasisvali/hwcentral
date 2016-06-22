$(document).ready(function () {

    $('#charm-correct').on('click', function (e) {
        var x = window.confirm("Are you sure you want to submit this assignment for correction? You will not be able to change any answers once the assignment is corrected.");
        if (x) {
        }
        else {
            e.preventDefault();
        }
    });
});