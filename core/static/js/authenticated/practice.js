$(document).ready(function () {
    var explorerWidgetHandle = ReactDOM.render(React.createElement(ExplorerWidget, {
        data_endpoint: "question-set-choice-widget/",
        target: $("#id_question_set")
    }), document.getElementById("question-set-explorer"));

    $("#id_subjectroom").chosen().change(explorerWidgetHandle.subjectroomChanged);
});