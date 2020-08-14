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

* dashboar

* admin_page.html = file used to generate the interview creation page. Note that this page is only 
  accessible by users who have already logged in. 

* admin_success.html = page that renders to indicate to the user that an interview has been successfully created 
  contains buttons to allow them to create another interview or return to the dashboard. 
