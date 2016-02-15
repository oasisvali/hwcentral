$(document).ready(function () {
    var SAVE_BUTTON_CLICK = false;

    // save serialized form data
    var PAGE_LOAD_FORM_DATA = $('#uncorrected_submission_form').serialize();

    // set up the save button handler
    $('#charm-save').click(function () {
        SAVE_BUTTON_CLICK = true;
    });
    $('#charm-correct').click(function () {
        SAVE_BUTTON_CLICK = true;
    });

    window.onbeforeunload = function () {
        // dont prompt for save button click
        if (SAVE_BUTTON_CLICK) {
            return undefined;
        }

        // check if there are any unresolved errors in the submission
        if ($('#uncorrected_submission_form .errorlist.nonfield').length > 0) {
            return 'You have unsaved answers (and some of them are invalid)! You will lose them if you navigate away without saving.';
        }

        // check if submission has changed - dont prompt if submission has not changed
        if (PAGE_LOAD_FORM_DATA === $('#uncorrected_submission_form').serialize()) {
            return undefined;
        }

        return 'You have unsaved answers! You will lose them if you navigate away without saving.';
    };
});