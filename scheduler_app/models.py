import os

from scheduler_app import db, admin, mail
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

class Administrator(UserMixin, db.Model):
	__tablename__ = 'administrator'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.Unicode)
	email=db.Column(db.Unicode)
	password=db.Column(db.Unicode)

class Candidate(db.Model):
	__tablename__ = 'candidate'
	id = db.Column(db.Integer, primary_key=True)
	airtable_id = db.Column(db.Unicode)
	first_name = db.Column(db.Unicode)
	last_name = db.Column(db.Unicode)
	email = db.Column(db.Unicode)
	interviews = db.relationship("Interview", back_populates="candidate")

class Client(db.Model):
	__tablename__ = 'client'
	id = db.Column(db.Integer, primary_key=True)
	airtable_id = db.Column(db.Unicode)
	first_name = db.Column(db.Unicode)
	last_name = db.Column(db.Unicode)
	email = db.Column(db.Unicode)
	interviews = db.relationship("Interview", back_populates="client")

class Interview(db.Model):
	__tablename__ = 'interview'
	id = db.Column(db.Integer, primary_key=True)
	candidate = db.relationship("Candidate", back_populates="interviews")
	client = db.relationship("Client", back_populates="interviews")
	candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	candidate_times = db.Column(db.Unicode)
	client_selection = db.Column(db.Unicode)


admin.add_view(ModelView(Administrator, db.session))
admin.add_view(ModelView(Candidate, db.session))
admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Interview, db.session))