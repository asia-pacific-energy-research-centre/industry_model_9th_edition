# Finalise industry results with a post hoc biogas switch (from gas to biogas)
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import function
from f10_biogas_function import biogas_switch

# Modelled years
proj_years = list(range(2021, 2101, 1))

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

id = ['scenarios', 'economy', 'sectors', 'sub1sectors',	'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels']

# Run biogas switch function for relevant economies
biogas_switch(economy = '20_USA', biogas_ref = False, biogas_tgt = False)