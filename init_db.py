from scheduler_app import db
from scheduler_app.models import Candidate, Client, Interview


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
    db.drop_all()
    db.create_all()
    #get_interview_test()