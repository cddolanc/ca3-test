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

# git_df = pd.DataFrame() # Define the dataframe
# pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option

# import glob

# root_dir1 = "/workspace/ca3-test/" # Don't forget trailing (last) slashes
# # root_dir2= "/workspace/ca3-test/" # Don't forget trailing (last) slashes
# # root_dir3 = "/workspace/ca3-test/" # Don't forget trailing (last) slashes
# for filename in glob.iglob(root_dir1 + '**/*index.html', recursive=True):
#     #  print(filename)
#      git_df = git_df.append({'Index' : filename},ignore_index = True)
#     #  git_df = git_df.sort({'Index' : filename},ignore_index = True)
#      # do stuff
# # # root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes       
# # for filename2 in glob.iglob(root_dir2 + '**/*.pdf', recursive=True):
# #     print(filename2)
# #     # git_df = git_df.append({'PDF' : filename2},ignore_index = True)
# # # root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes  
# # for filename3 in glob.iglob(root_dir3 + '**/*.md', recursive=True):
# #     print(filename3)
# #     # git_df = git_df.append({'Slides' : filename3},ignore_index = True)
# #     git_df = git_df.append({'Index' : filename, 'PDF' : filename2, 'Slides' : filename3},ignore_index = True)


# # dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))


# print(git_df)




# from os import walk

# for filename, subdirs, dirs in walk('/workspace/ca3-test/' + ):
#     print (filename, subdirs, dirs)


git_index_df = pd.DataFrame() # Define the dataframe
git_pdf_df = pd.DataFrame() # Define the dataframe
git_slides_df = pd.DataFrame() # Define the dataframe
pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option



root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes    
for filename in glob.iglob(root_dir + '**/*index.html', recursive=True):
    git_index_df = git_index_df.append({'Index' : filename},ignore_index = True)
     # do stuff
for filename2 in glob.iglob(root_dir + '**/*.pdf', recursive=True):
    git_pdf_df = git_pdf_df.append({'PDF' : filename2},ignore_index = True)
for filename3 in glob.iglob(root_dir + '**/*.md', recursive=True):
#     print(filename3)
    git_slides_df = git_slides_df.append({'Slides' : filename3},ignore_index = True)



print(git_index_df)

git_index_df['week_no'] = None

index_Index = git_index_df.columns.get_loc('Index')
index_week_no = git_index_df.columns.get_loc('week_no')
print(index_Index, index_week_no)
pattern=r'(?:wk\d+)'
for row in range(0, len(git_index_df)):
    week = re.search(pattern, git_index_df.iat[row, index_Index]).group()
    git_index_df.iat[row, index_week_no] =week

git_index_df.sort_values(by=['week_no'], inplace=True)
print(git_index_df)



git_pdf_df['week_no1'] = None

index_PDF = git_pdf_df.columns.get_loc('PDF')
index_week_no1 = git_pdf_df.columns.get_loc('week_no1')
print(index_PDF, index_week_no1)
pattern=r'(?:wk\d+)'
for row in range(0, len(git_pdf_df)):
    week1 = re.search(pattern, git_pdf_df.iat[row, index_PDF]).group()
    git_pdf_df.iat[row, index_week_no1] =week1

git_pdf_df.sort_values(by=['week_no1'], inplace=True)
print(git_pdf_df)



git_slides_df['week_no2'] = None

index_Slides = git_slides_df.columns.get_loc('Slides')
index_week_no2 = git_slides_df.columns.get_loc('week_no2')
print(index_Slides, index_week_no2)
pattern=r'(?:wk\d+)'
for row in range(0, len(git_slides_df)):
    week2 = re.search(pattern, git_slides_df.iat[row, index_Slides]).group()
    git_slides_df.iat[row, index_week_no2] =week2

git_slides_df.sort_values(by=['week_no2'], inplace=True)
print(git_slides_df)



df_git_pull = pd.concat([git_index_df,git_pdf_df,git_slides_df], axis=1)




print(df_git_pull)

# s = pd.Series(["/workspace/ca3-test/wk1/index.html", "/workspace/ca3-test/wk8/index.html", "/workspace/ca3-test/wk7/index.html", "/workspace/ca3-test/wk4/index.html", "/workspace/ca3-test/wk6/index.html", "/workspace/ca3-test/wk5/index.html", "/workspace/ca3-test/wk2/index.html", "/workspace/ca3-test/wk3/index.html", "/workspace/ca3-test/wk8s/index.html"])

# pattern= "[test\\\w\D\D](\D\d+\w)"
# pattern='(?:wk\d+)'
# def fetch_num(txt):
#     result = re.findall(pattern,txt)
#     if result: # if matched
#         return result[0]
#     else:
#         return txt

# s.apply(fetch_num)

# print(s)
df_git_pull = df_git_pull.drop(columns=['week_no1','week_no2'])
df_git_pull = df_git_pull[['Index', 'PDF', 'Slides', 'week_no']]

# git_index_df = Index.sort_values(by = 'Name')

print(df_git_pull)