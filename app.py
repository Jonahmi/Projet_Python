from flask import redirect, url_for, request, render_template, jsonify,flash, make_response, send_file
from config import app, db
from models import Employee,LeaveRequest,Absence,Admin,Presence
from emails import send_approval_email
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import qrcode
from datetime import datetime
from sqlalchemy import func

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vérification des informations d'identification
        admin = Admin.query.filter_by(username=username, passwd=password).first()
        if admin:
            # Authentification réussie, connectez l'utilisateur
            login_user(admin)
            # Rediriger vers la page demandée initialement ou vers le tableau de bord
            next_page = request.args.get('next')
            return redirect(next_page or url_for('permission'))
        else:
            # Authentification échouée, afficher un message d'erreur
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashbord'))

@app.route('/')
def dashbord():
    today = datetime.now().date()
    num_employees = Employee.query.count()

    # Nombre d'absences
    num_absences = Presence.query.filter(func.date(Presence.date_debut) != today).count()

    # Nombre de congés acceptés
    num_accepted_leave_requests = LeaveRequest.query.filter_by(status='Accepté').count()

    # Nombre de congés refusés
    num_rejected_leave_requests = LeaveRequest.query.filter_by(status='Refusé').count()

    # Requête pour récupérer les employés avec une date_debut différente de la date d'aujourd'hui
    employees_with_different_date = db.session.query(Employee).\
        join(Presence, Employee.employee_id == Presence.employee_id).\
        filter(func.date(Presence.date_debut) != today).\
        all()

    return render_template('index.html', num_employees=num_employees, num_absences=num_absences,
                           num_accepted_leave_requests=num_accepted_leave_requests,
                           num_rejected_leave_requests=num_rejected_leave_requests,
                           employees_with_different_date=employees_with_different_date)

@app.route('/employee')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    employees = Employee.query.paginate(page=page, per_page=per_page, error_out=False)
    print(employees.items)
    pass
    return render_template('table.html', employees=employees)

    

@app.route('/absence')
def absence():
    
    page = request.args.get('page', 1, type=int)
    absences = Absence.query.join(Employee).add_columns(Absence.id_A,Employee.nom, Employee.prenom, Absence.date_debut, Absence.date_fin).paginate(page=page, per_page=6)
    return render_template('table_A.html', absences=absences)

@app.route('/absences')
@login_required
def absences():
    
    page = request.args.get('page', 1, type=int)
    abs = Absence.query.join(Employee).add_columns(Absence.id_A,Employee.nom, Employee.prenom, Absence.date_debut, Absence.date_fin, Absence.motif).paginate(page=page, per_page=6)
    pass
    return render_template('table_Ad.html', abs=abs)
    
@app.route('/permission')
@login_required
def permission():
    page = request.args.get('page', 1, type=int)
    leave_requests = LeaveRequest.query.join(Employee).add_columns(LeaveRequest.id_L,Employee.nom, Employee.prenom,  LeaveRequest.date_debut, LeaveRequest.date_fin, LeaveRequest.motif,Employee.adresse,LeaveRequest.status).paginate(page=page, per_page=6)
    pass
    return render_template('table_P.html', leave_requests=leave_requests)
     

@app.route('/add_employee', methods=['POST'], endpoint='table')
def add_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        poste = request.form['poste']

        new_employee = Employee(
        employee_id = employee_id,
        nom = nom,
        prenom = prenom ,
        adresse = adresse,
        poste = poste
        )

        db.session.add(new_employee)
        db.session.commit()

        # Redirection vers votre page HTML après l'ajout de l'employé
        return redirect(url_for('index'))

@app.route('/ajouter_conge', methods=['POST'])
def ajouter_conge():
    
    employee_id = request.form.get('employee_id')
    date_debut = request.form.get('date_debut')
    date_fin = request.form.get('date_fin')
    motif = request.form.get('conges')
    status = request.form.get('status')

    # Vérifier si l'employé existe
    employee = Employee.query.get(employee_id)
    if employee is None:
        flash("Le numéro d'employé fourni ne correspond à aucun employé.", 'error')
        return redirect(url_for('get_leave_requests'))

    # Créer une instance de LeaveRequest avec les données du formulaire
    leave_request = LeaveRequest(
        employee_id=employee_id,
        date_debut=date_debut,
        date_fin=date_fin,
        motif=motif,
        status=status
    )

    # Ajouter l'instance à la session et confirmer les modifications
    db.session.add(leave_request)
    db.session.commit()

    # Rediriger vers une page de confirmation ou toute autre page appropriée
    flash("La demande de congé a été ajoutée avec succès.", 'success')
    return redirect(url_for('get_leave_requests'))
  

