###################################################################################################################
# @author(s): Greg Smith, Josh Gardner, Hung Nguyeb
# @desc.: 
# Module containing functions to compose emails to clients and candidates throughout the scheduling process.
# These emails are abstracted into this module to clean up the routes.py file and to make it easier for quick changes
# to be made to the verbage of these emails.
###################################################################################################################
from scheduler_app import mail
from flask_mail import Message
import os

scheduler_email = os.getenv('EMAIL_USERNAME')

# initial email to candidate with scheduler link
def send_candidate_scheduler_email(interview, url):
    msg = Message('[ACTION REQUIRED] Schedule your upcoming interview with ' + interview.company_name,
    sender=scheduler_email,
    recipients=[interview.candidate.email])
    msg.body = 'Dear ' + interview.candidate.first_name + ',\n\n'
    msg.body += 'Congratulations! ' + interview.company_name + ' would like you to interview for an open ' + \
        interview.position_name + ' position.\n\n'
    msg.body += 'Your point of contact is ' + interview.client.first_name + ' ' + interview.client.last_name + '. Please continue to the following link to schedule your interview:\n\n'
    msg.body += url + '\n\n'
    msg.body += 'Best wishes and good luck,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to candidate confirming picked times
def send_candidate_confirmed_times(interview):
    msg = Message('Availability for ' + interview.company_name + ' Interview Confirmed',
    sender=scheduler_email,
    recipients=[interview.candidate.email])
    msg.body = 'Dear ' + interview.candidate.first_name + ',\n\n'
    msg.body += 'Thank you for submitting your availability for your upcoming interview with' + interview.company_name + \
        '.\n\n'
    msg.body += 'Your interviewer has been sent this information and we will let you know when they have chosen one of your available time slots.\n\n'
    msg.body += 'No further action is required on your part. We wish you the best of luck!\n\n'
    msg.body += 'Best wishes,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to client with scheduler link
def send_client_scheduler_email(interview, url):
    candidate_full_name = interview.candidate.first_name + ' ' + interview.candidate.last_name
    msg = Message('[ACTION REQUIRED] Schedule your upcoming interview with ' + candidate_full_name,
    sender=scheduler_email,
    recipients=[interview.client.email])
    msg.body = 'Dear ' + interview.client.first_name + ',\n\n'
    msg.body += candidate_full_name + ' has submitted their availibility to interview for the open ' + interview.position_name + ' position at your company.\n\n'
    msg.body += 'Please continue to the following link to select a time:\n\n'
    msg.body += url + '\n\n'
    msg.body += 'Thank you,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to client to confirm time / Zoom link
def send_client_confirmation_email(interview, zoom_url, interview_datetime_client):
    candidate_full_name = interview.candidate.first_name + ' ' + interview.candidate.last_name
    msg = Message('Confirmed: Interview with ' + candidate_full_name + ' on ' + interview_datetime_client,
    sender=scheduler_email,
    recipients=[interview.client.email])
    msg.body = 'Dear ' + interview.client.first_name + ',\n\n'
    msg.body += 'Thank you for your selection! Your interview with ' + candidate_full_name + ' for the ' + interview.position_name + ' has been scheduled and the candidate has been notified of your selection.\n\n'
    msg.body += 'The interview has been scheduled for ' + interview_datetime_client + '.\n\n'
    msg.body += 'When it is time for the interview, click this Zoom link to meet:\n\n'
    msg.body += zoom_url + '\n\n'
    msg.body += 'Best wishes and good luck,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to candidate with client's confirmed time / Zoom link
def send_candidate_confirmation_email(interview, zoom_url, interview_datetime_candidate):
    client_full_name = interview.client.first_name + ' ' + interview.client.last_name
    msg = Message('Confirmed: Interview with ' + client_full_name + ' of ' + interview.company_name + ' on ' + interview_datetime_candidate,
    sender=scheduler_email,
    recipients=[interview.candidate.email])
    msg.body = 'Dear ' + interview.candidate.first_name + ',\n\n'
    msg.body += 'Great news! ' + client_full_name + ' has selected a time to interview you for the ' + interview.position_name + ' position.\n\n'
    msg.body += 'The interview has been scheduled for ' + interview_datetime_candidate + '.\n\n'
    msg.body += 'When it is time for the interview, click this Zoom link to meet:\n\n'
    msg.body += zoom_url + '\n\n'
    msg.body += 'Best wishes and good luck,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to candidate after inactivity
