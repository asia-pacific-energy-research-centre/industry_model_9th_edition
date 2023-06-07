# CONFIG script, April 2023
# Import dependencies
 
import pandas as pd 
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import os
import datetime
from datetime import datetime
import re
import shutil
from numpy.core.numeric import NaN
from openpyxl import Workbook
import xlsxwriter
import pandas.io.formats.excel
from pandas import ExcelWriter
import requests
import ssl
import urllib3
import xml.etree.ElementTree as ET
import io
import typing
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import lxml
import wbgapi as wb
import json
import pytest
import seaborn as sns
from pandas import json_normalize
from textwrap import wrap
import plotly
import sklearn
import featuretools as ft
import math
import itertools
from itertools import chain, combinations
import warnings

# Set directory
os.chdir(re.split('industry_model_9th_edition', os.getcwd())[0] + 'industry_model_9th_edition')

# Set file_date_id here so that if we are running the script alone, versus through integrate, 
# we can have the variable available
try:
    file_date_id
except NameError:
    file_date_id = None

USE_LATEST_OUTPUT_DATE_ID = True

# Create option to set file_date_id to the date_id of the latest created output files. 
# (helpful when producing graphs and analysing output data)
if USE_LATEST_OUTPUT_DATE_ID == True:
    list_of_files = glob.glob('./results/*.csv')

if len(list_of_files) > 0: 
    latest_file = max(list_of_files, key = os.path.getctime)
    # Get file_date_id using regular expression code as per below. 
    # Want to grab the firt 8 digits and then an underscore and then the next 4 digits
    file_date_id = re.search(r'date(\d{8})_(\d{4})', latest_file).group(0)
else:
    pass

# Modelling variables
BASE_YEAR = 2017
END_YEAR = 2100
Scenario_list = ['reference', 'target']

# Machine learning
DEGREE = 2
LAGS = 1
KFOLD_SPLIT = 3
TOP_MODELS = 5

model_output_file_name = 'model_output_years_{}_to_{}_{}.csv'.format(BASE_YEAR, END_YEAR, file_date_id)

EIGHTH_EDITION_DATA = True

scenario_id = 'model_development'

# Model concordance file names
model_concordance_version = file_date_id # Example: '20220824_1256'
model_concordance_file_name  = 'model_concordance{}.csv'.format(model_concordance_version)

# Analysis variables
SCENARIO_OF_INTEREST = 'reference'

# Economies (including larger regions)
economy_codes_path = './data/config/'

economy_list = pd.read_csv(economy_codes_path + 'APEC_economies.csv').iloc[:, 0]