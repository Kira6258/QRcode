from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

#user  table
class user(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(500),nullable=False)
    qrcodes=db.relationship('QRcodes',backref='user',lazy=True)

#qrcodes table
class QRcodes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.Text,nullable=False)
    image_path=db.Column(db.String(100))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


