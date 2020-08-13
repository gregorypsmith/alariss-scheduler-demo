########################################################################
#@author: Hung Nguyen
#@architects: Josh Gardner, Greg Smith
#@desc: File with supporting helper methods for creating an administrative 
#dashboard to manage open intervies, track their status, and cancel them 
#if needed. 
########################################################################
from scheduler_app.send_reminders import * 

# Note: @Hung, we have created what we think is a reasonable outline of the 
# functionality an admin dashboard would need to have. Feel free to add
# additional functionality and/or alter the structure of what we have outlined 
# here. Note that many of the lookup functions contained in this outline will 
# by necessity be highly inefficient, however since this system will not likely 
# be used for very high volumes of data this is largely irrelevant. 


#searches through interview table and returns a list of all open interviews 
#as interview objects. Done here as a helper function to keep the primary 
#function more succinct.  
def get_open_interviews():
	pass

#returns all the information about open interviews as a python object 
#object will be sent to the frontend via route.py
def get_all_open_interview_info():
	all_open_interviews = get_open_interviews()
	all_interview_info = []
	for interview in all_open_interviews:
		#do stuff here 
		data_object.append({
				"example 1": "@Hung please change this, this an example",
				"example 2": "you get the point lol"
			})
		all_interview_info.append(data_object)
	pass

#given an interview object, cancels the interview and notifies both parties of
#the cancellation via email. Updates the database so no more reminders are sent
#to either the client or the candidate.  
def cancel_interview(interview):
	#@Hung, this is still mostly unimplemented. I just put in the 
	#emailer function from Greg's module so you know you have hit
	#it will send cancellation emails to both parties.  
	send_cancellation_email(interview)



#given an interview object updates fields of the interview. 
def update_interview(interview, fields):
	pass

#return all interviews that include a candidate with the string
#candidate_name somewhere in their name. As an example, a user c
# could query "Mike" and get all people with the firstname Mike
#and a query with "Mik" would also return them.  
def lookup_interviews_by_candidate_name(candidate_name):
	pass 

#return all interviews that include a client with the string
#client_name somewhere in their name. As an example, a user c
# could query "Mike" and get all people with the firstname Mike
#and a query with "Mik" would also return them.  
def lookup_interviews_by_client_name(client_name):
	pass 


#return all interviews for positions at companies whose names 
#include the string company_name. 
def lookup_interviews_by_company_name(company_name):
	pass 


#return all interviews with the specified completion status 
def lookup_interviews_by_completion_status(completion_status):
	pass 

#return all interviews where the position title contains the 
#string position title. 
def lookup_interviews_by_position_title(position_title):
	pass 

#allows the user to just show interviews that meet certain criteria in a search.
#this is advanced functionality, so don;t worry about implementing this until 
#all other functionality has been implemented.
def filter_by(candidate_name, client_name, client_company, position_name, completion_status, position_title):
	retSet = set() 
	if candidate_name != None: 
		retSet.append(lookup_interviews_by_candidate_name(candidate_name)) 
	if client_name != None: 
		retSet.append(lookup_interviews_by_client_name(client_name)) 
	if client_company != None: 
		retSet.append(lookup_interviews_by_client_company_name(client_company))
	if completion_status != None: 
		retSet.append(lookup_interviews_by_completion_status(completion_status))
	if completion_status != None: 
		retSet.append(lookup_interviews_by_position_title(position_title))
	return retSet