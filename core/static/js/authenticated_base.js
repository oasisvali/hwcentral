var DATATABLES_DEBUG=false;
var CHART_ENDPOINT="http://localhost:8000/chart/";
var MIN_DIMENSION=600;
if (screen.width<=MIN_DIMENSION || screen.height<=MIN_DIMENSION){
    alert ("Sorry ! HWCentral does not support this device. To ensure an optimal experience, try logging in from a non-mobile device");
    window.stop();
}

$(document).ready(function () {
    $(function(){
       $("#assigned_date").pickadate({

            format: 'dd/mm/yyyy',
            monthSelector: false,
            yearSelector: false,
            onStart: function(){
                this.set('select',Date.now())
            },
            min: Date.now(),
        });
       $("#submission_date").pickadate({

            format: 'dd/mm/yyyy',
            monthSelector: false,
            yearSelector: false,
            min: Date.now()+2,
        });




        var from_$input = $('#assigned_date').pickadate(),
        assigned_picker = from_$input.pickadate('picker')

        var to_$input = $('#submission_date').pickadate(),
        submission_picker = to_$input.pickadate('picker')



        // Check if there’s a “from” or “to” date to start with.
        if ( assigned_picker.get('value') ) {
          submission_picker.set('min', assigned_picker.get('select'))
        }
        if ( submission_picker.get('value') ) {
          assigned_picker.set('max', submission_picker.get('select'))
        }

        // When something is selected, update the “assigned” and “submission” limits.
        assigned_picker.on('set', function(event) {
          if ( event.select ) {
            submission_picker.set('min', assigned_picker.get('select'))    
          }
          else if ( 'clear' in event ) {
            submission_picker.set('min', false)
          }
        })
        
        submission_picker.on('set', function(event) {
          if ( event.select ) {
            assigned_picker.set('max', submission_picker.get('select'))
          }
          else if ( 'clear' in event ) {
            assigned_picker.set('max', false)
          }
        })
    });
    $(document).tooltip();
    $('#announcement_table').dataTable({
        "pagingType":"full_numbers"
    });
    $('#active_assignment_table').dataTable();
    $('#graded_assignment_table').dataTable();
    $('#teacher_listing').dataTable();
    $(function(){
        $("#menu").accordion();
    });
})
