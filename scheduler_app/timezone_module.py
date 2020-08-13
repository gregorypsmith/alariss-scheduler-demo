###################################################################################################################
# @author(s): Josh Gardner, Greg Smith
# @desc.: 
# The basic idea is that we can take in a list of utc times and a timezone string and from that directly map 
# the utc integers into representations adjusted for the timezone. From there, we can map thse new representations
# into strings for that timezone and send them to the frontend. This module is argubaly excessive in that most of 
# the functionality is relatively simple. However, it is useful because the fucntionality is extremely delicate 
# and can be performed in a few different ways. This file makes it easier to alter the underlying representation. 
###################################################################################################################

import datetime
from datetime import timedelta, timezone
import json 
# gloabl variable used to map from hours of offset to seconds or milliseconds depending on 
# our use case. Assuming we are using milliseconds per hour based on javascript representation  
utc_UNITS_PER_HOUR = 3600


###################################################################################################
###################################################################################################
###  									NEW MODULE												###
###################################################################################################
###################################################################################################

# Given a utc time and an hour offset, provide the hour of day in tz as a string
def time_in_tz_str(utc_time, tz_hour_offset):
	utc_time_in_tz = utc_time + (tz_hour_offset * utc_UNITS_PER_HOUR)
	date_in_tz = datetime.datetime.fromtimestamp(utc_time_in_tz, timezone.utc)
	time_in_tz_str = ''
	if date_in_tz.hour < 10:
		time_in_tz_str += '0'
	return time_in_tz_str + str(date_in_tz.hour) + ":00"

# # Test Case 1: should give current hour in Eastern Daylight time
# now = int(datetime.datetime.utcnow().timestamp())
# print(datetime.datetime.fromtimestamp(now))
# print('- 4 = ')
# east_daylight_time = -4
# print(time_in_tz_str(now, east_daylight_time))

# # Test Case 2: goes to next day (should return 5:00)
# time2 = 1597273200 # 19:00 GMT
# print(datetime.datetime.fromtimestamp(1597273200))
# print('+ 10 = ')
# gmt_plus_10 = 10 # + 10 should go to 9
# print(time_in_tz_str(time2, gmt_plus_10))

# get the utc timestamp of midnight tomorrow in a given timezone offset
def get_tomorrow_midnight_cand_tz(candidate_offset):
	today_utc = datetime.datetime.today()
	tmrw_utc = today_utc + timedelta(days=2)
	tmrw_utc_midnight = datetime.datetime(tmrw_utc.year, tmrw_utc.month, tmrw_utc.day)
	tmrw_tz_midnight = tmrw_utc_midnight + timedelta(hours=candidate_offset)
	midnight_tz_int = tmrw_tz_midnight.timestamp()
	return midnight_tz_int

# # Test Case 1: when is it tomorrow midnight EDT? should be something 20:00
# print('EST midnight tomorrow: ')
# print(datetime.datetime.fromtimestamp(get_tomorrow_midnight_cand_tz(-4)))

# # Test Case 2: when is it tomorrow midnight China? should be something 8:00
# print('China midnight tomorrow: ')
# print(datetime.datetime.fromtimestamp(get_tomorrow_midnight_cand_tz(8)))


#helper function to get the next n days represented as strings of format
# Weekday, Month, Day Number. These functions face other client modules
#on the backend and directly feed critical info to frontend 
def get_next_n_day_strs(n, candidate_offset):
	start_time = get_tomorrow_midnight_cand_tz(candidate_offset)
	next_n_days = get_next_n_days_int(n, start_time)
	retList = [] 
	for day_int in next_n_days:
		retList.append(convert_int_to_frontend_str(day_int))
	return retList 

#gets the next seven days from the moment called as utc integers 
#start at midnight of next day in UTC 
def get_next_n_days_int(n, start_time_int):
	as_date_object = datetime.datetime.fromtimestamp(start_time_int, timezone.utc)
	delta = timedelta(days=1)
	utc_int_list = []
	for i in range(0, n):
		as_date_object += delta
		utc_int_list.append(as_date_object.timestamp())
	return utc_int_list

#maps a utc integer into a string of the form Weekday, Month Day Number 
#leaves out info about hours, minutes, etc.  
def convert_int_to_frontend_str(day_int):

	# lists to get string representations
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	months = [None, "January", "February", "March", "April", "May", "June", "July", "August", "September", \
              "October", "November", "December"]

	to_date = datetime.datetime.fromtimestamp(day_int, timezone.utc)
	ret_str = days[to_date.weekday()] + ', '
	ret_str += str(months[to_date.month]) + ' ' + str(to_date.day)
	return ret_str

# #Test case 1: Print today GMT
# print('Today (date only) as frontend str (GMT): ')
# print(convert_int_to_frontend_str(datetime.datetime.utcnow().timestamp()))


# Creates list of 24 * n_days_out utc times, separated by one hour, starting at start_utc
def get_times_list(start_utc, n_days_out):
	as_date_object = datetime.datetime.fromtimestamp(start_utc, timezone.utc)
	all_list = []
	outer_delta = timedelta(hours=1)
	for hour in range(24):
		loop_day = as_date_object 
		inner_delta = timedelta(days=1)
		for i in range(n_days_out):	
			all_list.append(loop_day.timestamp()) 
			loop_day += inner_delta 
		as_date_object += outer_delta 

	return all_list

