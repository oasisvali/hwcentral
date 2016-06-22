$(document).ready(function () {
    var openExplorerWidgetHandle = ReactDOM.render(React.createElement(OpenExplorerWidget, {
        aql_selected_callback: handle_aql_selected,
        aql_unselected_callback: handle_aql_unselected,
        data_endpoint: "question-set-choice-widget/",
        target: $("#id_question_set")
    }), document.getElementById("question-set-explorer"));

    $("#grade-change-dropdown > li").on('click', function () {
        var id = parseInt($(this).attr("id"));
        var grade = $(this).html();

        // get the value that was clicked and set it in the current grade
        $("#current-grade").html(grade);
        // use the openExplorerWidgetHandle to bind the explorer to the grade dropdown
        openExplorerWidgetHandle.updateFixedStandard(id);

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