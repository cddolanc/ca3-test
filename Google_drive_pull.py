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


res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX")

#print(type(res))

#print(res.text)


soup = bs4.BeautifulSoup(res.text,"lxml")


# vid_list_df= pd.DataFrame(columns = ['video', 'video_id', 'uploaded']) 
# videos = soup.find_all('div',class_ = 'Q5txwe')

# for video in videos:
#       video_title = video.text
#       video_id = video.parent.parent.parent.parent.attrs['data-id']
#       vid_list_df = vid_list_df.append({'video' : video_title,'video_id' : video_id},ignore_index = True)

# print(vid_list_df)


# x = re.search('P.*\.mp4', video_title)
# y = re.search('(^\d\d\d\w.\d\d.\d\d)', video_title)
# z = re.search('([\S]\d\d\W\d\d\W\d\d\W\d\d\W)', video_title)
# print(x.group())# Programming: Object-Oriented Approach.mp4
# print(y.group())
# print(z.group())


# vid_list_df= pd.DataFrame(columns = ['video_date', 'video_time', 'video_name','video_id', 'uploaded']) 
# videos = soup.find_all('div',class_ = 'Q5txwe')
# #video_id = video.parent.parent.parent.parent.attrs['data-id']
# print(len(videos))
# for video in videos:
# #     print(video)
#       video_title = video.text
#       x = re.search('P.*\.mp4', video_title)
#       y = re.search('(^\d\d\d\w.\d\d.\d\d)', video_title)
#       z = re.search('([\S]\d\d\W\d\d\W\d\d\W\d\d\W)', video_title)
#       x.group()
#       y.group()
#       z.group()
#       #df = df.append({'video' : video_title},ignore_index = True)
#       video_id = video.parent.parent.parent.parent.attrs['data-id']
#       vid_list_df = vid_list_df.append({'video_date' : y.group(),'video_time': z.group(),'video_name': x.group(),'video_id' : video_id},ignore_index = True)

# print(vid_list_df)


vid_list_df= pd.DataFrame(columns = ['video_date', 'video_time', 'video_name','video_id']) 
videos = soup.find_all('div',class_ = 'Q5txwe')

print(len(videos))
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

vid_list_df.insert(3, 'path', '<a href="https://drive.google.com/file/d/')
vid_list_df.insert(5, 'path_end', '">')
vid_list_df["url"] = vid_list_df["path"] + vid_list_df["video_id"] + vid_list_df["path_end"]
# vid_list_df.drop(columns=["path_end"])
vid_list_df["desc"] = (vid_list_df["video_date"].astype(str) + vid_list_df["video_time"].astype(str) + vid_list_df["video_name"].astype(str))
vid_list_df.reset_index(drop=True)
vid_list_df = vid_list_df.drop(vid_list_df.columns[[0, 1, 2]], axis=1) 
# vid_list_df.insert(4, 'path1', '<a href="')
# vid_list_df.insert(4, 'path2', '</a><br>')

print(vid_list_df)