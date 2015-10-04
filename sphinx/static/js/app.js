$(document).on("ready", function () {
    loadModule('var_constraints', 'temp');
    loadModule('mcmaq_subpart', 'temp2');
});

function loadModule(moduleName, targetId) {
    var moduleId = "#" + moduleName + "_holder";
    var moduleData = $(moduleId).html();
    $("#" + targetId).html(moduleData);
}

function loadTemplate(x) {
    loadModule(x.toLowerCase(), 'template_holder');
}

function loadVarConstraints(x) {
    // first load into temp, the use that to repopulate var_constraints
    loadModule('var_constraints', 'temp');
    $("#var_constraints").html("");
    for (var i = 0; i < x; i++) {
        $("#var_constraints").append($("#temp").html());
        $("#var_name").attr("id", "var_name" + i);
        $("#select_num").attr("id", "select_num" + i);
        $("#varType").attr("id", "varType" + i);
    }

}

function loadVarType(x, id) {
    var num = id.substr(id.length - 1);
    console.log(num);
    switch (parseInt(x)) {
        case 1:
            loadModule('options', 'varType' + num);
            break;
        case 2:
            loadModule('range', 'varType' + num);
            break;
        case 3:
            loadModule('fraction', 'varType' + num);
            break;
    }
}

function generatePreview() {
    var subpart_num = parseInt($("#subpart_index").val());
    console.log($("#subpart_index").val());
    // Temp Variables
    var contenttemp = {};
    contenttemp.text = $("#content_text").val();
    contenttemp.img = $("#content_img").val();
    var hinttemp = {};
    hinttemp.text = $("#hint_text").val();
    hinttemp.img = $("#hint_img").val();
    var solutiontemp = {};
    solutiontemp.text = $("#solution_text").val();
    solutiontemp.img = $("#solution_img").val();
    var vconsttemp = {};
    var x = getVarNum();
    for (var i = 0; i < x; i++) {
        var name = $("#var_name" + i).val();
        vconsttemp[name] = {};
        if (parseInt($("#select_num" + i).val()) != 0) {
                        switch (parseInt($("#select_num" + i).val())) {
                        case 1:
                            vconsttemp[name].options = $("#varType" + i + " input[name='var_options']").val().split(",").map(Number);
                            break;
                        case 2:
                            vconsttemp[name].range = {};
                            vconsttemp[name].range.include = [];
                            vconsttemp[name].range.include[0] = $("#varType" + i + " input[name='var_range']").val().split("-").map(Number);
                            vconsttemp[name].range.exclude = [];
                            vconsttemp[name].range.exclude[0] = $("#varType" + i + " input[name='var_exclude']").val().split("-").map(Number);
                            vconsttemp[name].range.decimal = parseInt($("#varType" + i + " input[name='var_decimal']").val());
                            break;
                        case 3:
                            vconsttemp[name].fraction = {};
                            vconsttemp[name].fraction.numerator = {};
                            vconsttemp[name].fraction.numerator.rangeint = {};
                            vconsttemp[name].fraction.numerator.rangeint.include = [];
                            vconsttemp[name].fraction.numerator.rangeint.include[0]= $("#varType" + i + " input[name='var_numerator']").val().split("-").map(Number);
                            vconsttemp[name].fraction.denominator = {};
                            vconsttemp[name].fraction.denominator.rangeint = {};
                            vconsttemp[name].fraction.numerator.rangeint.include = [];
                            vconsttemp[name].fraction.numerator.rangeint.include[0] = $("#varType" + i + " input[name='var_denominator']").val().split("-").map(Number);
                            break;
                    }
        }

    }

    // Create JSON object using common data
    var subpart = {};
    subpart[subpart_num] = {};
    var typenum;
    switch ($("#select_template").val()){
        case "0":   alert("No Template selected");
                    typenum = 0;
                    return;
        case "MCSAQ":   typenum = 1;
                        break;
        case "MCSAQ":   typenum = 2;
                        break;
        case "Numerical":   typenum = 3;
                            break;
        case "Textual":     typenum = 4;
                            break;

    }
    subpart[subpart_num].type = typenum;
    subpart[subpart_num].content = contenttemp;
    if (($("#subpart_index").val()) == ""){
        alert("No Subpart Index");
        return;
    } 
    subpart[subpart_num].subpart_index = parseInt($("#subpart_index").val());
    subpart[subpart_num].hint = hinttemp;
    subpart[subpart_num].solution = solutiontemp;
    subpart[subpart_num].variable_constraints = vconsttemp;


    var optionstemp = {};	// Used for MCMAQ, MCSAQ
    var answertemp = {}; // Used for Numericals
    var answertext; // Used Textual

    switch (typenum) {
        case 1:
            if ($("#radOrDrop").val() == "drop")
                {optionstemp.use_dropdown_widget = true;}
            optionstemp.correct = {};
            optionstemp.correct.text = $("#correct_text").val();
            optionstemp.correct.img = $("#correct_img").val();
            optionstemp.incorrect = [];
            optionstemp.incorrect[0] = {"text": $("#incorrect_text1").val(), "img": $("#incorrect_img1").val()};
            optionstemp.incorrect[1] = {"text": $("#incorrect_text2").val(), "img": $("#incorrect_img2").val()};
            optionstemp.incorrect[2] = {"text": $("#incorrect_text3").val(), "img": $("#incorrect_img3").val()};
            subpart[subpart_num].options = optionstemp;
            break;
        case 2:
            optionstemp.correct = [];
            for (var i = 0; i < parseInt($("#MCMAQcorrectselect").val()); i++) {
                optionstemp.correct[i] = {
                    "text": $("#mcmaq_correct" + i).val(),
                    "img": $("#mcmaq_correct_img" + i).val()
                };
            }
            optionstemp.incorrect = [];
            for (var i = 0; i < parseInt($("#MCMAQincorrectselect").val()); i++) {
                optionstemp.incorrect[i] = {
                    "text": $("#mcmaq_incorrect" + i).val(),
                    "img": $("#mcmaq_incorrect_img" + i).val()
                };
            }
            subpart[subpart_num].options = optionstemp;
            break;
        case 3:
            answertemp.value = $("#correct_ans").val();
            answertemp.tolerance = $("#tolerance_ans").val();
            subpart[subpart_num].answer = answertemp;
            break;
        case 4:
            answertext = $("#textual_ans").val();
            subpart[subpart_num].answer = answertext;
            break;
    }


    console.log(subpart[subpart_num]);

    processJSON(subpart[subpart_num]);
}


