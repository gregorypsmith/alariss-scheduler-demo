from scheduler_app import app, db, mail, login_manager
from flask_login import login_user, login_required, fresh_login_required, logout_user, current_user
from scheduler_app.models import User, Interview, Administrator
from flask import render_template, request, make_response, redirect, url_for, flash
from flask_mail import Message
import os 
from flask import render_template
import json 

scheduler_email = os.getenv('EMAIL_USERNAME')

@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(int(user_id))


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


# need flask-login to authenticate
@app.route("/administrator", methods=['GET', 'POST'])
@login_required
def administrator():
    if request.method == 'POST':

        # get and validate results from form
        candidate_fname = request.form['candidate_fname'].strip()
        candidate_lname = request.form['candidate_lname'].strip()
        candidate_email = request.form['candidate_email'].strip()
        candidate_position = request.form['candidate_position'].strip()
        client_fname = request.form['client_fname'].strip()
        client_lname = request.form['client_lname'].strip()
        client_company = request.form['client_company'].strip()
        client_email = request.form['client_email'].strip()
        client_timezone = request.form['client_timezone'].strip()

        if not candidate_fname or not candidate_email or not candidate_email \
            or not client_email or not client_fname or not client_fname:
            flash("One or more fields was filled out incorrectly. Please try again", "danger")
            return render_template('admin_page.html')

        # add users to db if necessary
        cand = User.query.filter_by(email=candidate_email).first()
        client = User.query.filter_by(email=client_email).first()

        if not cand:
            cand = User(
                first_name=candidate_fname,
                last_name=candidate_lname,
                email=candidate_email,
                timezone=''
            )
            db.session.add(cand)
        db.session.commit()

        if not client:
            client = User(
                first_name=client_fname,
                last_name=client_lname,
                email=client_email,
                timezone=client_timezone
            )
            db.session.add(client)
        db.session.commit()

        # Create new interview    
        interview = Interview(
            candidate_id=cand.id,
            client_id=client.id,
            company_name = client_company,
            position_name = candidate_position
        )
        db.session.add(interview)
        db.session.commit()

        # create email message for candidate
        client_fullname = client_fname + ' ' + client_lname
        msg = Message('[ACTION REQUIRED] Schedule your upcoming interview with ' + client_company,
        sender=scheduler_email,
        recipients=[cand.email])
        msg.body = 'Dear ' + candidate_fname + ',\n\n'
        msg.body += 'Congratulations! ' + client_company + ' would like you to interview as for an open ' + candidate_position + ' position.\n\n'
        msg.body += 'Your point of contact is ' + client_fullname + '. Please continue to the following link to schedule your interview:\n\n'
        msg.body += os.getenv("INDEX_URL") + url_for('select_timezone', interview_id=interview.id) + '\n\n'
        msg.body += 'Best wishes and good luck,\n'
        msg.body += 'The Alariss Global Team'
        mail.send(msg)

        return render_template('admin_success.html', candidate_email=candidate_email, client_email=client_email)

    return render_template('admin_page.html', errormsg='')


# login page for nick
@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email_form = request.form['email']
        password_form = request.form['password']
        admin = Administrator.query.filter_by(email=email_form).first()

        if admin:
            if admin.password == password_form:
                login_user(admin)
                # successful login
                return redirect(url_for('administrator'))

        # unsuccessful login        
        return render_template('login.html', errormsg='Incorrect email/password combination')

    # first time loading the page
    return render_template('login.html', errormsg='')


# @app.route("/interviews/<int:interview_id>/confirm_email", methods=['GET', 'POST'])


# Select your timezone
@app.route("/interviews/<int:interview_id>/select_timezone", methods=['GET', 'POST'])
def select_timezone(interview_id):

    interview = Interview.query.filter_by(id=interview_id).first()

    # If interview is not found
    if not interview:
        return render_template('select_timezone.html', error_msg='This interview could not be found.')

    candidate = interview.candidate

    if request.method == "POST":
        candidate_timezone = request.form['timezone']
        candidate.timezone = candidate_timezone

        db.session.commit()
        return redirect(url_for('candidate_scheduler', interview_id=interview.id))


    return render_template('select_timezone.html', errormsg='')


# schedule for candidate
@app.route("/interviews/<int:interview_id>/candidate_scheduler", methods=['GET', 'POST'])
def candidate_scheduler(interview_id):
	print("made it to routing stage!!")
	if request.method == "POST":
		print("Post operation called!!")
		candidate_time_info = 1 #will eventually be retrieved through the URL we sent, hardcoded for now
		candidate_time_info = request.form['submit_times']
		print(candidate_time_info)
		interview = Interview.query.filter_by(id=interview_id).first()
		interview.candidate_times = candidate_time_info

		return redirect(url_for('candidate_success_page'))
	return render_template('candidate_scheduler.html', client_GMT_offset = 0, candidate_GMT_offset = 0)


# Schedule for client
@app.route("/interviews/<int:interview_id>/client_scheduler", methods=['GET', 'POST'])
def client_scheduler(interview_id):

    interview = Interview.query.filter_by(id=interview_id).first()

    # if something went wrong
    if not interview:
        return render_template('select_timezone.html', error_msg='This interview could not be found. Please contact nick@alariss.com for assistance.')

    # TODO: Implement this method
    if request.method == "POST":
        pass
    
    return render_template('index.html', cand_id=1, client_id=1)


# confirmed page
@app.route("/confirmed")
def confirmed():
    return render_template('index.html')

# confirmed page
# @app.route("/candidate_success")
# def confirmed():
#     return render_template('candidate_success_page.html')