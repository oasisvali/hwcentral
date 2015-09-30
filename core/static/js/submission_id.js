var SHOW_HINT_BUTTON_CLASS = 'show_hint_button';
var HIDE_HINT_BUTTON_CLASS = 'hide_hint_button';
var SHOW_HINT_BUTTON_TEXT = 'Show Hint';
var HIDE_HINT_BUTTON_TEXT = 'Hide Hint';

var QUESTION_SUBPART_HINT_SELECTOR = '.question_subpart_hint';
var HINT_HIDING_CLASS = 'question_subpart_hint_hidden';

var SHOW_SOLUTION_BUTTON_CLASS = 'show_solution_button';
var HIDE_SOLUTION_BUTTON_CLASS = 'hide_solution_button';
var SHOW_SOLUTION_BUTTON_TEXT = 'Show Solution';
var HIDE_SOLUTION_BUTTON_TEXT = 'Hide Solution';

var QUESTION_SUBPART_SOLUTION_SELECTOR = '.question_subpart_solution';
var SOLUTION_HIDING_CLASS = 'question_subpart_solution_hidden';



$(document).ready(function () {
    $(document).on('click', '.'.concat(SHOW_HINT_BUTTON_CLASS), function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the hint visible
        $this.next(QUESTION_SUBPART_HINT_SELECTOR).removeClass(HINT_HIDING_CLASS);
        // update the button value
        $this.html(HIDE_HINT_BUTTON_TEXT);
        // update the button class
        $this.removeClass(SHOW_HINT_BUTTON_CLASS);
        $this.addClass(HIDE_HINT_BUTTON_CLASS);
    });

    $(document).on('click', '.'.concat(HIDE_HINT_BUTTON_CLASS), function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the hint invisible
        $this.next(QUESTION_SUBPART_HINT_SELECTOR).addClass(HINT_HIDING_CLASS);
        // update the button value
        $this.html(SHOW_HINT_BUTTON_TEXT);
        // update the button class
        $this.removeClass(HIDE_HINT_BUTTON_CLASS);
        $this.addClass(SHOW_HINT_BUTTON_CLASS);
    });

    $(document).on('click', '.'.concat(SHOW_SOLUTION_BUTTON_CLASS), function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the solution visible
        $this.next(QUESTION_SUBPART_SOLUTION_SELECTOR).removeClass(SOLUTION_HIDING_CLASS);
        // update the button value
        $this.html(HIDE_SOLUTION_BUTTON_TEXT);
        // update the button class
        $this.removeClass(SHOW_SOLUTION_BUTTON_CLASS);
        $this.addClass(HIDE_SOLUTION_BUTTON_CLASS);
    });

    $(document).on('click', '.'.concat(HIDE_SOLUTION_BUTTON_CLASS), function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the solution invisible
        $this.next(QUESTION_SUBPART_SOLUTION_SELECTOR).addClass(SOLUTION_HIDING_CLASS);
        // update the button value
        $this.html(SHOW_SOLUTION_BUTTON_TEXT);
        // update the button class
        $this.removeClass(HIDE_SOLUTION_BUTTON_CLASS);
        $this.addClass(SHOW_SOLUTION_BUTTON_CLASS);
    });

    $("#revision_button").click(function(){
        $("#revision_modal").modal('show');
    });

    // this will only have an effect if the global chosen has not been applied (to prevent global chosen from being applied,
    // the skip-global-chosen id must be present on page)
    $('select').chosen( {
        disable_search: true,
        width: '300px'
    });

});
