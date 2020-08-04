import os

from scheduler_app import db, admin, mail
from flask_admin.contrib.sqla import ModelView

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


admin.add_view(ModelView(Candidate, db.session))
admin.add_view(ModelView(Client, db.session))
admin.add_view(ModelView(Interview, db.session))

def get_interview_test():
	test_candidate = Candidate(
		first_name='cand1',
		last_name='',
		airtable_id='', 
		email=''
	)

	test_client = Client(
		first_name='client1',
		last_name='',
		airtable_id='', 
		email=''
	)

	db.session.add(test_candidate)
	db.session.add(test_client)
	db.session.commit()

	print(test_candidate)
	print(test_client)

	test_interview = Interview(
		candidate=test_candidate,
		client=test_client,
		candidate_times='',
		client_selection='doge'
	)

	db.session.add(test_interview)
	db.session.commit()

	get_interview = Interview.query.filter_by(client_selection='doge').first()


if __name__ == '__main__':
	#db.create_all()
	get_interview_test()



    