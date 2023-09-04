from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import UserMixin
from datetime import timedelta
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import requests 
import xlsxwriter
import os, json
from celery import Celery
from celery.schedules import crontab
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity,verify_jwt_in_request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from weasyprint import HTML
from flask import send_file


app = Flask(__name__)
cors = CORS(app)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['UPLOAD_FOLDER'] = '../frontend/public/images'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['SMTP_SERVER_HOST'] = "localhost"
app.config['SMTP_SERVER_PORT'] = 1025
app.config['SENDER_ADDRESS'] = "harsha@gmail.com"
app.config['SENDER_PASSWORD'] = ""



jwt = JWTManager(app)

cast = db.Table('cast',
    db.Column('celebrity_id', db.Integer, db.ForeignKey('celebrity.id', ondelete='CASCADE'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), primary_key=True)
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(380), nullable = False)
    phone_number = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(20), nullable = False, unique=True)
    u_type = db.Column(db.String(20), nullable = False)
    recent_login = db.Column(db.DateTime)
    def update_recent_login(self):
        self.recent_login = datetime.utcnow()
        db.session.commit()

class Celebrity(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    photo = db.Column(db.String(200))

class Ticket(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id', ondelete='CASCADE'), nullable = False)
    no_of_seats = db.Column(db.Integer, nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    
class Venue(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    city = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    capacity = db.Column(db.Integer, nullable = False)

class Tag(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

show_tags = db.Table('show_tags',
    db.Column('show_id', db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
)

class Show(db.Model): 
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    poster = db.Column(db.String(200))
    tags = db.relationship('Tag', secondary=show_tags, backref=db.backref('shows', lazy=True))
    cast = db.relationship('Celebrity', secondary=cast, backref=db.backref('shows', lazy=True))

    
class Screen(db.Model): 
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    timing = db.Column(db.DateTime, nullable = False)
    price = db.Column(db.Float, nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete='CASCADE'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)