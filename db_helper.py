# # 
# # This file contains functions which allow us to easily query the database, add new entries, and remove old entries.
# # Authors: Greg Smith
# #

# from app import db
# from database import Candidate, Client, Interview
# from airtable import Airtable

# # Creates a new candidate given an email address if one does not exist, querying AirTable
# # returns None if candidate is not in airtable DB
# def add_candidate(email):

#     query = Candidate.query.filter_by(email=email)

#     if not query.first():

