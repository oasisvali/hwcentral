var focused_textbox;

function AddText(text){
    focused_textbox.val(focused_textbox.val()+ text.toString());
}

$(document).ready(function(){

    $( "#maths_toolbox" ).dialog({ 
        autoOpen: false,
        resizable: false,
        width: 210,
        closeText: "X"
    });

    $( "#toolbox_button" ).click(function() {
      $( "#maths_toolbox" ).dialog( "open" );
    });
    $(".maths_toolbox_enabled").focus(function(){
        focused_textbox=$(this);
    });

});
