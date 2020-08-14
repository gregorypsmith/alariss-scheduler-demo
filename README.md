# Interview Scheduler for Clients and Candidates of Alariss

CAUTION NOTES: Database 
We are currently using a SqlLite Database. This was chosen due to time constraints and 
for ease of development. Ech time you push to the master branch you will overwrite the 
existing entries in the database. Consequently, switching to a better database system 
would be a massive improvemtn. Moreover you need to take care to record the contents 
of the remote database(accessible throught the admin dashboard) prior to making any 
pushes to the master branch. This is a major design flaw, however it is known and
deliberate due to the constraints under which the app was initially developed.

How to set up a local environment

1. Clone the alariss-scheduler Github repository on your local machine.
2. Create a virtual environment on your machine and cd into the repo directory.
3. Install all packages in the requirements.txt file. (pip install -r requirements.txt)
4. Receive the .env file from Nick and place it in the top level directory for the repository.
5. To run the app, type "python run.py" and hit Enter.
6. If you receive a SQLAlchemy error, type "python init_db.py" and hit enter (see warning
   above)
7. To access the local instance of the application, visit http://localhost:5000/

How to deploy

1. Login to the Alariss Heroku account.
2. Click on the 'alariss-scheduler' project.
3. Click on the 'Deploy' tab.
4. Scroll to the bottom, ensure 'master' is selected, and click 'Deploy from Github'.

Structure of Codebase

BACKEND STRUCTURE

The top level repository directory contains a folder 'scheduler_app', wherein all
the significant modules used within the app are located. Any .py file outside of this
directory is not part of the app itself but a helper script which performs tasks such
as initializing the database.

Within the scheduler_app directory, there are multiple modules whose functions are called
by the routes.py file, which connect the frontend pages to the backend logic. The modules
are as follows:

* timezone_modules.py = Library with functions to convert between candidate and client
  timezones and to generate the frontend representation of the appropriate interview
  slots given those timezones.

* email_module.py = Library with functions which construct the various emails to be 
  sent throughout the scheduling flow.

* zoom_module.py = Library with functions which create a Zoom Room object given a
  UTC timestamp and contact information of both parties. 

* send_reminders.py = Not fully implemented, but a module which ideally would run
  on a schedule to check which clients and candidates have not taken the required
  actions to schedule their interviews.

FRONTEND STRUCTURE

The frontend code is conatined within a folder 'scheduler_app/templates', wherein all
the significant files used to render the user interface are stored. 

The following files are used for formatting:

* layout.html = File that contains nav-bar with Alariss logo as well as imports for 
  packages like jquery that are used elsewhere in the frontend codebase. This file is included 
  into all other html files.

* login.html = file for the login page

* dashboard.html = renders the user dashboard for keeping track of all interviews and their 
  associated information. 

* admin_page.html = file used to generate the interview creation page. Note that this page is only 
  accessible by users who have already logged in. 

* admin_success.html = page that renders to indicate to the user that an interview has been successfully created 
  contains buttons to allow them to create another interview or return to the dashboard. 

* select_timezone.html = file that generates the page where candidates select their timezone. This page occurs 
  before the candidate is able to select their available times in candidate_scheduler.html

* candidate_scheduler.html= file used to generate a table of interview slots for the candidate to select from. 
  The candidate is only able to submit after first selecting ten or more timeslots. This file uses jquery and jinja
  to generate the table using data from the backend. This file contains the most opportunities for bugs to occur. 
  Pleasure use caution in making any alterations to this file or its coresponding route in routes.py. 

* candidate_success_page.html = file used to generate a confirmation page to inform the user of successful submission 

* client_scheduler.html = file that renders the page where the client selects their preferred meeeting time from a 
  dropdown list. 

* client_success_page.html = file that renders a success message inform the user that their choice has been submitted. 

* index.html = the default empyt page featuring the Alariss navbar and an error message. This is used if the candidate 
  or client attempts to access a page out of our predefined flow. 

DATABASE STRUCTURE 

The database code is contained within scheduler_app/models.py. The database itself is contained in scheduler_app/alariss.sqlite.
There are three tables in the database organized as follows: 

* Administrator = A necessary table for the Flask-Login package. Contains the following fields:
  - id: internal ID representation, primary key
  - first_name: first name of administrator
  - email: email address used to login to the admin dashboard
  - password: password used to login to the admin dashboard

* User = Table which stores information on our users, both clients and candidates. Note that these are in one shared table because
  one individual could be both roles in two different interviews.
  - id: internal ID representation, primary key
  - first_name: first name of user
  - last_name: last name of user
  - email: email address of user, used for sending automated scheduling emails
  - timezone: integer representation of the user's timezone, by GMT offset in hours

* Interview = Table which stores information on each interview; the most involved table in the database
  - id: internal ID representation, primary key
  - uuid: external ID representation, passed in URLs to identify an interview
  - candidate: the User object of the candidate in this interview
  - client: the User object of the client in this interview
  - candidate_times: a JSON string of UTC timestamps that the candidate is available to interview for
  - client_selection: an integer UTC timestamp of the client's selected interview time
  - company_name: Name of interviewing company, provided by admin
  - postion_name: Name of position to be interviewed for, provided by admin
  - status: Integer representing the current stage of the interview scheduling process
      1 = 'STARTED' = interview created
      2 = 'CANDIDATE_CF' = candidate has picked times
      3 = 'CLIENT_CF' = client has made a selection
      4 = 'CANCELLED' = Interview cancelled by administrator
  - created_time: DateTime object representing when this interview was created by admin
  - last_updated_time: Datetime object representing the last time the status field of this interview was updated
  - zoom_link: URL to the Zoom Room for the interview
  - archived: boolean value representing whether the admin has archived the interview in the dashboard, which takes
    it out of the primary view
  - zoom_pwd: password given to both client and candidate in interview confirmation email