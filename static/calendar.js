$(document).ready(function() {
    var calendar = $('#calendar').fullCalendar({
        editable: true,
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        // Ajout de l'événement clickDay
        dayClick: function(date, jsEvent, view) {
            var clickedDate = date.format('YYYY-MM-DD'); // Format de date attendu par le champ datetime-local
            var currentTime = moment().format('HH:mm'); // Format de l'heure attendu par le champ datetime-local
            var datetimeValue = clickedDate + 'T' + currentTime;
            $('#date_debut').val(datetimeValue);
            console.log('Date cliquée:', datetimeValue);
            // Affichage du modal
            $('#myModal').modal('show');
        },
        eventRender: function(event, element, view) {
            var html = '<div>' + event.title + '</div>'; // Afficher le nom et le prénom de l'employé
            element.find('.fc-content').html(html);
            
        },
        eventMouseover: function(calEvent, jsEvent, view) {
            var tooltip = '<div class="tooltiptext">';
            if (calEvent.backgroundColor === 'yellow') {
                tooltip += 'En attente';
            } else if (calEvent.backgroundColor === 'green') {
                tooltip += 'Accepté';
            } else if (calEvent.backgroundColor === 'red') {
                tooltip += 'Refusé';
            }
            tooltip += '</div>';
            $(this).append(tooltip);
        },
        eventMouseout: function(calEvent, jsEvent, view) {
            $(this).find('.tooltiptext').remove();
        }

        
    });

    // Récupérer les congés des employés depuis la base de données
    $.ajax({
        url: '/conge', // Endpoint pour récupérer les congés des employés
        type: 'GET',
        success: function(response) {
            var leaveRequests = response.leaveRequests;
            // Parcourir les congés et les ajouter en tant qu'événements sur le calendrier
            leaveRequests.forEach(function(leaveRequest) {
                var event = {
                    title: '<span class="event-title">' + leaveRequest.nom + '</span> <span class="event-title">' + leaveRequest.prenom + '</span>', // Nom et prénom de l'employé
                    start: leaveRequest.date_debut,
                    end: leaveRequest.date_fin
                };
                if (leaveRequest.status === 'en attente') {
                event.backgroundColor = 'yellow';
                } else if (leaveRequest.status === 'Accepté') {
                    event.backgroundColor = 'green';
                } else if (leaveRequest.status === 'Refusé') {
                    event.backgroundColor = 'red';
                }
                
                calendar.fullCalendar('renderEvent', event, true); // Ajouter l'événement au calendrier
            });
        },
        error: function(err) {
            console.error('Erreur lors de la récupération des congés:', err);
        }
    });
});