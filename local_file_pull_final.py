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


git_index_df['title_html'] = None # week number column for sorting
base_url = "https://github.com/cddolanc/ca3-test/tree/main/wk{}/index.html"

for row in range(0, len(git_index_df)):
    git_index_df.iat[row, index_week_no] =week
    res = requests.get(base_url.format(week))
    soup = bs4.BeautifulSoup(res.text,"lxml")
    title = soup.select('title')
    git_index_df = git_index_df.append({'title_html' : title},ignore_index = True)


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

df_git_pull['week_no']= df_git_pull['week_no'].str.extract('(\d+)').astype(int) # drop the 'wk' string from the week column

print(df_git_pull)


# git_index_df['title_html'] = None # week number column for sorting
# base_url = "https://github.com/cddolanc/ca3-test/tree/main/wk{}/index.html"

# for row in range(0, len(git_index_df)):
#     git_index_df.iat[row, index_week_no] =week
#     res = requests.get(base_url.format(week))
#     soup = bs4.BeautifulSoup(res.text,"lxml")
#     title = soup.select('title')
#     git_index_df = git_index_df.append({'title_html' : title},ignore_index = True)

# res = requests.get("http://workspace/ca3-test/wk2/index.html")#/workspace/ca3-test/wk2/index.html

# print(type(res))

# print(res.text)

# import bs4

# soup = bs4.BeautifulSoup(res.text,"lxml")

# print(soup)

# print(soup.select('title'))


# from bs4 import BeautifulSoup

# # soup = BeautifulSoup(open("C:\\example.html"), "html.parser")

# # for city in soup.find_all('span', {'class' : 'city-sh'}):
#     # print(city)


# soup = BeautifulSoup(open("/workspace/ca3-test/wk2/index.html"), 'lxml')


# print(soup.select('title'))


# def git_title():
#     for i in df_git_pull['week_no']:
#         soup = BeautifulSoup(open(str(df_git_pull['Index'])), 'lxml')
#         print(soup.select('title'))

# git_title()



# res = requests.get("https://github.com/cddolanc/ca3-test/tree/main/wk1/index.html")#/workspace/ca3-test/wk2/index.html

# # print(type(res))

# # # print(res.text)

# import bs4

# soup = bs4.BeautifulSoup(res.text,"lxml")

# #print(soup)

# print(soup.select('title'))


# https://github.com/cddolanc/ca3-test/tree/main/wk1


base_url = "https://github.com/cddolanc/ca3-test/tree/main/wk1/index.html"

res = requests.get(base_url.format('1'))

soup = bs4.BeautifulSoup(res.text,"lxml")
print(soup.select(.title))



# titles_html = []
# for n in range(1,10):
#     scrape_url = base_url.format(n)
#     res = requests.get(scrape_url)
#     soup = bs4.BeautifulSoup(res.text,"html")
#     print(soup.title.text)

# import requests
# r = requests.get('https://github.com/mikhail-cct/ca3-test/blob/master/wk1/index.html')
# import bs4
# html = bs4.BeautifulSoup(r.text)
# print(html.title)


# import requests 
# from bs4 import BeautifulSoup 
  
# # target url 
# url = 'https://github.com/mikhail-cct/ca3-test/blob/master/wk1/index.html'
  
# # making requests instance 
# reqs = requests.get(url) 
  
# # using the BeaitifulSoup module 
# soup = BeautifulSoup(reqs.text, 'html.parser') 
  
# # displaying the title 
# print("Title of the website is : ") 
# for title in soup.find_all('title'): 
#     print(title.get_text())