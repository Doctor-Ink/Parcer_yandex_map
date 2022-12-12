
import time

def format_duration(seconds):
    years = seconds // (365 * 24 * 3600)
    if years:
        years_str = f"{years} year" if years == 1 else f"{years} years"
    else:
        years_str = ''
    days = seconds // (24 * 3600) - years * 365
    if days:
        days_str = f"{days} day" if days == 1 else f"{days} days"
    else:
        days_str = ''
    hours = int(time.strftime("%H", time.gmtime(seconds)))
    if hours:
        hours_str = f"{hours} hour" if hours == 1 else f"{hours} hours"
    else:
        hours_str = ''
    minutes = int(time.strftime("%M", time.gmtime(seconds)))
    if minutes:
        minutes_str = f"{minutes} minute" if minutes == 1 else f"{minutes} minutes"
    else:
        minutes_str = ''
    seconds = int(time.strftime("%S", time.gmtime(seconds)))
    if seconds:
        seconds_str = f"{seconds} second" if seconds == 1 else f"{seconds} seconds"
    else:
        seconds_str = ''
    data_list = [years_str, days_str, hours_str, minutes_str, seconds_str]
    data_list = [item for item in data_list if item !='']
    result_str = ''
    for ind, val in enumerate(data_list):
        if len(data_list) == 1:
            return data_list[0]
        elif len(data_list) == 2:
            return data_list[0] + ' and ' + data_list[1]
        elif len(data_list) == 3:
            return data_list[0] + ', ' + data_list[1] + ' and ' + data_list[2]
        elif len(data_list) == 4:
            return data_list[0] + ', ' + data_list[1] + ', ' + data_list[2] + ' and ' + data_list[3]
        else:
            return data_list[0] + ', ' + data_list[1] + ', ' + data_list[2] + ', ' + data_list[3] + ' and ' + data_list[4]
    return result_str


print(format_duration(66666662))