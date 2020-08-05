from scheduler_app import app, db, mail, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from scheduler_app.models import User, Interview, Administrator
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
@login_required
@app.route("/administrator")
def administrator():
    return render_template('administrator.html')

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
                return render_template('admin_page.html')

        # unsuccessful login        
        return render_template('login.html', errormsg='Incorrect email/password combination')

    # first time loading the page
    return render_template('login.html', errormsg='')

# select your timezone
@app.route("/select-timezone")
def select_timezone():
    return render_template('index.html')

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

