$(document).ready(function () {
    setup_teacher();
});

function extract_subjectroom_pk() {
    return parseInt($("#subjectroom-select").val());
}

function extract_student_id() {
    return parseInt($("#student-select-holder > select").val());
}

function setup_teacher() {
    render_disabled_select_in_holder("student-select-holder");

    // enable-disable go button based on subjectroom select state
    $('#subjectroom-select').on('change', function () {
        $("#student-select-holder").empty();
        var subjectroom_pk = extract_subjectroom_pk();
        if (subjectroom_pk > 0) {
            $("#student-select-holder").html($("#student-select-" + subjectroom_pk)[0].outerHTML);
            $("#student-select-holder > select").chosen({width: '300px'});
            $("#go-button").removeClass("disabled_action_button");
        }
        else {
            $("#go-button").addClass("disabled_action_button");
            render_disabled_select_in_holder("student-select-holder");
        }
    });
    // on go button click make ajax request
    $("#go-button").on('click', function () {
        if ($(this).hasClass('disabled_action_button')) {
            return;
        }

        var subjectroom_pk = extract_subjectroom_pk();
        var endpoint = EDGE_ENDPOINT;
        var student_id = extract_student_id();

        if (student_id === 0) {
            endpoint += 'subject/' + subjectroom_pk;
        }
        else {
            endpoint += 'student/' + student_id + '/' + subjectroom_pk;
        }

        reset();
        loading();
        $.getJSON(endpoint, function (data) {
            show_data(data);
            if (student_id === 0) {
                render_questions(data.questions);
            }
        });

    });
}

function render_question_elem(question_elem) {
    if (!question_elem) {
        return "";
    }

    var elem_html = "<div class='question-elem-preview'>";
    if (question_elem.text) {
        elem_html += "<div>" + question_elem.text + "</div>";
    }
    if (question_elem.img_url) {
        elem_html += "<div><img src='" + question_elem.img_url + "' onerror='img_reload(this);'/></div>";
    }
    return elem_html + "</div>";
}

function render_question(question) {
    var question_html = "<li class='question-preview'><div class='container-preview'>" + render_question_elem(question.container.content) + "</div><ol type='a' class='subpart-preview'>";
    for (var i = 0; i < question.subparts.length; i++) {
        question_html += "<li>" + render_question_elem(question.subparts[i].content) + "</li>";
    }
    return question_html + "</ol></li>";
}

function render_questions(questions) {
    var $questions_row = $("#questions-row");
    if (questions.length === 0) {
        $questions_row.html(NO_DATA_IMG);
    }
    else {
        $questions_row.html("<ol type='1' id='questions-list'></ol>");
        var $questions_list = $("#questions-list");
        for (var i = 0; i < questions.length; i++) {
            var question_html = render_question(questions[i].data_model);
            $questions_list.append(question_html);
        }

        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    $("#questions-holder").removeClass('hidden');

}