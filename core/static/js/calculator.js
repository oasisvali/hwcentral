$( "#calculator" ).dialog({
    autoOpen: false 
});

$( "#calc_button" ).click(function() {
  $( "#calculator" ).dialog( "open" );
});