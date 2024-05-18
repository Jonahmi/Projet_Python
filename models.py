
from config import db

class Employee(db.Model):
    __tablename__ = 'Employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    adresse = db.Column(db.String(200))
    poste = db.Column(db.String(200))
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)


class LeaveRequest(db.Model):
    __tablename__ = 'LeaveRequest'
    id_L = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.employee_id'))
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    motif = db.Column(db.String(200))
    status = db.Column(db.String(50))

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()


class Absence(db.Model):
    __tablename__ = 'Absence'
    id_A = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.employee_id'))
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    motif  = db.Column(db.String(200))


class Presence(db.Model):
    __tablename__ = 'Presence'
    id_Pr= db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.employee_id'))
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    


class Admin (db.Model):
    __tablename__ = 'Admin'
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    passwd = db.Column(db.String(200))

    def get_id(self):
        # Retournez l'identifiant de l'utilisateur ici.
        return str(self.id)

    def is_active(self):
        # Tous les comptes admin sont considérés comme actifs.
        return True
    
    def is_authenticated(self):
        # Indique si l'utilisateur est authentifié.
        return True
