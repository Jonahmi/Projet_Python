function showAlert(message) {
    var dialogBox = $('<div>').addClass('dialog-box');
    var messageElement = $('<p>').text(message);
    var okButton = $('<button>').addClass('btn').text('OK').click(function() {
        dialogBox.remove();
    });

    dialogBox.append(messageElement);
    dialogBox.append(okButton);
    $('body').append(dialogBox);
}




$(document).ready(function() {
    $('.edit').click(function(e) {
        var id = $(this).data('id');
        $('#leave_request_id').val(id); 
    });

    $('#approveForm').submit(function(e) {
        e.preventDefault();
        var id = $('#leave_request_id').val();
        $.ajax({
            type: 'POST',
            url: '/update_status',
            data: JSON.stringify({ id: id, status: 'Accepté' }), 
            contentType: 'application/json',
            success: function(response) {
                showAlert('Statut mis à jour avec succès.');
                $('#ApproveModal').modal('hide');
                window.location.reload();
            },
            error: function(error) {
                console.log(error);
                showAlert('Erreur lors de la mise à jour du statut.');
            }
        });
    });
});



$(document).ready(function() {
    $('.delete').click(function(e) {
        e.preventDefault();
        var id = $(this).data('id');
        $('#rejectModal').modal('show'); // Afficher le modal de rejet
        $('#rejectForm').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/update_status',
                data: JSON.stringify({ id: id, status: 'Refusé' }), // Envoyer le statut 'Refusé'
                contentType: 'application/json',
                success: function(response) {
                    alert('Statut mis à jour avec succès.');
                    $('#rejectModal').modal('hide'); // Cacher le modal de rejet
                    window.location.reload();
                },
                error: function(error) {
                    console.log(error);
                    alert('Erreur lors de la mise à jour du statut.');
                }
            });
        });
    });
});
