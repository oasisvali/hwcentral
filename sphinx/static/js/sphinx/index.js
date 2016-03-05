$(document).on("ready", function () {
});

var TYPE_MAP = {
    "0": 0,
    "MCSAQ": 1,
    "MCMAQ": 2,
    "Numerical": 3,
    "Textual": 4
};

function loadModule(moduleName, targetId) {
    var moduleId = "#" + moduleName + "_holder";
    var moduleData = $(moduleId).html();
    $("#" + targetId).html(moduleData);
}

function loadTemplate(x) {
    $("#template_holder").empty();
    loadModule(x.toLowerCase(), 'template_holder');
}

function loadVarConstraints(x) {
    // first load into temp, then use that to repopulate var_constraints
    loadModule('var_constraints', 'temp');
    $("#var_constraints").empty();
    for (var i = 0; i < x; i++) {
        $("#var_constraints").append($("#temp").html());
        $("#var_name").attr("id", "var_name" + i);
        $("#select_num").attr("id", "select_num" + i);
        $("#varType").attr("id", "varType" + i);
    }

}

function loadVarType(x, id) {
    var num = id.substr(id.length - 1);
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

function buildImageName(target) {
    var stub = $(target).val();
    if (stub) {
        return stub + ".png";
    }
    return stub;
}

function loadImageName(source) {
    if (source !== undefined) {
        if (!source.endsWith(".png")) {
            alert("Invalid image name - " + source);
        }
        else {
            return source.substring(0, source.length - 4);
        }
    }
    return source;
}

function generatePreview() {
    var subpart_num = parseInt($("#subpart_index").val());
    // Temp Variables
    var contenttemp = {};
    contenttemp.text = $("#content_text").val();
    contenttemp.img = buildImageName("#content_img");
    var hinttemp = {};
    hinttemp.text = $("#hint_text").val();
    hinttemp.img = buildImageName("#hint_img");
    var solutiontemp = {};
    solutiontemp.text = $("#solution_text").val();
    solutiontemp.img = buildImageName("#solution_img");

    // Create JSON object using common data
    var subpart = {};
    subpart[subpart_num] = {};
    var typenum = TYPE_MAP[$("#select_template").val()];
    if (typenum === 0) {
        alert("No Template selected");
        return;
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

    var vconsttemp = {};
    var x = getVarNum();
    for (var i = 0; i < x; i++) {
        var name = $("#var_name" + i).val();
        if (name == "") {
            alert("Missing variable name");
            return;
        }
        vconsttemp[name] = {};
        var SEPERATOR = ",";
        if (parseInt($("#select_num" + i).val()) != 0) {
            switch (parseInt($("#select_num" + i).val())) {
                case 1:
                    vconsttemp[name].options = $("#varType" + i + " input[name='var_options']").val().split(SEPERATOR).map(Number);
                    break;
                case 2:
                    vconsttemp[name].range = {};
                    vconsttemp[name].range.include = [];
                    vconsttemp[name].range.include[0] = $("#varType" + i + " input[name='var_range']").val().split(SEPERATOR).map(Number);

                    var excludes = $("#varType" + i + " input[name='var_exclude']").val().split(SEPERATOR);
                    if (!((excludes.length === 1) && (excludes[0] === '' ))) {
                        vconsttemp[name].range.exclude = [];
                        vconsttemp[name].range.exclude[0] = excludes.map(Number);
                    }

                    var decimal_val = parseInt($("#varType" + i + " input[name='var_decimal']").val());
                    if (!isNaN(decimal_val)) {
                        vconsttemp[name].range.decimal = decimal_val;
                    }

                    break;
                case 3:
                    vconsttemp[name].fraction = {};
                    vconsttemp[name].fraction.numerator = {};
                    vconsttemp[name].fraction.numerator.rangeint = {};
                    vconsttemp[name].fraction.numerator.rangeint.include = [];
                    vconsttemp[name].fraction.numerator.rangeint.include[0] = $("#varType" + i + " input[name='var_numerator']").val().split(SEPERATOR).map(Number);
                    vconsttemp[name].fraction.denominator = {};
                    vconsttemp[name].fraction.denominator.rangeint = {};
                    vconsttemp[name].fraction.denominator.rangeint.include = [];
                    vconsttemp[name].fraction.denominator.rangeint.include[0] = $("#varType" + i + " input[name='var_denominator']").val().split(SEPERATOR).map(Number);
                    break;
            }
        }

    }

    subpart[subpart_num].variable_constraints = vconsttemp;


    var optionstemp = {};	// Used for MCMAQ, MCSAQ
    var answertemp = {}; // Used for Numericals

    switch (typenum) {
        case 1:
            if ($("#radOrDrop").val() == "drop")
                {optionstemp.use_dropdown_widget = true;}
            optionstemp.correct = {};
            optionstemp.correct.text = $("#MCSAQcorrect #mcqoption").val();
            optionstemp.correct.img = buildImageName("#MCSAQcorrect #mcqoption_img");
            optionstemp.incorrect = [];
            for (var i = 0; i < parseInt($("#MCSAQincorrectselect").val()); i++) {
                optionstemp.incorrect[i] = {
                    "text": $("#mcsaq_incorrect" + i).val(),
                    "img": buildImageName("#mcsaq_incorrect_img" + i)
                };
            }
            subpart[subpart_num].options = optionstemp;
            break;
        case 2:
            optionstemp.correct = [];
            for (var i = 0; i < parseInt($("#MCMAQcorrectselect").val()); i++) {
                optionstemp.correct[i] = {
                    "text": $("#mcmaq_correct" + i).val(),
                    "img": buildImageName("#mcmaq_correct_img" + i)
                };
            }
            optionstemp.incorrect = [];
            for (var i = 0; i < parseInt($("#MCMAQincorrectselect").val()); i++) {
                optionstemp.incorrect[i] = {
                    "text": $("#mcmaq_incorrect" + i).val(),
                    "img": buildImageName("#mcmaq_incorrect_img" + i)
                };
            }
            subpart[subpart_num].options = optionstemp;
            break;
        case 3:
            answertemp.value = coerce_numeric($("#correct_ans").val());
            ;

            var tolerance = coerce_numeric($("#tolerance_ans").val());

            if (!isNaN(tolerance)) {
                answertemp.tolerance = tolerance;
            }

            subpart[subpart_num].answer = answertemp;

            var unit = $('#unit_ans').val();
            if (unit) {
                subpart[subpart_num].unit = unit;
            }
            break;
        case 4:
            subpart[subpart_num].answer = $("#textual_ans").val();
            break;
    }

    console.log("Generated subpart:");
    console.log(subpart[subpart_num]);

    processJSON(subpart[subpart_num]);
}

function coerce_numeric(val) {
    if (!isNaN(val)) {
        return parseFloat(val);
    }
    return val;
}

function updateJSON() {
    var x = JSON.parse($("#resultJSON").val());
    reflectDiv(x);
    processJSON(x);
}

function reflectDiv(json_obj) {
    //clean up left pane
    $('#varNum').val('0').trigger('change');
    $('#select_template').val('0').trigger('change');
    $("#subpart_index").val("");
    $("#content_text").val("");
    $("#content_img").val("");
    $("#hint_text").val("");
    $("#hint_img").val("");
    $("#solution_text").val("");
    $("#solution_img").val("");

    //set subpart_num
    $("#subpart_index").val(json_obj.subpart_index);

    $("#content_text").val(json_obj.content.text);
    $("#content_img").val(loadImageName(json_obj.content.img));

    if (json_obj.hint !== undefined) {
        $("#hint_text").val(json_obj.hint.text);
        $("#hint_img").val(loadImageName(json_obj.hint.img));
    }
    if (json_obj.solution !== undefined) {
        $("#solution_text").val(json_obj.solution.text);
        $("#solution_img").val(loadImageName(json_obj.solution.img));
    }

    // render the right variable constraints
    if (json_obj.variable_constraints) {
        var numvars = Object.keys(json_obj.variable_constraints).length;
        // set the dropdown
        $("#varNum").val(numvars.toString()).trigger('change');
        for (var i = 0; i < numvars; i++) {
            var name = Object.keys(json_obj.variable_constraints)[i];
            $("#var_name" + i).val(name);

            var SEPERATOR = ",";

            if (Object.keys(json_obj.variable_constraints[name]).length !== 0) {
                if (json_obj.variable_constraints[name].options !== undefined) {
                    // set the select
                    $("#select_num" + i).val('1').trigger('change');
                    // populate the options
                    $("#varType" + i + " input[name='var_options']").val(json_obj.variable_constraints[name].options.join(SEPERATOR));
                }
                if (json_obj.variable_constraints[name].range !== undefined) {
                    // set the select
                    $("#select_num" + i).val('2').trigger('change');
                    // populate the include
                    $("#varType" + i + " input[name='var_range']").val(json_obj.variable_constraints[name].range.include[0].join(SEPERATOR));
                    if (json_obj.variable_constraints[name].range.exclude !== undefined) {
                        // populate the exclude
                        $("#varType" + i + " input[name='var_exclude']").val(json_obj.variable_constraints[name].range.exclude[0].join(SEPERATOR));
                    }
                    if (json_obj.variable_constraints[name].range.decimal !== undefined) {
                        // populate the decimal
                        $("#varType" + i + " input[name='var_decimal']").val(json_obj.variable_constraints[name].range.decimal);
                    }
                }
                if (json_obj.variable_constraints[name].fraction !== undefined) {
                    // set the select
                    $("#select_num" + i).val('3').trigger('change');
                    // numerator and denominator rangeint includes must exist. populate them
                    $("#varType" + i + " input[name='var_numerator']").val(json_obj.variable_constraints[name].fraction.numerator.rangeint.include[0].join(SEPERATOR));
                    $("#varType" + i + " input[name='var_denominator']").val(json_obj.variable_constraints[name].fraction.denominator.rangeint.include[0].join(SEPERATOR));
                }

            }

        }
    }

    // Render the subpart-type specific stuff
    var typenum = json_obj.type;
    $('#select_template :nth-child(' + (typenum + 1) + ')').prop('selected', true);
    $("#select_template").trigger('change');
    switch (typenum) {
        case 1:
            if (json_obj.options.use_dropdown_widget) {
                $("#radOrDrop").val('drop');
            }

            // set the select value
            $("#MCSAQincorrectselect").val(json_obj.options.incorrect.length.toString()).trigger('change');

            $("#MCSAQcorrect #mcqoption").val(json_obj.options.correct.text);
            $("#MCSAQcorrect #mcqoption_img").val(loadImageName(json_obj.options.correct.img));
            for (var i = 0; i < json_obj.options.incorrect.length; i++) {
                $("#mcsaq_incorrect" + i).val(json_obj.options.incorrect[i].text);
                $("#mcsaq_incorrect_img" + i).val(loadImageName(json_obj.options.incorrect[i].img));
            }
            break;
        case 2:
            // set the select values
            $("#MCMAQcorrectselect").val(json_obj.options.correct.length.toString()).trigger('change');
            $("#MCMAQincorrectselect").val(json_obj.options.incorrect.length.toString()).trigger('change');

            for (var i = 0; i < json_obj.options.correct.length; i++) {
                $("#mcmaq_correct" + i).val(json_obj.options.correct[i].text);
                $("#mcmaq_correct_img" + i).val(loadImageName(json_obj.options.correct[i].img));
            }

            for (var i = 0; i < json_obj.options.incorrect.length; i++) {
                $("#mcmaq_incorrect" + i).val(json_obj.options.incorrect[i].text);
                $("#mcmaq_incorrect_img" + i).val(loadImageName(json_obj.options.incorrect[i].img));
            }

            break;
        case 3:
            $("#correct_ans").val(json_obj.answer.value);
            $("#tolerance_ans").val(json_obj.answer.tolerance);
            $("#unit_ans").val(json_obj.unit);
            break;
        case 4:
            $("#textual_ans").val(json_obj.answer);
            break;

    }
}

function processJSON(x) {
    sanitize(x);
    console.log('Dumping json');
    $("#resultJSON").val(JSON.stringify(x, null, 2));

    var csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: 'deal-subpart/',
        cache: false,
        data: JSON.stringify({"subpart": x}),
        dataType: 'json',                   // what we expect in response
        contentType: 'application/json',    //what we are sending
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (responseData, textStatus, jqXHR) {
            if (responseData.success) {
                var y = responseData.payload;
                sanitize(y); // backend introduces some null keys which are cruft + cleanup of empty strings and empty obj
                populateDiv(y);
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
    console.log('Rendering result: ');
    console.log(result);

    $("#resultAns").empty();
    $("#resultQues").empty();
    $("#resultHint").empty();
    $("#resultSolution").empty();

    if (result.content.text != null) {
        $("#resultQues").html(result.content.text);
    }

    if (result.hint != null && result.hint.text != null) {
        $("#resultHint").html(result.hint.text);
    }

    if (result.solution != null && result.solution.text != null) {
        $("#resultSolution").html(result.solution.text);
    }

    switch (parseInt(result.type)) {

        case 1:
            $("#resultAns").append(
                "<h4>Correct Answer:</h4><ul><li>" + result.options.correct.text + "</li></ul>"
            );

            $('#resultAns').append("<h4>Incorrect Answers:</h4><ul>");
            for (var i = 0; i < result.options.incorrect.length; i++) {
                $("#resultAns").append("<li>" + result.options.incorrect[i].text + "</li>");
            }
            $('#resultAns').append("</ul>");
            break;
        case 2:
            $("#resultAns").append("<h4>Correct Answers:</h4><ul>");
            for (var i = 0; i < result.options.correct.length; i++) {
                $("#resultAns").append("<li>" + result.options.correct[i].text + "</li>");
            }
            $('#resultAns').append("</ul>");
            $("#resultAns").append("<h4>Incorrect Answers:</h4><ul>");
            for (var i = 0; i < result.options.incorrect.length; i++) {
                $("#resultAns").append("<li>" + result.options.incorrect[i].text + "</li>");
            }
            $('#resultAns').append("</ul>");
            break;
        case 3:
            var unit_str = "";
            if (result.unit) {
                unit_str = result.unit;
            }
            $("#resultAns").html(
                "<h4>Answer:</h4><div><span id='numerical_ans_value'>" + result.answer.value + "</span><span>" + unit_str + "</span></div>"
            );
            break;
        case 4:
            $("#resultAns").html(
                "<h4>Answer:</h4><div>" + result.answer + "</div>"
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
    loadModule('mcqoption', 'temp2');
    $("#MCMAQcorrect").empty();
    for (var i = 0; i < x; i++) {
        $("#MCMAQcorrect").append($("#temp2").html());
        $("#MCMAQcorrect #mcqoption").attr("id", "mcmaq_correct" + i);
        $("#MCMAQcorrect #mcqoption_img").attr("id", "mcmaq_correct_img" + i);
    }
}

function MCMAQincorrect(x) {
    // first load into temp2, the use that to repopulate MCMAQincorrect
    loadModule('mcqoption', 'temp2');
    $("#MCMAQincorrect").empty();
    for (var i = 0; i < x; i++) {
        $("#MCMAQincorrect").append($("#temp2").html());
        $("#MCMAQincorrect #mcqoption").attr("id", "mcmaq_incorrect" + i);
        $("#MCMAQincorrect #mcqoption_img").attr("id", "mcmaq_incorrect_img" + i);
    }
}

function MCSAQincorrect(x) {
    // first load into temp2, then use that to repopulate MCSAQincorrect
    loadModule('mcqoption', 'temp2');
    $("#MCSAQincorrect").empty();
    for (var i = 0; i < x; i++) {
        $("#MCSAQincorrect").append($("#temp2").html());
        $("#MCSAQincorrect #mcqoption").attr("id", "mcsaq_incorrect" + i);
        $("#MCSAQincorrect #mcqoption_img").attr("id", "mcsaq_incorrect_img" + i);
    }
}

function makeTextFile(text) {
    return window.URL.createObjectURL(new Blob([text], {type: 'text/plain'}));
}

function downloadJSON() {
    console.log('downloading');

    var link = document.getElementById('download-hidden-link');
    link.href = makeTextFile($('#resultJSON').val());
    ;
    link.click();   // start the download
}

var NULL_KEYS = ['img_url'];
var EMPTY_STRING_KEYS = ['text', 'img'];
var EMPTY_OBJ_KEYS = ['hint', 'solution'];
var OPTIONAL_FALSE_KEYS = ['use_dropdown_widget'];

function removeNulls(obj) {
    for (var k in obj) {
        if ((obj[k] === null) && (NULL_KEYS.indexOf(k) > -1)) {
            delete obj[k];
        }
        else if (typeof(obj[k]) == "object") {
            removeNulls(obj[k]);
        }
    }
}

function removeEmptyStrings(obj) {
    for (var k in obj) {
        if ((obj[k] === "") && (EMPTY_STRING_KEYS.indexOf(k) > -1)) {
            delete obj[k];
        }
        else if (typeof(obj[k]) == "object") {
            removeEmptyStrings(obj[k]);
        }
    }
}

function removeEmptyObjs(obj) {
    for (var k in obj) {
        if (($.isEmptyObject(obj[k])) && (EMPTY_OBJ_KEYS.indexOf(k) > -1)) {
            delete obj[k];
        }
        else if (typeof(obj[k]) == "object") {
            removeEmptyObjs(obj[k]);
        }
    }
}

function removeOptionalFalse(obj) {
    for (var k in obj) {
        if ((obj[k] === false) && (OPTIONAL_FALSE_KEYS.indexOf(k) > -1)) {
            delete obj[k];
        }
        else if (typeof(obj[k]) == "object") {
            removeOptionalFalse(obj[k]);
        }
    }
}

function sanitize(obj) {
    console.log('sanitizing');
    removeEmptyStrings(obj);
    removeNulls(obj);
    removeEmptyObjs(obj);
    removeOptionalFalse(obj);
    console.log(obj);
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
