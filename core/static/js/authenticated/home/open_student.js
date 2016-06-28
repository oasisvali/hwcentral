$(document).ready(function () {
    var explorerWidgetHandle = ReactDOM.render(React.createElement(ExplorerWidget, {
        aql_selected_callback: handle_aql_selected,
        aql_unselected_callback: handle_aql_unselected,
        first_pane_initial_selection: function () {
            return 0;
        },
        skip_first_pane: false,
        panes: [
            ["Subject", 2],
            ["Chapter", 4],
            ["Set #", 2]
        ],
        description_width: 4,
        data_endpoint: "question-set-choice-widget/",
        target: $("#id_question_set")
    }), document.getElementById("question-set-explorer"));

    $("#grade-change-dropdown > li").on('click', function () {
        var clicked_grade = parseInt($(this).html());
        var current_grade = parseInt($("#current-grade").html());

        if (clicked_grade === current_grade) {
            return;
        }

        // confirm that the user wishes to change the grade
        if (!confirm("Are you sure you wish to change your Grade? Your progress with your current grade will be saved.")) {
            return;
        }

        // set the clicked id in the grade-change-form
        var clicked_id = parseInt($(this).attr("id"));
        $("#new-grade-select").val(clicked_id);

        // submit the form
        document.getElementById('grade-change-form').submit();
    });
});

function handle_aql_unselected() {

    //disable submit button
    $submit_button = $("#submit_button");
    $submit_button.addClass("disabled_action_button");
    $submit_button.prop("disabled", true);
}

function handle_aql_selected() {

    // enable submit button
    $submit_button = $("#submit_button");
    $submit_button.removeClass("disabled_action_button");
    $submit_button.prop("disabled", false);
}