from flask import render_template, request, make_response, redirect, url_for, flash
from flask_mail import Message
from flask_login import login_user, login_required, fresh_login_required, logout_user, current_user

from scheduler_app import app, db, mail, login_manager
from scheduler_app.models import User, Interview, Administrator, InterviewStatus
from scheduler_app.forms import InterviewForm, SelectTimezoneForm, CandidateSelectionForm
import scheduler_app.timezone_module as tz_module
import scheduler_app.email_module as mail_module
import scheduler_app.zoom_module as zoom_module
import scheduler_app.dashboard_module as dashboard_module

import os, json, uuid
from datetime import datetime, timezone, timedelta
INTERVIEW_DAY_OPTIONS = 7


@app.context_processor
def utility_processor():
    def parse_interview_status(input_key):
        return [status for status, key in InterviewStatus.items() if key == input_key][0]

    
    def return_interview_datetime(ts):
        print(ts)
        if ts:
            d = datetime.fromtimestamp(int(ts), tz=timezone.utc)
            d -= timedelta(hours=7)
            return d.strftime("%Y-%m-%d %H:%M:%S PST")
        else:
            return "Not Confirmed"

    return dict(parse_interview_status=parse_interview_status, return_interview_datetime=return_interview_datetime)


@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(int(user_id))


@app.route("/")
@app.route("/index")
def home():
    return redirect(url_for("admin_dashboard"))


# admin dashboard
@app.route("/administrator/dashboard")
@login_required
def admin_dashboard():
    interviews = Interview.query.all()
    
    return render_template('dashboard.html', interviews=interviews)


# need flask-login to authenticate
@app.route("/administrator/create_interview", methods=['GET', 'POST'])
@login_required
def create_interview():
    form = InterviewForm()
    if form.validate_on_submit():
        # get and validate results from form
        candidate_fname = form.candidate_fname.data
        candidate_lname = form.candidate_lname.data
        candidate_email = form.candidate_email.data
        candidate_position = form.candidate_position.data
        client_fname = form.client_fname.data
        client_lname = form.client_lname.data
        client_company = form.client_company.data
        client_email = form.client_email.data
        client_timezone = form.client_timezone.data


        # add users to db if necessary
        cand = User.query.filter_by(email=candidate_email).first()
        client = User.query.filter_by(email=client_email).first()

        if not cand:
            cand = User(
                first_name=str(candidate_fname),
                last_name=str(candidate_lname),
                email=str(candidate_email)
            )
            db.session.add(cand)
        else: 
            cand.first_name=str(candidate_fname)
            cand.last_name=str(candidate_lname)
            cand.email=str(candidate_email)
        db.session.commit()

        if not client:
            client = User(
                first_name=str(client_fname),
                last_name=str(client_lname),
                email=str(client_email),
                timezone=int(client_timezone)
            )
            db.session.add(client)
        
        else: 
            client.first_name=str(client_fname)
            client.last_name=str(client_lname)
            client.email=str(client_email)
            client.timezone=int(client_timezone)
        db.session.commit()

        # Create new interview    
        interview = Interview(
            uuid=str(uuid.uuid4()),
            candidate_id=cand.id,
            client_id=client.id,
            company_name = client_company,
            position_name = candidate_position
        )
        db.session.add(interview)
        db.session.commit()

        # send email to candidate with scheduler
        url = os.getenv("INDEX_URL") + url_for('select_timezone', interview_uuid=interview.uuid)
        mail_module.send_candidate_scheduler_email(interview, url)
        
        # flash(f"Successfully created interview process between {candidate_email} and {client_email}", "success")
        return render_template('admin_success.html', candidate_email=candidate_email, client_email=client_email)

    return render_template('admin_page.html', form=form)

