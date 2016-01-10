$(document).ready(function () {
    datetime_input_setup();
});

function datetime_input_setup() {
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
}