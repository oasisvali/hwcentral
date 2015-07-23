$(document).ready(function(){

$( "#calculator_box" ).dialog({ 
    autoOpen: false,
    resizable: false
});

$( "#calc_button" ).click(function() {
  $( "#calculator_box" ).dialog( "open" );
});

$(".ui-dialog-titlebar-close").attr('title',"X");

});

