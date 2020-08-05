from scheduler_app import app, db, mail, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from scheduler_app.models import Administrator, Candidate, Client, Interview
from flask import render_template, request, make_response, redirect, url_for
from flask_mail import Message
import os 
from flask import render_template

admin_mail = os.environ.get('MAIL_USERNAME')

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
def admin():

    if request.method == 'POST':

        # get and validate results from form
        candidate_fname = request.form['candidate_fname'].strip()
        candidate_lname = request.form['candidate_lname'].strip()
        candidate_email = request.form['candidate_email'].strip()
        client_fname = request.form['client_fname'].strip()
        client_lname = request.form['client_lname'].strip()
        client_email = request.form['client_email'].strip()

        if not candidate_fname or not candidate_email or not candidate_email \
            or not client_email or not client_fname or not client_fname:
            return render_template('admin_page.html', errormsg = 'Error: One or more fields was \
                filled out incorrectly. Please try again')

        # add users to db if necessary
        cand = Candidate.query.filter_by(email=candidate_email).first()
        client = Client.query.filter_by(email=client_email).first()

        if not cand:
            cand = Candidate(
                first_name=candidate_fname,
                last_name=candidate_lname,
                airtable_id='', 
                email=candidate_email
            )
            db.session.add(cand)

        if not client:
            client = Client(
                first_name=client_fname,
                last_name=client_lname,
                airtable_id='', 
                email=client_email
            )
            db.session.add(client)
        db.session.commit()

        # create interview in db
        interview = Interview(
            candidate_id=cand.id,
            client_id=client.id,
            candidate_times='',
            client_selection=''
        )
        db.session.add(interview)
        db.session.commit()
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
                return admin()

        # unsuccessful login        
        return render_template('login.html', errormsg='Incorrect email/password combination')

    # first time loading the page
    return render_template('login.html', errormsg='')

# select your timezone
@app.route("/select-timezone", methods=['GET', 'POST'])
def select_timezone():
    return render_template('select_timezone.html')

# schedule for candidate
@app.route("/candidate-scheduler")
def candidate_scheduler():
    return render_template('candidate_scheduler.html')

# schedule for client
@app.route("/client-scheduler")
def client_scheduler():
    return render_template('index.html')

# confirmed page
@app.route("/confirmed")
def confirmed():
    return render_template('index.html')

