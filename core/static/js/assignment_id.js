$(document).ready(function () {
    $(document).on('click', '.show_hint_button', function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the hint visible
        $this.next('.question_hint').removeClass('question_hint_hidden');
        // update the button value
        $this.html('Hide Hint');
        // update the button class
        $this.removeClass('show_hint_button');
        $this.addClass('hide_hint_button');
    });

    $(document).on('click', '.hide_hint_button', function () {   // need delegated (not direct) event handler
        var $this = $(this);
        // make the hint invisible
        $this.next('.question_hint').addClass('question_hint_hidden');
        // update the button value
        $this.html('Show Hint');
        // update the button class
        $this.removeClass('hide_hint_button');
        $this.addClass('show_hint_button');
    });
});
