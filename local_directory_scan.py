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


git_index_df = git_index_df.sort_index(ascending = True)
print(git_index_df)

print(git_pdf_df)

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



git_index_df = Index.sort_values(by = 'Name')

print(git_index_df)