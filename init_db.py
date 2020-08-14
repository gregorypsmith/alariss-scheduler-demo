from scheduler_app import db
from scheduler_app.models import User, Interview, Administrator
import os, uuid


def get_interview_test():
	test_candidate = User(
		first_name='John',
		last_name='Doe',
		email='hung@alariss.com'
	)

	test_client_1 = User(
		first_name='Jane',
		last_name='Doe',
		email='hung.nguyen.0428@gmail.com',
		timezone="7"
	)

	test_client_2 = User(
		first_name="Greg",
		last_name="Smith",
		email='gregory@alariss.com',
		timezone="-7"
	)

	db.session.add(test_candidate)
	db.session.add(test_client_1),
	db.session.add(test_client_2)
	db.session.commit()

	test_interview = Interview(
		uuid=str(uuid.uuid4()),
		candidate=test_candidate,
		client=test_client_1,
		company_name="Alariss",
		position_name="Intern",
	)

	test_interview_2 = Interview(
		uuid=str(uuid.uuid4()),
		candidate=test_candidate,
		client=test_client_2,
		company_name="Alariss",
		position_name="Assistant",
	)

	db.session.add(test_interview)
	db.session.add(test_interview_2)
	db.session.commit()


	test_admin = Administrator(
		email=os.getenv('ADMIN_EMAIL'),
		password=os.getenv('ADMIN_PASSWORD')
	)

	db.session.add(test_admin)
	db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    get_interview_test()