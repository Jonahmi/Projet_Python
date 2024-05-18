from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sendgrid import SendGridAPIClient


# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/gestion_des_congés_et_permission_dabsences'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.secret_key = 'your_secret_key'

# Configuration de SendGrid
app.config['SENDGRID_API_KEY'] = 'your_sendgrid_api_key'

# Initialize SendGrid
sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])


# Initialize SQLAlchemy
db = SQLAlchemy(app)
