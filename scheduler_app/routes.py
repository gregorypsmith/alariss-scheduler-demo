from scheduler_app import app, db, mail, login_manager
from flask_login import login_user, login_required, fresh_login_required, logout_user, current_user
from scheduler_app.models import User, Interview, Administrator
from flask import render_template, request, make_response, redirect, url_for, flash
from flask_mail import Message
import os 
from flask import render_template
import json 
from pytz import timezone
import scheduler_app.timezone_module as tz_module
import scheduler_app.email_module as mail_module
import datetime

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
        print("Dank Client Timezone Memes:")
        print(client_timezone)

        if not candidate_fname or not candidate_email or not candidate_email \
            or not client_email or not client_fname or not client_fname:
            flash("One or more fields was filled out incorrectly. Please try again", "danger")
            return render_template('admin_page.html')

        # add users to db if necessary
        cand = User.query.filter_by(email=candidate_email).first()
        client = User.query.filter_by(email=client_email).first()

        if not cand:
            cand = User(
                first_name=str(candidate_fname),
                last_name=str(candidate_lname),
                email=str(candidate_email),
                timezone="meme beasts"
            )
            db.session.add(cand)
        else: 
            cand.first_name=str(candidate_fname)
            cand.last_name=str(candidate_lname)
            cand.email=str(candidate_email)
        db.session.commit()

        if not client:
            print("Yeet it wasn't client")
            client = User(
                first_name=str(client_fname),
                last_name=str(client_lname),
                email=str(client_email),
                timezone=str(client_timezone)
            )
            db.session.add(client)
        
        else: 
            client.first_name=str(client_fname)
            client.last_name=str(client_lname)
            client.email=str(client_email)
            client.timezone=str(client_timezone)
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

        # send email to candidate with scheduler
        url = os.getenv("INDEX_URL") + url_for('select_timezone', interview_id=interview.id)
        mail_module.send_candidate_scheduler_email(cand, client, interview, url)

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
        print("Dank Candidate Timezone Memes:")
        print(candidate_timezone)
        candidate.timezone = candidate_timezone
   

        # print("here")

        db.session.commit()
       
        print("Dank Candidate Timezone Memes II:")
        print(interview.candidate.timezone)
        print("Dank Client Timezone Memes II:")
        print(interview.client.timezone)
        return redirect(url_for('candidate_scheduler', interview_id=interview.id))


    return render_template('select_timezone.html', errormsg='')


# schedule for candidate
@app.route("/interviews/<int:interview_id>/candidate_scheduler", methods=['GET', 'POST'])
def candidate_scheduler(interview_id):
    print("made it to routing stage!!")
    interview = Interview.query.filter_by(id=interview_id).first()
    if request.method == "POST":
        print("Post operation called!!")
        candidate_time_info = request.form['submit_times']
        # print(candidate_time_info)
        interview.candidate_times = candidate_time_info
        db.session.commit()

        mail_module.send_candidate_confirmed_times(interview.candidate, interview)
        url = os.getenv("INDEX_URL") + url_for('client_scheduler', interview_id=interview.id)
        mail_module.send_client_scheduler_email(interview.candidate, interview.client, interview, url)
        return redirect(url_for('candidate_success'))


    cur_utc_int = int(datetime.datetime.utcnow().timestamp())
    print(cur_utc_int)
    client_offset = tz_module.timezone_str_to_utc_offset_int_in_hours(interview.client.timezone, cur_utc_int)
    candidate_offset = tz_module.timezone_str_to_utc_offset_int_in_hours(interview.candidate.timezone, cur_utc_int)
    print("Client Offset: " + str(client_offset))
    print("Candidate Offset: " + str(candidate_offset))
    return render_template('candidate_scheduler.html', client_GMT_offset = client_offset, candidate_GMT_offset = candidate_offset)


# Schedule for client
@app.route("/interviews/<int:interview_id>/client_scheduler", methods=['GET', 'POST'])
def client_scheduler(interview_id):

    interview = Interview.query.filter_by(id=interview_id).first()

    # if something went wrong
    if not interview:
        return render_template('select_timezone.html', error_msg='This interview could not be found. Please contact nick@alariss.com for assistance.')

    if request.method == 'POST':
        # save this
        selected_time_utc = request.form['timeint']

    return render_template('client_scheduler.html', times=times_object_list)


# confirmed page
@app.route("/confirmed")
def confirmed():
    return render_template('index.html')

# confirmed page
@app.route("/candidate_success")
def candidate_success():
    return render_template('candidate_success_page.html')

# confirmed page
@app.route("/client_success")
def client_success():
    return render_template('client_success_page.html')