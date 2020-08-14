import os
from datetime import datetime
from scheduler_app import db, admin, mail
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
import uuid

class Administrator(UserMixin, db.Model):
	__tablename__ = 'administrator'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20))
	email=db.Column(db.String(20))
	password=db.Column(db.String(40))


InterviewStatus = {
	"STARTED": 1,
	"CANDIDATE_CF": 2,
	"CLIENT_CF": 3,
	"CANCELLED": 4
}


class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	timezone = db.Column(db.Integer)


	def __repr__(self):
		return f"User {self.first_name} {self.last_name}, {self.email}"


class Interview(db.Model):
	__tablename__ = 'interview'
	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.String(50), default=str(uuid.uuid4()))
	candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	candidate = db.relationship("User", foreign_keys=candidate_id, backref='as_interviewee')
	client = db.relationship("User", foreign_keys=client_id, backref='as_interviewer')
	candidate_times = db.Column(db.String(1000))
	client_selection = db.Column(db.String(1000))
	company_name = db.Column(db.String(100))
	position_name = db.Column(db.String(200))
	created_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	last_updated_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	status = db.Column(db.Integer, default=InterviewStatus["STARTED"], nullable=False)
	zoom_link = db.Column(db.String(1000))
	zoom_pwd = db.Column(db.String(10))


	def __repr__(self):
		return f"Interview between Client {self.client_id} and Candidate {self.candidate_id}"


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Interview, db.session))
admin.add_view(ModelView(Administrator, db.session))
