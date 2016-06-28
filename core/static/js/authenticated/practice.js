$(document).ready(function () {
    var explorerWidgetHandle = ReactDOM.render(React.createElement(ExplorerWidget, {
        aql_selected_callback: handle_aql_selected,
        aql_unselected_callback: handle_aql_unselected,
        first_pane_initial_selection: get_selected_subjectroom,
        skip_first_pane: true,
        panes: [
            ["Subject", 0],
            ["Chapter", 4],
            ["Set #", 2]
        ],
        description_width: 6,
        data_endpoint: "question-set-choice-widget/",
        target: $("#id_question_set")
    }), document.getElementById("question-set-explorer"));

    $("#id_subjectroom").chosen().change(function () {
        explorerWidgetHandle.selectionChanged(0, get_selected_subjectroom());
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

function get_selected_subjectroom() {
    // check which subjectroom is selected
    var selected_subjectroom = $("#id_subjectroom").val();
    if (selected_subjectroom === "") {
        selected_subjectroom = 0;
    }
    else {
        selected_subjectroom = parseInt(selected_subjectroom);
    }
    return selected_subjectroom;
}