from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from scheduler_app.models import User, Interview

class InterviewForm(FlaskForm):
    candidate_fname = StringField(label="Candidate First Name", validators=[DataRequired(), Length(min=2, max=20)])
    candidate_lname = StringField(label="Candidate Last Name", validators=[DataRequired(), Length(min=2, max=20)])
    candidate_email = StringField(label="Candidate Email", validators=[DataRequired(), Email()])
    candidate_position = StringField(label="Candidate Position", validators=[DataRequired(), Length(min=2, max=60)])
    client_fname = StringField(label="Client First Name", validators=[DataRequired(), Length(min=2, max=20)])
    client_lname = StringField(label="Client Last Name", validators=[DataRequired(), Length(min=2, max=20)])
    client_company = StringField(label="Client Company", validators=[DataRequired(), Length(min=2, max=100)])
    client_email = StringField(label="Client Email", validators=[DataRequired(), Email()])
    client_timezone = SelectField(label="Client Timezone", choices=[
        ("", " --- Please Select a Timezone --- "),
        ('-10', "GMT -10:00"),
        ('-9', "GMT -9:00"),
        ('-8', "GMT -8:00"),
        ('-7', "GMT -7:00"),
        ('-6', "GMT -6:00"),
        ('-5', "GMT -5:00"),
        ('-4', "GMT -4:00"),
        ('-3', "GMT -3:00"),
        ('-2', "GMT -2:00"),
        ('-1', "GMT -1:00"),
        ('0', "GMT +0:00"),
        ('1', "GMT +1:00"),
        ('2', "GMT +2:00"),
        ('3', "GMT +3:00"),
        ('4', "GMT +4:00"),
        ('5', "GMT +5:00"),
        ('6', "GMT +6:00"),
        ('7', "GMT +7:00"),
        ('8', "GMT +8:00"),
        ('9', "GMT +9:00"),
        ('10', "GMT +10:00"),
        ('11', "GMT +11:00"),
        ('12', "GMT +12:00")
    ], validators=[DataRequired()])
    submit = SubmitField("Create Interview")


class SelectTimezoneForm(FlaskForm):
    candidate_timezone = SelectField(label="Client Timezone", choices=[
        ("None", " --- Please Select a Timezone --- "),
        ('-10', "GMT -10:00"),
        ('-9', "GMT -9:00"),
        ('-8', "GMT -8:00"),
        ('-7', "GMT -7:00"),
        ('-6', "GMT -6:00"),
        ('-5', "GMT -5:00"),
        ('-4', "GMT -4:00"),
        ('-3', "GMT -3:00"),
        ('-2', "GMT -2:00"),
        ('-1', "GMT -1:00"),
        ('0', "GMT +0:00"),
        ('1', "GMT +1:00"),
        ('2', "GMT +2:00"),
        ('3', "GMT +3:00"),
        ('4', "GMT +4:00"),
        ('5', "GMT +5:00"),
        ('6', "GMT +6:00"),
        ('7', "GMT +7:00"),
        ('8', "GMT +8:00"),
        ('9', "GMT +9:00"),
        ('10', "GMT +10:00"),
        ('11', "GMT +11:00"),
        ('12', "GMT +12:00")
    ], validators=[DataRequired()], id="candidate_timezone")
    submit = SubmitField("Select Timezone")


class CandidateSelectionForm(FlaskForm):
    candidate_time_info = HiddenField(label="Candidate Time Info", id="submit_times")
    submit = SubmitField("Select Times")