@app.route('/conge', methods=['GET'])
def get_leave_requests():
    leave_requests = LeaveRequest.query.all()

    formatted_leave_requests = []
    for leave_request in leave_requests:
        formatted_leave_request = {
            'id': leave_request.id_L,
            'nom': leave_request.employee.nom,
            'prenom': leave_request.employee.prenom,
            'date_debut': leave_request.date_debut.strftime('%Y-%m-%d'),
            'date_fin': leave_request.date_fin.strftime('%Y-%m-%d'),
            'status': leave_request.status 
        }
        formatted_leave_requests.append(formatted_leave_request)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'leaveRequests': formatted_leave_requests})
    else:
        return render_template('calendar_1.html', leave_requests=formatted_leave_requests)

@app.route('/add_absence', methods=['POST'])
def add_absence():
     if request.method == 'POST':
       
        employee_id = request.form['employee_id']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        motif = request.form['motif']
        
        absence = Absence(
        employee_id = employee_id,
        date_debut = date_debut,
        date_fin = date_fin,
        motif = motif)

        db.session.add(absence)
        db.session.commit()

        
        return redirect(url_for('absence'))
     



@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    id = data['id']
    status = data['status']
    leave_request = LeaveRequest.query.get(id)
    leave_request.status = status
    db.session.commit()
    return 'Statut mis à jour avec succès.', 200

@app.route('/delete_absence', methods=['POST'])
def delete_absence():
    if request.method == 'POST':
        absence_id = request.form.get('absence_id')
        if absence_id:
            absence = Absence.query.get(absence_id)
            if absence:
                db.session.delete(absence)
                db.session.commit()
                return redirect(url_for('absence'))
            else:
                return "Absence non trouvée."
        else:
            return "ID d'absence non fourni."
    return "Erreur lors de la suppression de l'absence."
# ____________________------------------------ delete and edit employee---------------------___________________________________

@app.route('/update_employee', methods=['POST'])
def update_employee():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        adresse = request.form.get('adresse')
        poste = request.form.get('poste')
        
        # Mettez à jour les informations de l'employé dans la base de données
        employee = Employee.query.get(employee_id)
        if employee:
            employee.nom = nom
            employee.prenom = prenom
            employee.adresse = adresse
            employee.poste = poste
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Erreur : Employé non trouvé."
    return "Erreur lors de la mise à jour des informations de l'employé."

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Supprimer les entrées liées dans les tables enfants (LeaveRequest, Absence)
    LeaveRequest.query.filter_by(employee_id=employee_id).delete()
    Absence.query.filter_by(employee_id=employee_id).delete()
    
    # Supprimer l'employé
    db.session.delete(employee)
    db.session.commit()
    
    return redirect(url_for('index'))

#------------______________________________email_______________________-----------------------------------------


@app.route('/process_approval', methods=['POST'])
def process_approval():
    if request.method == 'POST':
        leave_request_id = request.form.get('leave_request_id')
        leave_request = LeaveRequest.query.get(leave_request_id)
        leave_request.update_status('Accepté')
        to_email = request.form.get('to_email') 
        print(f"E-mail envoyé à : {to_email}")
        if send_approval_email( to_email):
            print("E-mail envoyé avec succès.")
            return 'Demande de congé approuvée et e-mail envoyé avec succès.'
        else:
            print("Erreur lors de l'envoi de l'e-mail. Veuillez réessayer.")
            return 'Erreur lors de l\'envoi de l\'e-mail. Veuillez réessayer.'


@app.route('/generate_qr/<employee_id>')
def generate_qr(employee_id):
    # Générer le QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(employee_id)
    qr.make(fit=True)

    # Créer une image du QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Sauvegarder l'image temporairement
    img_path = 'temp_qr.png'
    img.save(img_path)

    # Renvoyer l'image
    return send_file(img_path, mimetype='image/png')


@app.route('/scan')
def scanqr():
    
    return render_template('index_1.html')


@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    employee_id = request.json['employee_id']
    presence_record = Presence.query.filter_by(employee_id=employee_id).first()

    if presence_record:
        # L'employé est déjà enregistré, donc nous mettons à jour la date_debut et la date_fin
        if presence_record.date_fin:
            # Si la date_fin est déjà définie, cela signifie que l'employé a déjà scanné
            presence_record.date_debut = datetime.now()
            presence_record.date_fin = None
        else:
            # Sinon, c'est la deuxième fois que l'employé scanne, donc nous mettons à jour la date_fin
            presence_record.date_fin = datetime.now()
    else:
        # L'employé n'est pas encore enregistré, donc nous créons un nouveau enregistrement avec la date_debut
        new_presence = Presence(employee_id=employee_id, date_debut=datetime.now())
        db.session.add(new_presence)

    db.session.commit()
    return 'Success'



if __name__ == '__main__':
    app.run(debug=True)