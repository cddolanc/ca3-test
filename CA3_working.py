# pip install bs4
# pip install lxml
# pip install pandas

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
pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option


# Module variables to connect to moodle api:
# Insert token and URL for your site here.
# Mind that the endpoint can start with "/moodle" depending on your installation.
KEY = "bc7ad59923ad95f17dd955868790ccb5"
URL = "http://f0ae7213ef73.eu.ngrok.io/"
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


courseid = "2"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)


def pull_from_moodle():
    moodle_df= pd.DataFrame() # Define the dataframe
    pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option


    # pull moodle sections from LocalGetSections and assemble them in seperate moodle_dataframe columns
    for section in LocalGetSections(courseid).getsections:
        dates = re.findall('(\d{1,2} \w{3,})', section['name'])  # get the dates from the name section
        summary = re.findall(r'(\d{1,2} \w{3,})', section['summary'])  # get summary from summary section
        if len(dates) == 2:
            moodle_df= moodle_df.append({'Date' : dates, 'Link':section['summary']},ignore_index = True)  # assign each section pulled into dataframe columns

    # Clean date range data to just first date
    moodle_df["Date"] = moodle_df["Date"].str[0]


    # create 2 columns of number ranges for the week number to call data 
    moodle_df["year_wk_no"] = pd.DataFrame
    moodle_df["year_wk_no"] = pd.Series(range(40,68))  # googledrive year week range
    moodle_df["college_wk_no"] = pd.DataFrame
    moodle_df["college_wk_no"] = pd.Series(range(1,28)) # college year week range

    print(moodle_df)

# pull_from_moodle()

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
    vid_list_df["desc"] = (vid_list_df["video_date"].astype(str) + vid_list_df["video_time"].astype(str) + vid_list_df["video_name"].astype(str))
    vid_list_df = vid_list_df.drop(vid_list_df.columns[[0, 1, 2]], axis=1) 

    vid_list_df.insert(0, 'path', '<a href="https://drive.google.com/file/d/')
    vid_list_df.insert(2, 'path_end', '">')

    vid_list_df["url"] = (vid_list_df["path"].astype(str) + vid_list_df["video_id"].astype(str) + vid_list_df["path_end"].astype(str))
    vid_list_df = vid_list_df.drop(vid_list_df.columns[[0, 1, 2]], axis=1)

    

    cols = list(vid_list_df.columns.values)

    vid_list_df = vid_list_df[['Week_Number', 'url', 'desc']]
    vid_list_df.insert(3, 'path_ends', '</a><br>')
 
    vid_list_df["college_wk_no"] = pd.Series(range(1,28))

    


    for i in  range(len(vid_list_df["college_wk_no"])):
    # for row in vid_list_df["college_wk_no"]:
        data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
    
    # Assemble the correct summary
        
        summary = vid_list_df.iloc[i, 1] + vid_list_df.iloc[i, 2] + vid_list_df.iloc[i, 3]
        
        data[0]['summary'] = summary
        print(summary)
        
    # Set the correct section number 
        data[0]['section'] = i+1
        

    # Write the data back to Moodle
        sec_write = LocalUpdateSections(courseid, data)

        sec = LocalGetSections(courseid)

    print(vid_list_df)




    print(vid_list_df)


# google_drive_pull()


