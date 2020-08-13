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
        ("None", " --- Please Select a Timezone --- "),
        ('US/Hawaii', "(GMT -10:00) Hawaii"),
        ("US/Alaska", "(GMT -9:00) Alaska"),
        ("US/Pacific", "(GMT -8:00) Pacific Time (US &amp; Canada)"),
        ("US/Mountain", "(GMT -7:00) Mountain Time (US &amp; Canada)"),
        ("US/Central", "(GMT -6:00) Central Time (US &amp; Canada), Mexico City"),
        ("US/Eastern", "(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima"),
        ("Canada/Atlantic", "(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz"),
        ("Brazil/East", "(GMT -3:00) Brazil, Buenos Aires, Georgetown"),
        ("America/Noronha", "(GMT -2:00) Mid-Atlantic"),
        ("Atlantic/Azores", "(GMT -1:00) Azores, Cape Verde Islands"),
        ("Europe/London", "(GMT) Western Europe Time, London, Lisbon, Casablanca"),
        ("Europe/Paris", "(GMT +1:00) Brussels, Copenhagen, Madrid, Paris"),
        ("Africa/Johannesburg", "(GMT +2:00) Kaliningrad, South Africa"),
        ("Asia/Baghdad", "(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg"),
        ("Asia/Kabul", "(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi"),
        ("Indian/Maldives", "(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent"),
        ("Asia/Dhaka", "(GMT +6:00) Almaty, Dhaka, Colombo"),
        ("Asia/Jakarta", "(GMT +7:00) Bangkok, Hanoi, Jakarta"),
        ("Asia/Shanghai", "(GMT +8:00) China, Perth, Singapore, Hong Kong"),
        ("Asia/Tokyo", "(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk"),
        ("Australia/Melbourne", "(GMT +10:00) Eastern Australia, Guam, Vladivostok"),
        ("Pacific/Noumea", "(GMT +11:00) Magadan, Solomon Islands, New Caledonia"),
        ("Pacific/Auckland", "(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka")
    ], validators=[DataRequired()])
    submit = SubmitField("Create Interview")


class SelectTimezoneForm(FlaskForm):
    candidate_timezone = SelectField(label="Client Timezone", choices=[
        ("None", " --- Please Select a Timezone --- "),
        ('US/Hawaii', "(GMT -10:00) Hawaii"),
        ("US/Alaska", "(GMT -9:00) Alaska"),
        ("US/Pacific", "(GMT -8:00) Pacific Time (US &amp; Canada)"),
        ("US/Mountain", "(GMT -7:00) Mountain Time (US &amp; Canada)"),
        ("US/Central", "(GMT -6:00) Central Time (US &amp; Canada), Mexico City"),
        ("US/Eastern", "(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima"),
        ("Canada/Atlantic", "(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz"),
        ("Brazil/East", "(GMT -3:00) Brazil, Buenos Aires, Georgetown"),
        ("America/Noronha", "(GMT -2:00) Mid-Atlantic"),
        ("Atlantic/Azores", "(GMT -1:00) Azores, Cape Verde Islands"),
        ("Europe/London", "(GMT) Western Europe Time, London, Lisbon, Casablanca"),
        ("Europe/Paris", "(GMT +1:00) Brussels, Copenhagen, Madrid, Paris"),
        ("Africa/Johannesburg", "(GMT +2:00) Kaliningrad, South Africa"),
        ("Asia/Baghdad", "(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg"),
        ("Asia/Kabul", "(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi"),
        ("Indian/Maldives", "(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent"),
        ("Asia/Dhaka", "(GMT +6:00) Almaty, Dhaka, Colombo"),
        ("Asia/Jakarta", "(GMT +7:00) Bangkok, Hanoi, Jakarta"),
        ("Asia/Shanghai", "(GMT +8:00) China, Perth, Singapore, Hong Kong"),
        ("Asia/Tokyo", "(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk"),
        ("Australia/Melbourne", "(GMT +10:00) Eastern Australia, Guam, Vladivostok"),
        ("Pacific/Noumea", "(GMT +11:00) Magadan, Solomon Islands, New Caledonia"),
        ("Pacific/Auckland", "(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka")
    ], validators=[DataRequired()])
    submit = SubmitField("Select Timezone")


class CandidateSelectionForm(FlaskForm):
    candidate_time_info = HiddenField(label="Candidate Time Info")
    submit = SubmitField("Select Times")