@app.route("/interviews/<int:interview_id>/cancel", methods=['GET', 'POST'])
@login_required
def cancel_interview(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first()
    if interview:
        if interview.status != InterviewStatus["CANCELLED"]:
            interview.status = InterviewStatus["CANCELLED"]
            interview.last_updated_time = datetime.utcnow()
            mail_module.send_cancellation_email(interview)
            db.session.commit()
            flash("Successfully canceled interview", "success")
        else:
            flash("This interview is already cancelled", "danger")
    else:
        flash("This interview cannot be found", "danger")
    return redirect(url_for("admin_dashboard"))


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
                return redirect(url_for('admin_dashboard'))

        # unsuccessful login        
        return render_template('login.html', errormsg='Incorrect email/password combination')

    # first time loading the page
    return render_template('login.html', errormsg='')


# Select your timezone
@app.route("/interviews/<interview_uuid>/select_timezone", methods=['GET', 'POST'])
def select_timezone(interview_uuid):

    interview = Interview.query.filter_by(uuid=interview_uuid).first()

    # If interview is not found
    if not interview:
        flash("This interview could not be found.", "danger")
        return render_template('index.html')

    # If interview cancelled
    elif interview.status == InterviewStatus["CANCELLED"]:
        flash("This interview has been cancelled.", "danger")
        return render_template('index.html')

    # If candidate has already scheduled the interview
    elif interview.status != InterviewStatus["STARTED"]:
        flash("You have already selected your availablity for this interview.", "danger")
        return render_template('index.html')

    candidate = interview.candidate
    form = SelectTimezoneForm()

    if form.validate_on_submit():
        candidate.timezone = form.candidate_timezone.data
   
        db.session.commit()
        return redirect(url_for('candidate_scheduler', interview_uuid=interview.uuid))

    return render_template('select_timezone.html', form=form, interview=interview)


# schedule for candidate
@app.route("/interviews/<interview_uuid>/candidate_scheduler", methods=['GET', 'POST'])
def candidate_scheduler(interview_uuid):
    interview = Interview.query.filter_by(uuid=interview_uuid).first()

    # If interview is not found
    if not interview:
        flash("This interview could not be found.", "danger")
        return render_template('index.html')

    # If interview cancelled
    elif interview.status == InterviewStatus["CANCELLED"]:
        flash("This interview has been cancelled.", "danger")
        return render_template('index.html')
    
    # If candidate has already scheduled the interview
    elif interview.status != InterviewStatus["STARTED"]:
        flash("You have already selected your availablity for this interview.", "danger")
        return render_template('index.html')

    form = CandidateSelectionForm()
    
    if form.validate_on_submit():
        candidate_time_info = form.candidate_time_info.data
        if candidate_time_info:
            interview.candidate_times = candidate_time_info
            db.session.commit()

            mail_module.send_candidate_confirmed_times(interview)
            url = os.getenv("INDEX_URL") + url_for('client_scheduler', interview_uuid=interview.uuid)
            mail_module.send_client_scheduler_email(interview, url)

            interview.status = InterviewStatus["CANDIDATE_CF"]
            interview.last_updated_time = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('candidate_success'))
        else:
            flash("Please select a few time options.", "danger")

    candidate_offset = int(interview.candidate.timezone)
    headers = (tz_module.get_next_n_day_strs(7, candidate_offset))
    table = (tz_module.get_times_object(interview, INTERVIEW_DAY_OPTIONS))
    return render_template('candidate_scheduler.html', column_headers=headers, table_obj=table, form=form)


# Schedule for client
@app.route("/interviews/<interview_uuid>/client_scheduler", methods=['GET', 'POST'])
def client_scheduler(interview_uuid):

    interview = Interview.query.filter_by(uuid=interview_uuid).first()

    # If interview is not found
    if not interview:
        flash("This interview could not be found.", "danger")
        return render_template('index.html')

    # If interview cancelled
    elif interview.status == InterviewStatus["CANCELLED"]:
        flash("This interview has been cancelled.", "danger")
        return render_template('index.html')

    # If interview already submitted
    elif interview.status == InterviewStatus["CLIENT_CF"]:
        flash("This interview is already scheduled.", "danger")
        return render_template('index.html')
    
    # If candidate has not yet sent their availability
    elif interview.status == InterviewStatus["STARTED"]:
        flash("The candidate has not yet sent their availability.", "danger")
        return render_template('index.html')

    if request.method == 'POST':

        # save information in db
        
        selected_time_utc = request.form['time_int']
        if selected_time_utc == 'default':
            flash("Please select a time that you are avaiable to interview.", "danger")
            return redirect(url_for('client_scheduler', interview_uuid=interview.uuid))

        selected_time_utc = int(selected_time_utc)
        interview.client_selection = selected_time_utc
        interview.status = InterviewStatus["CLIENT_CF"]
        interview.last_updated_time = datetime.utcnow()

        # get formatted date strings we need for emails
        client_time_str = tz_module.get_date_in_tz(selected_time_utc, int(interview.client.timezone))
        cand_time_str = tz_module.get_date_in_tz(selected_time_utc, int(interview.candidate.timezone))

        # send confirmation email to both with link
        zoom_url = zoom_module.create_zoom_room(interview)
        interview.zoom_link = zoom_url
        db.session.commit()

        mail_module.send_client_confirmation_email(interview, zoom_url, client_time_str)
        mail_module.send_candidate_confirmation_email(interview, zoom_url, cand_time_str)

        return redirect(url_for("client_success"))

    times_int = json.loads(interview.candidate_times)
    times_int = sorted(times_int)
    times_str = []
    times_object_list = []
    for time in times_int:
        times_str.append(tz_module.get_date_in_tz(int(time), int(interview.client.timezone)))
    
    for i in range(len(times_str)):
        times_object_list.append({
            "str": str(times_str[i]),
            "int": int(times_int[i])
        })
    return render_template('client_scheduler.html', times=times_object_list, candidate=interview.candidate)

# confirmed page, candidate
@app.route("/candidate_success")
def candidate_success():
    return render_template('candidate_success_page.html')


# confirmed page, client
@app.route("/client_success")
def client_success():
    return render_template('client_success_page.html')