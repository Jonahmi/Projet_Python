from sendgrid.helpers.mail import Mail


def send_approval_email(sg, to_email):
    message = Mail(
        from_email='tsimanahyjonahmichel@gmail.com',
        to_emails=to_email,
        subject='Demande de congé approuvée',
        html_content='<strong>Votre demande de congé a été approuvée.</strong>')
    try:
        sg.send(message)
        return True  # Succès de l'envoi de l'email
    except Exception as e:
        print(str(e))  # Affiche l'erreur
        return False  # Échec de l'envoi de l'email