# print(len(get_times_list(now, 7)))
# Get all times GMT between tmrw midnight GMT to 1 day from now
# print(get_times_list(get_tomorrow_midnight_cand_tz(0), 1))

#Greg
# see whether a time is between 6am-10pm in the given timezone
def time_acceptable(time_utc_int, offset):
	to_date = datetime.datetime.fromtimestamp(time_utc_int, timezone.utc)
	to_date = to_date + timedelta(hours=offset)
	return to_date.hour >= 6 and to_date.hour <= 21


#Greg
# get date of a utc integer in the client timezone
def get_date_in_tz(utc_int, tz_hour_offset):
	to_date = datetime.datetime.fromtimestamp(utc_int, timezone.utc)
	to_date += timedelta(hours=tz_hour_offset)
	date_str = convert_int_to_frontend_str(to_date.timestamp())
	date_str += ' at ' + time_in_tz_str(utc_int, tz_hour_offset)
	return date_str

# #Test case 1: Print today GMT
# print('Today (with hours) as frontend str (GMT): ')
# print(get_date_in_tz(now, 0))

# #Test case 2: Print today EDT
# print('Today (with hours) as frontend str (EDT): ')
# print(get_date_in_tz(now, -4))


def col_vectors_to_rows_fixed_table(col_vecs):
	#assumes all col vectors have the same length 
	ret_rows = [] 
	for row in range(0, len(col_vecs[0])):
		row_vec = [] 
		for col in col_vecs: 
			row_vec.append(col[row])
		ret_rows.append(row_vec)
	return ret_rows 


# d_arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print("\n\n\n\n Fuckery")	
# print(col_vectors_to_rows_fixed_table(d_arr))

#each_day is a string returned by convert_int_to_frontend_str()
#elesewhere and we direct;ly compare it against teh same representations 
#for the other times. UNTESTED  
def get_all_times_on_day(target_day_str, times_list, offset):
	retList = [] 
	for time in times_list:
		time_as_str = convert_int_to_frontend_str(time + offset*utc_UNITS_PER_HOUR)
		if(target_day_str == time_as_str):
			retList.append(time)
	return retList 

# compare lists
def list_comparator(list):
	return int(list[0])

#this is where we filter out the fucked days for the candidate
def filter_fucked_days(cand_offset, n, times_list):
	#string giving date for frontend column purposes 
	the_n_days = get_next_n_day_strs(n, cand_offset)
	colList = [] 
	for each_day in the_n_days:
		times_on_fixed_day = get_all_times_on_day(each_day, times_list, cand_offset) 
		#this thing is a list of times on a fixed day sorted by hour 
		sorted_times = times_on_fixed_day
		colList.append(sorted_times)
	rowList = col_vectors_to_rows_fixed_table(colList)
	rowList_sorted = sorted(rowList, key=list_comparator)
	return rowList_sorted


#gets the times in utc that work for both client and candidate in terms of their 
#waking hours. Basically, we assume that both parties are available btwn 6am and 9pm 
#in their local times. Start at midnight of next day in terms of UTC(aka GMT+0)    
def get_acceptable_utc_times(client_offset, candidate_offset, start_utc, n_days_out):
	times_list = get_times_list(start_utc, n_days_out + 2)
	acceptable_times_list = []
	for hour in times_list:
		if time_acceptable(hour, client_offset) and time_acceptable(hour, candidate_offset):
			acceptable_times_list.append(hour)

	with_fucked_days_removed = filter_fucked_days(candidate_offset, n_days_out, acceptable_times_list)
	return with_fucked_days_removed

# # Test case 1: Client -3, cand 0, expect 9am-7pm
# midnight_tmrw_est = get_tomorrow_midnight_cand_tz(-5)

# times_get_acceptable_test = get_acceptable_utc_times(-5, 3, midnight_tmrw_est, 7)
# times_get_acceptable_test_2 = sorted(times_get_acceptable_test, key=list_comparator)

# # print(times_get_acceptable_test_2)
# for row in times_get_acceptable_test_2:
# 	row_str = ''
# 	for index in row:
# 		row_str += str(get_date_in_tz(index, 3)) + "  "
# 	print("["+row_str+"]")
# print("END OF OBJECT")

#helper function to get time information as object with two properties. First property is UTC integer in python 
#representation , UTC seconds. Second property is the corresponding hour as a string, e.g. 23:00.  
#These functions face other client modules on the backend and directly feed critical info to frontend 
def get_times_object(interview, n_days_out):

	# needed for helper function calls
	client_offset = int(interview.client.timezone)
	candidate_offset = int(interview.candidate.timezone)
	start_time = get_tomorrow_midnight_cand_tz(candidate_offset)

	# get info needed to construct table
	table_object = []
	acceptable_utc_times_by_hour = get_acceptable_utc_times(client_offset, candidate_offset, start_time, n_days_out)

	# append new row for each hour, each with n_days_out elements
	for row in acceptable_utc_times_by_hour:
		row_list = []
		for index in row:
			row_list.append({
				"hour_as_str": time_in_tz_str(index, candidate_offset),
				"as_utc_time": index,
				"date": get_date_in_tz(index, candidate_offset)
			})
		table_object.append(row_list)

	return table_object