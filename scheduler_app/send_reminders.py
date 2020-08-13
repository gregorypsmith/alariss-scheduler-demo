# ###################################################################################################################
# # @author(s): Greg Smith, Josh Gardner, Hung Nguyeb
# # @desc: 
# # Script to be run daily to remind candidate and/or client who has not submitted forms via the scheduler to do so.
# # Ideally we'll have configurable time frame in which reminders are sent, like 1, 2, 3 days etc.
# # All email content is located within email_module.py, not here; we simply call the functions that send those emails.
# ###################################################################################################################

# from scheduler_app import db
# from datetime import datetime, timedelta
# import os
# from flask import url_for
# import scheduler_app.email_module as mail_module
# from scheduler_app.models import User, Interview
# import scheduler_app.timezone_module as tz_module

# # Configurable reminders
# SEND_REMINDERS = True
# NUM_REMINDERS = 3 # how many days in a row do we send this?

# # Process the interviews, return a list of interviews to be processed
# def check_interviews():
#     interview_list = []
#     for interview in Interview.query():
#         now = datetime.utcnow()
#         if interview.status == 1 or interview.status == 2:
#             diff = now - interview.last_updated_time
#             if diff.days >= 1 and diff.days <= 1 + NUM_REMINDERS:
#                 ret.append(interview)
#         elif interview.status == 3:
#             diff = now - datetime.fromtimestamp(int(interview.client_selection), timezone.utc)
#             if diff.days < 1:
#                 ret.append(interview)
#     return interview_list

# # given interviews and reminders, construct urls and send emails
# def send_reminders():

#     if not SEND_REMINDERS:
#         return

#     interview_list = check_interviews()

#     for interview in interview_list:
#         # candidate hasn't selected times
#         if interview.status == 1:
#             url = os.getenv("INDEX_URL") + url_for('select_timezone', interview_id=interview.id)
#             mail_module.send_candidate_reminder(interview, url)
#         # client hasn't chosen a time
#         elif interview.status == 2:
#             url = os.getenv("INDEX_URL") + url_for('client_scheduler', interview_id=interview.id)
#             mail_module.send_client_reminder(interview, url)
#         # interview happening within a day
#         elif interview.status == 3:
#             date_str_candidate = tz_module.get_date_in_tz(int(interview.client_selection), interview.candidate.timezone)
#             date_str_client = tz_module.get_date_in_tz(int(interview.client_selection), interview.client.timezone)
#             send_candidate_interview_soon_email(interview, date_str_candidate)
#             send_client_interview_soon_email(interview, date_str_client)

# # Main function call
# send_reminders()