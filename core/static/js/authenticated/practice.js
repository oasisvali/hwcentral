$(document).ready(function () {
    var explorerWidgetHandle = ReactDOM.render(React.createElement(ExplorerWidget, {
        aql_selected_callback: handle_aql_selected,
        aql_unselected_callback: handle_aql_unselected,
        data_endpoint: "question-set-choice-widget/",
        target: $("#id_question_set")
    }), document.getElementById("question-set-explorer"));

    $("#id_subjectroom").chosen().change(explorerWidgetHandle.subjectroomChanged);
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