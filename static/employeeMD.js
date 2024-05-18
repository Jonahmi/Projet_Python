$(document).ready(function(){
    $('#editEmployeeModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Bouton qui a ouvert le modal
        var modal = $(this);
        
        // Vérifier si le modal ouvert est celui d'édition
        if (!modal.hasClass('addEmployeeModal')) {
            // Récupérer les données de l'employé depuis le bouton "Modifier"
            var employee_id = button.data('employee-id');
            var nom = button.data('nom');
            var prenom = button.data('prenom');
            var adresse = button.data('adresse');
            var poste = button.data('poste');

            // Remplir les champs du formulaire du modal d'édition avec les données récupérées
            modal.find('#employee_id').val(employee_id);
            modal.find('#nom').val(nom);
            modal.find('#prenom').val(prenom);
            modal.find('#adresse').val(adresse);
            modal.find('#poste').val(poste);
        }
    });
});



$(document).ready(function(){
    $('.delete').click(function(){
        var employeeId = $(this).data('employee-id');
        var deleteUrl = '/delete_employee/' + employeeId;
        $('#deleteForm').attr('action', deleteUrl);
    });
});