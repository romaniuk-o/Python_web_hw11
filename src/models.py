from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src import db


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phones = db.relationship('PhoneToContact', back_populates='contact')


class Notate(db.Model):
    __tablename__ = 'notates'
    id = db.Column(db.Integer, primary_key=True)
    notate = db.Column(db.String(1000), nullable=False)
    tag = db.Column(db.String(100), nullable=True)

    def __repr__(self):
         return f"User({self.id}, {self.notate}, {self.tag})"


class PhoneToContact(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    phone = db.Column(db.String(100))
    contact_id = db.Column(ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    contact = db.relationship('Contact', back_populates='phones')


