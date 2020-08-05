from scheduler_app import db
from scheduler_app.models import User, Interview


def get_interview_test():
	test_candidate = User(
		first_name='John',
		last_name='Doe',
		candidate_airtable_id='123456', 
		email='john@mail.com'
	)

	test_client_1 = User(
		first_name='Jane',
		last_name='Doe',
		client_airtable_id='123456', 
		email='jane@mail.com'
	)

	test_client_2 = User(
		first_name="Greg",
		last_name="Greg",
		client_airtable_id='123456',
		email='greg@mail.com'
	)

	db.session.add(test_candidate)
	db.session.add(test_client_1),
	db.session.add(test_client_2)
	db.session.commit()

	print(test_candidate)
	print(test_client_1)

	test_interview = Interview(
		candidate=test_candidate,
		client=test_client_1,
	)

	test_interview_2 = Interview(
		candidate=test_candidate,
		client=test_client_2,
	)

	db.session.add(test_interview)
	db.session.add(test_interview_2)
	db.session.commit()

	interviews = Interview.query.all()
	print(interviews)

	candidate = User.query.filter_by(id=2).first()
	print(candidate.as_interviewer)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    get_interview_test()