def local_files():
    ## Local direcory file scan and assemble dataframe:

    ## First create 3 dataframes for each filetype
    git_index_df = pd.DataFrame() # Define the 'Index file list' dataframe
    git_pdf_df = pd.DataFrame() # Define the 'PDF file list' dataframe
    git_slides_df = pd.DataFrame() # Define the 'Slides file list' dataframe

    #######'Index file list' dataframe
    root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes    
    for filename in glob.iglob(root_dir + '**/*index.html', recursive=True):
        git_index_df = git_index_df.append({'Index' : filename},ignore_index = True)
        
    git_index_df['week_no'] = None # week number column for sorting
    # find directories with 'wk' followed by a number and put it in the week column
    index_Index = git_index_df.columns.get_loc('Index')
    index_week_no = git_index_df.columns.get_loc('week_no')
    pattern=r'(?:wk\d+)'
    for row in range(0, len(git_index_df)):
        week = re.search(pattern, git_index_df.iat[row, index_Index]).group()
        git_index_df.iat[row, index_week_no] =week
        
    git_index_df.sort_values(by=['week_no'], inplace=True) # now sort by week column


    #######'PDF file list' dataframe (same process as for the 'Index file list' dataframe above)
    for filename2 in glob.iglob(root_dir + '**/*.pdf', recursive=True):
        git_pdf_df = git_pdf_df.append({'PDF' : filename2},ignore_index = True)
        
    git_pdf_df['week_no1'] = None

    index_PDF = git_pdf_df.columns.get_loc('PDF')
    index_week_no1 = git_pdf_df.columns.get_loc('week_no1')
    pattern=r'(?:wk\d+)'
    for row in range(0, len(git_pdf_df)):
        week1 = re.search(pattern, git_pdf_df.iat[row, index_PDF]).group()
        git_pdf_df.iat[row, index_week_no1] =week1

    git_pdf_df.sort_values(by=['week_no1'], inplace=True)
        
        
        
    #######'Slides file list' dataframe (same process as for the 'Index file list' dataframe above)
    for filename3 in glob.iglob(root_dir + '**/*.md', recursive=True):
        git_slides_df = git_slides_df.append({'Slides' : filename3},ignore_index = True)
        
    git_slides_df['week_no2'] = None

    index_Slides = git_slides_df.columns.get_loc('Slides')
    index_week_no2 = git_slides_df.columns.get_loc('week_no2')
    pattern=r'(?:wk\d+)'
    for row in range(0, len(git_slides_df)):
        week2 = re.search(pattern, git_slides_df.iat[row, index_Slides]).group()
        git_slides_df.iat[row, index_week_no2] =week2

    git_slides_df.sort_values(by=['week_no2'], inplace=True)	

    # Now we have our 3 dataframes in order we can integrate them into one and clean them up
    df_git_pull = pd.concat([git_index_df,git_pdf_df,git_slides_df], axis=1) # pull the 3 dataframes together

    df_git_pull = df_git_pull.drop(columns=['week_no1','week_no2']) #drop the week columns we don't need them anymore
    df_git_pull = df_git_pull[['Index', 'PDF', 'Slides', 'week_no']] # reorder the columns

    df_git_pull['week_no']= df_git_pull['week_no'].str.extract('(\d+)').astype(str) # drop the 'wk' string from the week column



    print(df_git_pull)

    df_git_pull.insert(4, 'header', '<a href="https://github.com/cddolanc/ca3-test/tree/main/wk')  # Header for html link
    df_git_pull.insert(5, 'path_HTML', '/index.html">HTML_link</a><br>')  # tail for htnl link
    df_git_pull.insert(6, 'path_pdf', '">PDF_link</a><br>') # tail for link pdf link
    df_git_pull.insert(7, 'path_md', '">PDF_Slides</a><br>') # tail for pdf slide (not currently working)
# .astype(str)


    print(df_git_pull)
    for i in  range(len(df_git_pull['Index'])):
    
        data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
    
    # Assemble the correct summary
        summary = df_git_pull.iloc[i, 4] + df_git_pull.iloc[i, 3] + df_git_pull.iloc[i, 5] + df_git_pull.iloc[i, 4] + df_git_pull.iloc[i, 3] + df_git_pull.iloc[i, 6] + df_git_pull.iloc[i, 4] + df_git_pull.iloc[i, 3] + df_git_pull.iloc[i, 7]
        
        data[0]['summary'] = summary
        print(summary)
        
    # Set the correct section number 
        data[0]['section'] = i=1
        

    # Write the data back to Moodle
        sec_write = LocalUpdateSections(courseid, data)

        sec = LocalGetSections(courseid)

    print(df_git_pull)


pull_from_moodle()
# google_drive_pull()
local_files()
pull_from_moodle()