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
from pytz import timezone
import pytz
import json 
# gloabl variable used to map from hours of offset to seconds or milliseconds depending on 
# our use case. Assuming we are using milliseconds per hour based on javascript representation  
utc_UNITS_PER_HOUR = 3600000


def time_in_tz_str(utc_time, tz_hour_offset):
	utc_time_in_tz = tz_hour_offset * utc_UNITS_PER_HOUR
	hour_of_day = utc_time_in_tz % 24 * utc_UNITS_PER_HOUR
	time_in_tz_str = ''
	if hour_of_day < 10:
		time_in_tz_str += '0'
	return time_in_tz_str + str(hour_of_day) + ":00"

 # Returns the difference in hours between timezone1 and timezone2
 # for a given date.
# def tz_diff(utc_int, tz1, tz2):

# 	print("tz_diff(utc_int, tz1, tz2), utc_int = " + str(utc_int))
# 	date = datetime.datetime.fromtimestamp(int(utc_int)/1000)
# 	return (tz2.localize(date) - 
# 		tz1.localize(date).astimezone(tz2)).seconds/3600

def tz_diff(utc_int, tz1, tz2):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    baseline_utc = timezone('Etc/GMT+0')
    print(utc_int)
    date = datetime.datetime.fromtimestamp(int(utc_int)/1000)
    tz1_localize = tz1.localize(date)
    tz2_localize = tz2.localize(date)
    as_timezone = tz2.localize(date).astimezone(tz2)
    print(tz1_localize)
    print(tz2_localize)
   
    diff = (tz2.localize(date).astimezone(baseline_utc) - tz1.localize(date).astimezone(baseline_utc)).seconds/3600
    if (diff > 12):
    	diff += -24
    print(diff)
    return diff
# cur_utc_int = int(datetime.datetime.utcnow().timestamp())*1000
# tz1 = timezone('Etc/GMT+4')
# tz2 = timezone('Etc/GMT-7')
# tz_diff(cur_utc_int, tz1, tz2)

#takes a string that names a timezone and maps it to the integer offset relative to utc(GMT) 
#the offest is in terms of hours. This is a critical note because utc is typically in milliseconds
#or in seconds. Directly used to pass offset to frontend
def timezone_str_to_utc_offset_int_in_hours(timezone_str, utc_int):
	print("timezone_str_to_utc_offset_int_in_hours(timezone_str, utc_int), utc_int = " + str(utc_int))
	utc_timezone = timezone("Etc/GMT+0")
	print("DANK MEMES")
	print(timezone_str)
	local_timezone = timezone(timezone_str)
	timezone_offset_integer = tz_diff(utc_int, local_timezone, utc_timezone)
	return timezone_offset_integer



#takes a string name of a timezone and an integer representing utc time in 
#seconds and then maps the int into its value in the new timezone 
def utc_int_to_timezone_adjusted_int(timezone_str, utc_int):
	print("utc_int_to_timezone_adjusted_int(timezone_str, utc_int), utc_int = " + str(utc_int))
	offset = utc_UNITS_PER_HOUR * timezone_str_to_utc_offset_int_in_hours(timezone_str, utc_int)
	print('OFFSET: ' + str(offset / utc_UNITS_PER_HOUR))
	return (offset + int(utc_int))

#maps the int representation of a time(adjusted utc) into a string representation
def int_time_representation_to_str_time_representation(int_representation, timezone_str):
	#I assume we are converting from javascript representation to 
	#python representation, i.e. milliseconds to seconds for utc
	print("int_time_representation_to_str_time_representation(int_representation, timezone_str), int_representation = " + str(int_representation))
	date = datetime.datetime.fromtimestamp(int_representation / 1000)
	print("int_time_representation_to_str_time_representation(int_representation, timezone_str), date = " + str(date))
	#Weekday, Month day number, year at hour:minute 
	dateStr = date.strftime("%A, %B %d, %Y at %H:00 " + timezone_str)
	return dateStr


#maps a list of times represented in utc into a list of strings with time zone info 
def int_times_list_to_str_times_list(utc_times_int_list, timezone_str):
	print("int_times_list_to_str_times_list(utc_times_int_list, timezone_str), utc_times_int_list = " + str(utc_times_int_list))
	str_times_list = []
	for each in utc_times_int_list:
		print("int_times_list_to_str_times_list(utc_times_int_list, timezone_str), each = " + str(each))
		adjusted_int = utc_int_to_timezone_adjusted_int(timezone_str, int(each))
		int_as_str_in_terms_of_utc = int_time_representation_to_str_time_representation(adjusted_int, timezone_str)
		str_times_list.append(int_as_str_in_terms_of_utc)
	return str_times_list 



#this is the primary function used externally. It takes an interview object(db ref)
#and returns two lists. The first is of strings 
def get_str_and_utc_lists_for_client(interview):
	utc_times_int_list = json.loads(interview.candidate_times)
	timezone_str = interview.client.timezone
	str_times_list = int_times_list_to_str_times_list(utc_times_int_list, timezone_str)

	print("get_str_and_utc_lists_for_client(interview), utc_times_int_list = " + str(utc_times_int_list))
	print("get_str_and_utc_lists_for_client(interview), str_times_int_list = " + str(str_times_list))
	#lists need to be in exactly the same order 
	return(utc_times_int_list, str_times_list)
