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
from scipy.interpolate import interp1d, splev, splrep

# Set directory
os.chdir(re.split('industry_model_9th_edition', os.getcwd())[0] + 'industry_model_9th_edition')

# Date
timestamp = datetime.now().strftime('%Y_%m_%d')

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
variable_path = './data/config/'

economy_list = pd.read_csv(variable_path + 'APEC_economies.csv').iloc[:, 0]
fuels_list = pd.read_csv(variable_path + 'EGEDA_fuels.csv').iloc[:, 0]
subfuels_list = pd.read_csv(variable_path + 'EGEDA_subfuels.csv').iloc[:, 0]

# Latest APEC_GDP_data file
path_to_gdp = '../macro_variables_9th/results/GDP_estimates/data/'
gdp_prefix = 'APEC_GDP_data_'

gdp_files = glob.glob(path_to_gdp + gdp_prefix + '*.csv')

if len(gdp_files) > 0:
    latest_gdp = max(gdp_files, key = os.path.getctime)
    gdp_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_gdp).group(0)

else:
    pass

# Path to industry production
path_to_prod = './data/industry_production/6_industry_scenarios/'
prod_prefix = 'industry_production_'

prod_files = glob.glob(path_to_prod + prod_prefix + '*.csv')

if len(prod_files) > 0:
    latest_prod = max(prod_files, key = os.path.getctime)
    prod_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_prod).group(0)

else:
    pass

# Path to industry energy trajectory
path_to_inden = './results/industry/1_total_energy_subsector/'
inden_prefix = 'industry_subsector_energy_trajectories_'

inden_files = glob.glob(path_to_inden + inden_prefix + '*.csv')

if len(inden_files) > 0:
    latest_inden = max(inden_files, key = os.path.getctime)
    inden_date = re.search(r'(\d{4})_(\d{2})_(\d{2})', latest_inden).group(0)

else:
    pass

# Path to EGEDA energy data
EGEDA_path = '../Outlook9th_EBT/results/'
EGEDA_prefix = 'model_df_wide_ref_'

EGEDA_files = glob.glob(EGEDA_path + EGEDA_prefix + '*.csv')

if len(EGEDA_files) > 0:
    latest_EGEDA = max(EGEDA_files, key = os.path.getctime)
    EGEDA_date = re.search(r'(\d{4})(\d{2})(\d{2})', latest_EGEDA).group(0)

else: 
    pass

# Colour palettes

pink_foam = ["#54bebe", "#76c8c8", "#98d1d1", "#badbdb", "#dedad2", "#e4bcad", "#df979e", "#d7658b", "#c80064"] + ["#ea5545"]
salmon_aqua = ["#e27c7c", "#a86464", "#6d4b4b", "#503f3f", "#333333", "#3c4e4b", "#466964", "#599e94", "#6cd4c5"] + ["#ea5545"]
retro_metro = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"] + ["#ea5545"]
orange_purple = ["#ffb400", "#d2980d", "#a57c1b", "#786028", "#363445", "#48446e", "#5e569b", "#776bcd", "#9080ff"] + ["#ea5545"]
dutch_field = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"] + ["#e60049"]
blue_red = ["#1984c5", "#22a7f0", "#63bff0", "#a7d5ed", "#e2e2e2", "#e1a692", "#de6e56", "#e14b31", "#c23728"] + ["#e60049"]
custom1 = ['#167288', '#8cdaec', '#b45248', '#d48c84', '#a89a49', '#d6cfa2', '#3cb464', '#9bddb1', '#643c6a', '#836394']
san_andreas = ['#000000', '#2a77a1', '#840410', '#263739', '#86446e', '#d78e10', '#4c75b7', '#bdbec6', '#58595a', '#335f3f']

custom_palette = {'reference': salmon_aqua[0],
                  'target': salmon_aqua[-2],
                  'reference activity': salmon_aqua[0],
                  'target activity': salmon_aqua[-2],
                  'reference energy': salmon_aqua[0],
                  'target energy': salmon_aqua[-2]}

fuel_industry = fuels_list[[0, 1, 5, 6, 7, 11, 14, 15, 16, 17]].reset_index(drop = True)

fuel_palette1 = {fuel_industry[x]: salmon_aqua[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette2 = {fuel_industry[x]: pink_foam[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette3 = {fuel_industry[x]: orange_purple[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette4 = {fuel_industry[x]: dutch_field[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette5 = {fuel_industry[x]: blue_red[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette6 = {fuel_industry[x]: custom1[x] for x in range(0, len(fuel_industry), 1)}
fuel_palette7 = {fuel_industry[x]: san_andreas[x] for x in range(0, len(fuel_industry), 1)}