function processJSON(x) {

    var csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: 'deal-subpart/',
        cache: false,
        data: JSON.stringify({"subpart": x}),
        dataType: 'json',                   // what we expect in response
        contentType: 'application/json',    //what we are sending
        beforeSend: function (request) {
            console.log(JSON.stringify({"subpart": x}));
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (responseData, textStatus, jqXHR) {
            if (responseData.success) {
                var y = responseData.payload;
                populateDiv(y);
                console.log(y);
            }
            else {
                alert('Error: ' + responseData.message);
            }
        },
        error: function (responseData, textStatus, errorThrown) {
            alert('POST failed');
        }
    });

}

function populateDiv(result) {
    console.log(result);
    $("#resultQues").html(result.content.text);
    $("#resultHint").html(result.hint.text);
    $("#resultSolution").html(result.solution.text);
    $("#resultJSON").html(JSON.stringify(result, null, 2));
    $("#resultAns").html("");
    switch (parseInt(result.type)) {

        case 1:
            $("#resultAns").html(
                "Correct Answer: " + result.options.correct.text + "<br><br>" +
                "Incorrect Answer 1: " + result.options.incorrect[0].text + "<br>" +
                "Incorrect Answer 2: " + result.options.incorrect[1].text + "<br>" +
                "Incorrect Answer 3: " + result.options.incorrect[2].text + "<br>"
            );
            break;
        case 2:
            $("#resultAns").append("Correct Answers:<br>");
            for (var i = 0; i < result.options.correct.length; i++) {
                $("#resultAns").append(result.options.correct[i].text + "<br>");
            }
            $("#resultAns").append("<br>Incorrect Answers:<br>");
            for (var i = 0; i < result.options.incorrect.length; i++) {
                $("#resultAns").append(result.options.incorrect[i].text + "<br>");
            }
            break;
        case 3:
            $("#resultAns").html(
                "Correct Answer: " + result.answer.value + "<br>"
            );
            break;
        case 4:
            $("#resultAns").html(
                "Correct Answer: " + result.answer + "<br>"
            );
            break;
    }

    updateJax();
}

function updateJax() {
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

function getVarNum() {
    return parseInt($("#varNum").val());
}

function MCMAQcorrect(x) {
    // first load into temp2, the use that to repopulate MCMAQcorrect
    loadModule('mcmaq_subpart', 'temp2');
    console.log("wew");
    $("#MCMAQcorrect").html("");
    for (var i = 0; i < x; i++) {
        $("#MCMAQcorrect").append($("#temp2").html());
        $("#mcmaqsub").attr("id", "mcmaq_correct" + i);
        $("#mcmaqsub_img").attr("id", "mcmaq_correct_img" + i);
    }
}

function MCMAQincorrect(x) {
    // first load into temp2, the use that to repopulate MCMAQincorrect
    loadModule('mcmaq_subpart', 'temp2');
    $("#MCMAQincorrect").html("");
    for (var i = 0; i < x; i++) {
        $("#MCMAQincorrect").append($("#temp2").html());
        $("#mcmaqsub").attr("id", "mcmaq_incorrect" + i);
        $("#mcmaqsub_img").attr("id", "mcmaq_incorrect_img" + i);
    }
}

function downloadJSON() {

}

function editJSON() {
    var x = JSON.parse($("#resultJSON").val());
    processJSON(x);
}

// CSRF protection stuffs

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
