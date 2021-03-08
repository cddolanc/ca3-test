import bs4
from requests import get, post
import json
from dateutil import parser
import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import re
import warnings
import glob
import numpy as np
warnings.filterwarnings('ignore') # We can suppress the warnings

# Module variables to connect to moodle api:
# Insert token and URL for your site here.
# Mind that the endpoint can start with "/moodle" depending on your installation.
KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    # print(parameters)
    response = post(URL+ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

################################################
# Rest-Api classes
################################################


class LocalGetSections(object):
    """Get settings of sections. Requires courseid. Optional you can specify sections via number or id."""

    def __init__(self, cid, secnums=[], secids=[]):
        self.getsections = call('local_wsmanagesections_get_sections',
                                courseid=cid, sectionnumbers=secnums, sectionids=secids)


class LocalUpdateSections(object):
    """Updates sectionnames. Requires: courseid and an array with sectionnumbers and sectionnames"""

    def __init__(self, cid, sectionsdata):
        self.updatesections = call(
            'local_wsmanagesections_update_sections', courseid=cid, sections=sectionsdata)


courseid = "12"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)

moodle_df= pd.DataFrame() # Define the dataframe
pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option


# pull moodle sections from LocalGetSections and assemble them in seperate moodle_dataframe columns
for section in LocalGetSections(courseid).getsections:
    dates = re.findall('(\d{1,2} \w{3,})', section['name'])
    summary = re.findall(r'(\d{1,2} \w{3,})', section['summary'])
    if len(dates) == 2:
        moodle_df= moodle_df.append({'Date' : dates, 'Link':section['summary']},ignore_index = True)

# Clean date range data to just first date
moodle_df["Date"] = moodle_df["Date"].str[0]


print(moodle_df)

# create 2 columns of number ranges for the week number to call data 
moodle_df["year_wk_no"] = pd.DataFrame
moodle_df["year_wk_no"] = pd.Series(range(40,68))  # googledrive year week range
moodle_df["college_wk_no"] = pd.DataFrame
moodle_df["college_wk_no"] = pd.Series(range(1,28)) # college year week range

print(moodle_df)



def google_drive_pull():
    res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX")
    soup = bs4.BeautifulSoup(res.text,"lxml")
    vid_list_df= pd.DataFrame(columns = ['video_date', 'video_time', 'video_name','video_id']) 
    videos = soup.find_all('div',class_ = 'Q5txwe')
    for video in videos:
      video_title = video.text
      x = re.search('P.*\.mp4', video_title)
      y = re.search('(^\d\d\d\w.\d\d.\d\d)', video_title)
      z = re.search('([\S]\d\d\W\d\d\W\d\d\W\d\d\W)', video_title)
      x.group()
      y.group()
      z.group()
      video_id = video.parent.parent.parent.parent.attrs['data-id']
      vid_list_df = vid_list_df.append({'video_date' : y.group(),'video_time': z.group(),'video_name': x.group(),'video_id' : video_id},ignore_index = True)

    vid_list_df['video_date'] = vid_list_df['video_date'].str.replace('-0', '-')

    vid_list_df['video_date']= pd.to_datetime(vid_list_df.video_date, format='%Y-%m-%d')

    vid_list_df['Week_Number'] = vid_list_df['video_date'].dt.week

    print(vid_list_df)

google_drive_pull()