def send_candidate_reminder(interview, url):
    client_full_name = interview.client.first_name + ' ' + interview.client.last_name
    msg = Message('[ACTION REQUIRED] ' + client_full_name + ' from ' + interview.company_name + ' is waiting for your interview selection!',
    sender=scheduler_email,
    recipients=[interview.candidate.email])
    msg.body = 'Dear ' + interview.candidate.first_name + ',\n\n'
    msg.body += 'We hope you\'re doing well! This is a friendly reminder that '
    msg.body += client_full_name + ' from ' + interview.company_name + ' would like to interview you for an open '
    msg.body += interview.position_name + ' position. It has been a while since we originally sent you this information.\n\n'
    msg.body += 'Please submit some times that you are available over the next week aft the following link:\n\n'
    msg.body += url + '\n\n'
    msg.body += 'Best wishes and good luck,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to client after inactivity
def send_client_reminder(interview, url):
    candidate_full_name = interview.candidate.first_name + ' ' + interview.candidate.last_name
    msg = Message('[ACTION REQUIRED] ' + candidate_full_name + ' is awaiting your response for their upcoming ' + interview.position_name + ' interview!',
    sender=scheduler_email,
    recipients=[interview.client.email])
    msg.body = 'Dear ' + interview.client.first_name + ',\n\n'
    msg.body += 'We hope you\'re doing well! This is a friendly reminder to schedule your interview with '
    msg.body += candidate_full_name + ' for your open ' + interview.position_name + ' position.\n\n'
    msg.body += 'Please select the time you\'d like to interview ' + candidate_full_name + ' at the following link:\n\n'
    msg.body += url + '\n\n'
    msg.body += 'Best wishes and good luck,\n'
    msg.body += 'The Alariss Global Team'
    mail.send(msg)

# email to both candidate and client when admin cancels intervieww
def send_cancellation_email(interview):
    candidate_full_name = interview.candidate.first_name + ' ' + interview.candidate.last_name
    client_full_name = interview.client.first_name + ' ' + interview.client.last_name
    msg = Message('Your interview has been cancelled',
    sender=scheduler_email,
    recipients=[interview.client.email, interview.candidate.email])
    msg.body = "Hello,\n\n"
    msg.body += 'The interview between ' + candidate_full_name + ' and ' + client_full_name + ' of '
    msg.body += interview.company_name + ' for the open ' + interview.position_name + ' role has been cancelled.\n\n'
    msg.body += 'If you believe this was in error, please contact nick@alariss.com for assistance.\n\n'
    msg.body += 'We apologize for the inconvenience!\n\n'
    msg.body += 'Sincerely,'
    msg.body += 'The Alariss Global Team'

# email to send candidate when interview is soon
def send_candidate_interview_soon_email(interview, interview_date_cand):
    client_full_name = interview.client.first_name + ' ' + interview.client.last_name
    msg = Message('Reminder: Your ' + interview.company_name + ' interview is less than 24 hours away!',
    sender=scheduler_email,
    recipients=[interview.candidate.email])
    msg.body += 'Dear' + interview.candidate.first_name + ',\n\n'
    msg.body += 'This is a friendly reminder that your interview with ' + client_full_name + ' from '
    msg.body += interview.company_name + ' for the open ' + interview.position_name + ' role is in less than 24 hours!\n\n'
    msg.body += 'The interview is scheduled for ' + interview_date_cand + ' (in your timezone).'
    msg.body += 'Please join the following Zoom link 5 minutes prior to the interview:\n\n'
    msg.body += interview.zoom_link + '\n\n'
    msg.body += 'Best of luck!'
    msg.body += 'The Alariss Global Team'

# email to send client when interview is soon
def send_client_interview_soon_email(interview, interview_date_client):
    candidate_full_name = interview.candidate.first_name + ' ' + interview.candidate.last_name
    msg = Message('Reminder: Your interview with ' + candidate_full_name + 'is less than 24 hours away!',
    sender=scheduler_email,
    recipients=[interview.client.email])
    msg.body += 'Dear' + interview.client.first_name + ',\n\n'
    msg.body += 'This is a friendly reminder that your interview with ' + candidate_full_name
    msg.body += 'for the open ' + interview.position_name + ' role is in less than 24 hours!\n\n'
    msg.body += 'The interview is scheduled for ' + interview_date_client + ' (in your timezone).'
    msg.body += 'Please join the following Zoom link when it is time to interview:\n\n'
    msg.body += interview.zoom_link + '\n\n'
    msg.body += 'We hope they\'re a good fit!'
    msg.body += 'The Alariss Global Team'
