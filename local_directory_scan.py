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
warnings.filterwarnings('ignore') # We can suppress the warnings


git_df = pd.DataFrame() # Define the dataframe
pd.set_option('display.max_colwidth', -1) #Turn off the truncating display option

import glob

root_dir1 = "/workspace/ca3-test/" # Don't forget trailing (last) slashes
root_dir2= "/workspace/ca3-test/" # Don't forget trailing (last) slashes
root_dir3 = "/workspace/ca3-test/" # Don't forget trailing (last) slashes
for filename in glob.iglob(root_dir1 + '**/*index.html', recursive=True):
     print(filename)
    #  git_df = git_df.append({'Index' : filename},ignore_index = True)
     # do stuff
# root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes       
for filename2 in glob.iglob(root_dir2 + '**/*.pdf', recursive=True):
    print(filename2)
    # git_df = git_df.append({'PDF' : filename2},ignore_index = True)
# root_dir = "/workspace/ca3-test/" # Don't forget trailing (last) slashes  
for filename3 in glob.iglob(root_dir3 + '**/*.md', recursive=True):
    print(filename3)
    # git_df = git_df.append({'Slides' : filename3},ignore_index = True)
    git_df = git_df.append({'Index' : filename, 'PDF' : filename2, 'Slides' : filename3},ignore_index = True)

    print(git_df)