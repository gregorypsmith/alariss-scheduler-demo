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
#and returns two lists. The first is of strings. These functions face other client modules
#on the backend and directly feed critical info to frontend 
def get_str_and_utc_lists_for_client(interview):
	utc_times_int_list = json.loads(interview.candidate_times)
	timezone_str = interview.client.timezone
	str_times_list = int_times_list_to_str_times_list(utc_times_int_list, timezone_str)

	print("get_str_and_utc_lists_for_client(interview), utc_times_int_list = " + str(utc_times_int_list))
	print("get_str_and_utc_lists_for_client(interview), str_times_int_list = " + str(str_times_list))
	#lists need to be in exactly the same order 
	return(utc_times_int_list, str_times_list)



#helper function to get the next n days represented as strings of format
# Weekday, Month, Day Number. These functions face other client modules
#on the backend and directly feed critical info to frontend 
def get_next_n_day_strs(n):
	next_n_days = get_next_n_days_as_utc(n)
	retList = [] 
	for day_utc in next_n_days:
		retList.append(convert_utc_to_frontend_str(day_utc))
	return retList 



#helper function to get time information as object with two properties. First property is UTC integer in python 
#representation , UTC seconds. Second property is the corresponding hour as a string, e.g. 23:00.  
#These functions face other client modules on the backend and directly feed critical info to frontend 
def get_times_object(interview, n_days_out):
	client_offset = int(interview.client.timezone)
	candidate_offset = int(interview.candidate.timezone)
	start_utc = Datetime.now()
	#stores all the critical nfo for the frontedn in an a list of objects
	times_object = []
	acceptable_utc_times = get_acceptable_utc_times(client_offset, candidate_offset, start_utc, n_days_out):
	for utc_int in acceptable_utc_times:
		times_object.append({
            "hour_as_str": time_in_tz_str(utc_int, tz_hour_offset),
            "as_utc_int": utc_int,
            "date": get_date_in_tz(utc_int, tz_hour_offset)
        })
	return times_object 

#gets the next seven days from the moment called as utc integers 
#start at midnight of next day in UTC 
def get_next_n_days_as_utc(n):
	return "implemented"

#maps a utc integer into a string of the form Weekday, Month Day Number 
#leaves out info about hours, minutes, etc.  
def convert_utc_to_frontend_str(day_utc):
	return "unimplemented"

#gets the times in utc that work for both client and candidate in terms of their 
#waking hours. Basically, we assume that both parties are available between 6am and 9pm 
#in their local times. Start at midnight of next day in terms of UTC(aka GMT+0)    
def get_acceptable_utc_times(client_offset, candidate_offset, start_utc, n_days_out):
	return "unimplemented"



##############################################################################################################################################
#######################################START JAVASCRIPT BULLSHIT##############################################################################
##############################################################################################################################################
//some crazy helper function for converting candidate times to utc for backend representation 
function convert_to_utc(hour_as_str, midnight_of_day){
    console.log(parseInt(hour_as_str.substring(0, 2)))
    var candidate_offset_ms = MS_PER_HOUR * parseInt({{candidate_GMT_offset}});
    var hour_ms = MS_PER_HOUR * parseInt(hour_as_str.substring(0, 2));
    var retVal = midnight_of_day + hour_ms  + candidate_offset_ms;
    var date = new Date(parseInt(midnight_of_day))
    console.log(date)
    var date = new Date(parseInt(retVal))
    console.log(date)
    return retVal;
}

function get_info_for_next_n_days(n){
    //list containing info objects for each day 
    retList = [] 
    //start at today 
    var today = new Date() # current utc time 
    for (var i=0; i < n; i++) {
        var tomorrow = new Date(today)
        tomorrow.setDate(tomorrow.getDate() + 1)
        retList.push(_get_date_info(tomorrow))
        //a day has passed lol 
        today = tomorrow
    }
    return retList 
}
    
//helper function that extracts detailed info for a given date and puts it into an easy to use object
function _get_date_info(today){    
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yr = 
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", 
              "October", "November", "December"]
    //do some crazy modding to get the UTC time in milliseconds of the start of the day
    var x = today.getTime()
    var at_midnight = x - ( x % (24 * MS_PER_HOUR))

    var day_of_week = days[today.getDay()]
    var month_name = months[today.getMonth()]
    well_formatted = day_of_week + "\n" + month_name + " " + dd
    well_formatted2 = day_of_week + ", " + month_name + " " + dd
    const date_info = {
            day: dd,
            month: mm,
            weekday: day_of_week,
            month_as_word:month_name,
            as_string: well_formatted,
            as_string_one_line: well_formatted2,
            at_midnight_of_day: at_midnight 
            }   
    return date_info
}

function get_acceptable_times(client_GMT_offset, candidate_GMT_offset){
    var diff = candidate_GMT_offset - client_GMT_offset
    var times = []
    for(var i=30; i < 46; i++) {
        // console.log("fuck fuck fuck a duck")
        var num = (i + diff) % 24
        // console.log(num)
        // console.log("div 10 is")
        // console.log(Math.floor(num/10))
        // console.log("\n\n")
        if(num >= 5){
        times.push(num)
        }
    }
    return convert_to_str_array(times)

}



function convert_to_str_array(times){
    var ret_str_array = []
    times = times.sort(function(a, b) {
                  return a - b;
                });
    // console.log("fuckery")
    console.log(times)
    var prev = times[0]   
    for(var i=0; i < times.length; i++) {
        var num_as_str = ""
        var num = times[i]
        if(num - prev > 1){
            ret_str_array.push("...")
        } 
        if(Math.floor(num/10) == 0){
            num_as_str = "0"+num.toString()+":00"
        }else{
            num_as_str = num.toString()+":00"
        }
        ret_str_array.push(num_as_str)
        prev = num
    }
    return ret_str_array

}




day_information = get_info_for_next_n_days(7);
var client_GMT_offset =parseInt({{client_GMT_offset}})
var candidate_GMT_offset = parseInt({{candidate_GMT_offset}})
times = get_acceptable_times(client_GMT_offset, candidate_GMT_offset)