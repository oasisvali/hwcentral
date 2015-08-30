var focused_textbox;

function add_text(text) {
    focused_textbox.val(focused_textbox.val()+ text.toString());
}

$(document).ready(function(){

    // first remove all instances of math toolbox apart from the first
    $('.math_toolbox').not($('.math_toolbox:first')).remove();

    $(".math_toolbox").dialog({
        autoOpen: false,
        resizable: false,
        width: 210,
        closeText: "X"
    });

    $(".toolbox_button").click(function () {
        $(".math_toolbox").dialog("open");
    });

    $(".math_toolbox_enabled").focus(function () {
        focused_textbox=$(this);
    });

});
