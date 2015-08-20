var SUBJECTROOM_SELECT = "#id_subjectroom";
var QUESTION_SET_SELECT = "#id_question_set";
var SELECT_ID_SEPERATOR = "_";

$(document).ready(function () {
    if ($(".pickadate").length) {
        $(function () {
            var ASSIGNED_DATE_INPUT_SELECTOR = "#assigned > #id_assigned_0";
            var DUE_DATE_INPUT_SELECTOR = "#due > #id_due_0";
            var ASSIGNED_TIME_INPUT_SELECTOR = "#assigned > #id_assigned_1";
            var DUE_TIME_INPUT_SELECTOR = "#due > #id_due_1";

            var DATE_FORMAT = "dd mmm yyyy";
            var TIME_FORMAT = "HH:i";


            var ASSIGNED_DATE_PICKER_SETTINGS = {
                format: DATE_FORMAT,
                monthSelector: false, // prevents drop downs for month and year picker
                yearSelector: false,
                onStart: function () {    // sets default date as current date
                    this.set('select', Date.now())
                },
                min: Date.now(), // prevents user from selecting past dates
            };

            var DUE_DATE_PICKER_SETTINGS = {
                format: DATE_FORMAT,
                monthSelector: false,
                yearSelector: false,
            };

            var assigned_input = $(ASSIGNED_DATE_INPUT_SELECTOR).pickadate(ASSIGNED_DATE_PICKER_SETTINGS);

            var due_input = $(DUE_DATE_INPUT_SELECTOR).pickadate(DUE_DATE_PICKER_SETTINGS);


            var assigned_picker = assigned_input.pickadate('picker');

            var due_picker = due_input.pickadate('picker');

            // Check if there’s a “from” date to start with.
            if (assigned_picker.get('value')) {
                due_picker.set('min', assigned_picker.get('select'));
            }

            // When something is selected, update the "submission” limits.
            assigned_picker.on('set', function (event) {
                if (event.select) {
                    due_picker.set('min', assigned_picker.get('select'));
                }
                else if ('clear' in event) {
                    due_picker.set('min', false);
                }
            });

            var ASSIGNED_TIME_PICKER_SETTINGS = {
                format: TIME_FORMAT, // puts format in 24 hour clock
                interval: 120,// sets interval to every 2 hours
            };
            var DUE_TIME_PICKER_SETTINGS = {
                format: TIME_FORMAT, // puts format in 24 hour clock
                interval: 120,// sets interval to every 2 hours
                disable: [ // disables all values except one for selection
                    true,
                    [22, 0],
                ],
            };

            $(ASSIGNED_TIME_INPUT_SELECTOR).pickatime(ASSIGNED_TIME_PICKER_SETTINGS);
            $(DUE_TIME_INPUT_SELECTOR).pickatime(DUE_TIME_PICKER_SETTINGS);

            // prettify
            var DATE_ICON = "<span class=\"input_box_graphic\"><span class=\"glyphicon glyphicon-calendar\"></span></span>";
            var TIME_ICON = "<span class=\"input_box_graphic\"><span class=\"glyphicon glyphicon-time\"></span></span>";

            $(DATE_ICON).insertAfter(ASSIGNED_DATE_INPUT_SELECTOR);
            $(DATE_ICON).insertAfter(DUE_DATE_INPUT_SELECTOR);
            $(TIME_ICON).insertAfter(ASSIGNED_TIME_INPUT_SELECTOR);
            $(TIME_ICON).insertAfter(DUE_TIME_INPUT_SELECTOR);
        });
    }

    // Following code updates the question set select depending on the selection of the subjectroom
    // First make clone of question set select so we can keep resetting the data
    var question_set_data = $(QUESTION_SET_SELECT).clone();
    update_question_set(question_set_data);
    $(SUBJECTROOM_SELECT).chosen().change(function () {
        update_question_set(question_set_data);
    });

    // Following code displays a description of the currently selected question set
    update_description_and_preview_link();
    $(QUESTION_SET_SELECT).chosen().change(update_description_and_preview_link);
});

function update_description_and_preview_link() {
    var DESCRIPTION_CONTAINER = "#aql_description";
    var PREVIEW_LINK_SELECTOR = "#preview_link";

    var val = $(QUESTION_SET_SELECT).val().split(SELECT_ID_SEPERATOR);
    $(DESCRIPTION_CONTAINER).text(val[val.length - 1]);
    var aql_id = val[val.length - 2];

    var preview_link = $(PREVIEW_LINK_SELECTOR).attr('href').split('/');
    preview_link[preview_link.length - 2] = aql_id;
    $(PREVIEW_LINK_SELECTOR).attr('href', preview_link.join('/'));
}

function cast_standard(standard) {
    if (standard !== "*") {
        return parseInt(standard);
    }
    return standard
}

function update_question_set(question_set_data) {
    // First reset the question set option
    $(QUESTION_SET_SELECT).empty();

    // Then check the currently selected subjectroom
    val = $(SUBJECTROOM_SELECT).val().split(SELECT_ID_SEPERATOR);
    var subjectroom_subject = parseInt(val[0]);
    var subjectroom_standard = cast_standard(val[1]);
    //console.log(subjectroom_subject);
    //console.log(subjectroom_standard);

    // Now remove all question sets that do not match
    $(question_set_data.clone()).find('option').each(function () {
        var val = $(this).val().split(SELECT_ID_SEPERATOR);
        var question_set_subject = parseInt(val[0]);
        var question_set_standard = cast_standard(val[1]);
        //console.log(question_set_subject);
        //console.log(question_set_standard);
        if ((question_set_subject === subjectroom_subject) && (question_set_standard === subjectroom_standard)) {
            $(QUESTION_SET_SELECT).append($(this));
        }
    });

    // Finally Re-render chosen
    $(QUESTION_SET_SELECT).trigger("chosen:updated");
}



      