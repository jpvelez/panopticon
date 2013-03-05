// Add dataTables interactivity to #employee-list table.
// "bootstrap" is a plugin to add bootstrap styles to dataTables pagination. 
$(document).ready(function() {
    $('#employee-list').dataTable( {
        "sDom": "<'row'<'offset6 span6'f>r>t<'row'<'span6'i><'span6'p>>",
        "aaSorting":  [[ 1, 'asc' ]],
        "iDisplayLength": 50,
        "sPaginationType": "bootstrap"
    } );
} );

// Set new class on the DataTables wrapper element to make the form elements appear inline rather than as a block.
$.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
} );