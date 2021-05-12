from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False, unique=True)

    def __init__(self, firstname, lastname, phonenumber):
        self.firstname = firstname
        self.lastname = lastname
        self.phonenumber = phonenumber
    
    def __repr__(self):
        return f'<User | {self.phonenumber}>'



    