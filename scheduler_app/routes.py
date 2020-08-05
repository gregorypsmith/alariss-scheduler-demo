from scheduler_app import app, db, mail
from scheduler_app.models import Candidate, Client, Interview
from flask import render_template, request, make_response, redirect, url_for
from flask_mail import Message
import os 
from flask import render_template

admin_mail = os.environ.get('MAIL_USERNAME')


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

# need flask-login to authenticate
@app.route("/nick-admin")
def nick_admin():
    return render_template('index.html')

# login page for nick
@app.route("/login")
def login():
    return render_template('index.html')

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

