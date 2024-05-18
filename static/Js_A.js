$(document).ready(function(){
    $('.delete').click(function(){
        var absenceId = $(this).data('absence-id');
        $('#absence_id').val(absenceId);
    });
});